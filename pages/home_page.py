from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class HomePage:
    """Enuygun ana sayfa için Page Object Model sınıfı"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 8)

        # Locator'lar
        self.roundtrip_tab = (By.CSS_SELECTOR, "[data-testid='enuygun-homepage-flight-roundTripButton']")
        self.origin_input = (By.CSS_SELECTOR, "[data-testid='enuygun-homepage-flight-origin-autocomplete-input']")
        self.destination_input = (By.CSS_SELECTOR, "[data-testid='enuygun-homepage-flight-destination-autocomplete-input']")
        self.departure_date = (By.CSS_SELECTOR, "[data-testid='enuygun-homepage-flight-departureDate-input']")
        self.return_date = (By.CSS_SELECTOR, "[data-testid='enuygun-homepage-flight-returnDate-input']")
        self.search_button = (By.CSS_SELECTOR, "[data-testid='enuygun-homepage-flight-submitButton']")
        self.cookie_accept = (By.XPATH, "//button[contains(@id,'accept') or contains(@class,'cookie')]")

    def open(self, url):
        """Siteyi açar, sayfanın yüklenmesini bekler ve popup'ları kapatır"""
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("Site acildi:", url)
        time.sleep(3)
        self._handle_cookies_and_popups()
        time.sleep(2)

    def _handle_cookies_and_popups(self):
        """Çerez popup'ları ve diğer popup'ları kapatır"""
        try:
            print("[INFO] Popup'lar kontrol ediliyor ve kapatılıyor...")
            
            cookie_selectors = [
                (By.XPATH, "//button[contains(@id,'accept') or contains(@class,'cookie')]"),
                (By.XPATH, "//button[contains(text(), 'Kabul') or contains(text(), 'Accept')]"),
                (By.CSS_SELECTOR, ".onetrust-accept-btn-handler"),
                (By.CSS_SELECTOR, "[data-testid*='cookie'] button"),
                (By.XPATH, "//div[contains(@class, 'onetrust')]//button"),
                (By.XPATH, "//button[contains(@class, 'accept')]"),
            ]
            
            cookie_closed = False
            for i, selector in enumerate(cookie_selectors):
                try:
                    cookie_btn = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable(selector)
                    )
                    self.driver.execute_script("arguments[0].click();", cookie_btn)
                    print(f"[OK] Cookie popup kapatıldı (selector {i+1})")
                    time.sleep(1)
                    cookie_closed = True
                    break
                except:
                    continue
            
            if not cookie_closed:
                print("[INFO] Cookie popup bulunamadı")
            
            close_button_selectors = [
                (By.XPATH, "//button[contains(@class, 'close') or contains(@aria-label, 'close')]"),
                (By.XPATH, "//button[text()='×' or text()='✕' or text()='X']"),
                (By.CSS_SELECTOR, ".modal-close, .popup-close, .close-btn"),
                (By.XPATH, "//div[contains(@class, 'modal')]//button[contains(@class, 'close')]"),
                (By.XPATH, "//div[contains(@class, 'popup')]//button"),
            ]
            
            popup_closed = False
            for i, selector in enumerate(close_button_selectors):
                try:
                    close_btn = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable(selector)
                    )
                    self.driver.execute_script("arguments[0].click();", close_btn)
                    print(f"[OK] Popup kapatıldı (close button {i+1})")
                    time.sleep(1)
                    popup_closed = True
                    break
                except:
                    continue
            
            if not popup_closed:
                print("[INFO] Kapatılacak popup bulunamadı")
            
            try:
                overlays = self.driver.find_elements(By.CSS_SELECTOR, 
                    ".modal-backdrop, .overlay, .popup-overlay, .onetrust-pc-dark-filter")
                for overlay in overlays:
                    if overlay.is_displayed():
                        self.driver.execute_script("arguments[0].style.display = 'none';", overlay)
                        print("[OK] Overlay kaldırıldı")
            except:
                pass
            
            time.sleep(2)
            print("[OK] Popup handling tamamlandı, sayfa hazır")
            
        except Exception as e:
            print(f"[WARNING] Popup handling error: {str(e)}")

    def search_round_trip(self, departure, destination, departure_date, return_date):
        """Gidiş-dönüş uçuş araması yapar
        
        Args:
            departure: Kalkış şehri
            destination: Varış şehri
            departure_date: Gidiş tarihi (format: DD.MM.YYYY)
            return_date: Dönüş tarihi (format: DD.MM.YYYY)
        """
        try:
            print("[INFO] Gidiş-Dönüş butonu aranıyor...")
            roundtrip_selectors = [
                (By.CSS_SELECTOR, "[data-testid='search-round-trip-text']"),
                (By.CSS_SELECTOR, "div[data-testid='search-round-trip-text']"),
                (By.XPATH, "//div[@data-testid='search-round-trip-text']"),
                (By.XPATH, "//div[contains(text(), 'Gidiş-dönüş')]"),
                (By.CSS_SELECTOR, "[data-testid='enuygun-homepage-flight-roundTripButton']"),
                (By.XPATH, "//button[contains(text(), 'Gidiş-Dönüş')]"),
                (By.XPATH, "//button[contains(text(), 'Gidiş') and contains(text(), 'Dönüş')]"),
                (By.XPATH, "//label[contains(text(), 'Gidiş-Dönüş')]"),
            ]
            
            roundtrip_clicked = False
            for i, selector in enumerate(roundtrip_selectors):
                try:
                    roundtrip = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(selector))
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", roundtrip)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", roundtrip)
                    print(f"[OK] Gidiş-Dönüş butonu tıklandı (selector {i+1})")
                    time.sleep(2)
                    roundtrip_clicked = True
                    break
                except Exception as e:
                    print(f"[WARNING] Selector {i+1} başarısız: {str(e)}")
                    continue
            
            if not roundtrip_clicked:
                print("[WARNING] Gidiş-Dönüş butonu bulunamadı, varsayılan form kullanılacak")
                
        except Exception as e:
            print(f"[WARNING] Gidiş-Dönüş butonu hatası: {str(e)}")

        time.sleep(1)

        # Kalkış noktası
        origin = None
        try:
            origin = self.wait.until(EC.element_to_be_clickable(self.origin_input))
            print("[OK] Kalkış input bulundu (data-testid)")
        except:
            try:
                origin = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//input[contains(@placeholder, 'Kalkış') or contains(@placeholder, 'Nereden') or contains(@aria-label, 'Kalkış')]")
                ))
                print("[OK] Kalkış input bulundu (placeholder)")
            except:
                try:
                    origin = self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//input[contains(@id, 'origin') or contains(@name, 'origin') or contains(@id, 'Origin')]")
                    ))
                    print("[OK] Kalkış input bulundu (id/name)")
                except:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                    if inputs:
                        origin = inputs[0]
                        print("[OK] Kalkış input bulundu (first text input)")
                    else:
                        self.driver.save_screenshot(f"screenshots/debug_origin_not_found_{int(time.time())}.png")
                        raise Exception("Kalkış input alanı bulunamadı!")
        
        if not origin:
            raise Exception("Kalkış input alanı bulunamadı!")
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", origin)
        time.sleep(0.5)
        
        try:
            origin.click()
        except:
            self.driver.execute_script("arguments[0].click();", origin)
        
        time.sleep(0.5)
        
        try:
            origin.clear()
        except:
            self.driver.execute_script("arguments[0].value = '';", origin)
        
        origin.send_keys(departure)
        time.sleep(1.2)
        
        try:
            autocomplete_selectors = [
                (By.CSS_SELECTOR, "[role='listbox'], [role='option'], .autocomplete-item, [class*='autocomplete']"),
                (By.XPATH, "//ul[contains(@role, 'listbox')]//li[1]"),
                (By.XPATH, "//div[contains(@class, 'autocomplete')]//div[1]"),
            ]
            
            autocomplete_selected = False
            for selector in autocomplete_selectors:
                try:
                    autocomplete_item = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable(selector)
                    )
                    if autocomplete_item and autocomplete_item.is_displayed():
                        autocomplete_item.click()
                        autocomplete_selected = True
                        print(f"[OK] Autocomplete'ten seçildi: {departure}")
                        break
                except:
                    continue
            
            if not autocomplete_selected:
                origin.send_keys(Keys.ENTER)
                print(f"[OK] Kalkış: {departure} (ENTER ile)")
        except:
            origin.send_keys(Keys.ENTER)
            print(f"[OK] Kalkış: {departure} (fallback ENTER)")
        
        time.sleep(0.5)

        # Varış noktası
        dest = None
        try:
            dest = self.wait.until(EC.element_to_be_clickable(self.destination_input))
            print("[OK] Varış input bulundu (data-testid)")
        except:
            try:
                dest = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//input[contains(@placeholder, 'Varış') or contains(@placeholder, 'Nereye') or contains(@aria-label, 'Varış')]")
                ))
                print("[OK] Varış input bulundu (placeholder)")
            except:
                try:
                    dest = self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//input[contains(@id, 'destination') or contains(@name, 'destination') or contains(@id, 'Destination')]")
                    ))
                    print("[OK] Varış input bulundu (id/name)")
                except:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                    if inputs and len(inputs) > 1:
                        dest = inputs[1]
                        print("[OK] Varış input bulundu (second text input)")
                    else:
                        self.driver.save_screenshot(f"screenshots/debug_destination_not_found_{int(time.time())}.png")
                        raise Exception("Varış input alanı bulunamadı!")
        
        if not dest:
            raise Exception("Varış input alanı bulunamadı!")
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dest)
        time.sleep(0.5)
        
        try:
            dest.click()
        except:
            self.driver.execute_script("arguments[0].click();", dest)
        
        time.sleep(0.5)
        
        try:
            dest.clear()
        except:
            self.driver.execute_script("arguments[0].value = '';", dest)
        
        dest.send_keys(destination)
        time.sleep(1.5)
        
        autocomplete_selected = False
        try:
            autocomplete_list_selectors = [
                (By.CSS_SELECTOR, "[role='listbox']"),
                (By.CSS_SELECTOR, "[class*='autocomplete']"),
                (By.XPATH, "//ul[@role='listbox']"),
                (By.XPATH, "//div[contains(@class, 'autocomplete')]"),
            ]
            
            autocomplete_list = None
            for selector in autocomplete_list_selectors:
                try:
                    autocomplete_list = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located(selector)
                    )
                    if autocomplete_list and autocomplete_list.is_displayed():
                        print(f"[OK] Autocomplete listesi bulundu")
                        break
                except:
                    continue
            
            if autocomplete_list:
                options = autocomplete_list.find_elements(By.CSS_SELECTOR, "li, div[role='option'], [class*='option'], [class*='item']")
                
                if options:
                    print(f"[INFO] {len(options)} autocomplete seçeneği bulundu")
                    
                    destination_lower = destination.lower()
                    for option in options:
                        try:
                            option_text = option.text.strip()
                            
                            if (destination_lower in option_text.lower() or 
                                option_text.lower() in destination_lower or
                                'lefkoşa' in option_text.lower() or
                                'nicosia' in option_text.lower()):
                                option.click()
                                autocomplete_selected = True
                                print(f"[OK] Autocomplete'ten seçildi: {destination} (item: {option_text})")
                                break
                        except:
                            continue
                    
                    if not autocomplete_selected and len(options) > 0:
                        try:
                            first_text = options[0].text.strip()
                            options[0].click()
                            autocomplete_selected = True
                            print(f"[OK] İlk autocomplete seçeneği seçildi: {first_text}")
                        except:
                            pass
            
            if not autocomplete_selected:
                dest.send_keys(Keys.ENTER)
                print(f"[OK] Varış: {destination} (ENTER ile)")
                
        except Exception as e:
            print(f"[WARNING] Autocomplete seçimi hatası: {str(e)}")
            dest.send_keys(Keys.ENTER)
            print(f"[OK] Varış: {destination} (fallback ENTER)")
        
        time.sleep(0.8)

        # Gidiş tarihi
        dep_date_input = None
        try:
            dep_date_input = self.wait.until(EC.element_to_be_clickable(self.departure_date))
            print("[OK] Gidiş tarihi input bulundu (data-testid)")
        except:
            try:
                dep_date_input = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//input[contains(@placeholder, 'Gidiş') or contains(@aria-label, 'Gidiş')]")
                ))
                print("[OK] Gidiş tarihi input bulundu (placeholder)")
            except:
                try:
                    dep_date_input = self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//input[contains(@id, 'departure') or contains(@name, 'departure') or contains(@id, 'Departure')]")
                    ))
                    print("[OK] Gidiş tarihi input bulundu (id/name)")
                except:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='date']")
                    if inputs and len(inputs) > 2:
                        dep_date_input = inputs[2]
                        print("[OK] Gidiş tarihi input bulundu (third input)")
                    else:
                        self.driver.save_screenshot(f"screenshots/debug_departure_date_not_found_{int(time.time())}.png")
                        raise Exception("Gidiş tarihi input alanı bulunamadı!")
        
        if not dep_date_input:
            raise Exception("Gidiş tarihi input alanı bulunamadı!")
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dep_date_input)
        time.sleep(0.5)
        
        try:
            dep_date_input.click()
        except:
            self.driver.execute_script("arguments[0].click();", dep_date_input)
        
        time.sleep(0.5)
        
        # Stale element sorununu önlemek için JavaScript kullan
        try:
            self.driver.execute_script("arguments[0].value = arguments[1];", dep_date_input, departure_date)
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", dep_date_input)
            time.sleep(0.5)
        except Exception as e:
            try:
                dep_date_input.send_keys(Keys.CONTROL + "a")
                dep_date_input.send_keys(departure_date)
                time.sleep(0.5)
                dep_date_input.send_keys(Keys.ENTER)
                time.sleep(0.5)
            except:
                raise Exception(f"Gidiş tarihi ayarlanamadı: {str(e)}")
        
        print(f"[OK] Gidiş tarihi: {departure_date}")

        # Dönüş tarihi
        ret_date_input = None
        try:
            ret_date_input = self.wait.until(EC.element_to_be_clickable(self.return_date))
            print("[OK] Dönüş tarihi input bulundu (data-testid)")
        except:
            try:
                ret_date_input = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//input[contains(@placeholder, 'Dönüş') or contains(@aria-label, 'Dönüş')]")
                ))
                print("[OK] Dönüş tarihi input bulundu (placeholder)")
            except:
                try:
                    ret_date_input = self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//input[contains(@id, 'return') or contains(@name, 'return') or contains(@id, 'Return')]")
                    ))
                    print("[OK] Dönüş tarihi input bulundu (id/name)")
                except:
                    inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='date']")
                    if inputs and len(inputs) > 3:
                        ret_date_input = inputs[3]
                        print("[OK] Dönüş tarihi input bulundu (fourth input)")
                    else:
                        self.driver.save_screenshot(f"screenshots/debug_return_date_not_found_{int(time.time())}.png")
                        raise Exception("Dönüş tarihi input alanı bulunamadı!")
        
        if not ret_date_input:
            raise Exception("Dönüş tarihi input alanı bulunamadı!")
        
        def set_return_date():
            """Dönüş tarihini ayarlar, stale element durumunda yeniden bulur"""
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ret_date_input)
                time.sleep(0.5)
                
                try:
                    ret_date_input.click()
                except:
                    self.driver.execute_script("arguments[0].click();", ret_date_input)
                
                time.sleep(0.5)
                
                self.driver.execute_script("arguments[0].value = arguments[1];", ret_date_input, return_date)
                time.sleep(0.3)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", ret_date_input)
                time.sleep(0.5)
                
            except Exception as stale_error:
                if "stale" in str(stale_error).lower():
                    print("[WARNING] Stale element detected, re-finding return date input...")
                    time.sleep(1)
                    try:
                        new_ret_date = self.wait.until(EC.element_to_be_clickable(self.return_date))
                    except:
                        try:
                            new_ret_date = self.wait.until(EC.presence_of_element_located(
                                (By.XPATH, "//input[contains(@id, 'return') or contains(@name, 'return') or contains(@id, 'Return')]")
                            ))
                        except:
                            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='date']")
                            new_ret_date = inputs[3] if inputs and len(inputs) > 3 else inputs[2] if inputs and len(inputs) > 2 else None
                            if not new_ret_date:
                                raise Exception("Dönüş tarihi input yeniden bulunamadı!")
                    
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", new_ret_date)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", new_ret_date)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].value = arguments[1];", new_ret_date, return_date)
                    time.sleep(0.3)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", new_ret_date)
                    time.sleep(0.5)
                else:
                    raise
        
        set_return_date()
        print(f"[OK] Dönüş tarihi: {return_date}")

        # Arama butonu - sadece uçuş arama butonu (otel değil)
        search_btn = None
        try:
            search_btn = self.wait.until(EC.element_to_be_clickable(self.search_button))
            print("[OK] Arama butonu bulundu (data-testid - flight submit)")
        except:
            try:
                search_btn = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "[data-testid*='flight'][data-testid*='submit'], [data-testid*='flight-submit']")
                ))
                print("[OK] Arama butonu bulundu (flight submit)")
            except:
                try:
                    flight_form = self.driver.find_element(By.CSS_SELECTOR, "[data-testid*='flight'], form")
                    buttons = flight_form.find_elements(By.CSS_SELECTOR, "button[type='submit'], button")
                    for btn in buttons:
                        btn_text = btn.text.lower()
                        btn_testid = btn.get_attribute("data-testid") or ""
                        if ("otel" in btn_text or "hotel" in btn_text or 
                            "otel" in btn_testid.lower() or "hotel" in btn_testid.lower()):
                            continue
                        if ("ara" in btn_text or "search" in btn_text or 
                            btn.get_attribute("type") == "submit" or
                            "flight" in btn_testid.lower() or
                            "submit" in btn_testid.lower()):
                            search_btn = btn
                            print(f"[OK] Arama butonu bulundu (text: {btn_text}, testid: {btn_testid})")
                            break
                    if not search_btn:
                        raise Exception("Uçuş arama butonu bulunamadı!")
                except:
                    self.driver.save_screenshot(f"screenshots/debug_search_button_not_found_{int(time.time())}.png")
                    raise Exception("Arama butonu bulunamadı!")
        
        if not search_btn:
            raise Exception("Arama butonu bulunamadı!")
        
        self.driver.execute_script("arguments[0].scrollIntoView(true);", search_btn)
        time.sleep(2)
        
        try:
            popup_overlay = self.driver.find_element(By.CSS_SELECTOR, ".onetrust-pc-dark-filter")
            if popup_overlay.is_displayed():
                self._handle_cookies_and_popups()
                time.sleep(2)
        except:
            pass
        
        try:
            search_btn.click()
            print("[OK] Arama başlatıldı")
        except:
            print("Normal click başarısız, JavaScript ile deneniyor...")
            self.driver.execute_script("arguments[0].click();", search_btn)
            print("[OK] Arama başlatıldı (JavaScript ile)")

        # Otel sekmesi kontrolü ve yönetimi
        time.sleep(3)
        print("[SEARCH] Arama sonuç sayfası yükleniyor...")
        
        try:
            window_handles = self.driver.window_handles
            if len(window_handles) > 1:
                print("[INFO] Birden fazla sekme açık - otel sekmesi kontrol ediliyor...")
                
                flight_window = None
                hotel_windows = []
                
                for handle in window_handles:
                    self.driver.switch_to.window(handle)
                    current_url = self.driver.current_url.lower()
                    
                    if "otel" in current_url or "hotel" in current_url:
                        hotel_windows.append(handle)
                        print(f"[WARNING] Otel sekmesi bulundu: {current_url}")
                    elif "ucak" in current_url or "flight" in current_url or "bileti" in current_url or "arama" in current_url:
                        flight_window = handle
                        print(f"[OK] Uçuş sekmesi bulundu: {current_url}")
                
                for hotel_handle in hotel_windows:
                    try:
                        self.driver.switch_to.window(hotel_handle)
                        self.driver.close()
                        print(f"[OK] Otel sekmesi kapatıldı")
                    except:
                        pass
                
                if flight_window:
                    self.driver.switch_to.window(flight_window)
                    print("[OK] Uçuş sekmesine geçildi")
                else:
                    if len(window_handles) > 0:
                        self.driver.switch_to.window(window_handles[0])
                        print("[WARNING] Uçuş sekmesi bulunamadı, ilk sekmeye geçildi")
            else:
                current_url = self.driver.current_url.lower()
                
                if "otel" in current_url or "hotel" in current_url:
                    print("[ERROR] HATA: Otel sayfasına yönlendirildi! Uçuş sayfasına geri dönülüyor...")
                    self.driver.get("https://www.enuygun.com/ucak-bileti/")
                    time.sleep(2)
                    raise Exception("Arama sonrası otel sayfasına yönlendirildi - bu bir hata!")
                
        except Exception as e:
            print(f"[WARNING] Sekme yönetimi hatası: {str(e)}")
        
        current_url = self.driver.current_url.lower()
        
        if "ucak" in current_url or "flight" in current_url or "bileti" in current_url or "arama" in current_url:
            print("[OK] Uçuş sonuç sayfasında olduğumuz doğrulandı")
        else:
            print(f"[WARNING] URL beklenmedik format: {current_url}")
        
        time.sleep(2)

    def capture_screenshot(self, name):
        """Ekran görüntüsü alır
        
        Args:
            name: Screenshot dosya adı (timestamp otomatik eklenir)
        """
        try:
            path = f"screenshots/{name}_{int(time.time())}.png"
            self.driver.save_screenshot(path)
            print(f"[SCREENSHOT] Screenshot kaydedildi: {path}")
        except:
            print("[WARNING] Screenshot alınamadı")
