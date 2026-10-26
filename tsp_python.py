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

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Held-Karp TSP experiment")
    parser.add_argument('--min-size', type=int, default=4)
    parser.add_argument('--max-size', type=int, default=10)
    args = parser.parse_args()
    if not 2 <= args.min_size <= args.max_size <= 20:
        parser.error('require 2 <= min-size <= max-size <= 20')
    results = tsp_rand_results(args.min_size - 1, args.max_size)
    with open('wyniki_tsp.txt', 'w') as output:
        for result in results:
            output.write(f"{result}\n")

if __name__ == '__main__':
    main()
