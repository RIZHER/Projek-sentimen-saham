import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

def scrape_idnfinancials_with_selenium(max_pages=None):
    """
    Scrapes company data using Selenium to handle JavaScript-rendered content.
    """
    all_data = []
    page_number = 1
    
    print("Memulai proses scraping dengan Selenium...")
    if max_pages:
        print(f"Scraping akan dibatasi hingga {max_pages} halaman.")
    else:
        print("Scraping akan berjalan hingga halaman terakhir.")

    # Mengatur driver Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Jalankan dalam mode headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
    
    # Menggunakan webdriver-manager untuk mendownload dan mengelola driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        while True:
            # Cek apakah batas halaman sudah tercapai
            if max_pages and page_number > max_pages:
                print(f"Batas halaman ({max_pages}) telah tercapai. Menghentikan scraping.")
                break

            # Buat URL berdasarkan nomor halaman
            if page_number == 1:
                url = "https://www.idnfinancials.com/id/company"
            else:
                url = f"https://www.idnfinancials.com/id/company/page/{page_number}"

            print(f"Mengakses data dari halaman: {url}")
            driver.get(url)

            # Menunggu hingga elemen .table-container muncul, yang menandakan konten sudah dimuat
            # Waktu tunggu diperpanjang menjadi 20 detik
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'table-container'))
                )
                print("Elemen utama 'table-container' ditemukan. Data sedang dimuat...")
            except TimeoutException:
                print("Waktu tunggu habis. Elemen utama tidak ditemukan. Menganggap ini adalah halaman terakhir atau halaman error.")
                break

            # Ambil HTML yang sudah lengkap setelah JavaScript di-render
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Cari semua elemen dengan class 'tc tc-company'
            company_elements = soup.find_all('div', class_='tc tc-company')
            
            if not company_elements:
                print("Tidak ada lagi data perusahaan yang ditemukan di halaman ini. Menghentikan proses scraping.")
                break
            
            # Ekstrak data dari setiap elemen
            for company_el in company_elements:
                # code_el = company_el.find('div', class_='code')
                # name_el = company_el.find('div', class_='name')
                
                code_el = company_el.find('div', {'class': 'code'})
                name_el = company_el.find('div', {'class': 'name'})
                if code_el and name_el:
                    code = code_el.get_text(strip=True)
                    name = name_el.get_text(strip=True)
                    all_data.append({'kode': code, 'nama': name})
            
            print(f"Berhasil mengambil data dari halaman {page_number}. Ditemukan {len(company_elements)} perusahaan.")
            
            page_number += 1
            time.sleep(3) # Beri jeda antara permintaan halaman

    finally:
        # Pastikan driver browser ditutup meskipun terjadi error
        driver.quit()

    # Simpan data ke CSV
    if all_data:
        df = pd.DataFrame(all_data)
        print(df)
        csv_filename = 'data_perusahaan_idnfinancials.csv'
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        print("\n" + "="*50)
        print(f"Proses scraping selesai! Data berhasil disimpan ke dalam file: '{csv_filename}'")
        print(f"Total {len(df)} data perusahaan berhasil diekstrak.")
        print("="*50)
    else:
        print("\nTidak ada data yang berhasil diekstrak.")

# --- Cara menjalankan fungsi scraping ---

if __name__ == "__main__":
    scrape_idnfinancials_with_selenium(max_pages=2)