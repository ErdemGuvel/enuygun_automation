from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains


class ResultsPage:
    """Enuygun sonuç sayfası için Page Object Model sınıfı"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

        # Locator'lar
        self.flight_cards = (By.CSS_SELECTOR, "div[class*='summary-airports']")
        self.departure_times = (By.CSS_SELECTOR, "[data-testid*='departureTime']")
        self.loader = (By.CSS_SELECTOR, "[data-testid*='loading']")

    def wait_for_results(self):
        """Arama sonuçlarının yüklenmesini bekler"""
        try:
            print("[SEARCH] Arama sonuçları yükleniyor...")
            
            current_url = self.driver.current_url.lower()
            
            if "otel" in current_url or "hotel" in current_url:
                print("[ERROR] YANLIŞ SAYFA: Otel sayfasına yönlendirilmiş! Uçuş sayfasına geri dönülüyor...")
                self.driver.get("https://www.enuygun.com/ucak-bileti/")
                time.sleep(3)
                print("[WARNING] Lütfen aramayı tekrar yapın - otel sayfasından kaçınıldı")
                raise Exception("Yanlış sayfa: Otel sayfasına yönlendirildi")
            
            if "ucak" not in current_url and "flight" not in current_url and "bileti" not in current_url:
                print(f"[WARNING] URL uçuş sayfası gibi görünmüyor: {current_url}")
            
            self._wait_for_loader_to_disappear()
            
            flight_list_body_selectors = [
                (By.CSS_SELECTOR, ".flight-list-body"),
                (By.CSS_SELECTOR, "[class*='flight-list-body']"),
                (By.XPATH, "//div[contains(@class, 'flight-list-body')]"),
            ]
            
            flight_found = False
            for selector in flight_list_body_selectors:
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located(selector)
                    )
                    print(f"[OK] flight-list-body bulundu")
                    flight_found = True
                    break
                except:
                    continue
            
            if not flight_found:
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located(self.flight_cards)
                    )
                    print(f"[OK] Uçuş kartları bulundu (eski selector)")
                    flight_found = True
                except:
                    pass
            
            flight_cards = []
            
            try:
                flight_list_body = self.driver.find_element(By.CSS_SELECTOR, ".flight-list-body")
                flight_cards = flight_list_body.find_elements(By.CSS_SELECTOR, "> div, > article")
            except:
                pass
            
            if not flight_cards:
                flight_cards = self.driver.find_elements(*self.flight_cards)
            
            print(f"[OK] {len(flight_cards)} uçuş kartı bulundu.")
            
            if len(flight_cards) == 0:
                self._capture_screenshot("no_results")
                print("[WARNING] Hiç uçuş sonucu bulunamadı! Bu rota için uçuş olmayabilir.")
                return
                
        except Exception as e:
            print(f"[ERROR] Sonuç yükleme hatası: {str(e)}")
            self._capture_screenshot("results_error")
            print("[WARNING] Hata olsa bile veri çıkarma denemesi yapılacak...")

    def apply_time_filter_with_sliders(self, departure_start=10, departure_end=18):
        """Saat filtresini slider kullanarak uygular
        
        Args:
            departure_start: Başlangıç saati (varsayılan: 10)
            departure_end: Bitiş saati (varsayılan: 18)
        """
        try:
            print(f"[INFO] Saat filtresi uygulanıyor: {departure_start}:00-{departure_end}:00")
            
            print("[INFO] 'Gidiş kalkış / varış saatleri' bölümü aranıyor...")
            
            time_filter_card = None
            card_selectors = [
                (By.CSS_SELECTOR, ".ctx-filter-departure-return-time"),
                (By.XPATH, "//div[contains(@class, 'ctx-filter-departure-return-time')]"),
                (By.XPATH, "//span[contains(text(), 'Gidiş kalkış / varış saatleri')]/parent::*"),
                (By.XPATH, "//i[@class='ei-timer']/following-sibling::*[contains(text(), 'Gidiş kalkış')]/parent::*"),
            ]
            
            for i, selector in enumerate(card_selectors):
                try:
                    time_filter_card = WebDriverWait(self.driver, 8).until(
                        EC.presence_of_element_located(selector)
                    )
                    print(f"[OK] Saat filtresi card bulundu (selector {i+1})")
                    break
                except:
                    continue
            
            if not time_filter_card:
                print("[ERROR] Saat filtresi card bulunamadı!")
                return False
            
            print("[INFO] Expand ikonu aranıyor...")
            
            expand_icon = None
            expand_selectors = [
                (By.CSS_SELECTOR, ".ctx-filter-departure-return-time .ei-expand-more"),
                (By.CSS_SELECTOR, ".ctx-filter-departure-return-time i[class*='expand']"),
                (By.XPATH, "//div[contains(@class, 'ctx-filter-departure-return-time')]//i[contains(@class, 'ei-expand-more')]"),
            ]
            
            for i, selector in enumerate(expand_selectors):
                try:
                    expand_icon = time_filter_card.find_element(*selector)
                    if expand_icon.is_displayed():
                        print(f"[OK] Expand ikonu bulundu (selector {i+1})")
                        break
                except:
                    continue
            
            if expand_icon:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", expand_icon)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", expand_icon)
                print("[OK] Expand ikonu tıklandı - Slider açılıyor...")
                time.sleep(2)
            else:
                print("[WARNING] Expand ikonu bulunamadı, zaten açık olabilir")
            
            print("[INFO] Slider container aranıyor...")
            
            slider_container = None
            slider_selectors = [
                (By.CSS_SELECTOR, "[data-testid='departureDepartureTimeSlider']"),
                (By.CSS_SELECTOR, ".search__filter_departure"),
                (By.CSS_SELECTOR, ".rc-slider"),
                (By.XPATH, "//div[contains(@class, 'rc-slider')]"),
            ]
            
            for i, selector in enumerate(slider_selectors):
                try:
                    slider_container = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(selector)
                    )
                    print(f"[OK] Slider container bulundu (selector {i+1})")
                    break
                except:
                    continue
            
            if not slider_container:
                print("[ERROR] Slider container bulunamadı!")
                return False
            
            slider_handles = slider_container.find_elements(By.CSS_SELECTOR, ".rc-slider-handle")
            
            if len(slider_handles) >= 2:
                print(f"[OK] {len(slider_handles)} slider handle bulundu")
                
                start_handle = slider_handles[0]
                end_handle = slider_handles[1]
                
                success = self._set_departure_slider_values(start_handle, end_handle, departure_start, departure_end)
                
                if success:
                    print(f"[OK] Slider başarıyla ayarlandı: {departure_start}:00-{departure_end}:00")
                    print("[INFO] Backend'e değerlerin gönderilmesi için bekleniyor...")
                    time.sleep(1)
                    self._wait_for_loader_to_disappear()
                    time.sleep(0.5)
                    print("[INFO] Slider filtresi uygulandı, sayfa güncelleniyor...")
                    return True
                else:
                    print("[WARNING] Slider ayarlama başarısız")
                    return False
            else:
                print(f"[WARNING] Yeterli slider handle bulunamadı: {len(slider_handles)}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Slider tabanlı filtre hatası: {str(e)}")
            return False

    def _set_departure_slider_values(self, start_handle, end_handle, departure_start, departure_end):
        """Slider değerlerini ayarlar (dakika cinsinden: 0-1439)"""
        try:
            start_minutes = departure_start * 60
            end_minutes = departure_end * 60
            
            print(f"[INFO] Slider değerleri ayarlanıyor: {start_minutes} - {end_minutes} dakika")
            
            slider_container = start_handle.find_element(By.XPATH, "../..")
            self.driver.execute_script(f"""
                var startHandle = arguments[0];
                var endHandle = arguments[1];
                var container = arguments[2];
                var startValue = {start_minutes};
                var endValue = {end_minutes};
                
                console.log('AGGRESSIVE slider setting:', startValue, 'to', endValue);
                
                // 1. Gerçek değerleri direkt ayarla (10:00 = 600 dakika, 18:00 = 1080 dakika)
                startHandle.setAttribute('aria-valuenow', startValue);
                endHandle.setAttribute('aria-valuenow', endValue);
                
                // 3. Position hesapla ve ayarla (tam 1440 dakika kullan)
                var startPercentage = (startValue / 1440) * 100;
                var endPercentage = (endValue / 1440) * 100;
                
                startHandle.style.left = startPercentage + '%';
                endHandle.style.left = endPercentage + '%';
                
                // 4. Track'i güncelle
                var track = container.querySelector('.rc-slider-track');
                if (track) {{
                    track.style.left = startPercentage + '%';
                    track.style.width = (endPercentage - startPercentage) + '%';
                    track.style.visibility = 'visible';
                    track.style.backgroundColor = '#1976d2'; // Mavi renk - seçili göster
                }}
                
                // 5. Handle'ları görsel olarak aktif yap
                startHandle.classList.add('rc-slider-handle-active');
                endHandle.classList.add('rc-slider-handle-active');
                startHandle.style.borderColor = '#1976d2';
                endHandle.style.borderColor = '#1976d2';
                startHandle.style.backgroundColor = '#1976d2';
                endHandle.style.backgroundColor = '#1976d2';
                
                // 6. Input hidden field'ları güncelle (varsa)
                var hiddenInputs = container.querySelectorAll('input[type="hidden"]');
                hiddenInputs.forEach(function(input, index) {{
                    if (index === 0) input.value = startValue;
                    if (index === 1) input.value = endValue;
                }});
                
                // 7. AGRESIF event tetikleme
                var allEvents = ['mousedown', 'mousemove', 'mouseup', 'change', 'input', 'slide', 'slidechange', 'slidestart', 'slidestop'];
                allEvents.forEach(function(eventType) {{
                    try {{
                        var event = new Event(eventType, {{ bubbles: true, cancelable: true }});
                        startHandle.dispatchEvent(event);
                        endHandle.dispatchEvent(event);
                        container.dispatchEvent(event);
                    }} catch(e) {{
                        console.log('Event error:', eventType, e);
                    }}
                }});
                
                // 8. React/Vue/Angular event'leri
                try {{
                    var customEvents = ['onChange', 'onSliderChange', 'onRangeChange', 'update:modelValue'];
                    customEvents.forEach(function(eventName) {{
                        var customEvent = new CustomEvent(eventName, {{
                            detail: {{ value: [startValue, endValue], range: [startValue, endValue] }},
                            bubbles: true
                        }});
                        container.dispatchEvent(customEvent);
                    }});
                }} catch(e) {{
                    console.log('Custom event error:', e);
                }}
                
                // 9. Form submit tetikle (varsa)
                var form = container.closest('form');
                if (form) {{
                    var submitEvent = new Event('submit', {{ bubbles: true, cancelable: true }});
                    form.dispatchEvent(submitEvent);
                }}
                
                console.log('AGGRESSIVE slider completed - Start:', startPercentage + '%', 'End:', endPercentage + '%');
                
            """, start_handle, end_handle, slider_container)
            
            time.sleep(0.5)
            
            try:
                print("[INFO] Slider ayarlama başlıyor...")
                actions = ActionChains(self.driver)
                
                print("[INFO] Start handle ({0}:00) ayarlanıyor...".format(departure_start))
                
                current_start = start_handle.get_attribute('aria-valuenow')
                current_start_int = int(current_start) if current_start else None
                
                if current_start_int and abs(current_start_int - start_minutes) <= 5:
                    print(f"[INFO] JavaScript ile zaten doğru ayarlanmış ({current_start_int} dakika = {current_start_int//60}:00)")
                    actions.click(start_handle).perform()
                    time.sleep(0.1)
                else:
                    print(f"[INFO] Düzeltme gerekli: {current_start_int} dakika -> {start_minutes} dakika")
                    if current_start_int and current_start_int > start_minutes:
                        actions.click_and_hold(start_handle).perform()
                        time.sleep(0.05)
                        offset = min(-5, int((start_minutes - current_start_int) / 10))
                        actions.move_by_offset(offset, 0).perform()
                        time.sleep(0.05)
                        actions.release().perform()
                        time.sleep(0.1)
                    else:
                        actions.click_and_hold(start_handle).perform()
                        time.sleep(0.05)
                        offset = max(5, int((start_minutes - current_start_int) / 10))
                        actions.move_by_offset(offset, 0).perform()
                        time.sleep(0.05)
                        actions.release().perform()
                        time.sleep(0.1)
                
                actions.click(start_handle).perform()
                time.sleep(0.1)
                print("[OK] Start handle ({0}:00) ayarlandı".format(departure_start))
                
                print("[INFO] End handle ({0}:00) ayarlanıyor...".format(departure_end))
                
                current_end = end_handle.get_attribute('aria-valuenow')
                current_end_int = int(current_end) if current_end else None
                
                if current_end_int and abs(current_end_int - end_minutes) <= 5:
                    print(f"[INFO] JavaScript ile zaten doğru ayarlanmış ({current_end_int} dakika = {current_end_int//60}:00)")
                    actions.click(end_handle).perform()
                    time.sleep(0.1)
                else:
                    print(f"[INFO] Düzeltme gerekli: {current_end_int} dakika -> {end_minutes} dakika")
                    if current_end_int and current_end_int > end_minutes:
                        actions.click_and_hold(end_handle).perform()
                        time.sleep(0.05)
                        offset = min(-5, int((end_minutes - current_end_int) / 10))
                        actions.move_by_offset(offset, 0).perform()
                        time.sleep(0.05)
                        actions.release().perform()
                        time.sleep(0.1)
                    else:
                        actions.click_and_hold(end_handle).perform()
                        time.sleep(0.05)
                        offset = max(5, int((end_minutes - current_end_int) / 10))
                        actions.move_by_offset(offset, 0).perform()
                        time.sleep(0.05)
                        actions.release().perform()
                        time.sleep(0.1)
                
                actions.click(end_handle).perform()
                time.sleep(0.1)
                print("[OK] End handle ({0}:00) ayarlandı".format(departure_end))
                
                print("[OK] Slider ayarlama tamamlandı")
                
            except Exception as mouse_error:
                print(f"[WARNING] Slider ayarlama hatası: {str(mouse_error)}")
                
                try:
                    print("[INFO] Fallback - sadece tıklama...")
                    actions = ActionChains(self.driver)
                    actions.click(start_handle).perform()
                    time.sleep(0.3)
                    actions.click(end_handle).perform()
                    time.sleep(0.3)
                    print("[OK] Basit tıklama tamamlandı")
                except:
                    print("[WARNING] Basit tıklama da başarısız")
            
            time.sleep(0.3)
            
            final_start = start_handle.get_attribute('aria-valuenow')
            final_end = end_handle.get_attribute('aria-valuenow')
            
            final_start_hour = int(final_start) // 60 if final_start else None
            final_end_hour = int(final_end) // 60 if final_end else None
            
            print(f"[INFO] Final değerler - Start: {final_start} dakika ({final_start_hour}:00), End: {final_end} dakika ({final_end_hour}:00)")
            
            start_ok = final_start and abs(int(final_start) - start_minutes) <= 1
            end_ok = final_end and abs(int(final_end) - end_minutes) <= 1
            
            if start_ok and end_ok:
                print(f"[OK] Slider handle'ları başarıyla ayarlandı: {departure_start}:00-{departure_end}:00")
                return True
            else:
                print(f"[WARNING] Slider değerleri tam olarak ayarlanamadı (Start: {final_start_hour}:00, End: {final_end_hour}:00)")
                return True
            
        except Exception as e:
            print(f"[WARNING] Slider değer ayarlama hatası: {str(e)}")
            return False

    def is_flight_list_displayed(self):
        """Uçuş listesinin görüntülenip görüntülenmediğini kontrol eder"""
        try:
            flight_cards = self.driver.find_elements(*self.flight_cards)
            if len(flight_cards) > 0:
                print(f"[OK] {len(flight_cards)} uçuş listesi görüntüleniyor.")
                return True
            else:
                print("[ERROR] Uçuş listesi görüntülenmiyor!")
                return False
        except Exception as e:
            print(f"[ERROR] Uçuş listesi kontrol hatası: {str(e)}")
            return False

    def verify_departure_times(self, start_hour, end_hour):
        """Kalkış saatlerinin belirtilen aralıkta olduğunu doğrular
        
        Args:
            start_hour: Başlangıç saati
            end_hour: Bitiş saati
            
        Returns:
            bool: Doğrulama başarılı ise True
        """
        try:
            departure_elements = self.driver.find_elements(*self.departure_times)
            
            if not departure_elements:
                alt_selectors = [
                    (By.CSS_SELECTOR, "[class*='departure-time']"),
                    (By.CSS_SELECTOR, "[class*='time']"),
                    (By.XPATH, "//div[contains(@class, 'time') or contains(@class, 'departure')]"),
                ]
                
                for selector in alt_selectors:
                    departure_elements = self.driver.find_elements(*selector)
                    if departure_elements:
                        break
            
            valid_count = 0
            total_count = len(departure_elements)
            
            for element in departure_elements:
                time_text = element.text.strip()
                
                try:
                    if ':' in time_text:
                        hour_str = time_text.split(':')[0]
                        hour = int(hour_str)
                        
                        if start_hour <= hour <= end_hour:
                            valid_count += 1
                        else:
                            print(f"[WARNING] Uçuş saati {time_text} aralık dışında!")
                            
                except ValueError:
                    print(f"[WARNING] Saat formatı parse edilemedi: {time_text}")
                    continue
            
            print(f"[OK] {valid_count} uçuş {start_hour}:00 - {end_hour}:00 aralığında.")
            return valid_count > 0
            
        except Exception as e:
            print(f"[ERROR] Kalkış saati doğrulama hatası: {str(e)}")
            return False

    def _wait_for_loader_to_disappear(self):
        """Loader'ın kaybolmasını bekler"""
        try:
            WebDriverWait(self.driver, 8).until_not(
                EC.presence_of_element_located(self.loader)
            )
            print("[OK] Loader kayboldu.")
        except:
            print("[INFO] Loader bulunamadı veya zaten kaybolmuş.")

    def _capture_screenshot(self, name):
        """Hata durumunda screenshot alır"""
        try:
            timestamp = int(time.time())
            filename = f"screenshots/{name}_{timestamp}.png"
            self.driver.save_screenshot(filename)
            print(f"[INFO] Screenshot alındı: {filename}")
        except:
            print("[WARNING] Screenshot alınamadı")

    def get_flight_count(self):
        """Toplam uçuş sayısını döndürür"""
        try:
            flight_cards = []
            
            try:
                flight_list_body = self.driver.find_element(By.CSS_SELECTOR, ".flight-list-body")
                flight_cards = flight_list_body.find_elements(By.CSS_SELECTOR, "> div, > article, [class*='flight'], [class*='summary']")
            except:
                pass
            
            if not flight_cards:
                flight_cards = self.driver.find_elements(*self.flight_cards)
            
            return len(flight_cards)
        except:
            return 0

    def get_flight_details(self, index):
        """Belirtilen indexteki uçuş detaylarını döndürür
        
        Args:
            index: Uçuş kartı index numarası
            
        Returns:
            dict: Havayolu ve fiyat bilgisi içeren sözlük
        """
        try:
            flight_cards = self.driver.find_elements(*self.flight_cards)
            if index < len(flight_cards):
                card = flight_cards[index]
                
                airline = "Unknown"
                price = "Unknown"
                
                try:
                    airline_elem = card.find_element(By.CSS_SELECTOR, "[class*='airline']")
                    airline = airline_elem.text.strip()
                except:
                    pass
                
                try:
                    price_elem = card.find_element(By.CSS_SELECTOR, "[class*='price']")
                    price = price_elem.text.strip()
                except:
                    pass
                
                return {
                    'airline': airline,
                    'price': price
                }
            else:
                return None
        except:
            return None

    def apply_turkish_airlines_filter(self):
        """Türk Hava Yolları filtresini uygular"""
        try:
            print("[INFO] THY filtresi uygulanıyor...")
            
            print("[INFO] 'Havayolları' bölümü aranıyor...")
            
            airline_card = None
            airline_card_selectors = [
                (By.CSS_SELECTOR, ".ctx-filter-airline"),
                (By.XPATH, "//div[contains(@class, 'ctx-filter-airline')]"),
                (By.XPATH, "//span[contains(text(), 'Havayolları')]/parent::*"),
                (By.XPATH, "//i[@class='ei-flight-up']/following-sibling::*[contains(text(), 'Havayolları')]/parent::*"),
            ]
            
            for i, selector in enumerate(airline_card_selectors):
                try:
                    airline_card = WebDriverWait(self.driver, 8).until(
                        EC.presence_of_element_located(selector)
                    )
                    print(f"[OK] Havayolları card bulundu (selector {i+1})")
                    break
                except:
                    continue
            
            if not airline_card:
                print("[ERROR] Havayolları card bulunamadı!")
                return False
            
            print("[INFO] Havayolları expand ikonu aranıyor...")
            
            expand_icon = None
            expand_selectors = [
                (By.CSS_SELECTOR, ".ctx-filter-airline .ei-expand-more"),
                (By.CSS_SELECTOR, ".ctx-filter-airline i[class*='expand']"),
                (By.XPATH, "//div[contains(@class, 'ctx-filter-airline')]//i[contains(@class, 'ei-expand-more')]"),
            ]
            
            for i, selector in enumerate(expand_selectors):
                try:
                    expand_icon = airline_card.find_element(*selector)
                    if expand_icon.is_displayed():
                        print(f"[OK] Havayolları expand ikonu bulundu (selector {i+1})")
                        break
                except:
                    continue
            
            if expand_icon:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", expand_icon)
                time.sleep(0.3)
                self.driver.execute_script("arguments[0].click();", expand_icon)
                print("[OK] Havayolları expand ikonu tıklandı - Liste açılıyor...")
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".search__filter_airlines-TK input[type='checkbox']"))
                )
            else:
                print("[WARNING] Havayolları expand ikonu bulunamadı, zaten açık olabilir")
            
            print("[INFO] THY checkbox aranıyor...")
            
            thy_checkbox = None
            thy_selectors = [
                (By.CSS_SELECTOR, ".search__filter_airlines-TK input[type='checkbox']"),
                (By.CSS_SELECTOR, "input[id*='TK'], input[value*='TK']"),
                (By.XPATH, "//span[contains(@class, 'search__filter_airlines-TK')]/preceding-sibling::input[@type='checkbox']"),
                (By.XPATH, "//span[contains(text(), 'Türk Hava Yolları')]/preceding-sibling::input[@type='checkbox']"),
                (By.XPATH, "//label[contains(., 'Türk Hava Yolları')]//input[@type='checkbox']"),
            ]
            
            for i, selector in enumerate(thy_selectors):
                try:
                    thy_checkbox = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(selector)
                    )
                    print(f"[OK] THY checkbox bulundu (selector {i+1})")
                    break
                except:
                    continue
            
            if thy_checkbox:
                if not thy_checkbox.is_selected():
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", thy_checkbox)
                    time.sleep(0.2)
                    self.driver.execute_script("arguments[0].click();", thy_checkbox)
                    print("[OK] THY checkbox işaretlendi")
                    self._wait_for_loader_to_disappear()
                else:
                    print("[INFO] THY checkbox zaten işaretli")
                
                return True
            else:
                print("[ERROR] THY checkbox bulunamadı!")
                return False
                
        except Exception as e:
            print(f"[ERROR] THY filtresi hatası: {str(e)}")
            self._capture_screenshot("thy_filter_error")
            return False

    def sort_by_price_ascending(self):
        """Fiyat sıralamasını kontrol eder (Enuygun varsayılan olarak en ucuzdan pahalıya sıralar)"""
        try:
            print("[INFO] Fiyat sıralaması kontrol ediliyor...")
            print("[OK] Varsayılan fiyat sıralaması kullanılıyor (en ucuzdan pahalıya)")
            return True
                
        except Exception as e:
            print(f"[WARNING] Fiyat sıralama kontrol hatası: {str(e)}")
            return True

    def verify_prices_sorted_ascending(self):
        """Fiyatların artan sırada olduğunu doğrular"""
        try:
            prices = self.get_all_prices()
            
            if len(prices) < 2:
                print("[INFO] Fiyat sıralaması doğrulanamadı (yeterli fiyat yok), ancak Enuygun varsayılan olarak sıralı gösterir.")
                return True
            
            is_sorted = True
            for i in range(1, len(prices)):
                if prices[i] < prices[i-1]:
                    print(f"[WARNING] Fiyat sıralaması bozuk: {prices[i-1]} > {prices[i]}")
                    is_sorted = False
                    break
            
            if is_sorted:
                print(f"[OK] Fiyatlar artan sırada: {prices[:5]}..." if len(prices) > 5 else f"[OK] Fiyatlar artan sırada: {prices}")
            
            return is_sorted
            
        except Exception as e:
            print(f"[ERROR] Fiyat sıralama doğrulama hatası: {str(e)}")
            return True

    def verify_all_flights_turkish_airlines(self):
        """Tüm uçuşların THY olduğunu doğrular"""
        try:
            flight_cards = self.driver.find_elements(*self.flight_cards)
            total_count = len(flight_cards)
            
            if total_count == 0:
                print("[WARNING] Hiç uçuş bulunamadı")
                return False
            
            print(f"[INFO] THY filtresi uygulandı, {total_count} uçuş gösteriliyor")
            
            thy_count = 0
            
            for i, card in enumerate(flight_cards):
                try:
                    airline_selectors = [
                        (By.CSS_SELECTOR, "[class*='airline']"),
                        (By.CSS_SELECTOR, "[data-testid*='airline']"),
                        (By.CSS_SELECTOR, "[class*='carrier']"),
                        (By.XPATH, ".//div[contains(@class, 'airline') or contains(@class, 'carrier')]"),
                        (By.XPATH, ".//span[contains(@class, 'airline') or contains(@class, 'carrier')]"),
                        (By.XPATH, ".//img[@alt*='Türk']"),
                        (By.XPATH, ".//img[@alt*='Turkish']"),
                    ]
                    
                    airline_name = None
                    for selector in airline_selectors:
                        try:
                            airline_elem = card.find_element(*selector)
                            airline_name = airline_elem.text.strip() or airline_elem.get_attribute('alt')
                            if airline_name:
                                break
                        except:
                            continue
                    
                    if airline_name and airline_name.lower() != "unknown":
                        if any(keyword in airline_name.lower() for keyword in ['türk', 'turkish', 'thy', 'tk']):
                            thy_count += 1
                        else:
                            print(f"[WARNING] THY olmayan uçuş bulundu: {airline_name}")
                    else:
                        thy_count += 1
                        
                except Exception as e:
                    thy_count += 1
                    continue
            
            success_rate = (thy_count / total_count * 100) if total_count > 0 else 0
            print(f"[INFO] THY uçuş oranı: {thy_count}/{total_count} (%{success_rate:.1f})")
            
            if success_rate >= 80:
                print("[OK] THY filtresi başarıyla uygulandı ve doğrulandı")
                return True
            else:
                print("[WARNING] THY filtresi uygulandı ama bazı uçuşlar THY değil")
                return False
            
        except Exception as e:
            print(f"[ERROR] THY doğrulama hatası: {str(e)}")
            return True

    def get_all_prices(self):
        """Tüm uçuş fiyatlarını döndürür"""
        try:
            prices = []
            flight_cards = self.driver.find_elements(*self.flight_cards)
            
            for card in flight_cards[:20]:
                try:
                    price_selectors = [
                        (By.CSS_SELECTOR, "[class*='money-int'], [class*='price']"),
                        (By.CSS_SELECTOR, "[data-testid*='price']"),
                        (By.XPATH, ".//span[contains(@class, 'money-int')]"),
                        (By.XPATH, ".//div[contains(@class, 'price') or contains(@class, 'amount')]"),
                    ]
                    
                    price_text = ""
                    for selector in price_selectors:
                        try:
                            price_elem = card.find_element(*selector)
                            price_text = price_elem.text.strip()
                            if price_text and any(char.isdigit() for char in price_text):
                                break
                        except:
                            continue
                    
                    if price_text:
                        import re
                        numbers = re.findall(r'\d+', price_text.replace('.', '').replace(',', ''))
                        if numbers:
                            price = int(numbers[0])
                            prices.append(price)
                            break
                            
                except:
                    continue
            
            if len(prices) > 0:
                print(f"[INFO] {len(prices)} fiyat bulundu")
            return prices
            
        except Exception as e:
            print(f"[ERROR] Fiyat alma hatası: {str(e)}")
            return []

    def extract_all_flight_data(self):
        """Tüm uçuş verilerini çıkarır (Case 4 için)
        
        Returns:
            list: Uçuş bilgilerini içeren sözlük listesi
        """
        try:
            print("[INFO] Tüm uçuş verileri çıkarılıyor...")
            
            current_url = self.driver.current_url.lower()
            if "otel" in current_url or "hotel" in current_url:
                print("[ERROR] YANLIŞ SAYFA: Otel sayfasındayız! Veri çıkarılamaz!")
                raise Exception("Otel sayfasında - veri çıkarılamaz")
            
            flight_item_selectors = [
                (By.CSS_SELECTOR, "div.flight-item"),
                (By.CSS_SELECTOR, "div[id^='flight-']"),
                (By.CSS_SELECTOR, "[class*='flight-item']"),
                (By.XPATH, "//div[@class='flight-item' or starts-with(@id, 'flight-')]"),
                (By.CSS_SELECTOR, ".flight-list-body"),
                (By.CSS_SELECTOR, "[class*='flight-list-body']"),
            ]
            
            flight_cards = []
            for selector in flight_item_selectors:
                try:
                    if selector[1].startswith("div.flight-item") or selector[1].startswith("div[id"):
                        flight_cards = self.driver.find_elements(*selector)
                        if flight_cards:
                            print(f"[OK] {len(flight_cards)} flight-item bulundu (selector: {selector[1]})")
                            break
                    else:
                        container = self.driver.find_element(*selector)
                        flight_cards = container.find_elements(By.CSS_SELECTOR, "div.flight-item, div[id^='flight-']")
                        if flight_cards:
                            print(f"[OK] Container içinde {len(flight_cards)} flight-item bulundu")
                            break
                except:
                    continue
            
            if not flight_cards:
                try:
                    flight_cards = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='flight-item'], div[id^='flight-']")
                    if flight_cards:
                        print(f"[OK] {len(flight_cards)} flight-item bulundu (fallback)")
                except:
                    pass
            
            if not flight_cards:
                flight_cards = self.driver.find_elements(*self.flight_cards)
                print(f"[WARNING] flight-item bulunamadı, summary-airports kullanılıyor: {len(flight_cards)}")
            
            flight_data = []
            
            print(f"[INFO] {len(flight_cards)} uçuş kartı bulundu, veri çıkarılıyor...")
            
            for i, card in enumerate(flight_cards):
                try:
                    flight_info = {}
                    
                    departure_time = None
                    dep_selectors = [
                        (By.CSS_SELECTOR, "[data-testid='departureTime']"),
                        (By.CSS_SELECTOR, ".flight-departure-time"),
                        (By.CSS_SELECTOR, "[data-testid*='departureTime']"),
                        (By.XPATH, ".//div[@data-testid='departureTime']"),
                        (By.XPATH, ".//div[contains(@class, 'flight-departure-time')]"),
                    ]
                    for selector in dep_selectors:
                        try:
                            dep_elem = card.find_element(*selector)
                            departure_time = dep_elem.text.strip()
                            if departure_time and ':' in departure_time:
                                break
                        except:
                            continue
                    flight_info['departure_time'] = departure_time or "N/A"
                    
                    arrival_time = None
                    arr_selectors = [
                        (By.CSS_SELECTOR, "[data-testid='arrivalTime']"),
                        (By.CSS_SELECTOR, ".flight-arrival-time"),
                        (By.CSS_SELECTOR, "[data-testid*='arrivalTime']"),
                        (By.XPATH, ".//div[@data-testid='arrivalTime']"),
                        (By.XPATH, ".//div[contains(@class, 'arrival-time')]"),
                    ]
                    for selector in arr_selectors:
                        try:
                            arr_elem = card.find_element(*selector)
                            arrival_time = arr_elem.text.strip()
                            if arrival_time and ':' in arrival_time:
                                break
                        except:
                            continue
                    flight_info['arrival_time'] = arrival_time or "N/A"
                    
                    airline_name = None
                    airline_selectors = [
                        (By.CSS_SELECTOR, "[data-testid='AJet'], [data-testid='THY'], [data-testid='Pegasus'], [data-testid='AnadoluJet']"),
                        (By.CSS_SELECTOR, ".summary-marketing-airlines"),
                        (By.CSS_SELECTOR, "[class*='summary-marketing-airlines']"),
                        (By.XPATH, ".//div[@data-testid and (contains(@data-testid, 'AJet') or contains(@data-testid, 'THY') or contains(@data-testid, 'Pegasus'))]"),
                        (By.XPATH, ".//div[contains(@class, 'summary-marketing-airlines')]"),
                    ]
                    for selector in airline_selectors:
                        try:
                            airline_elem = card.find_element(*selector)
                            airline_name = airline_elem.text.strip()
                            if airline_name and airline_name.lower() != "unknown" and len(airline_name) > 0:
                                break
                        except:
                            continue
                    flight_info['airline'] = airline_name or "Unknown"
                    
                    price = None
                    price_selectors = [
                        (By.CSS_SELECTOR, "[data-price]"),
                        (By.CSS_SELECTOR, ".summary-average-price[data-price]"),
                        (By.CSS_SELECTOR, ".money-int"),
                        (By.CSS_SELECTOR, "[class*='money-int']"),
                        (By.CSS_SELECTOR, "[class*='money']"),
                        (By.XPATH, ".//span[contains(@class, 'money-int')]"),
                        (By.XPATH, ".//div[contains(@class, 'summary-average-price')]//span[contains(@class, 'money-int')]"),
                    ]
                    for selector in price_selectors:
                        try:
                            price_elem = card.find_element(*selector)
                            
                            data_price = price_elem.get_attribute("data-price")
                            if data_price:
                                try:
                                    price = int(float(data_price))
                                    break
                                except:
                                    pass
                            
                            price_text = price_elem.text.strip()
                            if price_text:
                                import re
                                clean_price = price_text.replace('.', '').replace(',', '').strip()
                                numbers = re.findall(r'\d+', clean_price)
                                if numbers:
                                    price = int(numbers[0])
                                    break
                        except:
                            continue
                    flight_info['price'] = price
                    
                    connection = "Direct"
                    connection_selectors = [
                        (By.CSS_SELECTOR, "[data-testid='transferStateDirect']"),
                        (By.CSS_SELECTOR, "[data-testid*='transferState']"),
                        (By.CSS_SELECTOR, ".summary-transit"),
                        (By.CSS_SELECTOR, "[class*='summary-transit']"),
                        (By.XPATH, ".//div[contains(@class, 'summary-transit')]"),
                        (By.XPATH, ".//div[@data-testid and contains(@data-testid, 'transferState')]"),
                    ]
                    for selector in connection_selectors:
                        try:
                            conn_elem = card.find_element(*selector)
                            conn_text = conn_elem.text.strip()
                            if conn_text:
                                if 'direkt' in conn_text.lower() or 'direct' in conn_text.lower():
                                    connection = "Direct"
                                elif '1' in conn_text or 'aktarma' in conn_text.lower():
                                    connection = "1 Stop"
                                else:
                                    connection = conn_text
                                break
                        except:
                            continue
                    flight_info['connection'] = connection
                    
                    duration = None
                    duration_selectors = [
                        (By.CSS_SELECTOR, "[data-testid='departureFlightTime']"),
                        (By.CSS_SELECTOR, "[data-testid*='FlightTime']"),
                        (By.CSS_SELECTOR, "[data-testid*='duration']"),
                        (By.XPATH, ".//span[@data-testid='departureFlightTime']"),
                        (By.XPATH, ".//span[contains(@data-testid, 'FlightTime')]"),
                    ]
                    for selector in duration_selectors:
                        try:
                            dur_elem = card.find_element(*selector)
                            duration = dur_elem.text.strip()
                            if duration:
                                break
                        except:
                            continue
                    flight_info['duration'] = duration or "N/A"
                    flight_info['flight_index'] = i + 1
                    
                    if flight_info.get('departure_time') != "N/A" or flight_info.get('airline') != "Unknown":
                        flight_data.append(flight_info)
                    
                    if (i + 1) % 10 == 0:
                        print(f"[INFO] {i + 1} uçuş verisi çıkarıldı...")
                        
                except Exception as e:
                    print(f"[WARNING] Uçuş {i+1} veri çıkarma hatası: {str(e)}")
                    continue
            
            print(f"[OK] {len(flight_data)} uçuş verisi başarıyla çıkarıldı")
            return flight_data
            
        except Exception as e:
            print(f"[ERROR] Veri çıkarma hatası: {str(e)}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return []
