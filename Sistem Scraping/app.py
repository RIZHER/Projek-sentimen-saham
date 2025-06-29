import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import joblib
import mysql.connector
from datetime import datetime, timedelta
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize # Diperlukan jika Anda tokenisasi manual
from nltk.stem import PorterStemmer # Jika Anda menggunakan stemming
from sklearn.feature_extraction.text import TfidfVectorizer # Diperlukan untuk memuat vectorizer
from sklearn.preprocessing import LabelEncoder # Diperlukan untuk memuat label encoder

# Mengimpor fungsi scrape_detik_search_filtered dari modul multipageDetik.py
# Asumsi struktur:
# .
# ├── app.py
# ├── Scraping/
# │   ├── __init__.py
# │   └── multipageDetik.py
# └── my_model.joblib
# └── my_vectorizer.joblib
# └── my_label_encoder.joblib
from Scraping.multipageDetik import scrape_detik_search_filtered

# --- NLTK Data Download (Hanya perlu sekali jalan jika belum ada) ---
# import nltk
# try:
#     stopwords.words('indonesian')
#     nltk.data.find('tokenizers/punkt') # Cek apakah punkt sudah ada
# except LookupError:
#     print("📦 Mengunduh data NLTK 'stopwords' dan 'punkt'...")
#     nltk.download('stopwords')
#     nltk.download('punkt')
#     print("✅ Pengunduhan selesai.")

# --- Konfigurasi Database MySQL ---
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 8889, # Sesuaikan jika portnya berbeda di hosting Anda
    'database': 'AlphaSentimen',
    'user': 'root',
    'password': 'root'
}

# --- Konfigurasi File Scheduler Sederhana ---
LAST_RUN_FILE = 'last_run.txt' # File untuk menyimpan timestamp terakhir kali skrip dijalankan

# --- Lokasi Model, Vectorizer, dan Label Encoder (SESUAIKAN INI) ---
MODEL_PATH = 'my_model.joblib'
VECTORIZER_PATH = 'my_vectorizer.joblib'
LABEL_ENCODER_PATH = 'my_label_encoder.joblib'

