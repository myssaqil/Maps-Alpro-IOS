from flask import Flask
from controllers.maps_controller import rute_tercepat_controller, get_all_cities_controller, tambah_kota_jalur_controller

app = Flask(__name__)

app.add_url_rule('/rute-tercepat', 'rute_tercepat', rute_tercepat_controller, methods=['POST'])
app.add_url_rule('/daftar-kota', 'daftar_kota', get_all_cities_controller, methods=['GET'])
app.add_url_rule('/tambah-kota-jalur', 'tambah_kota_jalur', tambah_kota_jalur_controller, methods=['POST'])


if __name__ == '__main__':
    app.run(debug=True, port=8000)


