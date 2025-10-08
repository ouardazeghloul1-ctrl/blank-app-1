import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

# ✅ جلب بيانات عقارية تجريبية (تحاكي مواقع مثل Aqar وBayut)
def fetch_real_data(city):
    print(f"🔍 جاري جلب البيانات من المواقع للعقار في {city}...")

    # قائمة بيانات تجريبية تمثل نتائج المواقع العقارية
    simulated_data = []
    for i in range(50):
        price = random.randint(100000, 2000000)  # السعر
        area = random.randint(50, 500)  # المساحة
        rooms = random.randint(1, 6)  # عدد الغرف

        simulated_data.append({
            "City": city,
            "Price": price,
            "Area(m²)": area,
            "Rooms": rooms,
            "Source": random.choice(["Aqar", "Bayut"])
        })

        time.sleep(0.05)  # تأخير بسيط لمحاكاة تحميل المواقع

    # تحويل القائمة إلى جدول DataFrame
    df = pd.DataFrame(simulated_data)
    return df
