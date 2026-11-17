// AllocProbe 1.1 — расширение охвата: корутины (MoveNext) модов + ванильные
// классы Assembly-CSharp(-firstpass): Update-семейство и MoveNext.
// Приписка мусора по паре «сборка.класс» (для корутин — внешний класс).
// Отчёт раз в 2 с: [ALLOC] total | топ-12 | residual.
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
    [BepInPlugin("teberrian.allocprobe", "AllocProbe", "1.1.0")]
    public class Plugin : BaseUnityPlugin
    {
        private ManualLogSource Log;
        private Harmony harmony;
        private bool patched;
        private float next;
        private long lastHeap;

        private void Awake()
        {
            Log = Logger;
            patched = false;
            next = Time.realtimeSinceStartup + 5f;
            harmony = new Harmony("teberrian.allocprobe");
            Log.LogInfo("AllocProbe 1.1.0 loaded");
        }

        /// <summary>Человеческое имя метода: сборка.класс (корутины — внешний класс).</summary>
        private static string OwnerName(MethodBase m)
        {
            try
            {
                var t = m.DeclaringType;
                if (t == null) return "?";
                var outer = t;
                while (outer.IsNested && outer.DeclaringType != null)
                    outer = outer.DeclaringType;
                string asm;
                try { asm = outer.Assembly.GetName().Name; } catch { asm = "?"; }
                return asm + "." + outer.Name;
            }
            catch
            {
                return "?";
            }
        }

        /// <summary>Кандидаты на обёртку из одной сборки: Update-семейство + MoveNext.</summary>
        private static IEnumerable<MethodInfo> CandidateMethods(Type t)
        {
            if (t.IsAbstract || t.IsInterface) yield break;
            foreach (var m in t.GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly))
            {
                if (m.IsAbstract) continue;
                string n = m.Name;
                bool upd = (n == "Update" || n == "FixedUpdate" || n == "LateUpdate")
                           && m.ReturnType == typeof(void)
                           && m.GetParameters().Length == 0
                           && !m.IsVirtual;
                bool move = n == "MoveNext"
                            && m.ReturnType == typeof(bool)
                            && m.GetParameters().Length == 0
                            && !m.IsVirtual
                            && typeof(System.Collections.IEnumerator).IsAssignableFrom(t);
                if (upd || move) yield return m;
            }
        }

        private void PatchAll()
        {
            int methods = 0;
            var owners = new HashSet<string>();
            var targets = new List<Assembly>();

            foreach (var a in AppDomain.CurrentDomain.GetAssemblies())
            {
                string name;
                string loc = "";
                try { name = a.GetName().Name; loc = a.Location ?? ""; } catch { continue; }
                if (name == "AllocProbe" || name == "HeapWatch") continue;
                bool isMod = loc.Replace('/', '\\').ToLowerInvariant().Contains("bepinex\\plugins");
                bool isGame = name == "Assembly-CSharp" || name == "Assembly-CSharp-firstpass";
                if (!isMod && !isGame) continue;
                targets.Add(a);
            }

            foreach (var asm in targets)
            {
                Type[] types;
                try { types = asm.GetTypes(); }
                catch (ReflectionTypeLoadException e) { types = e.Types.Where(t => t != null).ToArray(); }
                catch { continue; }

                var list = new List<MethodInfo>();
                foreach (var t in types)
                    list.AddRange(CandidateMethods(t));

                foreach (var m in list)
                {
                    try
                    {
                        harmony.Patch(m,
                            prefix: new HarmonyMethod(typeof(Patches), nameof(Patches.Prefix)),
                            postfix: new HarmonyMethod(typeof(Patches), nameof(Patches.Suffix)));
                        methods++;
                        owners.Add(OwnerName(m));
                    }
                    catch
                    {
                        // отдельный метод не патчится — не критично
                    }
                }
            }
            patched = true;
            Log.LogInfo($"AllocProbe 1.1: patched {methods} methods across {owners.Count} owner classes");
        }

        private void Update()
        {
            if (!patched)
            {
                if (Time.realtimeSinceStartup < next) return;
                PatchAll();
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
                    parts.Add($"{kv.Key}={kv.Value / 1024.0:0} KB");
                    PluginAccumulator.Bytes[kv.Key] = 0;
                }
            }
            long residual = total - sum;
            Log.LogInfo($"[ALLOC] total={(total > 0 ? total : 0) / 1024.0:0} KB/2s | {(parts.Count > 0 ? string.Join("; ", parts.Take(14)) : "все по нулям")} | residual={residual / 1024.0:0} KB/2s");
        }
    }

    /// <summary>Статические обёртки: меряем кучу до/после оригинального метода.</summary>
    internal static class Patches
    {
        public static void Prefix(ref long __state)
        {
            __state = GC.GetTotalMemory(false);
        }

        public static void Suffix(long __state, MethodBase __originalMethod)
        {
            try
            {
                long d = GC.GetTotalMemory(false) - __state;
                if (d <= 0) return;
                string owner = null;
                var t = __originalMethod.DeclaringType;
                if (t != null)
                {
                    var outer = t;
                    while (outer.IsNested && outer.DeclaringType != null)
                        outer = outer.DeclaringType;
                    string asm;
                    try { asm = outer.Assembly.GetName().Name; } catch { asm = "?"; }
                    owner = asm + "." + outer.Name;
                }
                if (owner != null)
                    PluginAccumulator.Add(owner, d);
            }
            catch
            {
                // диагностика не должна ронять игру
            }
        }
    }

    /// <summary>Счётчик по имени «сборка.класс».</summary>
    internal static class PluginAccumulator
    {
        public static readonly Dictionary<string, long> Bytes = new Dictionary<string, long>();

        public static void Add(string owner, long d)
        {
            lock (Bytes)
            {
                Bytes.TryGetValue(owner, out long v);
                Bytes[owner] = v + d;
            }
        }
    }
}
