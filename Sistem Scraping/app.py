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
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import sys
import fcntl # Library untuk lock file di sistem Unix/Linux

# --- TENTUKAN JALUR DASAR SKRIP INI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from Scraping.multipageDetik import scrape_detik_search_filtered

# --- NLTK Data Download ---
import nltk
try:
    os.environ['NLTK_DATA'] = os.path.join(BASE_DIR, 'nltk_data')
    
    stopwords.words('indonesian')
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("📦 Mengunduh data NLTK 'stopwords' dan 'punkt'...")
    nltk.download('stopwords', download_dir=os.path.join(BASE_DIR, 'nltk_data'))
    nltk.download('punkt', download_dir=os.path.join(BASE_DIR, 'nltk_data'))
    print("✅ Pengunduhan selesai.")

# Pastikan NLTK_DATA PATH diatur agar NLTK menemukan data yang diunduh
os.environ['NLTK_DATA'] = os.path.join(BASE_DIR, 'nltk_data')


# --- Konfigurasi Database MySQL ---
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 8889, # Sesuaikan jika portnya berbeda di hosting Anda
    'database': 'AlphaSentimen',
    'user': 'root',
    'password': 'root'
}

# --- Konfigurasi File Scheduler Sederhana ---
LAST_RUN_FILE = os.path.join(BASE_DIR, 'last_run.txt')

# --- Lokasi Model, Vectorizer, dan Label Encoder ---
MODEL_PATH = os.path.join(BASE_DIR, 'my_model.joblib')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'my_vectorizer.joblib')
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, 'my_label_encoder.joblib')

# --- Konfigurasi Lock File ---
LOCK_FILE = os.path.join(BASE_DIR, 'app_scraper.lock')


# --- Inisialisasi Stopwords dan Stemmer (HARUS SAMA PERSIS DENGAN SAAT PELATIHAN MODEL) ---
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


# --- Fungsi Baru: Update Sentimen Keseluruhan Saham di saham_profile ---
def update_overall_stock_sentiment(db_connection):
    """
    Mengambil semua saham, menghitung sentimen mayoritas dari berita terkait,
    dan memperbarui kolom 'sentimen' di tabel 'saham_profile'.
    """
    print(f"[{datetime.now()}] Memulai pembaruan sentimen keseluruhan saham di 'saham_profile'...")
    cursor = None
    try:
        cursor = db_connection.cursor(dictionary=True)

        # Ambil semua saham_id dari tabel saham_profile
        cursor.execute("SELECT saham_id, nama_saham FROM saham_profile")
        all_stocks = cursor.fetchall()

        if not all_stocks:
            print(f"[{datetime.now()}] Tidak ada saham ditemukan di tabel 'saham_profile' untuk diperbarui sentimennya.")
            return

        for stock in all_stocks:
            saham_id = stock['saham_id']
            nama_saham = stock['nama_saham']

            print(f"[{datetime.now()}] Menganalisis sentimen untuk '{nama_saham}' (ID: {saham_id})...")

            # Ambil semua sentimen berita yang terkait dengan saham_id ini
            cursor.execute("""
                SELECT sentimen, COUNT(*) as count
                FROM berita
                WHERE saham_id = %s
                GROUP BY sentimen
                ORDER BY count DESC
                LIMIT 1
            """, (saham_id,))
            
            majority_sentiment_row = cursor.fetchone()

            if majority_sentiment_row:
                majority_sentiment = majority_sentiment_row['sentimen']
                print(f"[{datetime.now()}] Sentimen mayoritas untuk '{nama_saham}' adalah: {majority_sentiment}")
                
                # Perbarui kolom 'sentimen' di tabel 'saham_profile'
                update_saham_profile_query = """
                    UPDATE saham_profile
                    SET sentimen = %s
                    WHERE saham_id = %s;
                """
                cursor.execute(update_saham_profile_query, (majority_sentiment, saham_id))
                db_connection.commit()
                print(f"[{datetime.now()}] Kolom sentimen di 'saham_profile' untuk '{nama_saham}' berhasil diperbarui menjadi '{majority_sentiment}'.")
            else:
                print(f"[{datetime.now()}] Tidak ada data sentimen berita untuk '{nama_saham}' (ID: {saham_id}). Sentimen saham tidak diperbarui.")

    except mysql.connector.Error as err:
        print(f"[{datetime.now()}] Kesalahan Database saat memperbarui sentimen saham: {err}")
    except Exception as e:
        print(f"[{datetime.now()}] Terjadi kesalahan tak terduga saat memperbarui sentimen saham: {e}")
    finally:
        if cursor:
            cursor.close()
    print(f"[{datetime.now()}] Pembaruan sentimen keseluruhan saham selesai.")


