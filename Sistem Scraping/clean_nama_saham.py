import pandas as pd
import re

def clean_company_name_from_csv(input_csv_path, output_csv_path):
    """
    Membaca file CSV, membersihkan kolom 'Nama Perusahaan' dari 'PT.', 'Tbk', dan '(Persero) Tbk',
    kemudian menyimpan hasilnya ke file CSV baru.
    """
    try:
        # Membaca file CSV
        df = pd.read_csv(input_csv_path)

        # Memastikan kolom 'Nama Perusahaan' ada
        if 'Nama Perusahaan' not in df.columns:
            print(f"Error: Kolom 'Nama Perusahaan' tidak ditemukan di file CSV '{input_csv_path}'.")
            print(f"Kolom yang tersedia: {df.columns.tolist()}")
            return

        print(f"Membaca data dari '{input_csv_path}'...")
        print("Contoh Nama Perusahaan sebelum dibersihkan:")
        print(df['Nama Perusahaan'].head())

        # Fungsi untuk membersihkan nama perusahaan
        def clean_name(name):
            # Mengganti 'PT.' di awal string (case-insensitive)
            name = re.sub(r'^(PT\.)\s*', '', name, flags=re.IGNORECASE).strip()
            # Mengganti '(Persero) Tbk' (case-insensitive, opsional spasi di depannya)
            name = re.sub(r'\s*\(Persero\)\s*Tbk', '', name, flags=re.IGNORECASE).strip()
            # Mengganti 'Tbk' di akhir string (case-insensitive, opsional spasi di depannya)
            name = re.sub(r'\s*Tbk$', '', name, flags=re.IGNORECASE).strip()
            return name

        # Menerapkan fungsi pembersihan ke kolom 'Nama Perusahaan'
        df['Nama Perusahaan'] = df['Nama Perusahaan'].apply(clean_name)

        print("\nContoh Nama Perusahaan setelah dibersihkan:")
        print(df['Nama Perusahaan'].head())

        # Menyimpan hasil ke file CSV baru
        df.to_csv(output_csv_path, index=False, encoding='utf-8')
        print(f"\nData berhasil dibersihkan dan disimpan ke '{output_csv_path}'")

    except FileNotFoundError:
        print(f"Error: File '{input_csv_path}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi error: {e}")

if __name__ == "__main__":
    # Ganti dengan nama file CSV input Anda
    input_csv_file = 'data_saham_idnfinancials_rel_next_page.csv' 
    # Nama file CSV output
    output_csv_file = 'data_saham_cleaned.csv' 

    clean_company_name_from_csv(input_csv_file, output_csv_file)