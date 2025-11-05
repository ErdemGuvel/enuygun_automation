"""
Test hataları ve önemli anlar için screenshot yardımcı sınıfı
"""
from pathlib import Path
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from utils.logger import logger


class ScreenshotHelper:
    """Test çalıştırma sırasında screenshot almak için yardımcı sınıf"""
    
    def __init__(self, screenshot_dir="screenshots"):
        """Screenshot helper'ı başlatır
        
        Args:
            screenshot_dir: Screenshot dizini (varsayılan: screenshots)
        """
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Screenshot directory: {self.screenshot_dir.absolute()}")
    
    def take_screenshot(self, driver: WebDriver, name: str = None) -> str:
        """Screenshot alır ve screenshots dizinine kaydeder
        
        Args:
            driver: Selenium WebDriver instance'ı
            name: Screenshot dosya adı (opsiyonel)
            
        Returns:
            str: Kaydedilen screenshot dosyasının yolu
        """
        try:
            if name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name = f"screenshot_{timestamp}"
            
            if not name.endswith('.png'):
                name = f"{name}.png"
            
            screenshot_path = self.screenshot_dir / name
            driver.save_screenshot(str(screenshot_path))
            
            logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
        
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            return None
    
    def take_screenshot_on_failure(self, driver: WebDriver, test_name: str) -> str:
        """Test başarısız olduğunda screenshot alır
        
        Args:
            driver: Selenium WebDriver instance'ı
            test_name: Başarısız olan test adı
            
        Returns:
            str: Kaydedilen screenshot dosyasının yolu
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_test_name = "".join(c for c in test_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"FAILED_{safe_test_name}_{timestamp}.png"
        
        return self.take_screenshot(driver, filename)
    
    def take_element_screenshot(self, driver: WebDriver, element, name: str = None) -> str:
        """Belirli bir elementin screenshot'ını alır
        
        Args:
            driver: Selenium WebDriver instance'ı
            element: Screenshot alınacak WebElement
            name: Screenshot dosya adı (opsiyonel)
            
        Returns:
            str: Kaydedilen screenshot dosyasının yolu
        """
        try:
            if name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name = f"element_{timestamp}"
            
            if not name.endswith('.png'):
                name = f"{name}.png"
            
            screenshot_path = self.screenshot_dir / name
            element.screenshot(str(screenshot_path))
            
            logger.info(f"Element screenshot saved: {screenshot_path}")
            return str(screenshot_path)
        
        except Exception as e:
            logger.error(f"Failed to take element screenshot: {str(e)}")
            return None
