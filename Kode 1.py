import heapq
from itertools import permutations
import random

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)]

    def add_edge(self, u, v, w):
        self.graph[u][v] = w
        self.graph[v][u] = w  # undirected graph

    def display(self):
        print("Adjacency Matrix:")
        for row in self.graph:
            print(row)

    def dijkstra(self, start):
        dist = [float('inf')] * self.V
        dist[start] = 0
        pq = [(0, start)]

        while pq:
            d, u = heapq.heappop(pq)
            for v in range(self.V):
                if self.graph[u][v] > 0 and dist[v] > d + self.graph[u][v]:
                    dist[v] = d + self.graph[u][v]
                    heapq.heappush(pq, (dist[v], v))

        print(f"Shortest paths from city {start}:")
        for i, d in enumerate(dist):
            print(f"To city {i}: {d} minutes")

    def tsp(self, start=0):
        cities = list(range(self.V))
        cities.remove(start)
        min_path = float('inf')
        best_route = []

        for perm in permutations(cities):
            cost = 0
            k = start
            for j in perm:
                cost += self.graph[k][j]
                k = j
            cost += self.graph[k][start]

            if cost < min_path:
                min_path = cost
                best_route = [start] + list(perm) + [start]

        print("TSP route:", best_route)
        print("Total travel time:", min_path, "minutes")

# Fungsi untuk membuat graf acak dengan 30 edge dan bobot waktu tempuh
def generate_random_graph(vertices, edges):
    g = Graph(vertices)
    added = set()

    while len(added) < edges:
        u = random.randint(0, vertices - 1)
        v = random.randint(0, vertices - 1)
        if u != v and (u, v) not in added and (v, u) not in added:
            weight = random.randint(30, 300)  # waktu tempuh dalam menit
            g.add_edge(u, v, weight)
            added.add((u, v))
    return g

# Buat graf untuk tiga mode transportasi
print("\n=== Mobil ===")
g_car = generate_random_graph(10, 30)
g_car.display()
g_car.dijkstra(0)
g_car.tsp(0)

print("\n=== Kereta ===")
g_train = generate_random_graph(10, 30)
g_train.display()
g_train.dijkstra(0)
g_train.tsp(0)

print("\n=== Pesawat ===")
g_plane = generate_random_graph(10, 30)
g_plane.display()
g_plane.dijkstra(0)
g_plane.tsp(0)
