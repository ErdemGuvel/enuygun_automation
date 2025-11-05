import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import io


def load_config():
    """Config dosyasını yükler
    
    Returns:
        dict: Config ayarları
    """
    with io.open('config/config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def create_driver():
    """WebDriver instance oluşturur (Chrome veya Firefox)
    
    Returns:
        WebDriver: Yapılandırılmış WebDriver instance'ı
    """
    config = load_config()
    browser_name = config['browser']['name'].lower()
    headless = config['browser']['headless']
    width = config['browser']['window_size']['width']
    height = config['browser']['window_size']['height']

    if browser_name == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-features=TranslateUI')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-sync')
        options.add_argument('--disable-default-apps')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-logging')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument(f'--window-size={width},{height}')
        options.page_load_strategy = 'eager'
        
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    elif browser_name == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument(f'--width={width}')
        options.add_argument(f'--height={height}')
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    else:
        raise ValueError(f"Desteklenmeyen tarayıcı: {browser_name}")

    driver.implicitly_wait(config['browser']['implicit_wait'])
    driver.set_page_load_timeout(config['browser']['page_load_timeout'])
    return driver
