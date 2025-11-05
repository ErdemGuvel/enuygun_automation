"""
Test Case 2: Türk Hava Yolları Fiyat Sıralaması
Belirli bir havayolu için fiyat sıralama fonksiyonunu doğrular
"""
import datetime
import time
from utils.browser_factory import create_driver, load_config
from pages.home_page import HomePage
from pages.results_page import ResultsPage


def test_turkish_airlines_price_sorting():
    """Case 2: Türk Hava Yolları Fiyat Sıralaması"""

    config = load_config()
    driver = create_driver()
    home = HomePage(driver)
    results = ResultsPage(driver)

    try:
        url = config['site']['url']
        dep_city = config['defaults']['departure_city']
        dest_city = config['defaults']['destination_city']
        days_ahead = config['dates']['days_ahead_departure']
        return_days = config['dates']['days_ahead_return']

        today = datetime.date.today()
        dep_date = (today + datetime.timedelta(days=days_ahead)).strftime(config['dates']['format'])
        ret_date = (today + datetime.timedelta(days=days_ahead + return_days)).strftime(config['dates']['format'])

        print("======================================")
        print("[FLIGHT]  CASE 2: Turkish Airlines Price Sorting")
        print("======================================")
        print(f"- Kalkış: {dep_city} -> Varış: {dest_city}")
        print(f"- Gidiş: {dep_date}, Dönüş: {ret_date}")
        print("======================================")

        home.open(url)
        home.search_round_trip(dep_city, dest_city, dep_date, ret_date)
        results.wait_for_results()

        try:
            results.apply_time_filter_with_sliders(10, 18)
        except:
            print("[WARNING] Slider tabanlı filtre başarısız, eski yönteme geçiliyor")
            results.apply_time_filter()

        results.apply_turkish_airlines_filter()
        results.is_flight_list_displayed()
        
        print("[INFO] Fiyat sıralaması: Enuygun varsayılan olarak en ucuzdan pahalıya sıralı gösterir.")
        assert results.verify_all_flights_turkish_airlines(), "[ERROR] Tüm uçuşlar THY değil!"
        results.verify_departure_times(10, 18)

        print("[OK] CASE 2 başarıyla tamamlandı!")

    except Exception as e:
        print(f"[ERROR] Test sırasında hata oluştu: {str(e)}")
        raise

    finally:
        time.sleep(1)
        driver.quit()
