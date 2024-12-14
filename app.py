from flask import Flask, jsonify
from flask_cors import CORS  # CORS paketini ekliyoruz
import pyodbc

app = Flask(__name__)

# CORS ayarları
cors = CORS(app, resources={r"/*": {"origins": "*"}})  # Her yerden gelen isteklere izin verir

# Windows Authentication ile MSSQL Bağlantısı yapan fonksiyon
def get_db_connection():
    try:
        server = 'DESKTOP-G6ATIH2\\SQLEXPRESS'  # Yerel bağlantınız
        database = 'OgrenciDB'
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes')
        return conn  # Bağlantıyı döndür
    except pyodbc.Error as e:
        return None  # Bağlantı hatasında None döndür

@app.route('/get_data', methods=['GET'])
def get_data():
    conn = get_db_connection()  # Veritabanı bağlantısı al
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500  # Bağlantı hatası durumu

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notlar')  # Veritabanındaki tabloyu sorgulama
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            # Sütunları tablo yapınıza göre düzenleyin
            data.append({'id': row[0], 'isim': row[1], 'not': row[2]})  
        
        return jsonify(data)  # Veriyi JSON formatında döndür
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Sorgu hatasında hata mesajı döndür
    finally:
        conn.close()  # Bağlantıyı kapatıyoruz

# API'yi çalıştır
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Sunucuyu dış IP'lerden erişilebilir hale getiriyoruz
