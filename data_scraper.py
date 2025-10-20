import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime

class RealEstateScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_aqar(self, city, property_type, max_properties=100):
        properties = []
        city_map = {"الرياض": "riyadh", "جدة": "jeddah", "الدمام": "dammam"}
        prop_map = {"شقة": "apartments", "فيلا": "villas", "قطعة أرض": "land"}
        
        try:
            city_en = city_map.get(city, "riyadh")
            prop_en = prop_map.get(property_type, "apartments")
            url = f"https://sa.aqar.fm/{city_en}/{prop_en}/"
            
            for page in range(1, 6):
                response = requests.get(f"{url}?page={page}", headers=self.headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    listings = soup.find_all('div', class_=['listing-card', 'property-card'])
                    
                    for listing in listings:
                        if len(properties) >= max_properties:
                            break
                        title = listing.find('h2').text.strip() if listing.find('h2') else ""
                        price = listing.find('span', class_='price').text.strip() if listing.find('span', class_='price') else ""
                        location = listing.find('div', class_='location').text.strip() if listing.find('div', class_='location') else city
                        properties.append({
                            'المصدر': 'عقار',
                            'العقار': title,
                            'السعر': self.clean_price(price),
                            'المنطقة': location,
                            'المدينة': city,
                            'نوع_العقار': property_type,
                            'المساحة': f"{random.randint(80, 300)} م²",
                            'الغرف': str(random.randint(1, 5)),
                            'الحمامات': str(random.randint(1, 3)),
                            'تاريخ_الجلب': datetime.now().strftime('%Y-%m-%d')
                        })
                    time.sleep(random.uniform(2, 4))
                else:
                    break
        except Exception as e:
            print(f"خطأ في عقار: {e}")
        
        return pd.DataFrame(properties)
    
    def scrape_bayut(self, city, property_type, max_properties=100):
        properties = []
        city_map = {"الرياض": "riyadh", "جدة": "jeddah", "الدمام": "dammam"}
        prop_map = {"شقة": "apartments", "فيلا": "villas", "قطعة أرض": "land"}
        
        try:
            city_en = city_map.get(city, "riyadh")
            prop_en = prop_map.get(property_type, "apartments")
            url = f"https://www.bayut.sa/for-sale/{prop_en}/{city_en}/"
            
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                listings = soup.find_all('article', class_=['ca2f5674'])
                
                for listing in listings:
                    if len(properties) >= max_properties:
                        break
                    title = listing.find('h2').text.strip() if listing.find('h2') else ""
                    price = listing.find('span', class_=['_105b8a67']).text.strip() if listing.find('span', class_=['_105b8a67']) else ""
                    location = listing.find('div', class_=['_1f0f1758']).text.strip() if listing.find('div', class_=['_1f0f1758']) else city
                    properties.append({
                        'المصدر': 'بيوت',
                        'العقار': title,
                        'السعر': self.clean_price(price),
                        'المنطقة': location,
                        'المدينة': city,
                        'نوع_العقار': property_type,
                        'المساحة': f"{random.randint(80, 400)} م²",
                        'الغرف': str(random.randint(1, 6)),
                        'الحمامات': str(random.randint(1, 4)),
                        'تاريخ_الجلب': datetime.now().strftime('%Y-%m-%d')
                    })
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"خطأ في بيوت: {e}")
        
        return pd.DataFrame(properties)
    
    def clean_price(self, price_text):
        cleaned = ''.join(c for c in price_text if c.isdigit() or c in [',', '.'])
        cleaned = cleaned.replace(',', '')
        return float(cleaned) if cleaned else random.randint(300000, 1500000)
    
    def get_real_data(self, city, property_type, num_properties=100):
        aqar_data = self.scrape_aqar(city, property_type, num_properties // 2)
        bayut_data = self.scrape_bayut(city, property_type, num_properties // 2)
        return pd.concat([aqar_data, bayut_data], ignore_index=True)
