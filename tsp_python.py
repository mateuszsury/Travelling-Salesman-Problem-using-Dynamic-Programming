import time
import numpy as np

def tsp_dynamic_programming(distances):
    n = len(distances)
    memo = {}

    def tsp_dp_helper(mask, last):
        if mask == (1 << n) - 1:
            return distances[last][0], [last, 0]

        if (mask, last) in memo:
            return memo[(mask, last)]

        min_cost = float('inf')
        best_path = []

        for city in range(1, n):
            if not (mask & (1 << city)):
                new_mask = mask | (1 << city)
                cost, path = tsp_dp_helper(new_mask, city)

                if distances[last][city] + cost < min_cost:
                    min_cost = distances[last][city] + cost
                    best_path = [last] + path

        memo[(mask, last)] = (min_cost, best_path)
        return min_cost, best_path

    return tsp_dp_helper(1, 0)

def tsp_rand(size, seed):
    print("data:", size)
    data = np.zeros((size, size), dtype=int)
    for a in range(size):
        for b in range(size):
            seed = (seed * 69069 + 1) & 0xFFFFFFFF
            d = (seed % 99 + 1) * (a != b)
            data[a][b] = d
            print('{:2d}'.format(d), end=" ")
        print()
    print()
    return data

def tsp_rand_results(start, end):
    all_data = []
    for n in range(start + 1, end + 1):
        data = tsp_rand(n, n)
        start_time = time.time()
        cost, path = tsp_dynamic_programming(data)
        end_time = time.time()

        print(f"programowanie dynamiczne ({end_time - start_time:.3f}s):")
        print(cost)
        print(' '.join(map(str, path)), end="\n\n")

        result = {
            "data": n,
            "cost": cost,
            "path": path,
            "end_time": end_time - start_time  # Dodaj informację o czasie zakończenia
        }
        all_data.append(result)

    return all_data

# Zapisz wyniki do pliku txt
results = tsp_rand_results(10, 21)
with open("wyniki_tsp.txt", "w") as file:
    for result in results:
        file.write(f"data: {result['data']}\n")
        file.write(f"programowanie dynamiczne ({result['end_time']:.3f}s):\n")
        file.write(f"{result['cost']}\n")
        file.write(' '.join(map(str, result['path'])) + "\n\n")