# --- Inisialisasi Stopwords dan Stemmer (HARUS SAMA PERSIS DENGAN SAAT PELATIHAN MODEL) ---
# Enhanced Indonesian stopwords (disalin dari notebook)
indonesian_stopwords = {
    'ada', 'adalah', 'adanya', 'adapun', 'agak', 'agaknya', 'agar', 'akan', 'akankah', 'akhir',
    'akhiri', 'akhirnya', 'aku', 'akulah', 'amat', 'amatlah', 'anda', 'andalah', 'antar',
    'antara', 'antaranya', 'apa', 'apaan', 'apabila', 'apakah', 'apalagi', 'apatah', 'artinya',
    'asal', 'asalkan', 'atas', 'atau', 'ataukah', 'ataupun', 'awalnya', 'bagai', 'bagaikan',
    'bagaimana', 'bagaimanakah', 'bagaimanapun', 'bagi', 'bagian', 'bahkan', 'bahwa', 'bahwasanya',
    'baik', 'bakal', 'bakalan', 'balik', 'banyak', 'bapak', 'baru', 'bawah', 'beberapa', 'begini',
    'beginian', 'beginikah', 'beginilah', 'begitu', 'begitukah', 'begitulah', 'begitupun', 'bekerja',
    'belakang', 'belakangan', 'belum', 'belumlah', 'benar', 'benarkah', 'benarlah', 'berada',
    'berakhir', 'berakhirlah', 'berakhirnya', 'berapa', 'berapakah', 'berapalah', 'berapapun',
    'berarti', 'berawal', 'berbagai', 'berdatangan', 'beri', 'berikan', 'berikut', 'berikutnya',
    'berjumlah', 'berkali-kali', 'berkata', 'berkehendak', 'berkeinginan', 'berkenaan', 'berlainan',
    'berlalu', 'berlangsung', 'berlebihan', 'bermacam', 'bermacam-macam', 'bermaksud', 'bermula',
    'bersama', 'bersama-sama', 'bersiap', 'bersiap-siap', 'bertanya', 'bertanya-tanya', 'berturut',
    'berturut-turut', 'bertutur', 'berujar', 'berupa', 'besar', 'betul', 'betulkah', 'biasa',
    'biasanya', 'bila', 'bilakah', 'bisa', 'bisakah', 'boleh', 'bolehkah', 'bukan', 'bukankah',
    'bukanlah', 'bukannya', 'bulan', 'bung', 'cara', 'caranya', 'cukup', 'cukupkah', 'cukuplah',
    'cuma', 'dahulu', 'dalam', 'dan', 'dapat', 'dari', 'daripada', 'datang', 'dekat', 'demi',
    'demikian', 'demikianlah', 'dengan', 'depan', 'di', 'dia', 'diakhiri', 'diakhirinya', 'dialah',
    'diantara', 'diantaranya', 'diberi', 'diberikan', 'diberikannya', 'dibuat', 'dibuatnya', 'didapat',
    'didatangkan', 'digunakan', 'diibaratkan', 'diibaratkannya', 'diingat', 'diingatkan', 'diinginkan',
    'dijawab', 'dijelaskan', 'dijelaskannya', 'dikarenakan', 'dikatakan', 'dikatakannya', 'dikerjakan',
    'diketahui', 'diketahuinya', 'dikira', 'dilakukan', 'dilakukannya', 'dimaksud', 'dimaksudkan',
    'dimaksudkannya', 'dimaksudnya', 'diminta', 'dimintai', 'dimisalkan', 'dimulai', 'dimulailah',
    'dimulainya', 'dimungkinkan', 'dini', 'dipastikan', 'diperbuat', 'diperbuatnya', 'dipergunakan',
    'diperkirakan', 'diperlihatkan', 'diperlukan', 'diperlukannya', 'dipersoalkan', 'dipertanyakan',
    'dipunyai', 'diri', 'dirinya', 'disampaikan', 'disebut', 'disebutkan', 'disebutkannya', 'disini',
    'disinilah', 'ditambahkan', 'ditandaskan', 'ditanya', 'ditanyai', 'ditanyakan', 'ditegaskan',
    'ditujukan', 'ditunjuk', 'ditunjuki', 'ditunjukkan', 'ditunjukkannya', 'ditunjuknya', 'dituturkan',
    'dituturkannya', 'diucapkan', 'diucapkannya', 'diungkapkan', 'dong', 'dua', 'dulu', 'empat',
    'enggak', 'enggaknya', 'entah', 'entahlah', 'guna', 'gunanya', 'hal', 'hampir', 'hanya',
    'hanyalah', 'hari', 'harus', 'haruslah', 'harusnya', 'hendak', 'hendaklah', 'hendaknya',
    'hingga', 'ia', 'ialah', 'iaitu', 'ibarat', 'ibaratkan', 'ibaratnya', 'ibu', 'ikut', 'ingat',
    'ingat-ingat', 'ingin', 'inginkah', 'inginkan', 'ini', 'inikah', 'inilah', 'itu', 'itukah',
    'itulah', 'jadi', 'jadilah', 'jadinya', 'jangan', 'jangankan', 'janganlah', 'jauh', 'jawab',
    'jawaban', 'jawabnya', 'jelas', 'jelaskan', 'jelaslah', 'jelasnya', 'jika', 'jikalau', 'juga',
    'jumlah', 'jumlahnya', 'justru', 'kala', 'kalau', 'kalaulah', 'kalaupun', 'kalian', 'kami',
    'kamilah', 'kamu', 'kamulah', 'kan', 'kapan', 'kapankah', 'kapanpun', 'karena', 'karenanya',
    'kasus', 'kata', 'katakan', 'katakanlah', 'katanya', 'ke', 'keadaan', 'kebetulan', 'kecil',
    'kedua', 'keduanya', 'keinginan', 'kelamaan', 'kelihatan', 'kelihatannya', 'keluar', 'kemana',
    'kemana-mana', 'kemarin', 'kemudian', 'kemungkinan', 'kemungkinannya', 'kenapa', 'kepada',
    'kepadanya', 'kesampaian', 'keseluruhan', 'keseluruhannya', 'keterlaluan', 'ketika', 'ketimbang',
    'kira', 'kira-kira', 'kiranya', 'kita', 'kitalah', 'kok', 'kurang', 'lagi', 'lagian', 'lah',
    'lain', 'lainnya', 'lalu', 'lama', 'lamanya', 'lanjut', 'lanjutnya', 'lebih', 'lewat', 'lima',
    'luar', 'macam', 'maka', 'makanya', 'makin', 'malah', 'malahan', 'mampu', 'mana', 'manakala',
    'manalagi', 'masa', 'masalah', 'masalahnya', 'masih', 'masihkah', 'masing', 'masing-masing',
    'mau', 'maupun', 'melainkan', 'melakukan', 'melalui', 'melihat', 'melihatnya', 'memang',
    'memastikan', 'memberi', 'memberikan', 'membuat', 'memerlukan', 'memihak', 'meminta', 'memintakan',
    'memisalkan', 'memperbuat', 'mempergunakan', 'memperkirakan', 'memperlihatkan', 'mempersiapkan',
    'mempersoalkan', 'mempertanyakan', 'mempunyai', 'memulai', 'memungkinkan', 'menaiki', 'menambahkan',
    'menandaskan', 'menanti', 'menantikan', 'menanya', 'menanyai', 'menanyakan', 'mendapat',
    'mendapatkan', 'mendatang', 'mendatangi', 'mendatangkan', 'menegaskan', 'mengakhiri', 'mengapa',
    'mengatakan', 'mengatakannya', 'mengenai', 'mengerjakan', 'mengetahui', 'menggunakan', 'menghendaki',
    'mengibaratkan', 'mengibaratkannya', 'mengingat', 'mengingatkan', 'menginginkan', 'mengira',
    'mengucapkan', 'mengucapkannya', 'mengungkapkan', 'menjadi', 'menjawab', 'menjelaskan', 'menuju',
    'menunjuk', 'menunjuki', 'menunjukkan', 'menunjuknya', 'menurut', 'menuturkan', 'menyampaikan',
    'menyangkut', 'menyatakan', 'menyebutkan', 'menyeluruh', 'menyiapkan', 'merasa', 'mereka',
    'merekalah', 'merupakan', 'meski', 'meskipun', 'meyakini', 'meyakinkan', 'minta', 'mirip',
    'misal', 'misalkan', 'misalnya', 'mula', 'mulai', 'mulailah', 'mulanya', 'mungkin', 'mungkinkah',
    'nah', 'naik', 'namun', 'nanti', 'nantinya', 'nyaris', 'oleh', 'olehnya', 'pada', 'padahal',
    'padanya', 'pak', 'paling', 'panjang', 'pantas', 'para', 'pasti', 'pastilah', 'penting',
    'pentingnya', 'percuma', 'perlu', 'perlukah', 'perlunya', 'pernah', 'persoalan', 'pertama',
    'pertama-tama', 'pertanyaan', 'pertanyakan', 'pihak', 'pihaknya', 'pukul', 'pula', 'pun',
    'punya', 'rasa', 'rasanya', 'rata', 'rupanya', 'saat', 'saatnya', 'saja', 'sajalah', 'saling',
    'sama', 'sama-sama', 'sambil', 'sampai', 'sampai-sampai', 'sampaikan', 'sana', 'sangat',
    'sangatlah', 'satu', 'saya', 'sayalah', 'se', 'sebab', 'sebabnya', 'sebagai', 'sebagaimana',
    'sebagainya', 'sebagian', 'sebaik', 'sebaik-baiknya', 'sebaiknya', 'sebaliknya', 'sebanyak',
    'sebegini', 'sebegitu', 'sebelum', 'sebelumnya', 'sebenarnya', 'seberapa', 'sebesar', 'sebetulnya',
    'sebisanya', 'sebuah', 'sebut', 'sebutlah', 'sebutnya', 'secara', 'secukupnya', 'sedang',
    'sedangkan', 'sedemikian', 'sedikit', 'sedikitnya', 'seenaknya', 'segala', 'segalanya', 'segera',
    'seharusnya', 'sehingga', 'seingat', 'sejak', 'sejauh', 'sejenak', 'sejumlah', 'sekadar',
    'sekadarnya', 'sekali', 'sekali-kali', 'sekalian', 'sekaligus', 'sekalipun', 'sekarang', 'sekarang',
    'sekecil', 'sekiranya', 'sekitar', 'sekitarnya', 'sekurang-kurangnya', 'sekurangnya', 'sela',
    'selagi', 'selain', 'selaku', 'selalu', 'selama', 'selama-lamanya', 'selamanya', 'selanjutnya',
    'seluruh', 'seluruhnya', 'semacam', 'semakin', 'semampu', 'semampunya', 'semasa', 'semasih',
    'semata', 'semata-mata', 'semaunya', 'sementara', 'semisal', 'semisalnya', 'sempat', 'semua',
    'semuanya', 'semula', 'sendiri', 'sendirian', 'sendirinya', 'seolah', 'seolah-olah', 'seorang',
    'sepanjang', 'sepantasnya', 'sepantasnyalah', 'seperlunya', 'seperti', 'sepertinya', 'sepihak',
    'sering', 'seringnya', 'serta', 'serupa', 'sesaat', 'sesama', 'sesampai', 'sesegera', 'sesekali',
    'seseorang', 'sesuai', 'sesuatu', 'sesuatunya', 'sesudah', 'sesudahnya', 'setelah', 'setempat',
    'setengah', 'seterusnya', 'setiap', 'setiba', 'setibanya', 'setidak-tidaknya', 'setidaknya',
    'setinggi', 'seusai', 'sewaktu', 'siap', 'siapa', 'siapakah', 'siapapun', 'sini', 'sinilah',
    'soal', 'soalnya', 'suatu', 'sudah', 'sudahkah', 'sudahlah', 'supaya', 'tadi', 'tadinya',
    'tahu', 'tahun', 'tak', 'tambah', 'tambahnya', 'tampak', 'tampaknya', 'tandas', 'tandasnya',
    'tanpa', 'tanya', 'tanyakan', 'tanyanya', 'tapi', 'tegas', 'tegasnya', 'telah', 'tempat',
    'tengah', 'tentang', 'tentu', 'tentulah', 'tentunya', 'tepat', 'terakhir', 'terasa', 'terbanyak',
    'terdahulu', 'terdapat', 'terdiri', 'terhadap', 'terhadapnya', 'teringat', 'teringat-ingat',
    'terjadi', 'terjadilah', 'terjadinya', 'terkira', 'terlalu', 'terlebih', 'terlihat', 'termasuk',
    'ternyata', 'tersampaikan', 'tersebut', 'tersebutlah', 'tertentu', 'tertuju', 'terus', 'terutama',
    'tetap', 'tetapi', 'tiap', 'tiba', 'tiba-tiba', 'tidak', 'tidakkah', 'tidaklah', 'tiga', 'tinggi',
    'toh', 'tunjuk', 'turut', 'tutur', 'tuturnya', 'ucap', 'ucapnya', 'ujar', 'ujarnya', 'umum',
    'umumnya', 'ungkap', 'ungkapnya', 'untuk', 'usah', 'usai', 'waduh', 'wah', 'wahai', 'waktu',
    'waktunya', 'walau', 'walaupun', 'wong', 'yaitu', 'yakin', 'yakni', 'yang', 'pt', 'tbk'
}

