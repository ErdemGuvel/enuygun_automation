"""
Test çalıştırma loglama için yardımcı sınıf
"""
import logging
import yaml
from pathlib import Path
from datetime import datetime


class Logger:
    """Test otomasyonu için özel logger sınıfı"""
    
    _instance = None
    _logger = None
    
    def __new__(cls, config_path="config/config.yaml"):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, config_path="config/config.yaml"):
        if self._logger is None:
            self.config_path = config_path
            self.config = self._load_config()
            self._logger = self._setup_logger()
    
    def _load_config(self):
        """YAML dosyasından konfigürasyon yükler"""
        config_file = Path(self.config_path)
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def _setup_logger(self):
        """Dosya ve konsol handler'ları ile logger kurar"""
        logger = logging.getLogger('enuygun_automation')
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()
        
        log_level = self.config.get('logging', {}).get('level', 'INFO')
        level = getattr(logging, log_level.upper(), logging.INFO)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        log_file = self.config.get('logging', {}).get('file', 'logs/test_execution.log')
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        return logger
    
    def get_logger(self):
        """Logger instance'ını döndürür"""
        return self._logger
    
    def info(self, message):
        """Info seviyesinde log yazar"""
        self._logger.info(message)
    
    def debug(self, message):
        """Debug seviyesinde log yazar"""
        self._logger.debug(message)
    
    def warning(self, message):
        """Warning seviyesinde log yazar"""
        self._logger.warning(message)
    
    def error(self, message):
        """Error seviyesinde log yazar"""
        self._logger.error(message)
    
    def critical(self, message):
        """Critical seviyesinde log yazar"""
        self._logger.critical(message)


logger = Logger().get_logger()