# --- Fungsi Utama Aplikasi ---
def main():
    print(f"[{datetime.now()}] Memulai aplikasi Sentimen Analisis Berita...")

    # --- 0. Implementasi Lock File ---
    lock_file_fd = None
    try:
        lock_file_fd = open(LOCK_FILE, 'w')
        fcntl.flock(lock_file_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print(f"[{datetime.now()}] Acquired lock: {LOCK_FILE}")
    except IOError:
        print(f"[{datetime.now()}] ERROR: Lock file '{LOCK_FILE}' sudah ada atau tidak bisa didapat. Skrip lain mungkin sedang berjalan. Keluar.")
        if lock_file_fd:
            lock_file_fd.close()
        sys.exit(0)
    except Exception as e:
        print(f"[{datetime.now()}] ERROR: Kesalahan tak terduga saat mencoba lock file: {e}")
        sys.exit(1)

    try: # Seluruh logika aplikasi utama dipindahkan ke dalam blok try ini

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
            minimum_interval = timedelta(hours=1)

            if time_diff < minimum_interval:
                time_to_wait = minimum_interval - time_diff
                print(f"[{current_time}] Skrip terakhir dijalankan {time_diff} yang lalu.")
                print(f"⏳ Menunggu {time_to_wait} sebelum melanjutkan scraping...")
                time.sleep(time_to_wait.total_seconds())
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
            sys.exit(1)
        except Exception as e:
            print(f"Error tak terduga saat memuat model/vectorizer/encoder: {e}")
            sys.exit(1)

        db_connection = None
        try:
            # --- 3. Koneksi ke Database MySQL ---
            db_connection = mysql.connector.connect(**DB_CONFIG)
            cursor = db_connection.cursor(dictionary=True)

            print("Berhasil terhubung ke database MySQL.")

            # --- 4. Ambil Kata Kunci (nama_saham) dari tabel saham_profile ---
            cursor.execute("SELECT saham_id, nama_saham FROM saham_profile")
            stock_keywords = cursor.fetchall()

            if not stock_keywords:
                print("Tidak ada kata kunci saham ditemukan di tabel 'saham_profile'.")
                # Jika tidak ada saham, tetap perlu menutup koneksi dan lock
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
                
                search_query = f"{nama_saham}" 
                print(f"\n--- Memproses kata kunci: '{search_query}' (Saham ID: {saham_id}) ---")

                raw_scraped_data = scrape_detik_search_filtered(search_query, max_articles=20)
                
                if not raw_scraped_data:
                    print(f"Tidak ada berita baru yang di-scrape untuk '{search_query}'.")
                    continue

                print(f"Ditemukan {len(raw_scraped_data)} artikel potensial untuk '{search_query}'.")

                new_articles_for_stock = []
                for article in raw_scraped_data:
                    if article['url'] not in existing_urls:
                        new_articles_for_stock.append(article)
                        existing_urls.add(article['url'])

                if not new_articles_for_stock:
                    print(f"Tidak ada artikel baru yang unik setelah pengecekan duplikat untuk '{search_query}'.")
                    continue

                print(f"Ditemukan {len(new_articles_for_stock)} artikel BARU dan UNIK untuk '{search_query}'.")

                new_articles_df = pd.DataFrame(new_articles_for_stock)

                # --- 7. Pra-pemrosesan dan Sentimen Analisis dengan ML Model ---
                print("Melakukan pra-pemrosesan dan analisis sentimen dengan model ML...")
                
                new_articles_df['text_gabungan'] = new_articles_df['judul'].apply(preprocess_text) + ' ' + \
                                                   new_articles_df['isi_berita'].apply(preprocess_text)

                new_articles_df = new_articles_df[new_articles_df['text_gabungan'].str.strip() != '']
                
                if new_articles_df.empty:
                    print(f"Tidak ada konten yang valid setelah pra-pemrosesan untuk '{search_query}'.")
                    continue

                X_new = vectorizer.transform(new_articles_df['text_gabungan'])
                predictions_encoded = sentiment_model.predict(X_new)
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
                            row['sentimen']
                        ))
                        articles_inserted_count += 1
                        total_new_articles_processed += 1
                    except mysql.connector.Error as err:
                        print(f"Error saat menyimpan berita ke DB: {err} untuk URL: {row['url']}")
                        continue
                
                db_connection.commit()
                print(f"Berhasil menyimpan {articles_inserted_count} berita baru untuk Saham ID {saham_id} ke database.")

            print(f"\nTotal {total_new_articles_processed} artikel baru diproses dan disimpan ke database.")

            # --- PANGGIL FUNGSI UNTUK MEMPERBARUI SENTIMEN KESELURUHAN SAHAM DI SINI ---
            update_overall_stock_sentiment(db_connection)

        except mysql.connector.Error as err:
            print(f"Kesalahan Database: {err}")
            sys.exit(1)
        except Exception as e:
            print(f"Terjadi kesalahan tak terduga: {e}")
            sys.exit(1)
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

    finally: # Blok finally ini akan selalu dieksekusi, memastikan lock file dilepas
        # --- Pastikan lock file dilepas saat skrip selesai (penting!) ---
        if lock_file_fd:
            fcntl.flock(lock_file_fd, fcntl.LOCK_UN) # Lepaskan kunci
            lock_file_fd.close()
            # os.remove(LOCK_FILE) # Tidak menghapus file, biarkan tetap ada untuk debug/inspeksi manual
            print(f"[{datetime.now()}] Released lock: {LOCK_FILE}")
            # Anda bisa menghapus os.remove(LOCK_FILE) jika Anda ingin file lock tetap ada dan hanya dikunci/dilepas.
            # Jika Anda ingin file lock otomatis hilang, uncomment baris di bawah:
            os.remove(LOCK_FILE) 
            print(f"[{datetime.now()}] Removed lock file: {LOCK_FILE}")


if __name__ == "__main__":
    main()