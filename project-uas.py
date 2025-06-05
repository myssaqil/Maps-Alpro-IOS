class Kota:
    def __init__(self):
        self.daftarKota = {}

    def tambahkanKota(self, kota):
        kota = kota.title()
        if kota not in self.daftarKota:
            self.daftarKota[kota] = []

    def tambahkanJalan(self, kota1, kota2):
        kota1 = kota1.title()
        kota2 = kota2.title()
        if kota1 in self.daftarKota and kota2 in self.daftarKota:
            if kota2 not in self.daftarKota[kota1]:
                self.daftarKota[kota1].append(kota2)
            if kota1 not in self.daftarKota[kota2]:
                self.daftarKota[kota2].append(kota1)

    def tampilkanKota(self):
        print("Daftar Kota dan Tetangga:")
        for kota, tetangga in self.daftarKota.items():
            print(f"- {kota}: {tetangga}")

if __name__ == "__main__":
    kotaObject = Kota()
    kota = ["Jakarta", "Bandung", "Surabaya", "Semarang", "Yogyakarta"]
    for k in kota:
        kotaObject.tambahkanKota(k)

    kotaObject.tambahkanJalan("Jakarta", "Bandung")
    kotaObject.tambahkanJalan("Jakarta", "Semarang")
    kotaObject.tambahkanJalan("Bandung", "Yogyakarta")
    kotaObject.tampilkanKota()

class JalurTercepatDijkstra(Kota):
    def __init__(self):
        super().__init__()
        self.bobotJarak = {}

    # override tambah jalan untuk tambahkan jarak
    def tambahkanJalan(self, kota1, kota2, jarak):
        kota1 = kota1.title()
        kota2 = kota2.title()
        if kota1 in self.daftarKota and kota2 in self.daftarKota:
            super().tambahkanJalan(kota1, kota2)
            if kota1 not in self.bobotJarak:
                self.bobotJarak[kota1] = {}
            if kota2 not in self.bobotJarak:
                self.bobotJarak[kota2] = {}
            self.bobotJarak[kota1][kota2] = jarak
            self.bobotJarak[kota2][kota1] = jarak

    def dijkstra(self, start):
        unvisited = set(self.daftarKota.keys())
        distances = {k: float('inf') for k in self.daftarKota}
        previous = {k: None for k in self.daftarKota}
        distances[start] = 0

        while unvisited:
            current = min(unvisited, key=lambda k: distances[k])
            unvisited.remove(current)

            for neighbor in self.daftarKota[current]:
                if neighbor in unvisited:
                    jarak = self.bobotJarak.get(current, {}).get(neighbor, float('inf'))
                    alt = distances[current] + jarak
                    if alt < distances[neighbor]:
                        distances[neighbor] = alt
                        previous[neighbor] = current

        return distances, previous
    
jalur = JalurTercepatDijkstra()
for k in kota:
    jalur.tambahkanKota(k)
jalur.tambahkanJalan("Jakarta", "Bandung", 150)
jalur.tambahkanJalan("Jakarta", "Semarang", 450)
jalur.tambahkanJalan("Bandung", "Yogyakarta", 390)
jalur.tambahkanJalan("Semarang", "Surabaya", 320)
jalur.tambahkanJalan("Yogyakarta", "Surabaya", 430)

distances, previous = jalur.dijkstra("Jakarta")
print("Jarak dari Jakarta ke kota lain:")
for kota_, jarak in distances.items():
    print(f"{kota_}: {jarak} km")