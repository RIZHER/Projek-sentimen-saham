import pandas as pd
import mysql.connector
from mysql.connector import Error

# --- Konfigurasi Database MySQL ---
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 8889,
    'database': 'AlphaSentimen',
    'user': 'root',
    'password': 'root'
}

# --- Nama Tabel dan Kolom ---
table_name = 'saham_profile'
# Kolom yang akan diambil dari CSV (saham_id sudah auto-increment, sentimen, created_at, updated_at diset default)
columns_from_csv = ['kode_saham', 'nama_saham']
csv_file = 'data_saham_cleaned.csv'

def insert_data_from_csv_to_mysql_with_auto_increment_and_defaults(db_config, table, columns_from_csv_list, file_path):
    """
    Menginput data dari file CSV ke tabel MySQL yang ditentukan, dengan asumsi saham_id
    adalah auto-increment dan nilai default untuk 'sentimen', 'created_at', serta 'updated_at'.

    Args:
        db_config (dict): Dictionary berisi konfigurasi database.
        table (str): Nama tabel di database MySQL.
        columns_from_csv_list (list): Daftar nama kolom yang akan diambil dari file CSV.
        file_path (str): Path ke file CSV.
    """
    conn = None
    cursor = None
    try:
        # Membaca data dari CSV
        df = pd.read_csv(file_path)

        # Memastikan kolom-kolom di CSV yang akan digunakan tersedia
        df_columns = df.columns.tolist()
        for col in columns_from_csv_list:
            if col not in df_columns:
                print(f"Peringatan: Kolom '{col}' tidak ditemukan di file CSV. Pastikan nama kolom di CSV sesuai.")
                # Anda bisa memilih untuk menghentikan proses atau melanjutkan dengan peringatan

        # Koneksi ke database MySQL
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print('Berhasil terhubung ke database MySQL')
            cursor = conn.cursor()

            # Kolom yang akan diisi secara eksplisit (dari CSV + default)
            # saham_id dihilangkan karena diasumsikan auto-increment
            db_columns_to_insert = columns_from_csv_list + ['sentimen', 'created_at', 'updated_at']
            column_names_sql = ', '.join(db_columns_to_insert)

            # Membuat query INSERT
            # Placeholder untuk kolom dari CSV, diikuti oleh nilai default
            placeholders_csv = ', '.join(['%s'] * len(columns_from_csv_list))
            insert_query = f"INSERT INTO {table} ({column_names_sql}) VALUES ({placeholders_csv}, 'Neutral', NOW(), NOW())"

            # Iterasi melalui setiap baris DataFrame dan memasukkan data
            for index, row in df.iterrows():
                try:
                    # Mengambil nilai hanya untuk kolom yang berasal dari CSV
                    data_to_insert = [row[col] for col in columns_from_csv_list]
                    cursor.execute(insert_query, data_to_insert)
                except KeyError as e:
                    print(f"Error: Kolom tidak ditemukan di baris {index}. Error: {e}")
                    continue # Melanjutkan ke baris berikutnya jika ada kesalahan kolom

            # Commit transaksi
            conn.commit()
            print(f"{cursor.rowcount} baris data berhasil dimasukkan ke tabel '{table}'.")

    except Error as e:
        print(f"Error saat menginput data ke MySQL: {e}")
    except FileNotFoundError:
        print(f"Error: File CSV tidak ditemukan di '{file_path}'.")
    except Exception as e:
        print(f"Terjadi kesalahan tak terduga: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print('Koneksi database MySQL ditutup.')

# Panggil fungsi untuk menginput data
insert_data_from_csv_to_mysql_with_auto_increment_and_defaults(DB_CONFIG, table_name, columns_from_csv, csv_file)