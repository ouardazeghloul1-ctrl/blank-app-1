# run_scraper_job.py
import os
from data_scraper import RealEstateScraper
from datetime import datetime

def run_and_save(city="الرياض", property_type="شقة", num=100):
    scraper = RealEstateScraper()
    df = scraper.get_real_data(city, property_type, num)
    os.makedirs("data", exist_ok=True)
    filename = f"data/real_estate_data_{city}_{property_type}.csv"
    df.to_csv(filename, index=False)
    with open("data/last_update.txt", "w", encoding="utf-8") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Saved:", filename)

if __name__ == "__main__":
    run_and_save()
