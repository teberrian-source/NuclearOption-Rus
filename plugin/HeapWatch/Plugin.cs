// HeapWatch — диагностический плагин: раз в 2 секунды пишет в лог объём
// managed-кучи и счётчики сборок GC. Назначение: локализовать мод, который
// «кормит» GC и вызывает ритмичные подфризы. Отключается переносом папки
// из BepInEx/plugins в BepInEx/disabledPlugins.
using System;
using System.Diagnostics;
using BepInEx;
using BepInEx.Logging;
using UnityEngine;
using UnityEngine.Profiling;

namespace HeapWatch
{
    [BepInPlugin("teberrian.heapwatch", "HeapWatch", "1.0.0")]
    public class Plugin : BaseUnityPlugin
    {
        private ManualLogSource Log;
        private float next;
        private long lastHeap;
        private int lastGen0, lastGen1, lastGen2;

        private void Awake()
        {
            Log = Logger;
            next = Time.realtimeSinceStartup + 2f;
            Log.LogInfo("HeapWatch 1.0.0 loaded");
        }

        private void Update()
        {
            var now = Time.realtimeSinceStartup;
            if (now < next) return;
            next = now + 2f;

            long heap = GC.GetTotalMemory(false);
            int g0 = GC.CollectionCount(0), g1 = GC.CollectionCount(1), g2 = GC.CollectionCount(2);
            var proc = Process.GetCurrentProcess();
            float fps = 1f / Time.smoothDeltaTime;

            Log.LogInfo(string.Format(
                "[HEAP] mono={0:0.0} MB (+{1:0} KB/2s) | unityHeap={2:0.0} MB | proc={3:0} MB | GC gen0={4} gen1={5} gen2={6} | fps={7:0}",
                heap / 1048576.0, (heap - lastHeap) / 1024.0,
                Profiler.usedHeapSize / 1048576.0,
                proc.PrivateMemorySize64 / 1048576.0,
                g0 - lastGen0, g1 - lastGen1, g2 - lastGen2,
                fps));

            lastHeap = heap; lastGen0 = g0; lastGen1 = g1; lastGen2 = g2;
        }
    }
}
