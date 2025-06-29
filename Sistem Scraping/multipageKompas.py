import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

def scrape_kompas_search_filtered(query, max_articles):
    """
    Scrapes the latest text articles from Kompas.com search results.
    It iterates through multiple pages to reach the target number of articles.
    """

    base_url = "https://search.kompas.com/search"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    scraped_data = []
    page = 1
    scraped_count = 0
    
    # --- Tambahkan counter untuk halaman yang tidak relevan ---
    irrelevant_page_count = 0
    max_irrelevant_pages = 10 # Atur batas halaman yang tidak relevan secara berturut-turut
    
    print(f"Mulai scraping berita terbaru untuk kata kunci '{query}'. Target: {max_articles} artikel.")

    while scraped_count < max_articles:
        if irrelevant_page_count >= max_irrelevant_pages:
            print(f"\n--- [OPTIMASI] Melewatkan kata kunci '{query}' karena tidak ada artikel relevan selama {max_irrelevant_pages} halaman berturut-turut. ---")
            break

        # Kompas.com menggunakan parameter 'q' untuk query dan 'p' untuk halaman
        search_url = f"{base_url}?q={query}&p={page}"
        print(f"\n--- Mengakses halaman {page} untuk kata kunci '{query}' ---")
        
        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error saat mengakses URL pencarian {search_url}: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('div', {'class': 'articleItem'})
        
        if not articles:
            print(f"Tidak ada artikel lagi di halaman {page}. Menghentikan scraping untuk '{query}'.")
            break

        # Cek apakah ada artikel relevan di halaman ini
        found_relevant_on_page = False
        
        for article in articles:
            if scraped_count >= max_articles:
                break
            
            link_tag = article.find('a', {'class': 'article-link'}) 
            if not link_tag or not link_tag.has_attr('href'):
                continue
            
            article_url = link_tag['href']
            
            # Melewatkan link non-artikel dan yang sudah di-scrape
            if not article_url.startswith("https://") or any(data['url'] == article_url for data in scraped_data):
                continue

            try:
                article_response = requests.get(article_url, headers=headers)
                article_response.raise_for_status()
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
                
                title_tag = article_soup.find('h1', {'class': 'read__title'})
                judul = title_tag.get_text(strip=True) if title_tag else "Judul tidak ditemukan"

                body_tag = article_soup.find('div', {'class': 'read__content'})
                isi_berita = ""
                if body_tag:
                    paragraphs = body_tag.find_all('p')
                    unwanted_phrases = ["Baca juga:", "Lihat juga:", "KOMPAS.com -", "Halaman selanjutnya", "Editor:", "Penulis:"]
                    isi_berita_list = []
                    for p in paragraphs:
                        text = p.get_text(strip=True)
                        if text and not any(unwanted in text for unwanted in unwanted_phrases):
                            isi_berita_list.append(text)
                    
                    isi_berita = "\n".join(isi_berita_list)
                
                # --- Verifikasi relevansi ---
                if isi_berita and (query.lower() in judul.lower() or query.lower() in isi_berita.lower()):
                    scraped_data.append({
                        'kata_kunci': query,
                        'judul': judul,
                        'url': article_url,
                        'isi_berita': isi_berita.strip()
                    })
                    scraped_count += 1
                    found_relevant_on_page = True # Tandai bahwa artikel relevan ditemukan di halaman ini
                    print(f"  -> [SUCCESS] ({scraped_count}/{max_articles}) Berhasil scrape: {judul}")
                else:
                    print(f"  -> [SKIPPED] Tidak relevan dengan kata kunci: {judul} (URL: {article_url})")

            except requests.exceptions.RequestException as e:
                print(f"Error saat mengakses artikel {article_url}: {e}")
                continue
        
        # --- Perbarui counter relevansi ---
        if found_relevant_on_page:
            irrelevant_page_count = 0 # Reset counter jika ada artikel yang relevan di halaman ini
        else:
            irrelevant_page_count += 1 # Tambah counter jika tidak ada yang relevan
            print(f"  -> Tidak ada artikel relevan di halaman {page}. Counter: {irrelevant_page_count}/{max_irrelevant_pages}")
            
        page += 1
        print(f"  -> Menunggu 2 detik sebelum pindah ke halaman berikutnya untuk '{query}'...")
        time.sleep(2)
            
    return scraped_data

def save_to_csv(data, filename):
    """Saves the scraped data to a CSV file using pandas."""
    if not data:
        print("Tidak ada data untuk disimpan.")
        return

    df = pd.DataFrame(data)
    try:
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"✅ Data berhasil disimpan ke file CSV: '{os.path.abspath(filename)}'")
    except Exception as e:
        print(f"❌ Gagal menyimpan data ke CSV: {e}")

# --- Contoh Penggunaan dengan Multiple Keywords ---
if __name__ == "__main__":
    
    # Daftar kata kunci yang ingin di-scrape
    keywords_to_scrape = [
        "bca", # BBCA
        "bri", # BBRI
        "bni", # TPIA
        "goto", # BREN
        "bank mandiri", # BMRI
        "Astra", # BYAN
        "Telkom",
    ]
    
    # Anda bisa mengatur jumlah artikel yang diinginkan per kata kunci
    jumlah_berita_per_keyword = 100
    
    # List kosong untuk menampung semua data
    all_scraped_data = []

    # Loop melalui setiap kata kunci
    for keyword in keywords_to_scrape:
        print("\n" + "="*50)
        print(f"MEMULAI SCRAPING UNTUK KATA KUNCI: {keyword.upper()}")
        print("="*50 + "\n")
        
        # Panggil fungsi scraping untuk setiap kata kunci
        data_per_keyword = scrape_kompas_search_filtered(keyword, jumlah_berita_per_keyword)
        
        # Tambahkan hasil scraping ke list gabungan
        all_scraped_data.extend(data_per_keyword)
        
        print(f"\n--- Selesai scraping '{keyword}'. Total {len(data_per_keyword)} artikel berhasil diambil. ---")
        # Jeda waktu yang lebih lama antar kata kunci untuk mengurangi risiko pemblokiran
        print("Menunggu 5 detik sebelum pindah ke kata kunci berikutnya...")
        time.sleep(5)

    print("\n" + "#"*50)
    print(f"SCRAPING SEMUA KATA KUNCI SELESAI. TOTAL DATA: {len(all_scraped_data)} ARTIKEL")
    print("#"*50 + "\n")

    # Simpan semua data gabungan ke dalam satu file CSV
    if all_scraped_data:
        # Tentukan nama file output gabungan
        output_filename_csv = "berita_kompas_multikeyword_2.csv"
        
        # Simpan ke CSV
        save_to_csv(all_scraped_data, output_filename_csv)
    else:
        print("Tidak ada data yang berhasil di-scrape dari semua kata kunci.")