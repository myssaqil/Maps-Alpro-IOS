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