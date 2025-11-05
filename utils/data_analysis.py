"""
Case 4 için veri analizi - İstatistiksel analiz ve görselleştirme
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from typing import List, Dict, Any
from utils.logger import logger
from utils.csv_helper import CSVHelper


class DataAnalyzer:
    """Uçuş verileri için gelişmiş analiz ve görselleştirme sınıfı"""

    def __init__(self, flight_data: List[Dict[str, Any]]):
        """Uçuş verisi ile başlatır
        
        Args:
            flight_data: Uçuş bilgilerini içeren sözlük listesi
        """
        self.flight_data = flight_data
        self.df = pd.DataFrame(flight_data) if flight_data else pd.DataFrame()

    def calculate_airline_price_stats(self) -> Dict[str, Dict[str, float]]:
        """Havayolu başına fiyat istatistiklerini hesaplar (Min, Max, Ortalama)
        
        Returns:
            dict: Havayolu adı -> {min, max, avg, count} sözlüğü
        """
        if self.df.empty or 'airline' not in self.df.columns or 'price' not in self.df.columns:
            return {}

        airline_stats = {}
        for airline in self.df['airline'].unique():
            if airline == "Unknown" or pd.isna(airline):
                continue
                
            airline_data = self.df[self.df['airline'] == airline]
            prices = airline_data['price'].dropna()
            prices = prices[prices.notna()]
            
            if not prices.empty and len(prices) > 0:
                prices = pd.to_numeric(prices, errors='coerce').dropna()
                
                if len(prices) > 0:
                    airline_stats[airline] = {
                        "min": float(prices.min()),
                        "max": float(prices.max()),
                        "avg": float(prices.mean()),
                        "count": len(prices)
                    }

        return airline_stats

    def find_cost_effective_flights(self) -> List[Dict[str, Any]]:
        """En uygun maliyetli uçuşları bulur (en düşük %30 fiyat aralığı)
        
        Returns:
            list: En uygun maliyetli uçuşların listesi
        """
        if self.df.empty or 'price' not in self.df.columns:
            return []

        prices = pd.to_numeric(self.df['price'], errors='coerce').dropna()
        if prices.empty:
            return []

        threshold = prices.quantile(0.30)
        cost_effective_df = self.df[pd.to_numeric(self.df['price'], errors='coerce') <= threshold]
        cost_effective_df = cost_effective_df.sort_values(by='price', ascending=True)
        
        return cost_effective_df.to_dict('records')

    def create_price_distribution_chart(self, filename: str):
        """Fiyat dağılım histogram grafiği oluşturur
        
        Args:
            filename: Grafik dosyasının kaydedileceği yol
        """
        try:
            if self.df.empty or 'price' not in self.df.columns:
                print("[WARNING] Fiyat verisi bulunamadı, grafik oluşturulamadı")
                return

            prices = pd.to_numeric(self.df['price'], errors='coerce').dropna()
            if prices.empty:
                print("[WARNING] Geçerli fiyat verisi yok")
                return

            plt.figure(figsize=(10, 6))
            plt.hist(prices, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            plt.title('Uçuş Fiyat Dağılımı', fontsize=16, fontweight='bold')
            plt.xlabel('Fiyat (TL)', fontsize=12)
            plt.ylabel('Uçuş Sayısı', fontsize=12)
            plt.grid(True, alpha=0.3)
            
            stats_text = f'Min: {prices.min():.0f}TL\nMax: {prices.max():.0f}TL\nOrtalama: {prices.mean():.0f}TL'
            plt.text(0.7, 0.8, stats_text, transform=plt.gca().transAxes, 
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
            
            plt.tight_layout()
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"[OK] Fiyat dağılım grafiği kaydedildi: {filename}")
            
        except Exception as e:
            print(f"[WARNING] Grafik oluşturma hatası: {str(e)}")

    def create_airline_comparison_chart(self, filename: str):
        """Havayolu fiyat karşılaştırma grafiği oluşturur
        
        Args:
            filename: Grafik dosyasının kaydedileceği yol
        """
        try:
            airline_stats = self.calculate_airline_price_stats()
            if not airline_stats:
                print("[WARNING] Havayolu verisi bulunamadı, grafik oluşturulamadı")
                return

            airlines = list(airline_stats.keys())
            avg_prices = [stats['avg'] for stats in airline_stats.values()]
            min_prices = [stats['min'] for stats in airline_stats.values()]
            max_prices = [stats['max'] for stats in airline_stats.values()]

            fig, ax = plt.subplots(figsize=(12, 8))
            
            x = np.arange(len(airlines))
            width = 0.25

            ax.bar(x - width, min_prices, width, label='Min Fiyat', alpha=0.8, color='lightgreen')
            ax.bar(x, avg_prices, width, label='Ortalama Fiyat', alpha=0.8, color='skyblue')
            ax.bar(x + width, max_prices, width, label='Max Fiyat', alpha=0.8, color='lightcoral')

            ax.set_xlabel('Havayolu', fontsize=12)
            ax.set_ylabel('Fiyat (TL)', fontsize=12)
            ax.set_title('Havayolu Fiyat Karşılaştırması', fontsize=16, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(airlines, rotation=45, ha='right')
            ax.legend()
            ax.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"[OK] Havayolu karşılaştırma grafiği kaydedildi: {filename}")
            
        except Exception as e:
            print(f"[WARNING] Grafik oluşturma hatası: {str(e)}")

    def create_time_price_heatmap(self, filename: str):
        """Saat bazında fiyat ısı haritası oluşturur
        
        Args:
            filename: Grafik dosyasının kaydedileceği yol
        """
        try:
            if self.df.empty or 'departure_time' not in self.df.columns or 'price' not in self.df.columns:
                print("[WARNING] Saat ve fiyat verisi bulunamadı, ısı haritası oluşturulamadı")
                return

            def extract_hour(time_str):
                """Kalkış saatinden saat bilgisini çıkarır"""
                try:
                    if pd.isna(time_str) or time_str == "N/A":
                        return None
                    time_str = str(time_str)
                    if ':' in time_str:
                        hour_str = time_str.split(':')[0].strip()
                        hour = int(hour_str)
                        if 0 <= hour <= 23:
                            return hour
                    return None
                except:
                    return None

            self.df['hour'] = self.df['departure_time'].apply(extract_hour)
            self.df['price_numeric'] = pd.to_numeric(self.df['price'], errors='coerce')
            hourly_data = self.df.dropna(subset=['hour', 'price_numeric'])
            
            if hourly_data.empty:
                print("[WARNING] Saat verisi çıkarılamadı veya geçerli fiyat yok")
                return

            hourly_prices = hourly_data.groupby('hour')['price_numeric'].mean().reset_index()
            price_matrix = np.zeros((4, 6))
            
            for i in range(4):
                for j in range(6):
                    hour = i * 6 + j
                    hour_data = hourly_prices[hourly_prices['hour'] == hour]
                    if not hour_data.empty:
                        price_matrix[i, j] = hour_data['price_numeric'].iloc[0]
                    else:
                        price_matrix[i, j] = np.nan

            plt.figure(figsize=(14, 8))
            
            mask = np.isnan(price_matrix)
            sns.heatmap(price_matrix, annot=True, fmt='.0f', cmap='YlOrRd', 
                       cbar_kws={'label': 'Ortalama Fiyat (TL)'}, mask=mask,
                       vmin=price_matrix[~np.isnan(price_matrix)].min() if not np.all(np.isnan(price_matrix)) else 0,
                       vmax=price_matrix[~np.isnan(price_matrix)].max() if not np.all(np.isnan(price_matrix)) else 1000)
            
            plt.title('Saat Bazında Fiyat Dağılımı - Isı Haritası', fontsize=16, fontweight='bold')
            plt.xlabel('Saat Aralığı', fontsize=12)
            plt.ylabel('Gün Bölümü', fontsize=12)
            
            hour_ticks = [f"{i*6:02d}:00-{(i+1)*6-1:02d}:59" for i in range(6)]
            day_ticks = ['Gece (00-05)', 'Sabah (06-11)', 'Öğle (12-17)', 'Akşam (18-23)']
            
            plt.xticks(np.arange(6) + 0.5, hour_ticks, rotation=45, ha='right')
            plt.yticks(np.arange(4) + 0.5, day_ticks)
            
            plt.tight_layout()
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"[OK] Saat bazında fiyat ısı haritası kaydedildi: {filename}")
            
        except Exception as e:
            print(f"[WARNING] Isı haritası oluşturma hatası: {str(e)}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")

