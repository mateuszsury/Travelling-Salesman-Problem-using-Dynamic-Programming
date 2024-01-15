# def tsp_nearest_neighbor(distances):
#     num_cities = len(distances)
#     unvisited_cities = set(range(num_cities))
#     current_city = 0
#     tour = [current_city]

#     while unvisited_cities:
#         nearest_city = min(unvisited_cities, key=lambda city: distances[current_city][city])
#         tour.append(nearest_city)
#         unvisited_cities.remove(nearest_city)
#         current_city = nearest_city

#     tour.append(tour[0])

#     return tour


def tsp_rand(size, seed):   # wykorzystanie algorytmu nearest neighbour
    print("data:", size)
    distances = [[0] * size for _ in range(size)]   # macierz odleglosci miedzy miastami
    
    for a in range(size):   # generowanie odleglosci miedzy miastami
        for b in range(size):
            seed = (seed * 69069 + 1) & 0xFFFFFFFF
            d = (seed % 99 + 1) * (a != b)
            distances[a][b] = d
            print('{:2d}'.format(d), end=" ")
        print()
    print()

    num_cities = len(distances)
    unvisited_cities = set(range(num_cities))
    current_city = 0    # poczatek trasy
    tour = [current_city]

    while unvisited_cities: # szukanie najblizszego nieodwiedzonego miasta
        nearest_city = min(unvisited_cities, key=lambda city: distances[current_city][city])
        tour.append(nearest_city)   # dodanie do trasy
        unvisited_cities.remove(nearest_city)   # usuniecie z listy nieodwiedzonych
        current_city = nearest_city # aktualizacja ostanio dodanego miasta do trasy

    tour.append(tour[0])    # dodanie miasta poczatkowego aby zamknąc trasę
    
    print("Najkrótsza trasa:", tour)
    print()


# Przykładowe użycie:
for n in range(10, 21):
    tsp_rand(n, n)
