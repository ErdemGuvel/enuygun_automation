# ✈️ Web Automation Case Study – Enuygun.com

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.x-green?style=for-the-badge&logo=selenium)
![Pytest](https://img.shields.io/badge/Pytest-Testing-orange?style=for-the-badge&logo=pytest)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Selenium WebDriver ve pytest kullanılarak geliştirilmiş profesyonel web otomasyon test framework'ü**

[🚀 Özellikler](#-özellikler) • [📦 Kurulum](#-kurulum) • [🧪 Test Senaryoları](#-test-senaryoları) • [📊 Raporlar](#-raporlar)

</div>

---

## 🇹🇷 TÜRKÇE

### 📋 Proje Hakkında

Bu proje, **Enuygun.com** web sitesi için geliştirilmiş kapsamlı bir otomasyon test framework'üdür. **Page Object Model (POM)** tasarım deseni kullanılarak, sürdürülebilir, ölçeklenebilir ve bakımı kolay bir yapı oluşturulmuştur.

**Geliştirici:** Erdem Güvel

### ✨ Özellikler

| Özellik | Açıklama |
|---------|----------|
| 🏗️ **Page Object Model** | Temiz ve sürdürülebilir kod yapısı |
| 🌐 **Çoklu Tarayıcı Desteği** | Chrome ve Firefox desteği |
| ⚙️ **YAML Yapılandırma** | Kolay ve esnek yapılandırma |
| 📸 **Otomatik Ekran Görüntüsü** | Başarısız testler için otomatik screenshot |
| 📊 **Test Raporlama** | HTML formatında detaylı raporlar |
| 📈 **Veri Analizi** | Uçuş verilerinin analizi ve görselleştirilmesi |
| 🛡️ **Güçlü Hata Yönetimi** | Kapsamlı exception handling |
| 🔄 **Otomatik Driver Yönetimi** | WebDriver Manager ile otomatik driver indirme |

### 📁 Proje Yapısı

```
enuygun_automation/
├── 📂 config/
│   └── config.yaml              # Yapılandırma dosyası
├── 📂 pages/                    # Page Object Model
│   ├── home_page.py            # Ana sayfa objesi
│   └── results_page.py         # Sonuç sayfası objesi
├── 📂 tests/                    # Test case'leri
│   ├── test_case1_basic_search.py
│   ├── test_case2_price_sort.py
│   ├── test_case3_critical_path.py
│   └── test_case4_analysis.py
├── 📂 utils/                    # Yardımcı araçlar
│   ├── browser_factory.py      # Tarayıcı yönetimi
│   ├── logger.py               # Loglama
│   ├── screenshot.py           # Ekran görüntüsü
│   ├── csv_helper.py           # CSV işlemleri
│   └── data_analysis.py        # Veri analizi
├── 📂 reports/                 # Raporlar ve çıktılar
├── 📂 screenshots/              # Ekran görüntüleri
└── requirements.txt            # Python bağımlılıkları
```

### 🚀 Kurulum

#### Sistem Gereksinimleri

- 🐍 Python 3.8 veya üzeri
- 🌐 Chrome veya Firefox tarayıcı
- 📡 İnternet bağlantısı

#### Adımlar

1. **📥 Projeyi klonlayın**
   ```bash
   git clone <repository-url>
   cd enuygun_automation
   ```

2. **🔧 Virtual environment oluşturun (önerilir)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **📦 Bağımlılıkları yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

4. **⚙️ Yapılandırma**
   `config/config.yaml` dosyasında tarayıcı ayarları, şehirler ve tarihleri yapılandırın.

### 🧪 Test Senaryoları

#### 📌 Case 1: Temel Uçuş Arama ve Saat Filtresi

**🎯 Amaç:** Temel uçuş arama fonksiyonunu ve saat filtresi doğrulamasını test etme

**📝 İşlemler:**
- ✈️ İstanbul-Ankara gidiş-dönüş araması
- ⏰ Slider tabanlı saat filtresi (10:00 AM - 6:00 PM)
- ✅ Uçuş saatlerinin doğrulanması

```bash
pytest tests/test_case1_basic_search.py -v -s
```

#### 📌 Case 2: Türk Hava Yolları Fiyat Sıralama

**🎯 Amaç:** Türk Hava Yolları için filtre doğrulama

**📝 İşlemler:**
- ✈️ İstanbul-Ankara araması
- ⏰ Saat filtresi (10:00-18:00)
- 🏢 THY filtresi uygulama
- ✅ Tüm uçuşların THY olduğunu doğrulama

```bash
pytest tests/test_case2_price_sort.py -v -s
```

#### 📌 Case 3: Kritik Yol Testi

**🎯 Amaç:** Kullanıcının kritik yolculuğunu end-to-end test etme

**🛤️ Kritik Yol:**
1. 🏠 Ana sayfa → Cookie/popup kapatma
2. 🔄 Gidiş-dönüş seçimi → Şehir ve tarih girişi
3. 🔍 Arama yapma → Sonuçları kontrol etme
4. 🎛️ Filtre uygulama (10:00-18:00) → Detaylı doğrulamalar

```bash
pytest tests/test_case3_critical_path.py -v -s
```

#### 📌 Case 4: Veri Analizi ve Kategorizasyon

**🎯 Amaç:** Veri çıkarma, analiz ve görselleştirme

**📊 İşlemler:**
1. ✈️ İstanbul → Lefkoşa rotası için arama
2. 📥 Tüm uçuş verilerini çıkarma (kalkış/varış saatleri, havayolu, fiyat, aktarma, süre)
3. 💾 CSV'ye kaydetme
4. 📈 İstatistiksel analiz (min/max/avg fiyatlar)
5. 💰 En uygun uçuşları belirleme (alt %30 algoritması)
6. 📊 Görselleştirmeler (fiyat dağılımı, havayolu karşılaştırma, ısı haritası)

**📤 Çıktılar:**
- 📄 `reports/flight_data_*.csv`
- 📊 `reports/price_distribution_*.png`
- 📈 `reports/airline_comparison_*.png`
- 🔥 `reports/time_price_heatmap_*.png`

```bash
pytest tests/test_case4_analysis.py -v -s
```

### 🧪 Testleri Çalıştırma

```bash
# Tüm testleri çalıştır
pytest

# Belirli bir test
pytest tests/test_case1_basic_search.py -v -s

# HTML rapor ile
pytest --html=reports/report.html --self-contained-html

# Verbose mod ile
pytest -v

# Sadece başarısız testleri tekrar çalıştır
pytest --lf
```

### ⚙️ Yapılandırma

`config/config.yaml` dosyasından tüm ayarları yapılandırabilirsiniz:

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

### 📊 Raporlar ve Çıktılar

- **📄 HTML Raporları:** `pytest --html=reports/report.html --self-contained-html`
- **📸 Ekran Görüntüleri:** Başarısız testler için `screenshots/` klasörüne otomatik kaydedilir
- **📈 Case 4 Çıktıları:**
  - CSV: `reports/flight_data_*.csv`
  - Grafikler: `price_distribution_*.png`, `airline_comparison_*.png`, `time_price_heatmap_*.png`

### 🔧 Sorun Giderme

| Sorun | Çözüm |
|-------|-------|
| 🚫 **Driver Bulunamadı** | `pip install --upgrade webdriver-manager` |
| 🔍 **Element Bulunamadı** | `config.yaml`'da `implicit_wait` değerini artırın |
| 🍪 **Popup/Cookie Sorunları** | `pages/home_page.py` → `_handle_cookies_and_popups()` |
| 🎚️ **Slider Filtresi** | `pages/results_page.py` → `apply_time_filter_with_sliders()` |
| ⏱️ **Testler Yavaş** | `config.yaml` → `headless: true`, `implicit_wait` değerini düşürün |

### 🛠️ Geliştirme

**Yeni Test Ekleme:**
1. `tests/` klasöründe yeni test dosyası oluşturun
2. Page Object Model pattern'ini kullanın
3. Config dosyasından parametreleri okuyun

**Locator Stratejisi (Öncelik Sırası):**
1. 🎯 `data-testid` attribute'ları (en güvenilir)
2. 🎨 CSS Selector (class/id kombinasyonları)
3. 🔍 XPath (son çare)

### 📝 Notlar

- ⚠️ Testler gerçek web sitesi üzerinde çalışır (internet gerekli)
- ⚠️ Locator'lar site güncellemelerinde değişebilir
- ✅ ChromeDriver ve GeckoDriver otomatik indirilir
- ✅ Testler parametreli (config.yaml'dan okunur)
- ✅ Page Object Model kullanıldığı için bakımı kolaydır

---

## 🇬🇧 ENGLISH

### 📋 About the Project

This project is a comprehensive automation test framework developed for **Enuygun.com** website. Built using **Page Object Model (POM)** design pattern, it provides a maintainable, scalable, and easy-to-maintain structure.

**Developer:** Erdem Güvel

### ✨ Features

| Feature | Description |
|---------|-------------|
| 🏗️ **Page Object Model** | Clean and maintainable code structure |
| 🌐 **Multi-Browser Support** | Chrome and Firefox support |
| ⚙️ **YAML Configuration** | Easy and flexible configuration |
| 📸 **Automatic Screenshots** | Auto screenshot for failed tests |
| 📊 **Test Reporting** | Detailed HTML reports |
| 📈 **Data Analysis** | Flight data analysis and visualization |
| 🛡️ **Robust Error Handling** | Comprehensive exception handling |
| 🔄 **Automatic Driver Management** | Auto driver download with WebDriver Manager |

### 📁 Project Structure

```
enuygun_automation/
├── 📂 config/
│   └── config.yaml              # Configuration file
├── 📂 pages/                    # Page Object Model
│   ├── home_page.py            # Home page object
│   └── results_page.py         # Results page object
├── 📂 tests/                    # Test cases
│   ├── test_case1_basic_search.py
│   ├── test_case2_price_sort.py
│   ├── test_case3_critical_path.py
│   └── test_case4_analysis.py
├── 📂 utils/                    # Utility tools
│   ├── browser_factory.py      # Browser management
│   ├── logger.py               # Logging
│   ├── screenshot.py           # Screenshot capture
│   ├── csv_helper.py           # CSV operations
│   └── data_analysis.py        # Data analysis
├── 📂 reports/                  # Reports and outputs
├── 📂 screenshots/              # Screenshots
└── requirements.txt            # Python dependencies
```

### 🚀 Installation

#### System Requirements

- 🐍 Python 3.8 or higher
- 🌐 Chrome or Firefox browser
- 📡 Internet connection

#### Steps

1. **📥 Clone the repository**
   ```bash
   git clone <repository-url>
   cd enuygun_automation
   ```

2. **🔧 Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **📦 Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **⚙️ Configuration**
   Configure browser settings, cities, and dates in `config/config.yaml` file.

### 🧪 Test Scenarios

#### 📌 Case 1: Basic Flight Search and Time Filter

**🎯 Objective:** Test basic flight search functionality and time filter validation

**📝 Operations:**
- ✈️ Istanbul-Ankara round-trip search
- ⏰ Slider-based time filter (10:00 AM - 6:00 PM)
- ✅ Flight time validation

```bash
pytest tests/test_case1_basic_search.py -v -s
```

#### 📌 Case 2: Turkish Airlines Price Sorting

**🎯 Objective:** Filter validation for Turkish Airlines

**📝 Operations:**
- ✈️ Istanbul-Ankara search
- ⏰ Time filter (10:00-18:00)
- 🏢 Turkish Airlines filter application
- ✅ Verify all flights are Turkish Airlines

```bash
pytest tests/test_case2_price_sort.py -v -s
```

#### 📌 Case 3: Critical Path Testing

**🎯 Objective:** End-to-end testing of user's critical journey

**🛤️ Critical Path:**
1. 🏠 Home page → Cookie/popup closing
2. 🔄 Round-trip selection → City and date input
3. 🔍 Search execution → Results verification
4. 🎛️ Filter application (10:00-18:00) → Detailed validations

```bash
pytest tests/test_case3_critical_path.py -v -s
```

#### 📌 Case 4: Data Analysis and Categorization

**🎯 Objective:** Data extraction, analysis, and visualization

**📊 Operations:**
1. ✈️ Search for Istanbul → Lefkoşa route
2. 📥 Extract all flight data (departure/arrival times, airline, price, transfer, duration)
3. 💾 Save to CSV
4. 📈 Statistical analysis (min/max/avg prices)
5. 💰 Identify best flights (bottom 30% algorithm)
6. 📊 Visualizations (price distribution, airline comparison, heatmap)

**📤 Outputs:**
- 📄 `reports/flight_data_*.csv`
- 📊 `reports/price_distribution_*.png`
- 📈 `reports/airline_comparison_*.png`
- 🔥 `reports/time_price_heatmap_*.png`

```bash
pytest tests/test_case4_analysis.py -v -s
```

### 🧪 Running Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_case1_basic_search.py -v -s

# With HTML report
pytest --html=reports/report.html --self-contained-html

# Verbose mode
pytest -v

# Run only failed tests
pytest --lf
```

### ⚙️ Configuration

Configure all settings from `config/config.yaml` file:

```yaml
browser:
  name: "chrome"              # "chrome" or "firefox"
  headless: false             # true: headless mode
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

### 📊 Reports and Outputs

- **📄 HTML Reports:** `pytest --html=reports/report.html --self-contained-html`
- **📸 Screenshots:** Automatically saved to `screenshots/` folder for failed tests
- **📈 Case 4 Outputs:**
  - CSV: `reports/flight_data_*.csv`
  - Charts: `price_distribution_*.png`, `airline_comparison_*.png`, `time_price_heatmap_*.png`

### 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| 🚫 **Driver Not Found** | `pip install --upgrade webdriver-manager` |
| 🔍 **Element Not Found** | Increase `implicit_wait` value in `config.yaml` |
| 🍪 **Popup/Cookie Issues** | `pages/home_page.py` → `_handle_cookies_and_popups()` |
| 🎚️ **Slider Filter** | `pages/results_page.py` → `apply_time_filter_with_sliders()` |
| ⏱️ **Slow Tests** | `config.yaml` → `headless: true`, decrease `implicit_wait` value |

### 🛠️ Development

**Adding New Tests:**
1. Create new test file in `tests/` folder
2. Use Page Object Model pattern
3. Read parameters from config file

**Locator Strategy (Priority Order):**
1. 🎯 `data-testid` attributes (most reliable)
2. 🎨 CSS Selector (class/id combinations)
3. 🔍 XPath (last resort)

### 📝 Notes

- ⚠️ Tests run on real website (internet required)
- ⚠️ Locators may change with site updates
- ✅ ChromeDriver and GeckoDriver are automatically downloaded
- ✅ Tests are parameterized (read from config.yaml)
- ✅ Easy maintenance due to Page Object Model usage

---

<div align="center">

**Made with ❤️ by Erdem Güvel**

⭐ Star this repo if you find it helpful!

</div>
