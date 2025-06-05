import heapq

class Graph:
    def __init__(self, cities):
        self.cities = cities
        self.V = len(cities)
        self.graph = [[0 for _ in range(self.V)] for _ in range(self.V)]

    def add_edge(self, city1, city2, distance):
        u = self.cities.index(city1)
        v = self.cities.index(city2)
        self.graph[u][v] = distance
        self.graph[v][u] = distance

    def display_graph(self):
        print("\nAdjacency Matrix (Distance in KM):")
        for i in range(self.V):
            print(f"{self.cities[i]:10}: {self.graph[i]}")

    def dijkstra(self, start_city):
        start = self.cities.index(start_city)
        dist = [float('inf')] * self.V
        dist[start] = 0
        pq = [(0, start)]

        while pq:
            d, u = heapq.heappop(pq)
            for v in range(self.V):
                if self.graph[u][v] > 0 and dist[v] > d + self.graph[u][v]:
                    dist[v] = d + self.graph[u][v]
                    heapq.heappush(pq, (dist[v], v))

        print(f"\nJarak terpendek dari kota {start_city}:")
        for i in range(self.V):
            print(f"Ke {self.cities[i]:10}: {dist[i]} km")

# --- Data Kota dan Jalur (Statis) ---
cities = [
    "Jakarta", "Bandung", "Surabaya", "Semarang", "Yogyakarta",
    "Medan", "Palembang", "Makassar", "Bali", "Pontianak"
]

graph = Graph(cities)

edges = [
    ("Jakarta", "Bandung", 150),
    ("Jakarta", "Semarang", 450),
    ("Jakarta", "Palembang", 600),
    ("Jakarta", "Pontianak", 850),
    ("Bandung", "Yogyakarta", 390),
    ("Bandung", "Surabaya", 680),
    ("Semarang", "Yogyakarta", 120),
    ("Semarang", "Surabaya", 320),
    ("Surabaya", "Bali", 430),
    ("Yogyakarta", "Bali", 550),
    ("Medan", "Palembang", 920),
    ("Medan", "Pontianak", 1100),
    ("Makassar", "Bali", 780),
    ("Makassar", "Surabaya", 950),
    ("Palembang", "Pontianak", 980),
    ("Bandung", "Palembang", 640),
    ("Bandung", "Pontianak", 870),
    ("Semarang", "Makassar", 1050),
    ("Jakarta", "Makassar", 1350),
    ("Medan", "Makassar", 1550),
    ("Medan", "Bandung", 1410),
    ("Yogyakarta", "Palembang", 700),
    ("Yogyakarta", "Makassar", 1180),
    ("Surabaya", "Pontianak", 1220),
    ("Bandung", "Makassar", 1250),
    ("Bali", "Pontianak", 980),
    ("Palembang", "Bali", 960),
    ("Medan", "Bali", 1720),
    ("Jakarta", "Bali", 950),
    ("Surabaya", "Medan", 1800)
]

# Tambahkan semua edge ke graf
for u, v, d in edges:
    graph.add_edge(u, v, d)

# Tampilkan matriks graf
graph.display_graph()

# Pilih kota asal (misalnya: Jakarta)
asal = "Jakarta"
graph.dijkstra(asal)
