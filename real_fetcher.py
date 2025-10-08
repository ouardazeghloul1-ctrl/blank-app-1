import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

# ✅ محاكاة جلب بيانات واقعية من مواقع مثل Aqar وBayut
def get_real_data(city):
    print(f"جاري جلب البيانات من المواقع للعقار في {city}...")

    # قائمة بيانات تجريبية (تحاكي ما يتم استخراجه من المواقع)
    simulated_data = []
    for i in range(50):
        price = random.randint(100000, 2000000)
        area = random.randint(50, 500)
        rooms = random.randint(1, 6)
        simulated_data.append({
            "City": city,
            "Price": price,
            "Area(m²)": area,
            "Rooms": rooms,
            "Source": random.choice(["Aqar", "Bayut"])
        })
        time.sleep(0.1)

    df = pd.DataFrame(simulated_data)
    return df
