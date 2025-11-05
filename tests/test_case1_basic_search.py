import datetime
import time
from utils.browser_factory import create_driver, load_config
from pages.home_page import HomePage
from pages.results_page import ResultsPage


def test_basic_flight_search():
    """Case 1: Basic Flight Search and Time Filter"""

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
        print("CASE 1: Basic Flight Search & Time Filter")
        print("======================================")
        print(f"Kalkis: {dep_city} -> Varis: {dest_city}")
        print(f"Gidis: {dep_date}, Donus: {ret_date}")
        print("======================================")

        home.open(url)
        home.search_round_trip(dep_city, dest_city, dep_date, ret_date)
        results.wait_for_results()

        print("[INFO] Gidiş kalkış saati 10:00-18:00 aralığına ayarlanıyor...")
        try:
            results.apply_time_filter_with_sliders(departure_start=10, departure_end=18)
        except:
            print("[WARNING] Slider tabanlı filtre başarısız, eski yönteme geçiliyor")
            results.apply_time_filter()

        results.is_flight_list_displayed()
        results.verify_departure_times(10, 18)

        print("CASE 1 basariyla tamamlandi!")

    except Exception as e:
        print(f"Test sirasinda hata olustu: {str(e)}")
        raise

    finally:
        time.sleep(1)  
        driver.quit()