# stemmer = PorterStemmer() # Aktifkan jika Anda menggunakannya saat training

# --- Fungsi Pra-pemrosesan Teks (HARUS SAMA PERSIS DENGAN SAAT PELATIHAN MODEL) ---
def preprocess_text(text):
    """
    Melakukan pra-pemrosesan teks agar sesuai dengan input model sentimen.
    Sesuaikan langkah-langkah ini agar SAMA PERSIS dengan yang digunakan saat melatih model Anda.
    """
    if not isinstance(text, str):
        return ""

    text = str(text).lower()

    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Remove email addresses
    text = re.sub(r'\\S+@\\S+', '', text)

    # Remove numbers but keep percentage
    text = re.sub(r'\\d+(?!\\s*%)', '', text)

    # Remove extra whitespace
    text = re.sub(r'\\s+', ' ', text)

    # Remove punctuation except % and -
    text = re.sub(r'[^\\w\\s%-]', ' ', text)
    
    # Tokenisasi (diperlukan jika remove_stopwords_indonesian menggunakan word_tokenize)
    words = word_tokenize(text) # Menggunakan word_tokenize NLTK

    # Remove Indonesian stopwords
    filtered_words = [word for word in words if word not in indonesian_stopwords]

    # Lakukan stemming (jika Anda menggunakannya saat melatih model, aktifkan baris di bawah)
    # stemmed_words = [stemmer.stem(word) for word in filtered_words]
    # return ' '.join(stemmed_words)

    return ' '.join(filtered_words).strip()


