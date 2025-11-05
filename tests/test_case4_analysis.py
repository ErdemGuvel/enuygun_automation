"""
Test Case 4: Analysis and Categorization
Develops tests for extracting and analyzing data from search results
"""
import datetime
import time
import csv
import os
from utils.browser_factory import create_driver, load_config
from pages.home_page import HomePage
from pages.results_page import ResultsPage
from utils.csv_helper import CSVHelper
from utils.data_analysis import DataAnalyzer


def test_flight_data_analysis():
    """
    Case 4: Analysis and Categorization - Data Extraction & Analysis
    
    PREREQUISITES (ÖNCÜLLER):
    =========================
    Bu test aşağıdaki verileri toplamak ve analiz etmek için gereklidir:
    
    1. Departure/Arrival Times (Kalkış/Varış Saatleri)
       - Format: HH:MM (örn: 10:30, 18:45)
       - Purpose: Saat bazında fiyat analizi için
    
    2. Airline Name (Havayolu Adı)
       - Format: String (örn: "Türk Hava Yolları", "Pegasus")
       - Purpose: Havayolu bazında fiyat istatistikleri için
    
    3. Price (Fiyat)
       - Format: Numeric (TL cinsinden)
       - Purpose: Fiyat analizi, karşılaştırma ve en uygun uçuş belirleme için
    
    4. Connection Information (Aktarma Bilgisi)
       - Format: String (örn: "Direct", "1 Stop", "Has Connection")
       - Purpose: Uçuş özelliklerini kategorize etmek için
    
    5. Flight Duration (Uçuş Süresi)
       - Format: String (örn: "1s 30d", "2s 15d")
       - Purpose: Uçuş süresi analizi için
    
    TEST WORKFLOW:
    ==============
    1. Perform flight search (Istanbul -> Nicosia)
    2. Extract all flight data (prerequisites listed above)
    3. Save data to CSV file
    4. Read CSV file and analyze data
    5. Generate visualizations:
       - Airline price comparison (Min, Max, Avg) - GRAPH
       - Price distribution by time slots - HEAT MAP
       - Cost-effective flights identification - ALGORITHM
    6. Test is repeatable for different dates and routes
    """

    config = load_config()
    driver = create_driver()
    home = HomePage(driver)
    results = ResultsPage(driver)

    try:
        url = config['site']['url']
        dep_city = "İstanbul"
        dest_city = "Lefkoşa"
        days_ahead = config['dates']['days_ahead_departure']
        return_days = config['dates']['days_ahead_return']

        today = datetime.date.today()
        dep_date = (today + datetime.timedelta(days=days_ahead)).strftime(config['dates']['format'])
        ret_date = (today + datetime.timedelta(days=days_ahead + return_days)).strftime(config['dates']['format'])

        print("=" * 70)
        print("[ANALYSIS] CASE 4: Flight Data Analysis & Categorization")
        print("=" * 70)
        print("[PREREQUISITES] Data to be collected:")
        print("   • Departure/Arrival Times (HH:MM format)")
        print("   • Airline Name")
        print("   • Price (TL)")
        print("   • Connection Information (Direct/Stop)")
        print("   • Flight Duration")
        print("=" * 70)
        print(f"[INFO] Route: {dep_city} -> {dest_city}")
        print(f"[INFO] Dates: {dep_date} -> {ret_date}")
        print(f"[INFO] Test tekrarlanabilir - farklı rotalar için şehir/tarihleri değiştirin")
        print("=" * 70)

        print("\n[STEP 1] Ana sayfaya git ve arama yap")
        home.open(url)
        print(f"[INFO] Searching: {dep_city} -> {dest_city}")
        print(f"[INFO] Dates: {dep_date} - {ret_date}")
        home.search_round_trip(dep_city, dest_city, dep_date, ret_date)
        print("[OK] Uçuş araması tamamlandı")

        print("\n[STEP 2] Arama sonuçlarını bekle")
        results.wait_for_results()
        time.sleep(2)
        
        flight_count = results.get_flight_count()
        
        if flight_count == 0:
            print("[WARNING] Bu rota için uçuş bulunamadı. Alternatif yaklaşım deneniyor...")
            time.sleep(3)
            flight_count = results.get_flight_count()
        
        print(f"[INFO] {flight_count} uçuş bulundu")

        print("\n[STEP 3] Tüm sonuçlardan uçuş verilerini çıkar")
        print("[INFO] Çıkarılan veriler: kalkış/varış saatleri, havayolu, fiyat, bağlantı, süre")
        
        flight_data = results.extract_all_flight_data()
        
        if not flight_data or len(flight_data) == 0:
            print("[ERROR] Uçuş verisi çıkarılamadı!")
            print("[INFO] Bu rota için uçuş olmayabilir veya sayfa yapısı değişmiş olabilir")
            print("[INFO] Test sonlandırılıyor - farklı rota deneyin veya sayfa yapısını kontrol edin")
            raise Exception("Uçuş verisi çıkarılamadı")
        
        print(f"[OK] {len(flight_data)} uçuş kaydı başarıyla çıkarıldı")
        
        if len(flight_data) > 0:
            print("[INFO] Sample extracted data (first flight):")
            sample = flight_data[0]
            print(f"   • Departure: {sample.get('departure_time', 'N/A')}")
            print(f"   • Arrival: {sample.get('arrival_time', 'N/A')}")
            print(f"   • Airline: {sample.get('airline', 'N/A')}")
            print(f"   • Price: {sample.get('price', 'N/A')}TL")
            print(f"   • Connection: {sample.get('connection', 'N/A')}")
            print(f"   • Duration: {sample.get('duration', 'N/A')}")

        print("\n[STEP 4] Çıkarılan verileri CSV dosyasına kaydet")
        csv_filename = f"flight_data_{dep_city.replace(' ', '_')}_{dest_city.replace(' ', '_')}_{today.strftime('%Y%m%d')}.csv"
        csv_path = os.path.join("reports", csv_filename)
        os.makedirs("reports", exist_ok=True)
        
        CSVHelper.save_flight_data(flight_data, csv_path)
        print(f"[OK] {len(flight_data)} uçuş verisi CSV'ye kaydedildi: {csv_path}")
        print(f"[INFO] CSV dosyası içeriği: departure_time, arrival_time, airline, price, connection, duration")

        print("\n[STEP 5] CSV dosyasını oku ve veriyi analiz et")
        print("[INFO] Analiz için CSV dosyası okunuyor...")
        
        csv_helper = CSVHelper()
        csv_base_name = csv_filename.replace('.csv', '').replace('reports/', '')
        loaded_data = csv_helper.read_from_csv(csv_base_name)
        
        if loaded_data and len(loaded_data) > 0:
            print(f"[OK] CSV dosyası başarıyla okundu: {len(loaded_data)} kayıt CSV'den yüklendi")
            print("[INFO] CSV dosyasından veri analiz ediliyor")
            analyzer = DataAnalyzer(loaded_data)
        else:
            print("[WARNING] CSV dosyası okunamadı veya boş, orijinal çıkarılan veri kullanılacak")
            print("[INFO] CSV yeni oluşturulmuş olabilir - analiz orijinal veri ile devam edecek")
            analyzer = DataAnalyzer(flight_data)
        
        print("\n[STEP 6] Havayolu başına fiyat istatistiklerini hesapla (Min, Max, Ortalama)")
        print("[INFO] CSV verisinden havayolu başına fiyat istatistikleri hesaplanıyor...")
        airline_stats = analyzer.calculate_airline_price_stats()
        
        if airline_stats:
            print("[DATA] Havayolu Fiyat İstatistikleri (Min, Max, Ortalama):")
            for airline, stats in sorted(airline_stats.items()):
                if airline != "Unknown":
                    print(f"   • {airline}:")
                    print(f"     - Minimum Fiyat: {stats['min']:.0f}TL")
                    print(f"     - Maksimum Fiyat: {stats['max']:.0f}TL")
                    print(f"     - Ortalama Fiyat: {stats['avg']:.0f}TL")
                    print(f"     - Uçuş Sayısı: {stats['count']}")
        else:
            print("[WARNING] Havayolu istatistikleri hesaplanamadı")

        print("\n[STEP 7] En uygun maliyetli uçuşları belirle (Algoritma)")
        print("[INFO] Algoritma: En düşük %30 fiyat aralığındaki uçuşları buluyor...")
        cost_effective_flights = analyzer.find_cost_effective_flights()
        print(f"[OK] Algoritma {len(cost_effective_flights)} en uygun maliyetli uçuş belirledi")
        
        if cost_effective_flights:
            print("[INFO] En uygun maliyetli ilk 5 uçuş:")
            for i, flight in enumerate(cost_effective_flights[:5], 1):
                airline = flight.get('airline', 'Unknown')
                price = flight.get('price', 'N/A')
                dep_time = flight.get('departure_time', 'N/A')
                connection = flight.get('connection', 'N/A')
                print(f"   {i}. {airline} - {price}TL | Kalkış: {dep_time} | Bağlantı: {connection}")

        print("\n[STEP 8] Analiz edilen verilerden görselleştirmeleri oluştur")
        
        os.makedirs("reports", exist_ok=True)
        
        route_suffix = f"{dep_city.replace(' ', '_')}_{dest_city.replace(' ', '_')}"
        timestamp = today.strftime('%Y%m%d')
        
        print("[INFO] Havayolu fiyat karşılaştırma grafiği oluşturuluyor (Havayolu başına Min, Max, Ortalama)...")
        airline_comp_file = f"reports/airline_comparison_{route_suffix}_{timestamp}.png"
        analyzer.create_airline_comparison_chart(airline_comp_file)
        print(f"[OK] Grafik kaydedildi: {airline_comp_file}")
        
        print("[INFO] Farklı saat dilimlerinde fiyat dağılımı ısı haritası oluşturuluyor...")
        heatmap_file = f"reports/time_price_heatmap_{route_suffix}_{timestamp}.png"
        analyzer.create_time_price_heatmap(heatmap_file)
        print(f"[OK] Isı haritası kaydedildi: {heatmap_file}")
        
        print("[INFO] Fiyat dağılım grafiği oluşturuluyor...")
        price_dist_file = f"reports/price_distribution_{route_suffix}_{timestamp}.png"
        analyzer.create_price_distribution_chart(price_dist_file)
        print(f"[OK] Grafik kaydedildi: {price_dist_file}")
        
        print("[OK] Tüm görselleştirmeler CSV verisinden başarıyla oluşturuldu")

        print("\n" + "=" * 70)
        print("[BAŞARILI] CASE 4 ANALİZİ TAMAMLANDI!")
        print("=" * 60)
        print("[ÖZET] Analiz Sonuçları:")
        print(f"   • Rota: {dep_city} -> {dest_city}")
        print(f"   • Tarihler: {dep_date} - {ret_date}")
        print(f"   • Analiz edilen toplam uçuş: {len(flight_data)}")
        print(f"   • Bulunan havayolları: {len(airline_stats)}")
        
        valid_prices = [f['price'] for f in flight_data if f.get('price') is not None]
        if valid_prices:
            print(f"   • Fiyat aralığı: {min(valid_prices)}TL - {max(valid_prices)}TL")
            print(f"   • Ortalama fiyat: {sum(valid_prices)/len(valid_prices):.2f}TL")
        
        print(f"   • En uygun maliyetli uçuşlar: {len(cost_effective_flights)}")
        print(f"   • CSV dosyası: {csv_path}")
        print(f"   • Görselleştirmeler: {airline_comp_file}, {heatmap_file}, {price_dist_file}")
        print("=" * 70)
        
        print("\n[INFO] Browser 10 saniye açık kalacak...")
        time.sleep(10)
        print("[INFO] Browser kapatılıyor...")

    except Exception as e:
        print(f"[ERROR] Test sırasında hata oluştu: {str(e)}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        try:
            driver.save_screenshot(f"screenshots/case4_failure_{int(time.time())}.png")
            print("[SCREENSHOT] Hata ekran görüntüsü kaydedildi")
        except:
            pass
        raise

    finally:
        print("\n[INFO] Browser kapatılıyor...")
        driver.quit()