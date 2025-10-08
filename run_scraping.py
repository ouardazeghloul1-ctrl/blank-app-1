from scraper_engine import WardaScraper
from data_cleaner import DataCleaner
from config import CITIES, PROPERTY_TYPES
import pandas as pd
import logging
import os

# إنشاء المجلدات إذا لم تكن موجودة
os.makedirs('outputs', exist_ok=True)
os.makedirs('logs', exist_ok=True)

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraping.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def main():
    print("🚀 بدء جمع البيانات العقارية لـ Warda Realty...")
    print("=" * 60)
    
    scraper = WardaScraper()
    total_properties = 0
    
    # جمع البيانات من جميع المدن وأنواع العقارات
    for city in CITIES:
        city_properties = 0
        print(f"\n🏙️  جاري جمع بيانات: {city}")
        print("-" * 40)
        
        for prop_type in PROPERTY_TYPES:
            print(f"📊 نوع العقار: {prop_type}")
            
            # جمع من Aqar
            aqar_success = scraper.scrape_aqar(city, prop_type)
            aqar_count = len([d for d in scraper.data if d['Source'] == 'Aqar.fm' and d['City'] == city and d['Property_Type'] == prop_type])
            
            # جمع من Bayut
            bayut_success = scraper.scrape_bayut(city, prop_type)
            bayut_count = len([d for d in scraper.data if d['Source'] == 'Bayut.sa' and d['City'] == city and d['Property_Type'] == prop_type])
            
            city_properties += (aqar_count + bayut_count)
            print(f"   ✅ Aqar: {aqar_count} عقار | Bayut: {bayut_count} عقار")
        
        total_properties += city_properties
        print(f"📈 إجمالي عقارات {city}: {city_properties}")
    
    if scraper.data:
        # تنظيف البيانات
        df = pd.DataFrame(scraper.data)
        cleaner = DataCleaner(df)
        cleaned_df = cleaner.clean_data()
        
        # حفظ البيانات
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M')
        output_file = f"outputs/warda_realty_data_{timestamp}.csv"
        cleaned_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print("\n" + "=" * 60)
        print(f"✅ تم جمع {len(cleaned_df)} عقار بنجاح!")
        print(f"📁 الملف المحفوظ: {output_file}")
        
        # عرض إحصائيات سريعة
        print("\n📊 إحصائيات البيانات المجمعة:")
        print(f"🏙️  المدن: {', '.join(cleaned_df['City'].unique())}")
        print(f"🏠 أنواع العقارات: {', '.join(cleaned_df['Property_Type'].unique())}")
        print(f"💰 نطاق الأسعار: {cleaned_df['Price'].min():,} - {cleaned_df['Price'].max():,} ريال")
        print(f"📐 نطاق المساحات: {cleaned_df['Area'].min()} - {cleaned_df['Area'].max()} م²")
        print(f"🌐 المصادر: {', '.join(cleaned_df['Source'].unique())}")
        
        return output_file
        
    else:
        print("❌ لم يتم جمع أي بيانات - تحقق من الاتصال بالإنترنت أو هيكل المواقع")
        return None

if __name__ == "__main__":
    main()
