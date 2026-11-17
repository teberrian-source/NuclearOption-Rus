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
    [BepInPlugin("teberrian.allocprobe", "AllocProbe", "1.7.0")]
    public class Plugin : BaseUnityPlugin
    {
        private ManualLogSource Log;
        private Harmony harmony;
        private bool started;
        private float next;
        private float rescan;
        private long lastHeap;
        private readonly HashSet<string> patchedAsms = new HashSet<string>();
        private readonly HashSet<string> modAsmNames = new HashSet<string>();

        // 1.6: полная обёртка — только у главных подозреваемых; остальные моды — как в 1.4
        private static readonly HashSet<string> FullWrap = new HashSet<string>
        {
            "GroundControlRts", "NavalPower", "PlayableVehicles",
        };

        private void Awake()
        {
            Log = Logger;
            started = false;
            next = Time.realtimeSinceStartup + 5f;
            rescan = Time.realtimeSinceStartup + 10f;
            harmony = new Harmony("teberrian.allocprobe");
            Log.LogInfo("AllocProbe 1.7.0 loaded");
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

        private static readonly HashSet<string> Callbacks = new HashSet<string>
        {
            "Start", "Awake", "OnEnable", "OnDisable", "OnDestroy",
            "OnGUI", "OnDrawGizmos", "OnDrawGizmosSelected",
            "OnRenderObject", "OnPostRender", "OnPreRender", "OnWillRenderObject",
            "OnTriggerEnter", "OnTriggerStay", "OnTriggerExit",
            "OnCollisionEnter", "OnCollisionStay", "OnCollisionExit",
            "OnControllerColliderHit", "OnParticleCollision",
            "OnAnimatorMove", "OnApplicationFocus", "OnApplicationPause",
            "OnMouseEnter", "OnMouseOver", "OnMouseExit", "OnMouseDown", "OnMouseUp",
        };

        /// <summary>Кандидаты на обёртку из одной сборки: Update-семейство, корутины и движковые колбэки.</summary>
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
                bool cb = Callbacks.Contains(n)
                          && m.ReturnType == typeof(void)
                          && !m.IsVirtual;
                if (upd || move || cb) yield return m;
            }
        }

        private void PatchAll()
        {
            var targets = new List<Assembly>();

            foreach (var a in AppDomain.CurrentDomain.GetAssemblies())
            {
                string name;
                string loc = "";
                try { name = a.GetName().Name; loc = a.Location ?? ""; } catch { continue; }
                if (name == "AllocProbe" || name == "HeapWatch") continue;
                if (patchedAsms.Contains(name)) continue;
                bool isMod = loc.Replace('/', '\\').ToLowerInvariant().Contains("bepinex\\plugins");
                if (isMod) modAsmNames.Add(name);
                bool isGame = name == "Assembly-CSharp" || name == "Assembly-CSharp-firstpass";
                // 1.3: TMP и uGUI — их перестройки идут из Canvas-колбэков движка, минуя Update
                bool isUi = name == "Unity.TextMeshPro" || name == "UnityEngine.UI";
                if (!isMod && !isGame && !isUi) continue;
                targets.Add(a);
            }

            foreach (var asm in targets)
            {
                Type[] types;
                try { types = asm.GetTypes(); }
                catch (ReflectionTypeLoadException e) { types = e.Types.Where(t => t != null).ToArray(); }
                catch { continue; }

                var list = new List<MethodInfo>();
                bool isUiAsm = asm.GetName().Name == "Unity.TextMeshPro" || asm.GetName().Name == "UnityEngine.UI";
                bool fullWrap = FullWrap.Contains(asm.GetName().Name);
                foreach (var t in types)
                {
                    if (isUiAsm || fullWrap)
                    {
                        // TMP/UI и подозреваемые сборки: оборачиваем почти всё, кроме
                        // аксессоров и тривиальных методов — иначе штурм GC на горячих путях
                        foreach (var m in t.GetMethods(BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly))
                        {
                            if (m.IsAbstract || m.IsVirtual) continue;
                            if (t.IsAbstract || t.IsInterface) continue;
                            string mn = m.Name;
                            if (mn.StartsWith("get_") || mn.StartsWith("set_") ||
                                mn.StartsWith("add_") || mn.StartsWith("remove_")) continue;
                            try
                            {
                                var body = m.GetMethodBody();
                                if (body == null || body.GetILAsByteArray().Length < 24) continue;
                            }
                            catch { continue; }
                            list.Add(m);
                        }
                        continue;
                    }
                    list.AddRange(CandidateMethods(t));
                }

                foreach (var m in list)
                    pending.Add(m); // 1.7: патчим порциями по кадрам, не одним махом
                patchedAsms.Add(asm.GetName().Name);
            }
        }

        /// <summary>Непатченные методы, ожидающие Harmony-обёртки (порционно).</summary>
        private readonly List<MethodInfo> pending = new List<MethodInfo>();
        private const int PatchBudgetPerFrame = 250;

        /// <summary>Патчит до PatchBudgetPerFrame методов за вызов; true — ещё есть работа.</summary>
        private bool PatchChunk()
        {
            int n = 0;
            while (pending.Count > 0 && n < PatchBudgetPerFrame)
            {
                var m = pending[pending.Count - 1];
                pending.RemoveAt(pending.Count - 1);
                try
                {
                    harmony.Patch(m,
                        prefix: new HarmonyMethod(typeof(Patches), nameof(Patches.Prefix)),
                        postfix: new HarmonyMethod(typeof(Patches), nameof(Patches.Suffix)));
                }
                catch
                {
                    // отдельный метод не патчится — не критично
                }
                n++;
            }
            return pending.Count > 0;
        }

        private void Update()
        {
            // 1.7: патчинг порциями — не вешаем кадр; замер стартует, когда всё обёрнуто
            if (pending.Count > 0)
            {
                PatchChunk();
                if (pending.Count > 0) return;
                Log.LogInfo($"AllocProbe: patching complete ({patchedAsms.Count} assemblies)");
                next = Time.realtimeSinceStartup + 2f;
                lastHeap = GC.GetTotalMemory(false);
                started = true;
                return;
            }
            if (!started)
            {
                if (Time.realtimeSinceStartup < next) return;
                PatchAll();
                next = Time.realtimeSinceStartup + 2f;
                lastHeap = GC.GetTotalMemory(false);
                return;
            }

            // доскан лениво загруженных сборок раз в 10 с
            if (Time.realtimeSinceStartup >= rescan)
            {
                rescan = Time.realtimeSinceStartup + 10f;
                PatchAll();
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
        // кэш: MethodBase -> имя владельца (без аллокации строк в горячем пути)
        private static readonly System.Collections.Concurrent.ConcurrentDictionary<MethodBase, string> OwnerCache =
            new System.Collections.Concurrent.ConcurrentDictionary<MethodBase, string>();

        /// <summary>Имя владельца с кэшированием: «сборка.класс» (корутины — внешний класс).</summary>
        private static string OwnerOf(MethodBase m)
        {
            return OwnerCache.GetOrAdd(m, mm =>
            {
                try
                {
                    var t = mm.DeclaringType;
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
            });
        }

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
                string owner = OwnerOf(__originalMethod);
                if (owner != null && owner != "?")
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
