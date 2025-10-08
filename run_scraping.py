import os
import logging
from realfetcher import fetch_data

# ✅ إنشاء المجلدات الناقصة تلقائياً
for folder in ["outputs", "logs", "models", "assets"]:
    os.makedirs(folder, exist_ok=True)

# ✅ التأكد من وجود ملف السجل حتى لا يفشل logging
log_file = os.path.join("logs", "scraping.log")
if not os.path.exists(log_file):
    open(log_file, "a", encoding="utf-8").close()

# ✅ إعداد التسجيل (logging)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def run_scraper(city, district="", property_type="Apartment"):
    """
    يقوم بجلب البيانات الحقيقية من الإنترنت ويخزنها في مجلد outputs.
    """
    try:
        logging.info(f"Starting scraping for {city}, {district}, {property_type}")
        df = fetch_data(city=city, district=district, property_type=property_type)

        if df is None or df.empty:
            logging.warning("No data fetched.")
            return None

        # ✅ حفظ البيانات في ملف CSV داخل مجلد outputs
        csv_path = os.path.join("outputs", f"{city}_{property_type}.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        logging.info(f"Data saved to {csv_path}")
        return df

    except Exception as e:
        logging.error(f"Error in run_scraper: {str(e)}")
        return None
