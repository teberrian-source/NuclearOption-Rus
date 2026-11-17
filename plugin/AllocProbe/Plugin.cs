// AllocProbe — диагностический плагин (план Б охоты на GC-мусор).
// При первом Update обходит все сборки, загруженные из BepInEx\plugins,
// и оборачивает Harmony-префиксами/суффиксами их Update/FixedUpdate/LateUpdate.
// Каждый вызов меряет GC.GetTotalMemory(false) до/после; положительная дельта
// аккумулируется на сборку (DLL) владельца метода. Раз в 2 секунды пишет в лог:
//   [ALLOC] total=+X KB/2s | DLL=+Y KB/2s ... | residual=Z KB/2s
// residual = общий рост кучи минус attributed — мусор вне обёрнутых Update
// (ваниль, корутины, события и т.п.).
// Отключение: перенести папку из BepInEx/plugins в BepInEx/disabledPlugins.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;

namespace AllocProbe
{
    [BepInPlugin("teberrian.allocprobe", "AllocProbe", "1.0.0")]
    public class Plugin : BaseUnityPlugin
    {
        private ManualLogSource Log;
        private Harmony harmony;
        private bool patched;
        private float next;
        private long lastHeap;
        private const string Self1 = "AllocProbe";
        private const string Self2 = "HeapWatch";

        private void Awake()
        {
            Log = Logger;
            patched = false;
            next = Time.realtimeSinceStartup + 5f; // дать всем плагинам загрузиться
            harmony = new Harmony("teberrian.allocprobe");
            Log.LogInfo("AllocProbe 1.0.0 loaded");
        }

        /// <summary>Сборки, чьи DLL лежат в BepInEx/plugins (кроме самой диагностики).</summary>

        /// <summary>Сборки, чьи DLL лежат в BepInEx/plugins (кроме самой диагностики).</summary>
        private static bool IsModAssembly(Assembly a)
        {
            try
            {
                string loc = a.Location;
                if (string.IsNullOrEmpty(loc)) return false;
                if (!loc.Replace('/', '\\').ToLowerInvariant().Contains("bepinex\\plugins")) return false;
                string name = a.GetName().Name;
                if (name == Self1 || name == Self2) return false;
                return true;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>Обёртка Update-семейства всех модовых сборок.</summary>
        private void PatchMods()
        {
            int methods = 0;
            var assemblies = AppDomain.CurrentDomain.GetAssemblies().Where(IsModAssembly).ToList();
            foreach (var asm in assemblies)
            {
                Type[] types;
                try { types = asm.GetTypes(); }
                catch (ReflectionTypeLoadException e) { types = e.Types.Where(t => t != null).ToArray(); }
                catch { continue; }

                var target = new List<MethodInfo>();
                foreach (var t in types)
                {
                    if (t.IsAbstract || t.IsInterface) continue;
                    foreach (var m in t.GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly))
                    {
                        if (m.IsAbstract || m.IsVirtual) continue;
                        if (m.ReturnType != typeof(void)) continue;
                        if (m.GetParameters().Length != 0) continue;
                        string n = m.Name;
                        if (n == "Update" || n == "FixedUpdate" || n == "LateUpdate")
                            target.Add(m);
                    }
                }
                foreach (var m in target)
                {
                    try
                    {
                        harmony.Patch(m,
                            prefix: new HarmonyMethod(typeof(Patches), nameof(Patches.Prefix)),
                            postfix: new HarmonyMethod(typeof(Patches), nameof(Patches.Suffix)));
                        methods++;
                    }
                    catch (Exception ex)
                    {
                        Log.LogWarning($"patch failed {m.DeclaringType?.Name}.{m.Name}: {ex.Message}");
                    }
                }
            }
            patched = true;
            Log.LogInfo($"AllocProbe: patched {methods} Update-methods in {assemblies.Count} assemblies");
            foreach (var a in assemblies) Log.LogInfo("  asm: " + a.GetName().Name);
        }

        private void Update()
        {
            if (!patched)
            {
                if (Time.realtimeSinceStartup < next) return;
                PatchMods();
                next = Time.realtimeSinceStartup + 2f;
                lastHeap = GC.GetTotalMemory(false);
                return;
            }

            float now = Time.realtimeSinceStartup;
            if (now < next) return;
            next = now + 2f;

            long heap = GC.GetTotalMemory(false);
            long total = heap - lastHeap;
            lastHeap = heap;

            long sum = 0;
            var parts = new List<string>();
            lock (PluginAccumulator.Bytes)
            {
                foreach (var kv in PluginAccumulator.Bytes.OrderByDescending(k => k.Value))
                {
                    if (kv.Value <= 0) continue;
                    sum += kv.Value;
                    string name;
                    try { name = kv.Key.GetName().Name; } catch { name = "?"; }
                    parts.Add($"{name}={kv.Value / 1024.0:0} KB");
                    PluginAccumulator.Bytes[kv.Key] = 0;
                }
            }
            long residual = total - sum;
            Log.LogInfo($"[ALLOC] total={(total > 0 ? total : 0) / 1024.0:0} KB/2s | {(parts.Count > 0 ? string.Join("; ", parts.Take(12)) : "все по нулям")} | residual={residual / 1024.0:0} KB/2s");
        }
    }

    /// <summary>Статические обёртки: меряем кучу до/после оригинального метода.</summary>
    internal static class Patches
    {
        /// <summary>Запоминаем объём кучи до вызова.</summary>
        public static void Prefix(ref long __state)
        {
            __state = GC.GetTotalMemory(false);
        }

        /// <summary>Положительная дельта — мусор этого Update; пишем на сборку владельца.</summary>
        public static void Suffix(long __state, MethodBase __originalMethod)
        {
            try
            {
                long d = GC.GetTotalMemory(false) - __state;
                if (d <= 0) return;
                var asm = __originalMethod.DeclaringType?.Assembly;
                if (asm == null) return;
                PluginAccumulator.Add(asm, d);
            }
            catch
            {
                // диагностика не должна ронять игру
            }
        }
    }

    /// <summary>Счётчик, доступный из статических обёрток (без ссылки на плагин).</summary>
    internal static class PluginAccumulator
    {
        /// <summary>Сборка -> накопленные байты мусора.</summary>
        public static readonly Dictionary<Assembly, long> Bytes = new Dictionary<Assembly, long>();

        /// <summary>Прибавить дельту к счётчику сборки (потокобезопасно достаточно).</summary>
        public static void Add(Assembly a, long d)
        {
            lock (Bytes)
            {
                Bytes.TryGetValue(a, out long v);
                Bytes[a] = v + d;
            }
        }
    }
}
