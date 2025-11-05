# WINGIE ENUYGUN GROUP
## Junior QA Engineer - Case Study

**Hazırlayan:** Erdem Güvel

Enuygun.com web sitesi için Selenium WebDriver ve pytest kullanılarak geliştirilmiş otomatik test framework'ü. **Page Object Model (POM)** tasarım deseni ile yapılandırılmıştır.

## ✨ Özellikler

- ✅ **Page Object Model (POM)** - Temiz ve sürdürülebilir kod yapısı
- ✅ **Multi-Browser Support** - Chrome ve Firefox desteği
- ✅ **YAML Configuration** - Kolay yapılandırma
- ✅ **Screenshot Capture** - Başarısız testler için otomatik ekran görüntüsü
- ✅ **Test Reporting** - HTML raporları
- ✅ **Data Analysis** - Uçuş verilerinin analizi ve görselleştirilmesi (Case 4)
- ✅ **Robust Error Handling** - Kapsamlı hata yönetimi

## 📁 Proje Yapısı

```
enuygun_automation/
├── config/
│   └── config.yaml              # Yapılandırma dosyası
├── pages/                       # Page Object Model
│   ├── home_page.py            # Ana sayfa
│   └── results_page.py        # Sonuç sayfası
├── tests/                       # Test case'leri
│   ├── test_case1_basic_search.py
│   ├── test_case2_price_sort.py
│   ├── test_case3_critical_path.py
│   └── test_case4_analysis.py
├── utils/                       # Yardımcı araçlar
│   ├── browser_factory.py
│   ├── logger.py
│   ├── screenshot.py
│   ├── csv_helper.py           # Case 4 için
│   └── data_analysis.py        # Case 4 için
├── reports/                     # Raporlar, CSV, grafikler
├── screenshots/                 # Ekran görüntüleri
└── requirements.txt
```

## 🚀 Kurulum

### Sistem Gereksinimleri

- Python 3.8+
- Chrome/Firefox (Driver'lar otomatik indirilir)
- İnternet bağlantısı

### Adımlar

1. **Projeyi klonlayın**
   ```bash
   git clone <repository-url>
   cd enuygun_automation
   ```

2. **Virtual environment oluşturun (önerilir)**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Bağımlılıkları yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

4. **Config dosyasını kontrol edin**
   `config/config.yaml` dosyasında browser ayarları, şehirler ve tarihleri yapılandırın.

## 📝 Test Senaryoları

### Case 1: Basic Flight Search and Time Filter

**Amaç:** Temel uçuş arama ve saat filtresi doğrulama

**İşlemler:**
- İstanbul-Ankara gidiş-dönüş araması
- Slider tabanlı saat filtresi (10:00 AM - 6:00 PM)
- Uçuş saatlerinin doğrulanması

```bash
pytest tests/test_case1_basic_search.py -v -s
```

### Case 2: Price Sorting for Turkish Airlines

**Amaç:** Türk Hava Yolları için filtre doğrulama

**İşlemler:**
- İstanbul-Ankara araması
- Saat filtresi (10:00-18:00)
- THY filtresi uygulama
- Tüm uçuşların THY olduğunu doğrulama

```bash
pytest tests/test_case2_price_sort.py -v -s
```

### Case 3: Critical Path Testing

**Amaç:** Kritik kullanıcı yolculuğunu test etme

**Kritik Yol:**
1. Ana sayfa → Cookie/popup kapatma
2. Gidiş-dönüş seçimi → Şehir ve tarih girişi
3. Arama yapma → Sonuçları kontrol etme
4. Filtre uygulama (10:00-18:00) → Detaylı doğrulamalar

```bash
pytest tests/test_case3_critical_path.py -v -s
```

### Case 4: Analysis and Categorization

**Amaç:** Veri çıkarma, analiz ve görselleştirme

**İşlemler:**
1. İstanbul → Lefkoşa rotası için arama
2. Tüm uçuş verilerini çıkarma (kalkış/varış saatleri, havayolu, fiyat, aktarma, süre)
3. CSV'ye kaydetme
4. İstatistiksel analiz (min/max/avg fiyatlar)
5. En uygun uçuşları belirleme (alt %30 algoritması)
6. Görselleştirmeler (fiyat dağılımı, havayolu karşılaştırma, ısı haritası)

**Çıktılar:**
- `reports/flight_data_*.csv`
- `reports/price_distribution_*.png`
- `reports/airline_comparison_*.png`
- `reports/time_price_heatmap_*.png`

```bash
pytest tests/test_case4_analysis.py -v -s
```

## 🧪 Testleri Çalıştırma

```bash
# Tüm testler
pytest

# Belirli test
pytest tests/test_case1_basic_search.py -v -s

# HTML rapor ile
pytest --html=reports/report.html --self-contained-html
```

## ⚙️ Yapılandırma

`config/config.yaml` dosyasından ayarları yapılandırabilirsiniz:

```yaml
browser:
  name: "chrome"              # "chrome" veya "firefox"
  headless: false             # true: görünmez mod
  window_size:
    width: 1366
    height: 768
  implicit_wait: 3
  page_load_timeout: 10

defaults:
  departure_city: "İstanbul"
  destination_city: "Ankara"

dates:
  days_ahead_departure: 15
  days_ahead_return: 3
  format: "%d.%m.%Y"
```

## 📊 Raporlar ve Çıktılar

- **HTML Raporları:** `pytest --html=reports/report.html --self-contained-html`
- **Ekran Görüntüleri:** Başarısız testler için `screenshots/` klasörüne otomatik kaydedilir
- **Case 4 Çıktıları:**
  - CSV: `reports/flight_data_*.csv`
  - Grafikler: `price_distribution_*.png`, `airline_comparison_*.png`, `time_price_heatmap_*.png`

## 🔧 Sorun Giderme

**Driver Bulunamadı:**
```bash
pip install --upgrade webdriver-manager
```

**Element Bulunamadı:**
- `config.yaml`'da `implicit_wait` değerini artırın
- `pages/` klasöründeki locator'ları güncelleyin

**Popup/Cookie Sorunları:** `pages/home_page.py` → `_handle_cookies_and_popups()`

**Slider Filtresi:** `pages/results_page.py` → `apply_time_filter_with_sliders()`

**Testler Yavaş:** `config.yaml` → `headless: true`, `implicit_wait` değerini düşürün

## 🛠️ Geliştirme

**Yeni Test Ekleme:**
1. `tests/` klasöründe yeni test dosyası oluşturun
2. Page Object Model pattern'ini kullanın
3. Config dosyasından parametreleri okuyun

**Locator Stratejisi (Öncelik Sırası):**
1. `data-testid` attribute'ları (en güvenilir)
2. CSS Selector (class/id kombinasyonları)
3. XPath (son çare)

## 📝 Notlar

- ⚠️ Testler gerçek web sitesi üzerinde çalışır (internet gerekli)
- ⚠️ Locator'lar site güncellemelerinde değişebilir
- ✅ ChromeDriver ve GeckoDriver otomatik indirilir
- ✅ Testler parametreli (config.yaml'dan okunur)
- ✅ Page Object Model kullanıldığı için bakımı kolaydır
