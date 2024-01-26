import requests
from bs4 import BeautifulSoup
import sqlite3

# Veritabanı bağlantısı oluştur
baglanti = sqlite3.connect("tradingview.db")

# Tablo oluştur
cursor = baglanti.cursor()
cursor.execute("""CREATE TABLE if not exists fikirler (
    id integer primary key autoincrement,
    isim text,
    page_num integer,
    text text
)""")

# Veritabanından verileri çek
url = "https://tr.tradingview.com/markets/cryptocurrencies/prices-all/"

# Sayfayı al
sayfa = requests.get(url)

# HTML içeriğini parse et
icerik = BeautifulSoup(sayfa.content, 'html.parser')

# İlk class'taki div elementlerini seç
div_elements1 = icerik.find_all("a", class_="apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat")

# Sadece ilk 10 ismi al
isimler = [div_element.get_text(strip=True) for div_element in div_elements1[:]]

# base_url'yi farklı sayfa numaraları için güncelle
for isim in isimler:
    for page_num in range(1, 6):  # Örneğin, burada sadece ilk 5 sayfa çekilecek
        base_url = f"https://tr.tradingview.com/symbols/{isim}USD/ideas/page-{page_num}/"

        # URL oluştur
        tradingview_url = base_url.format(isim)

        # Oluşturulan URL'yi yazdır
        print(f"{isim}- Sayfa {page_num}: {tradingview_url}")

        # Oluşturulan URL'ye GET isteği gönder
        tradingview_sayfa = requests.get(tradingview_url)

        # HTML içeriğini parse et
        tradingview_icerik = BeautifulSoup(tradingview_sayfa.content, 'html.parser')

        # TradingView sayfasındaki p elementlerini seç
        p_elements = tradingview_icerik.find_all("p", class_="tv-widget-idea__description-row tv-widget-idea__description-row--clamped js-widget-idea__popup")

        # Her bir p elementinin metnini yazdır
        for p_element in p_elements:
            # Veritabanına kaydet
            cursor.execute("""INSERT INTO fikirler (isim, page_num, text) VALUES (?, ?, ?)""", (isim, page_num, p_element.get_text()))

# Değişiklikleri veritabanına kaydet
baglanti.commit()

# Bağlantıyı kapat
baglanti.close()
