from flask import request, jsonify
from models.maps import Maps

graph_obj = Maps()


def rute_tercepat_controller():
    data = request.get_json()
    dari = data.get("dari")
    ke = data.get("ke")
    KECEPATAN_RATA2 = data.get("avg_kecepatan")

    if dari not in graph_obj.adj_list or ke not in graph_obj.adj_list:
        return jsonify({"error": "Kota tidak ditemukan"}), 400

    jarak, path = graph_obj.dijkstra(dari, ke)
    if jarak == float("inf"):
        return jsonify({"error": "Rute tidak ditemukan"}), 404

    result = []
    for kota in path:
        info_kota = graph_obj.kota_dict.get(kota)
        result.append({
            "nama": kota,
            "lat": info_kota.lat,
            "lon": info_kota.lon
        })

    waktu_tempuh_jam = jarak / KECEPATAN_RATA2
    waktu_jam = int(waktu_tempuh_jam)
    waktu_menit = int((waktu_tempuh_jam - waktu_jam) * 60)

    return jsonify({
        "dari": dari,
        "ke": ke,
        "jarak_km": round(jarak, 2),
        "waktu_tempuh": f"{waktu_jam} jam {waktu_menit} menit",
        "rute": result
    })




def get_all_cities_controller():
    daftar_kota = list(graph_obj.adj_list.keys())
    return jsonify({"daftar_kota": daftar_kota})


def tambah_kota_jalur_controller():
    data = request.get_json()
    nama = data.get("nama")
    lat = data.get("lat")
    lon = data.get("lon")
    jalur_ke = data.get("jalur_ke", [])

    if not nama or lat is None or lon is None:
        return jsonify({"error": "Nama, lat, dan lon wajib diisi"}), 400

    if nama in graph_obj.kota_dict:
        return jsonify({"error": "Kota sudah ada"}), 400

    berhasil_tambah = graph_obj.tambah_kota(nama, lat, lon)
    if not berhasil_tambah:
        return jsonify({"error": "Gagal menambah kota"}), 500

    for kota_tetangga in jalur_ke:
        if kota_tetangga not in graph_obj.kota_dict:
            return jsonify({"error": f"Kota tetangga {kota_tetangga} tidak ditemukan"}), 404
        graph_obj.tambah_jalur(nama, kota_tetangga)

    return jsonify({
        "message": f"Kota {nama} berhasil ditambahkan",
        "jalur_ke": jalur_ke
    }), 201