# --- Fungsi Web Scraping yang Disediakan Pengguna (multipageDetik.py) ---
# Fungsi ini diimpor dari file 'Scraping/multipageDetik.py'
# Pastikan file tersebut ada di lokasi yang benar dan berisi fungsi scrape_detik_search_filtered
# Pastikan juga ada file __init__.py kosong di dalam folder 'Scraping'
# def scrape_detik_search_filtered(query, max_articles=50):
#     ... (kode scraping Anda sebelumnya) ...

# --- Fungsi Utama Aplikasi ---
def main():
    print(f"[{datetime.now()}] Memulai aplikasi Sentimen Analisis Berita...")

    # --- 1. Pengecekan Waktu Terakhir Dijalankan ---
    current_time = datetime.now()
    last_run_time = None
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, 'r') as f:
            try:
                last_run_time_str = f.read().strip()
                if last_run_time_str:
                    last_run_time = datetime.fromisoformat(last_run_time_str)
            except ValueError:
                print("Peringatan: Format waktu terakhir dijalankan tidak valid. Mengabaikan.")

    # Logika untuk menunggu jika belum 1 jam
    if last_run_time:
        time_diff = current_time - last_run_time
        # Waktu minimum yang harus dilalui sebelum menjalankan scraping berikutnya (1 jam)
        minimum_interval = timedelta(hours=1)

        if time_diff < minimum_interval:
            time_to_wait = minimum_interval - time_diff
            print(f"[{current_time}] Skrip terakhir dijalankan {time_diff} yang lalu.")
            print(f"⏳ Menunggu {time_to_wait} sebelum melanjutkan scraping...")
            time.sleep(time_to_wait.total_seconds())
            # Setelah menunggu, perbarui current_time agar log selanjutnya akurat
            current_time = datetime.now()
            print(f"[{current_time}] Lanjutkan setelah menunggu.")
        else:
            print(f"[{current_time}] Waktu sudah lebih dari 1 jam sejak terakhir dijalankan. Melanjutkan.")
    else:
        print(f"[{current_time}] File catatan waktu terakhir dijalankan tidak ditemukan atau kosong. Melanjutkan.")


    # --- 2. Muat Model Sentimen, Vectorizer, dan Label Encoder ---
    sentiment_model = None
    vectorizer = None
    label_encoder = None
    try:
        sentiment_model = joblib.load(MODEL_PATH)
        print(f"Model sentimen berhasil dimuat dari {MODEL_PATH}.")
        
        vectorizer = joblib.load(VECTORIZER_PATH)
        print(f"Vectorizer berhasil dimuat dari {VECTORIZER_PATH}.")

        label_encoder = joblib.load(LABEL_ENCODER_PATH)
        print(f"Label Encoder berhasil dimuat dari {LABEL_ENCODER_PATH}.")

    except FileNotFoundError as e:
        print(f"Error: Gagal memuat model, vectorizer, atau label encoder. Pastikan file ada di lokasi yang benar. {e}")
        return # Hentikan jika file tidak bisa dimuat
    except Exception as e:
        print(f"Error tak terduga saat memuat model/vectorizer/encoder: {e}")
        return

    db_connection = None
    try:
        # --- 3. Koneksi ke Database MySQL ---
        db_connection = mysql.connector.connect(**DB_CONFIG)
        cursor = db_connection.cursor(dictionary=True) # dictionary=True agar hasil query berupa dict

        print("Berhasil terhubung ke database MySQL.")

        # --- 4. Ambil Kata Kunci (nama_saham) dari tabel saham_profile ---
        cursor.execute("SELECT saham_id, nama_saham FROM saham_profile")
        stock_keywords = cursor.fetchall()

        if not stock_keywords:
            print("Tidak ada kata kunci saham ditemukan di tabel 'saham_profile'.")
            return

        print(f"Ditemukan {len(stock_keywords)} kata kunci saham.")

        # --- 5. Dapatkan semua URL berita yang sudah ada di database ---
        cursor.execute("SELECT url FROM berita")
        existing_urls = {row['url'] for row in cursor.fetchall()}
        print(f"Ditemukan {len(existing_urls)} URL berita yang sudah ada di database.")

        total_new_articles_processed = 0

        # --- 6. Iterasi Setiap Kata Kunci untuk Scraping dan Analisis ---
        for stock in stock_keywords:
            saham_id = stock['saham_id']
            nama_saham = stock['nama_saham']
            
            # Buat query untuk scraping, hanya menggunakan nama_saham
            search_query = f"{nama_saham}" 
            print(f"\n--- Memproses kata kunci: '{search_query}' (Saham ID: {saham_id}) ---")

            # Lakukan scraping menggunakan fungsi yang diimpor
            raw_scraped_data = scrape_detik_search_filtered(search_query, max_articles=20) # Batasi per saham untuk efisiensi
            
            if not raw_scraped_data:
                print(f"Tidak ada berita baru yang di-scrape untuk '{search_query}'.")
                continue

            print(f"Ditemukan {len(raw_scraped_data)} artikel potensial untuk '{search_query}'.")

            new_articles_for_stock = []
            for article in raw_scraped_data:
                # Pengecekan duplikat dengan URL yang sudah ada di database
                if article['url'] not in existing_urls:
                    new_articles_for_stock.append(article)
                    existing_urls.add(article['url']) # Tambahkan ke set agar tidak diproses lagi dalam loop yang sama

            if not new_articles_for_stock:
                print(f"Tidak ada artikel baru yang unik setelah pengecekan duplikat untuk '{search_query}'.")
                continue

            print(f"Ditemukan {len(new_articles_for_stock)} artikel BARU dan UNIK untuk '{search_query}'.")

            # Konversi ke DataFrame untuk kemudahan pemrosesan
            new_articles_df = pd.DataFrame(new_articles_for_stock)

            # --- 7. Pra-pemrosesan dan Sentimen Analisis dengan ML Model ---
            print("Melakukan pra-pemrosesan dan analisis sentimen dengan model ML...")
            
            # Gabungkan judul dan isi berita seperti di notebook jika Anda melatihnya dengan text_gabungan
            # Jika Anda melatih model hanya dengan 'isi_berita', sesuaikan di sini
            new_articles_df['text_gabungan'] = new_articles_df['judul'].apply(preprocess_text) + ' ' + \
                                               new_articles_df['isi_berita'].apply(preprocess_text)

            # Pastikan teks yang bersih tidak kosong sebelum vektorisasi dan prediksi
            new_articles_df = new_articles_df[new_articles_df['text_gabungan'].str.strip() != '']
            
            if new_articles_df.empty:
                print(f"Tidak ada konten yang valid setelah pra-pemrosesan untuk '{search_query}'.")
                continue

            # Vektorisasi teks (gunakan .transform(), BUKAN .fit_transform())
            X_new = vectorizer.transform(new_articles_df['text_gabungan'])
            
            # Prediksi sentimen (akan mengembalikan label angka)
            predictions_encoded = sentiment_model.predict(X_new)
            
            # Konversi label angka kembali ke label string menggunakan inverse_transform
            new_articles_df['sentimen'] = label_encoder.inverse_transform(predictions_encoded)

            print(f"Analisis sentimen selesai untuk {len(new_articles_df)} artikel.")

            # --- 8. Simpan Berita Baru ke Database MySQL ---
            insert_query = """
            INSERT INTO berita (saham_id, url, judul_berita, isi_berita, sentimen)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                judul_berita = VALUES(judul_berita), 
                isi_berita = VALUES(isi_berita), 
                sentimen = VALUES(sentimen);
            """
            
            articles_inserted_count = 0
            for index, row in new_articles_df.iterrows():
                try:
                    cursor.execute(insert_query, (
                        saham_id,
                        row['url'],
                        row['judul'],
                        row['isi_berita'],
                        row['sentimen'] # Menggunakan sentimen dari model ML
                    ))
                    articles_inserted_count += 1
                    total_new_articles_processed += 1
                except mysql.connector.Error as err:
                    print(f"Error saat menyimpan berita ke DB: {err} untuk URL: {row['url']}")
                    continue
            
            db_connection.commit() # Commit setiap selesai satu batch saham
            print(f"Berhasil menyimpan {articles_inserted_count} berita baru untuk Saham ID {saham_id} ke database.")

        print(f"\nTotal {total_new_articles_processed} artikel baru diproses dan disimpan ke database.")

    except mysql.connector.Error as err:
        print(f"Kesalahan Database: {err}")
    except Exception as e:
        print(f"Terjadi kesalahan tak terduga: {e}")
    finally:
        if db_connection and db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("Koneksi database ditutup.")
            
        # --- Simpan Waktu Terakhir Dijalankan (SETELAH SEMUA PROSES SELESAI) ---
        with open(LAST_RUN_FILE, 'w') as f:
            f.write(current_time.isoformat())
        print(f"[{datetime.now()}] Waktu terakhir dijalankan disimpan: {current_time.isoformat()}")
        print(f"[{datetime.now()}] Aplikasi Sentimen Analisis Berita selesai.")


if __name__ == "__main__":
    main()

