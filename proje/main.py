
"""-----------------------------------------------------------------------------------------"""
import requests
from bs4 import BeautifulSoup
import sqlite3

print("Ad                 SIRA        FİYAT          DEGİSİM")
# KAYNAK URL
# Sayfayı ALIYORUZ ihtiyacımız olan isimleri fiyatları ve hacim tablsonu çekip yazzdırıyoruz
url = "https://tr.tradingview.com/markets/cryptocurrencies/prices-all/"

sayfa = requests.get(url)

icerik = BeautifulSoup(sayfa.content, 'html.parser')

# Tablo içindeki tüm satırları seç
satirlar = icerik.find_all('tr')

# Her bir satır için
for satir in satirlar:
    # Satırdaki tüm hücreleri seç (en fazla 4 hücre)
    hucreler = satir.find_all('td', limit=4)

    # Her bir hücreyi yazdırmak için bir liste oluştur
    hucrе_metinleri = [hucre.get_text().strip() for hucre in hucreler]

    # Verileri düzenli bir şekilde yazdır
    if hucrе_metinleri:
        ad, sira, fiyat, degisim = hucrе_metinleri
        print("{:<20} {:<6} ${:<18} {:<10}".format(ad, sira, fiyat, degisim))
        #karakter genişliğini ayarlıyoruz

#SQL E KAYDETME İSİM VB..

# Sayfayı al
sayfa = requests.get(url)

# HTML içeriğini parse et
icerik = BeautifulSoup(sayfa.content, 'html.parser')

# SQLite veritabanı bağlantısı oluştur
conn = sqlite3.connect('cryptocurrency_prices.db')
cursor = conn.cursor()

# Tablo oluştur (eğer daha önce oluşturulmamışsa)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cryptocurrencies (
        ad TEXT,
        sira INTEGER,
        fiyat TEXT,
        degisim TEXT
    )
''')

# Commit işlemi
conn.commit()

# Tablo içindeki tüm satırları seç
satirlar = icerik.find_all('tr')

# Her bir satır için
for satir in satirlar:
    # Satırdaki tüm hücreleri seç (en fazla 4 hücre)
    hucreler = satir.find_all('td', limit=4)

    # Her bir hücreyi yazdırmak için bir liste oluştur
    hucrе_metinleri = [hucre.get_text().strip() for hucre in hucreler]

    # Veritabanına veri eklemek için
    if hucrе_metinleri:
        ad, sira, fiyat, degisim = hucrе_metinleri
        cursor.execute("INSERT INTO cryptocurrencies VALUES (?, ?, ?, ?)", (ad, sira, fiyat, degisim))

# Commit işlemi
conn.commit()

# Veritabanı bağlantısını kapat
conn.close()

#SQL KAYDETME BİTERR




#COİN İSİMLERİNİ ÇEKER
urltr = "https://tr.tradingview.com/markets/cryptocurrencies/prices-all/"
# Sayfayı al
sayfatr = requests.get(urltr)
# HTML içeriğini parse et
iceriktr = BeautifulSoup(sayfatr.content, 'html.parser')
# İlk class'taki div elementlerini seç
div_elements1tr = iceriktr.find_all("a", class_="apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat")
# Sadece ilk 10 ismi al
isimler = [div_element.get_text(strip=True) for div_element in div_elements1tr[:]]
#print(isimler)


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

        # TradingView sayfasındaki p ve span elementlerini seç
        p_elements = tradingview_icerik.find_all("p", class_="tv-widget-idea__description-row tv-widget-idea__description-row--clamped js-widget-idea__popup")
        p_elements2 = tradingview_icerik.find_all("span", class_="tv-card-user-info__name")
        p_elements3 = tradingview_icerik.find_all("span", class_="tv-card-social-item__count")
        p_elements4 = tradingview_icerik.find_all("span", class_="content-PlSmolIm badge-idea-content-ZleujXqe")
        # Her bir p ve span elementinin metnini yazdır

        for i in range(min(len(p_elements), len(p_elements2), len(p_elements3), len(p_elements4))):  # En kısa listenin uzunluğuna göre döngü
            p_yorumlar = p_elements[i].get_text()
            span_kadi = p_elements2[i].get_text()
            span_begeni = p_elements3[i].get_text()
            span_para = p_elements4[i].get_text()  # p_elements4'ten metni al
            print(f"{p_yorumlar} | KullanıcıAdı = {span_kadi} | BEGENİ SAYISI = {span_begeni} | ÖNGÖRÜ = {span_para}")  # Tüm metinleri yan yana yazdır

#SQL 2. KAYIT YORUMLAR
import requests
from bs4 import BeautifulSoup
import sqlite3

# Coin isimlerini çek
urltr = "https://tr.tradingview.com/markets/cryptocurrencies/prices-all/"
sayfatr = requests.get(urltr)
iceriktr = BeautifulSoup(sayfatr.content, 'html.parser')
div_elements1tr = iceriktr.find_all("a", class_="apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat")
aaaa = [div_element.get_text(strip=True) for div_element in div_elements1tr[:]]

# SQLite veritabanı bağlantısı oluştur
conn = sqlite3.connect('tradingview_data.db')
cursor = conn.cursor()

# Tablo oluştur (eğer daha önce oluşturulmamışsa)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS yeniii (
        coin_name TEXT,
        yorum TEXT,
        kullanici_adi TEXT,
        begeni_sayisi TEXT,
        ongoru TEXT
    )
''')

# Commit işlemi
conn.commit()

# base_url'yi farklı sayfa numaraları için güncelle
for isim in aaaa:
    for page_num in range(1, 11):
        base_url = f"https://tr.tradingview.com/symbols/{isim}USD/ideas/page-{page_num}/"
        tradingview_url = base_url.format(isim)

        tradingview_sayfa = requests.get(tradingview_url)
        tradingview_icerik = BeautifulSoup(tradingview_sayfa.content, 'html.parser')

        # TradingView sayfasındaki p ve span elementlerini seç
        p_yesss = tradingview_icerik.find_all("p",
                                                 class_="tv-widget-idea__description-row tv-widget-idea__description-row--clamped js-widget-idea__popup")
        qeqeqqe = tradingview_icerik.find_all("span", class_="tv-card-user-info__name")
        adaaasasasa = tradingview_icerik.find_all("span", class_="tv-card-social-item__count")
        adasasadadaas = tradingview_icerik.find_all("span", class_="content-PlSmolIm badge-idea-content-ZleujXqe")

        # Her bir p ve span elementinin metnini veritabanına ekle
        for i in range(min(len(p_yesss), len(qeqeqqe), len(adaaasasasa), len(adasasadadaas))):
            coin_name = isim
            yorum = p_yesss[i].get_text()
            kullanici_adi = qeqeqqe[i].get_text()
            begeni_sayisi = adaaasasasa[i].get_text()
            ongoru = adasasadadaas[i].get_text()

            cursor.execute("INSERT INTO yeniii VALUES (?, ?, ?, ?, ?)",
                           (coin_name, yorum, kullanici_adi, begeni_sayisi, ongoru))

            # Veritabanına eklenen veriyi yazdır
            print(f"Veri eklendi: {coin_name} ")

# Commit işlemi
conn.commit()

# Veritabanı bağlantısını kapat
conn.close()
