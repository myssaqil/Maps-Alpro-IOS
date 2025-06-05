class KatakanPeta:
    def __init__(self):
        self.daftarKota = {}
        self.jumlahKota = 0
        self.peta = {}

    def tambahkanKota(self, kota):
        if kota not in self.daftarKota:
            self.daftarKota[kota] = {}
            self.jumlahKota += 1

    def tambahkanJalan(self, kota1, cities):
        for kota in cities:
            if kota1 in self.daftarKota and kota in self.daftarKota:
                self.daftarKota[kota1][kota] = cities[kota]
                self.daftarKota[kota][kota1] = cities[kota]

    def tampilkanKota(self):
        print("Daftar Kota:")
        for kota in self.daftarKota:
            print("-", kota)
        print(f"Jumlah Kota: {self.jumlahKota}")

    def tampilkanPeta(self):
        print("\nPeta:")
        for i, kota in enumerate(self.peta):
            print(f"{i+1}. {kota}")
            for kotaTetangga, rute in self.peta[kota].items():
                print(f"  --> {kotaTetangga}:")
                for jalan in rute.values():
                    print(f"     --> {jalan} km")

    def buatkanRute(self, start):
        peta = {}
        distances, routes = self.dijkstra(start)
        for kota, jarak in distances.items():
            peta[kota] = {
                "rute": self.route(distances, routes, start, kota),
                "jarak": jarak
            }
        self.peta[start] = peta

    def dijkstra(self, start):
        unvisited = list(self.daftarKota.keys())
        distances = {city: float('inf') for city in self.daftarKota}
        routes = {}
        distances[start] = 0

        while unvisited:
            current = min(unvisited, key=lambda city: distances[city])
            unvisited.remove(current)

            for tetangga, jarak in self.daftarKota[current].items():
                total_jarak = distances[current] + jarak
                if total_jarak < distances[tetangga]:
                    distances[tetangga] = total_jarak
                    routes[tetangga] = current

        del distances[start]
        return distances, routes

    def route(self, distances, routes, start, target):
        path = {}
        kota = target
        while kota != start:
            if routes[kota] == start:
                path[kota] = distances[kota]
            else:
                path[kota] = round(distances[kota] - distances[routes[kota]], 1)
            kota = routes[kota]
        return path

    def cariRuteTercepat(self, dari, ke):
        dari = dari.title()
        ke = ke.title()
        if dari in self.daftarKota and ke in self.daftarKota:
            print(f"\nDari {dari} ke {ke}, berjarak {self.peta[dari][ke]['jarak']} km")
            print("Dengan rute:")
            for jalan, jarak in reversed(self.peta[dari][ke]['rute'].items()):
                print(f"\t ---> {jalan} ({jarak} km)")
        else:
            print(f"{dari} atau {ke} tidak berada di daftar kota")


# === Daftar Kota & Edge (30 edge, 10 kota) ===
kota = [
    "Jakarta", "Bandung", "Surabaya", "Semarang", "Yogyakarta",
    "Medan", "Palembang", "Makassar", "Bali", "Pontianak"
]

peta = KatakanPeta()

for k in kota:
    peta.tambahkanKota(k)

# Tambahkan 30 jalur antar kota dengan jarak (km)
peta.tambahkanJalan("Jakarta", {"Bandung": 150, "Semarang": 450, "Palembang": 600})
peta.tambahkanJalan("Bandung", {"Yogyakarta": 390, "Surabaya": 680, "Pontianak": 870})
peta.tambahkanJalan("Semarang", {"Yogyakarta": 120, "Surabaya": 320, "Makassar": 1050})
peta.tambahkanJalan("Yogyakarta", {"Bali": 550, "Palembang": 700, "Makassar": 1180})
peta.tambahkanJalan("Surabaya", {"Bali": 430, "Makassar": 950, "Medan": 1800})
peta.tambahkanJalan("Medan", {"Palembang": 920, "Pontianak": 1100, "Bali": 1720})
peta.tambahkanJalan("Palembang", {"Pontianak": 980, "Bali": 960})
peta.tambahkanJalan("Makassar", {"Bali": 780, "Jakarta": 1350})
peta.tambahkanJalan("Jakarta", {"Pontianak": 850, "Bali": 950})

# Buat rute semua kota
for k in kota:
    peta.buatkanRute(k)

# Tampilkan
peta.tampilkanKota()
peta.tampilkanPeta()

# Interaktif cari rute tercepat
print("\n=== CARI RUTE TERCEPAT ===")
while True:
    dari = input("Cari Rute Tercepat dari (exit untuk keluar): ")
    if dari.lower() == "exit":
        break
    ke = input("Ke kota: ")
    if ke.lower() == "exit":
        break
    peta.cariRuteTercepat(dari, ke)
    print()