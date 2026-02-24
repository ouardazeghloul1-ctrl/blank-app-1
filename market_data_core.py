# ==============================================
# market_data_core.py - المصدر الوحيد للبيانات الحقيقية
# ==============================================
# سياسة صارمة: REAL DATA ONLY - لا random, لا fallback, لا simulation
# في حالة الفشل: Exception واضح فقط - لا تعويض وهمي
# ==============================================

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import re
import logging

# إعداد التسجيل البسيط
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MarketDataScraper:
    """
    جامع البيانات الحقيقية من السوق العقاري السعودي
    المصادر: Aqar.fm, Bayut.sa
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_headers()
        
    def setup_headers(self):
        """إعداد رؤوس الطلبات لمحاكاة متصفح حقيقي"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ar-SA,ar;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session.headers.update(self.headers)
    
    def scrape_aqar(self, city, property_type):
        """
        جمع البيانات من Aqar.fm
        المصدر: https://sa.aqar.fm/
        """
        properties = []
        
        # تحويل أسماء المدن والأنواع للإنجليزية
        city_map = {
            'الرياض': 'riyadh',
            'جدة': 'jeddah',
            'الدمام': 'dammam',
            'مكة': 'makkah',
            'المدينة': 'almadinah',
            'الخبر': 'al-khubar'
        }
        
        prop_map = {
            'شقة': 'apartments',
            'فيلا': 'villas',
            'أرض': 'land',
            'مكتب': 'offices',
            'محل': 'shops'
        }
        
        city_en = city_map.get(city, city.lower())
        prop_en = prop_map.get(property_type, property_type.lower())
        
        # محاولة جمع البيانات من أول 3 صفحات
        for page in range(1, 4):
            try:
                url = f"https://sa.aqar.fm/{city_en}/{prop_en}/?page={page}"
                logging.info(f"جاري جمع البيانات من Aqar: {url}")
                
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # البحث عن بطاقات العقارات - Aqar تستخدم كلاسات متنوعة
                listings = soup.find_all('div', class_=lambda x: x and any(
                    cls in str(x).lower() for cls in ['listing-card', 'property-card', 'card', 'item']
                ) if x else False)
                
                if not listings:
                    # محاولة بديلة
                    listings = soup.find_all(['article', 'div'], attrs={
                        'data-testid': lambda x: x and 'property' in str(x).lower() if x else False
                    })
                
                for listing in listings:
                    property_data = self._parse_aqar_listing(listing, city, property_type)
                    if property_data and self._validate_property_data(property_data):
                        properties.append(property_data)
                        
                # احترام الموقع - تأخير ثابت
                time.sleep(2)
                
            except requests.exceptions.RequestException as e:
                logging.error(f"خطأ في الاتصال بـ Aqar: {e}")
                continue
            except Exception as e:
                logging.error(f"خطأ غير متوقع في Aqar: {e}")
                continue
        
        return properties
    
    def _parse_aqar_listing(self, listing, city, property_type):
        """تحليل بيانات العقار الواحد من Aqar"""
        try:
            # استخراج السعر
            price_elem = listing.find(['span', 'div'], class_=lambda x: x and any(
                cls in str(x).lower() for cls in ['price', 'cost', 'السعر']
            ) if x else False)
            
            price_text = price_elem.get_text(strip=True) if price_elem else ""
            price = self._extract_price(price_text)
            
            # استخراج المساحة
            area_elem = listing.find(['span', 'div'], class_=lambda x: x and any(
                cls in str(x).lower() for cls in ['area', 'size', 'المساحة']
            ) if x else False)
            
            area_text = area_elem.get_text(strip=True) if area_elem else ""
            area = self._extract_area(area_text)
            
            # استخراج الحي/المنطقة
            district_elem = listing.find(['span', 'div'], class_=lambda x: x and any(
                cls in str(x).lower() for cls in ['location', 'district', 'region', 'الموقع']
            ) if x else False)
            
            district = district_elem.get_text(strip=True) if district_elem else ""
            
            # استخراج العنوان
            title_elem = listing.find(['h2', 'h3', 'a'], class_=lambda x: x and any(
                cls in str(x).lower() for cls in ['title', 'name', 'العنوان']
            ) if x else False)
            
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            # التحقق من وجود البيانات الأساسية
            if not price or not area:
                return None
            
            # تنظيف المنطقة
            district = self._clean_district(district, city)
            
            return {
                'العقار': title if title else f"{property_type} في {city}",
                'المدينة': city,
                'المنطقة': district,
                'نوع_العقار': property_type,
                'السعر': price,
                'المساحة': area,
                'سعر_المتر': round(price / area) if area > 0 else 0,
                'المصدر': 'Aqar.fm',
                'تاريخ_الجلب': datetime.now().strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            logging.warning(f"خطأ في تحليل عقار Aqar: {e}")
            return None
    
    def scrape_bayut(self, city, property_type):
        """
        جمع البيانات من Bayut.sa
        المصدر: https://www.bayut.sa/
        """
        properties = []
        
        city_map = {
            'الرياض': 'riyadh',
            'جدة': 'jeddah',
            'الدمام': 'dammam',
            'مكة': 'makkah',
            'المدينة': 'madinah',
            'الخبر': 'khobar'
        }
        
        prop_map = {
            'شقة': 'apartments',
            'فيلا': 'villas',
            'أرض': 'land',
            'مكتب': 'offices',
            'محل': 'shops'
        }
        
        city_en = city_map.get(city, city.lower())
        prop_en = prop_map.get(property_type, property_type.lower())
        
        # Bayut تستخدم ترقيم صفحات مختلف
        for page in range(1, 4):
            try:
                url = f"https://www.bayut.sa/en/search/{city_en}/{prop_en}/?page={page}"
                logging.info(f"جاري جمع البيانات من Bayut: {url}")
                
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # البحث عن بطاقات العقارات في Bayut
                listings = soup.find_all(['article', 'div'], class_=lambda x: x and any(
                    cls in str(x).lower() for cls in ['ca2f5674', 'property-card', 'listing-card']
                ) if x else False)
                
                for listing in listings:
                    property_data = self._parse_bayut_listing(listing, city, property_type)
                    if property_data and self._validate_property_data(property_data):
                        properties.append(property_data)
                
                time.sleep(2)
                
            except requests.exceptions.RequestException as e:
                logging.error(f"خطأ في الاتصال بـ Bayut: {e}")
                continue
            except Exception as e:
                logging.error(f"خطأ غير متوقع في Bayut: {e}")
                continue
        
        return properties
    
    def _parse_bayut_listing(self, listing, city, property_type):
        """تحليل بيانات العقار الواحد من Bayut"""
        try:
            # استخراج السعر
            price_elem = listing.find(['span', 'div'], class_=lambda x: x and any(
                cls in str(x).lower() for cls in ['_105b8a67', 'price']
            ) if x else False)
            
            price_text = price_elem.get_text(strip=True) if price_elem else ""
            price = self._extract_price(price_text)
            
            # استخراج المساحة
            area_elem = listing.find(['span', 'div'], class_=lambda x: x and any(
                cls in str(x).lower() for cls in ['_1f0f1758', 'area']
            ) if x else False)
            
            area_text = area_elem.get_text(strip=True) if area_elem else ""
            area = self._extract_area(area_text)
            
            # استخراج الموقع
            location_elem = listing.find(['div', 'span'], class_=lambda x: x and any(
                cls in str(x).lower() for cls in ['_812aa185', 'location']
            ) if x else False)
            
            location_text = location_elem.get_text(strip=True) if location_elem else ""
            
            # استخراج العنوان
            title_elem = listing.find(['h2', 'h3'], class_=lambda x: x and any(
                cls in str(x).lower() for cls in ['_7c8e3d9a', 'title']
            ) if x else False)
            
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            if not price or not area:
                return None
            
            # استخراج الحي من النص الكامل للموقع
            district = self._extract_district_from_text(location_text, city)
            
            return {
                'العقار': title if title else f"{property_type} في {city}",
                'المدينة': city,
                'المنطقة': district,
                'نوع_العقار': property_type,
                'السعر': price,
                'المساحة': area,
                'سعر_المتر': round(price / area) if area > 0 else 0,
                'المصدر': 'Bayut.sa',
                'تاريخ_الجلب': datetime.now().strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            logging.warning(f"خطأ في تحليل عقار Bayut: {e}")
            return None
    
    def _extract_price(self, price_text):
        """استخراج السعر من النص - نسخة محسنة تجمع كل الأرقام"""
        try:
            if not price_text:
                return None
            
            # إزالة الفواصل
            cleaned = price_text.replace(',', '')
            
            # التعامل مع صيغة المليون
            if 'مليون' in cleaned or 'million' in cleaned.lower():
                # استخراج الرقم العشري
                match = re.search(r'(\d+(?:\.\d+)?)', cleaned)
                if match:
                    price = float(match.group(1))
                    if price < 100:  # إذا كان أقل من 100 فهو بالمليون
                        return int(price * 1000000)
                    return int(price)
            else:
                # استخراج كل الأرقام المتتالية
                numbers = re.findall(r'\d+', cleaned)
                if numbers:
                    # جمع كل الأرقام معاً (مثلاً: 1 200 000 -> 1200000)
                    full_number = ''.join(numbers)
                    return int(full_number)
            
            return None
            
        except Exception as e:
            logging.warning(f"خطأ في استخراج السعر من '{price_text}': {e}")
            return None
    
    def _extract_area(self, area_text):
        """استخراج المساحة من النص"""
        try:
            if not area_text:
                return None
            
            numbers = re.findall(r'\d+', area_text)
            return int(numbers[0]) if numbers else None
            
        except Exception as e:
            logging.warning(f"خطأ في استخراج المساحة من '{area_text}': {e}")
            return None
    
    def _extract_district_from_text(self, text, city):
        """استخراج اسم الحي من النص"""
        try:
            if not text:
                return city
            
            # قائمة الأحياء المعروفة لكل مدينة
            districts_map = {
                'الرياض': ['النخيل', 'الملز', 'العليا', 'المرسلات', 'الغدير', 'الربوة', 'المروج', 'الوشام', 'السفارات', 'حي الملقا'],
                'جدة': ['الروضة', 'الزهراء', 'الشاطئ', 'النسيم', 'الفيصلية', 'السلام', 'الخالدية', 'الرحاب', 'الحمراء', 'المنار'],
                'الدمام': ['الحمراء', 'الشاطئ', 'الريان', 'الثقبة', 'الفيصلية', 'النهضة', 'المركز', 'الفلاح', 'الخالدية', 'الجامعيين']
            }
            
            # البحث عن اسم حي معروف في النص
            known_districts = districts_map.get(city, [])
            for district in known_districts:
                if district in text:
                    return district
            
            # إذا لم نجد حياً معروفاً، نرجع أول جزء من النص
            parts = text.split('،')
            if parts:
                return parts[0].strip()
            
            return city
            
        except Exception:
            return city
    
    def _clean_district(self, district_text, city):
        """تنظيف اسم المنطقة"""
        try:
            if not district_text:
                return city
            
            # إزالة الكلمات الزائدة
            district_text = re.sub(r'[،,].*$', '', district_text)
            district_text = district_text.strip()
            
            # إذا كان النص طويلاً جداً، نرجع المدينة
            if len(district_text) > 50:
                return city
            
            return district_text
            
        except Exception:
            return city
    
    def _validate_property_data(self, data):
        """
        التحقق من صحة البيانات
        سياسة صارمة: نطاقات واقعية للعقار السعودي
        """
        try:
            # التحقق من وجود كل الحقول
            required_fields = ['العقار', 'المدينة', 'المنطقة', 'نوع_العقار', 'السعر', 'المساحة']
            if not all(field in data for field in required_fields):
                return False
            
            # التحقق من القيم
            price = data['السعر']
            area = data['المساحة']
            
            # نطاقات منطقية للعقار السعودي
            if price < 50000 or price > 100000000:  # أقل من 50 ألف أو أكثر من 100 مليون
                return False
            
            if area < 10 or area > 10000:  # أقل من 10 متر أو أكثر من 10,000 متر
                return False
            
            return True
            
        except Exception:
            return False


# ==============================================
# الدالة الوحيدة المسموح باستدعائها من الخارج
# ==============================================

def get_market_data(city, property_type):
    """
    الدالة الرئيسية - المصدر الوحيد للبيانات الحقيقية
    سياسة صارمة: REAL DATA ONLY - لا random, لا fallback, لا simulation
    
    سياسة الفشل: مصدر واحد يكفي للنجاح
    - ✅ لو Aqar فشل لكن Bayut نجح → نكمل
    - ✅ لو Bayut فشل لكن Aqar نجح → نكمل
    - ❌ فقط لو فشل المصدران معاً → نرمي Exception
    
    سياسة إزالة التكرار: نعتبر العقار واحداً بغض النظر عن المصدر
    - ✅ نستخدم (السعر + المساحة + المنطقة) فقط
    - ❌ لا نستخدم المصدر في المقارنة
    
    المدخلات:
        city: المدينة (مثال: 'الرياض')
        property_type: نوع العقار (مثال: 'شقة')
    
    المخرجات:
        DataFrame بالبيانات الحقيقية
    
    في حالة فشل المصدرين: Exception واضح
    """
    
    logging.info(f"🔍 بدء جمع البيانات الحقيقية: {city} - {property_type}")
    
    # إنشاء كائن الجامع
    scraper = MarketDataScraper()
    
    # جمع البيانات من المصدرين
    aqar_properties = scraper.scrape_aqar(city, property_type)
    bayut_properties = scraper.scrape_bayut(city, property_type)
    
    # دمج البيانات
    all_properties = aqar_properties + bayut_properties
    
    # التحقق من وجود بيانات - سياسة "مصدر واحد يكفي"
    if not all_properties:
        error_msg = f"❌ فشل جمع البيانات الحقيقية لـ {city} - {property_type} من جميع المصادر"
        logging.error(error_msg)
        raise Exception(error_msg)
    
    # إنشاء DataFrame
    df = pd.DataFrame(all_properties)
    
    # ✅ إزالة التكرارات بناءً على العقار نفسه (بدون النظر للمصدر)
    df = df.drop_duplicates(subset=['السعر', 'المساحة', 'المنطقة'])
    
    logging.info(f"✅ تم جمع {len(df)} عقار حقيقي من السوق")
    logging.info(f"📊 المصادر: Aqar: {len(aqar_properties)} | Bayut: {len(bayut_properties)}")
    
    # توحيد الأعمدة – معيار المنصة
    df = df.rename(columns={
        "المنطقة": "الحي",
        "السعر": "price",
        "المساحة": "area"
    })
    
    # استخدام وقت الجلب الفعلي لجميع العقارات (لتنبيهات الزمن بدقة)
    df["date"] = pd.to_datetime(datetime.now())
    
    # إضافة حقول ثابتة لضمان اكتمال البيانات
    df["المدينة"] = city
    df["نوع_العقار"] = property_type
    
    return df.reset_index(drop=True)


# ==============================================
# اختبار ذاتي - يمكن تشغيله للتحقق
# ==============================================

if __name__ == "__main__":
    print("🧪 اختبار جمع البيانات الحقيقية...")
    print("=" * 50)
    
    try:
        # اختبار بسيط - الرياض + شقة
        test_data = get_market_data("الرياض", "شقة")
        print(f"✅ نجح الاختبار - تم جمع {len(test_data)} عقار")
        print("\n📊 نموذج من البيانات (بالتنسيق النهائي للمنصة):")
        print(test_data[['المدينة', 'الحي', 'price', 'area', 'date', 'نوع_العقار']].head(5))
        
    except Exception as e:
        print(f"❌ فشل الاختبار: {e}")
        print("\n⚠️ هذا متوقع إذا كان الموقع محجوباً أو لا توجد بيانات")
        print("لكن المهم: لا يوجد random ولا fallback")
