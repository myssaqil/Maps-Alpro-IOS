import json
from math import radians, cos, sin, sqrt, atan2
import heapq
from models.city import City
from models.city_connection import CityConnection

class Maps:
    def __init__(self, kota_file='./data/city.json', jalur_file='./data/city-connection.json'):
        self.kota_list = []
        self.kota_dict = {}  # key: city-name, value: City object
        self.adj_list = {}   # key: city-name, value: list of City (city objects)
        self.kota_file = kota_file      
        self.jalur_file = jalur_file

        # Load kota
        with open(kota_file) as f:
            data_kota = json.load(f)
            for k in data_kota:
                kota_obj = City(k["nama"], k["lat"], k["lon"])
                self.kota_list.append(kota_obj)
                self.kota_dict[kota_obj.nama] = kota_obj

        with open(jalur_file) as f:
            data_jalur = json.load(f)
            for kota, tetangga_list in data_jalur["jalur"].items():
                self.adj_list[kota] = []
                for tetangga_nama in tetangga_list:
                    if kota in self.kota_dict and tetangga_nama in self.kota_dict:
                        jarak = self.jarak_haversine(
                            self.kota_dict[kota].lat, self.kota_dict[kota].lon,
                            self.kota_dict[tetangga_nama].lat, self.kota_dict[tetangga_nama].lon
                        )
                        self.adj_list[kota].append(CityConnection(tetangga_nama, jarak))


    #Method menghitung jarak dari 2 kota berdasar lat longnya
    def jarak_haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c
    #Algoritma dijkstra untuk mendapatkan rute terdekat berdasar tetangga
    def dijkstra(self, start, end):
        queue = [(0, start, [])]
        visited = set()

        while queue:
            (jarak, node, path) = heapq.heappop(queue)
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]
            if node == end:
                return jarak, path

            for tetangga_obj in self.adj_list.get(node, []):
                if tetangga_obj.kota not in visited:
                    heapq.heappush(queue, (jarak + tetangga_obj.jarak, tetangga_obj.kota, path))

        return float("inf"), []
    
    def simpan_json(self):
        # Simpan kota ke file JSON
        data_kota = [{"nama": k.nama, "lat": k.lat, "lon": k.lon} for k in self.kota_list]
        with open(self.kota_file, "w") as f:
            json.dump(data_kota, f, indent=4)

        # Simpan jalur ke file JSON
        data_jalur = {"jalur": {}}
        for kota, tetangga_list in self.adj_list.items():
            data_jalur["jalur"][kota] = [t.kota for t in tetangga_list]
        with open(self.jalur_file, "w") as f:
            json.dump(data_jalur, f, indent=4)

    def tambah_kota(self, nama, lat, lon):
        if nama in self.kota_dict:
            return False
        kota_obj = City(nama, lat, lon)
        self.kota_list.append(kota_obj)
        self.kota_dict[nama] = kota_obj
        self.adj_list[nama] = []
        self.simpan_json() 
        return True

    def tambah_jalur(self, dari, ke):
        if dari not in self.kota_dict or ke not in self.kota_dict:
            return False
        # Hitung jarak
        jarak = self.jarak_haversine(
            self.kota_dict[dari].lat, self.kota_dict[dari].lon,
            self.kota_dict[ke].lat, self.kota_dict[ke].lon
        )
        # Tambahkan jalur
        self.adj_list.setdefault(dari, [])
        # Cek apakah jalur sudah ada
        if all(t.kota != ke for t in self.adj_list[dari]):
            self.adj_list[dari].append(CityConnection(ke, jarak))
            self.simpan_json() 
        return True

