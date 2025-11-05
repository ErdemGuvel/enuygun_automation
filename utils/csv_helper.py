"""
Test verilerini CSV dosyalarına kaydetmek için yardımcı sınıf
"""
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from utils.logger import logger


class CSVHelper:
    """CSV işlemleri için yardımcı sınıf"""
    
    def __init__(self, output_dir="reports"):
        """CSV helper'ı başlatır
        
        Args:
            output_dir: Çıktı dizini (varsayılan: reports)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"CSV output directory: {self.output_dir.absolute()}")
    
    @staticmethod
    def save_flight_data(flight_data: List[Dict], filepath: str):
        """Uçuş verilerini CSV dosyasına kaydeder (Case 4 için static method)
        
        Args:
            flight_data: Uçuş sözlüklerinin listesi
            filepath: CSV dosyasının kaydedileceği tam yol
        """
        try:
            import os
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            if not flight_data:
                print("[WARNING] Kaydedilecek veri yok")
                return
            
            fieldnames = set()
            for flight in flight_data:
                fieldnames.update(flight.keys())
            fieldnames = sorted(list(fieldnames))
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(flight_data)
            
            print(f"[OK] {len(flight_data)} uçuş verisi CSV'ye kaydedildi: {filepath}")
            
        except Exception as e:
            print(f"[ERROR] CSV kaydetme hatası: {str(e)}")
    
    def save_to_csv(self, data: List[Dict], filename: str, headers: List[str] = None) -> str:
        """Veriyi CSV dosyasına kaydeder
        
        Args:
            data: Veri içeren sözlük listesi
            filename: CSV dosya adı (uzantı olmadan)
            headers: Opsiyonel sütun başlıkları listesi
            
        Returns:
            str: Kaydedilen CSV dosyasının yolu
        """
        try:
            if not filename.endswith('.csv'):
                filename = f"{filename}.csv"
            
            csv_path = self.output_dir / filename
            
            if not data:
                logger.warning(f"No data to save to CSV: {filename}")
                return None
            
            if headers is None:
                headers = list(data[0].keys())
            
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            
            logger.info(f"Data saved to CSV: {csv_path} ({len(data)} rows)")
            return str(csv_path)
        
        except Exception as e:
            logger.error(f"Failed to save CSV file: {str(e)}")
            return None
    
    def append_to_csv(self, data: List[Dict], filename: str, headers: List[str] = None) -> str:
        """Mevcut CSV dosyasına veri ekler veya yeni dosya oluşturur
        
        Args:
            data: Veri içeren sözlük listesi
            filename: CSV dosya adı (uzantı olmadan)
            headers: Opsiyonel sütun başlıkları listesi
            
        Returns:
            str: CSV dosyasının yolu
        """
        try:
            if not filename.endswith('.csv'):
                filename = f"{filename}.csv"
            
            csv_path = self.output_dir / filename
            file_exists = csv_path.exists()
            
            if not data:
                logger.warning(f"No data to append to CSV: {filename}")
                return None
            
            if headers is None:
                headers = list(data[0].keys())
            
            with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerows(data)
            
            logger.info(f"Data appended to CSV: {csv_path} ({len(data)} rows)")
            return str(csv_path)
        
        except Exception as e:
            logger.error(f"Failed to append to CSV file: {str(e)}")
            return None
    
    def read_from_csv(self, filename: str) -> List[Dict]:
        """CSV dosyasından veri okur
        
        Args:
            filename: CSV dosya adı (uzantılı veya uzantısız)
            
        Returns:
            list: Veri içeren sözlük listesi
        """
        try:
            if not filename.endswith('.csv'):
                filename = f"{filename}.csv"
            
            csv_path = self.output_dir / filename
            
            if not csv_path.exists():
                logger.warning(f"CSV file not found: {filename}")
                return []
            
            data = []
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)
            
            logger.info(f"Data read from CSV: {csv_path} ({len(data)} rows)")
            return data
        
        except Exception as e:
            logger.error(f"Failed to read CSV file: {str(e)}")
            return []
