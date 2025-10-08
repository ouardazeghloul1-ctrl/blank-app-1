import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
import logging
import re

class WardaScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_headers()
        self.data = []
        
    def setup_headers(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ar-SA,ar;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        self.session.headers.update(self.headers)
    
    def scrape_aqar(self, city, property_type):
        """جمع البيانات من Aqar.fm"""
        try:
            city_map = {
                'الرياض': 'riyadh', 
                'جدة': 'jeddah', 
                'الدمام': 'dammam', 
                'مكة': 'makkah', 
                'المدينة': 'almadinah'
            }
            prop_map = {'شقة': 'apartment', 'فيلا': 'villa', 'أرض': 'land'}
            
            search_city = city_map.get(city, city)
            search_prop = prop_map.get(property_type, property_type)
            
            url = f"https://aqar.fm/search?city={search_city}&type={search_prop}"
            print(f"🔍 جاري جمع البيانات من Aqar: {city} - {property_type}")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # البحث بمرونة في العناصر
            listings = soup.find_all(['div', 'article'], class_=lambda x: x and any(
                cls in str(x).lower() for cls in ['card', 'listing', 'property', 'item']
            ))
            
            for listing in listings[:20]:
                property_data = self.parse_aqar_listing(listing, city, property_type)
                if property_data and self.validate_property_data(property_data):
                    self.data.append(property_data)
            
            self.respectful_delay()
            return True
            
        except Exception as e:
            logging.error(f"❌ خطأ في Aqar لـ {city}-{property_type}: {e}")
            return False
    
    def scrape_bayut(self, city, property_type):
        """جمع البيانات من Bayut.sa"""
        try:
            city_map = {
                'الرياض': 'riyadh', 
                'جدة': 'jeddah', 
                'الدمام': 'dammam',
                'مكة': 'makkah-al-mukarramah',
                'المدينة': 'al-madinah-al-munawwarah'
            }
            prop_map = {'شقة': 'apartments', 'فيلا': 'villas', 'أرض': 'land'}
            
            search_city = city_map.get(city, city.lower())
            search_prop = prop_map.get(property_type, property_type.lower())
            
            url = f"https://www.bayut.sa/en/search/{search_city}/{search_prop}/"
            print(f"🔍 جاري جمع البيانات من Bayut: {city} - {property_type}")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # البحث في Bayut
            listings = soup.find_all(['article', 'div', 'li'], attrs={
                'class': lambda x: x and any(
                    cls in str(x).lower() for cls in ['property', 'listing', 'card', 'item']
                ) if x else False
            })
            
            for listing in listings[:20]:
                property_data = self.parse_bayut_listing(listing, city, property_type)
                if property_data and self.validate_property_data(property_data):
                    self.data.append(property_data)
            
            self.respectful_delay()
            return True
            
        except Exception as e:
            logging.error(f"❌ خطأ في Bayut لـ {city}-{property_type}: {e}")
            return False
    
    def parse_aqar_listing(self, listing, city, property_type):
        """تحليل بيانات كل عقار في Aqar"""
        try:
            price_text = self.extract_text(listing, ['.price', '.cost', '[class*="price"]'])
            price = self.extract_price(price_text)
            
            area_text = self.extract_text(listing, ['.area', '.size', '[class*="area"]'])
            area = self.extract_area(area_text)
            
            district = self.extract_text(listing, ['.district', '.location', '.region', '.address'])
            title = self.extract_text(listing, ['.title', 'h2', 'h3', 'a'])
            
            if price and area:
                return {
                    'City': city,
                    'District': district or city,
                    'Property_Type': property_type,
                    'Price': price,
                    'Area': area,
                    'Source': 'Aqar.fm',
                    'Date': datetime.now().strftime('%Y-%m-%d'),
                    'Title': title or f"{property_type} في {city}"
                }
        except Exception as e:
            logging.warning(f"⚠️ خطأ في تحليل عقار Aqar: {e}")
        return None
    
    def parse_bayut_listing(self, listing, city, property_type):
        """تحليل بيانات كل عقار في Bayut"""
        try:
            price_text = self.extract_text(listing, [
                '[aria-label*="price"]', 
                '.price',
                '[class*="price"]',
                '.c4fc20ba'
            ])
            price = self.extract_price(price_text)
            
            area_text = self.extract_text(listing, [
                '[aria-label*="area"]',
                '.area',
                '[class*="area"]',
                '.c4a22b7e'
            ])
            area = self.extract_area(area_text)
            
            district = self.extract_text(listing, [
                '[aria-label*="location"]',
                '.location',
                '.neighborhood'
            ])
            
            title = self.extract_text(listing, [
                'h2',
                'h3',
                '[aria-label*="title"]',
                '.title'
            ])
            
            if price and area:
                return {
                    'City': city,
                    'District': district or city,
                    'Property_Type': property_type,
                    'Price': price,
                    'Area': area,
                    'Source': 'Bayut.sa',
                    'Date': datetime.now().strftime('%Y-%m-%d'),
                    'Title': title or f"{property_type} في {city}"
                }
        except Exception as e:
            logging.warning(f"⚠️ خطأ في تحليل عقار Bayut: {e}")
        return None
    
    def extract_text(self, element, selectors):
        """استخراج النص باستخدام multiple selectors"""
        for selector in selectors:
            try:
                found = element.select_one(selector)
                if found and found.get_text(strip=True):
                    return found.get_text(strip=True)
            except:
                continue
        return ""
    
    def extract_price(self, price_text):
        """استخراج السعر من النص"""
        try:
            if 'مليون' in price_text.lower() or 'million' in price_text.lower():
                # استخراج الأرقام مع الكسور
                numbers = re.findall(r'[\d.]+', price_text)
                if numbers:
                    price = float(numbers[0].replace(',', ''))
                    if price < 100:  # إذا كان الرقم أقل من 100 فهو بالمليون
                        return int(price * 1000000)
                    return int(price)
            else:
                cleaned = re.sub(r'[^\d]', '', price_text)
                if cleaned:
                    return int(cleaned)
        except:
            pass
        return None
    
    def extract_area(self, area_text):
        """استخراج المساحة من النص"""
        try:
            numbers = re.findall(r'\d+', area_text)
            return int(numbers[0]) if numbers else None
        except:
            return None
    
    def validate_property_data(self, data):
        """التحقق من صحة البيانات"""
        return (
            data['Price'] is not None and 
            data['Area'] is not None and
            10000 <= data['Price'] <= 50000000 and
            10 <= data['Area'] <= 5000
        )
    
    def respectful_delay(self):
        """فاصل زمني محترم"""
        time.sleep(random.uniform(2, 4))
