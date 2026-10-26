using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

class Program
{
    static void TspRand(int size, uint seed)
    {
        Console.WriteLine($"data: {size}");
        for (int a = 0; a < size; a++)
        {
            for (int b = 0; b < size; b++)
            {
                seed = ((seed * 69069) + 1u) & 0xFFFFFFFFu;
                int d = ((int)(seed % 99) + 1) * (a != b ? 1 : 0);
                Console.Write($"{d,2} ");
            }
            Console.WriteLine();
        }
        Console.WriteLine();
    }

    static Tuple<int, List<int>> TspDynamicProgramming(List<List<int>> distances)
    {
        int n = distances.Count;
        var memo = new Dictionary<(int Mask, int Last), Tuple<int, List<int>>>();

        Tuple<int, List<int>> TspDpHelper(int mask, int last)
        {
            if (mask == (1 << n) - 1)
                return new Tuple<int, List<int>>(distances[last][0], new List<int> { last, 0 });

            if (memo.TryGetValue((mask, last), out var cached))
                return cached;

            int minCost = int.MaxValue;
            List<int> bestPath = new List<int>();

            for (int city = 0; city < n; city++)
            {
                if ((mask & (1 << city)) == 0)
                {
                    int newMask = mask | (1 << city);
                    var (cost, path) = TspDpHelper(newMask, city);

                    if (distances[last][city] + cost < minCost)
                    {
                        minCost = distances[last][city] + cost;
                        bestPath = new List<int> { last }.Concat(path).ToList();
                    }
                }
            }

            memo[(mask, last)] = new Tuple<int, List<int>>(minCost, bestPath);
            return new Tuple<int, List<int>>(minCost, bestPath);
        }

        var result = TspDpHelper(1, 0);
        return result;
    }

    static void TspRandMultiple(int start, int end)
    {
        using (StreamWriter file = new StreamWriter("wyniki_tsp_csharp_run.txt"))
        {
            for (int n = start + 1; n < end + 1; n++)
            {
                var data = new List<List<int>>(n);
                uint seed = (uint)n;
                for (int a = 0; a < n; a++)
                {
                    var row = new List<int>(n);
                    for (int b = 0; b < n; b++)
                    {
                        seed = ((seed * 69069) + 1u) & 0xFFFFFFFFu;
                        int d = ((int)(seed % 99) + 1) * (a != b ? 1 : 0);
                        row.Add(d);
                    }
                    data.Add(row);
                }

                Console.WriteLine($"data: {n}");
                for (int i = 0; i < n; i++)
                {
                    Console.WriteLine(string.Join(" ", data[i]));
                }
                Console.WriteLine();

                var startTime = DateTime.Now;
                var (cost, path) = TspDynamicProgramming(data);
                var endTime = DateTime.Now;

                Console.WriteLine($"programowanie dynamiczne ({(endTime - startTime).TotalSeconds:F3}s):");
                Console.WriteLine(cost);
                Console.WriteLine(string.Join(" ", path));
                Console.WriteLine();

                file.WriteLine($"data: {n}");
                for (int i = 0; i < n; i++)
                {
                    file.WriteLine(string.Join(" ", data[i]));
                }
                file.WriteLine();
                file.WriteLine($"programowanie dynamiczne ({(endTime - startTime).TotalSeconds:F3}s):");
                file.WriteLine(cost);
                file.WriteLine(string.Join(" ", path));
                file.WriteLine();
            }
        }
    }

    static void Main(string[] args)
    {
        if (args.Contains("--self-test"))
        {
            var matrix = new List<List<int>> {
                new() {0,10,15,20}, new() {10,0,35,25},
                new() {15,35,0,30}, new() {20,25,30,0}
            };
            var (cost, path) = TspDynamicProgramming(matrix);
            if (cost != 80 || path.Count != 5 || path[0] != 0 || path[^1] != 0 || path.Take(4).Distinct().Count() != 4)
                throw new InvalidOperationException("TSP cost or route regression");
            Console.WriteLine("TSP self-test: PASS");
            return;
        }
        TspRandMultiple(3, 10);
    }
}
