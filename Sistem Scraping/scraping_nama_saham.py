import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_idnfinancials_rel_next_page():
    base_url = "https://www.idnfinancials.com/id/company"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    all_stock_data = []
    current_page_url = base_url # Start with the base URL for the first page
    page_counter = 1 # Just for logging purposes

    while current_page_url:
        full_url = current_page_url
        # If it's the base URL, ensure it's /page/1
        if current_page_url == base_url:
            full_url = f"{base_url}/page/1"
        
        print(f"Mengambil data dari halaman {page_counter}: {full_url}")
        
        try:
            response = requests.get(full_url, headers=headers)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            soup = BeautifulSoup(response.text, 'html.parser')

            company_divs = soup.find_all('div', class_='tc tc-company')

            if not company_divs:
                # If no company divs found, it might be the very last page with no content, or an error
                print(f"Tidak ada data perusahaan ditemukan di halaman {page_counter}. Berhenti scraping.")
                break # Stop if no data found on what should be a data page
            
            for company_div in company_divs:
                stock_code_span = company_div.find('span', class_='code')
                company_name_span = company_div.find('span', class_='name')

                if stock_code_span and company_name_span:
                    stock_code = stock_code_span.text.strip().upper()
                    company_name = company_name_span.text.strip()
                    
                    all_stock_data.append({
                        "Kode Saham": stock_code,
                        "Nama Perusahaan": company_name
                    })
            
            print(f"Halaman {page_counter} selesai. Total data terkumpul: {len(all_stock_data)}")

            # --- Optimal Logic to find the 'Next' page link using rel="next" ---
            # Look for an 'a' tag with rel="next" attribute
            next_page_link_tag = soup.find('a', rel='next')
            
            if next_page_link_tag:
                relative_next_url = next_page_link_tag.get('href')
                if relative_next_url:
                    # Construct full URL. The website already provides full URL, but good to ensure.
                    if not relative_next_url.startswith('http'):
                        # If for some reason it's relative, make it absolute
                        # We need to be careful with the base URL, ensuring it matches "https://www.idnfinancials.com"
                        # The screenshot shows full URL, so this might not be strictly necessary
                        # but it's a good defensive coding practice.
                        current_page_url = "https://www.idnfinancials.com" + relative_next_url
                    else:
                        current_page_url = relative_next_url
                else:
                    # href attribute is empty, so no next page
                    current_page_url = None
            else:
                # No 'a' tag with rel="next" found, implies this is the last page
                print(f"Tidak ada tombol 'Next' (rel='next') ditemukan. Diasumsikan halaman terakhir.")
                current_page_url = None
            
            page_counter += 1
            time.sleep(1.5) # Be polite: Add a slight delay between page requests

        except requests.exceptions.RequestException as e:
            print(f"Error saat mengambil halaman {page_counter} ({full_url}): {e}")
            current_page_url = None # Stop scraping on error
        except Exception as e:
            print(f"Terjadi error tak terduga saat scraping halaman {page_counter} ({full_url}): {e}")
            current_page_url = None # Stop scraping on unexpected error

    print(f"\nSelesai scraping. Total {len(all_stock_data)} entri perusahaan berhasil dikumpulkan.")
    return all_stock_data

if __name__ == "__main__":
    companies = scrape_idnfinancials_rel_next_page()

    if companies:
        df = pd.DataFrame(companies)
        print("\nData Saham (5 baris pertama):")
        print(df.head())
        print(f"\nTotal entri unik: {df['Kode Saham'].nunique()}")

        # Save to CSV
        csv_filename = "data_saham_idnfinancials_rel_next_page.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        print(f"\nData berhasil disimpan ke {csv_filename}")

        # Save to Excel (requires openpyxl: pip install openpyxl)
        excel_filename = "data_saham_idnfinancials_rel_next_page.xlsx"
        df.to_excel(excel_filename, index=False)
        print(f"Data berhasil disimpan ke {excel_filename}")
    else:
        print("Tidak ada data yang berhasil di-scrape dari semua halaman.")