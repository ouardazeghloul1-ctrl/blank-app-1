import requests
from bs4 import BeautifulSoup
import random

def fetch_real_data(city, property_type):
    """
    🏙️ تجلب بيانات العقارات من مواقع مختلفة (تجريبية)
    """
    urls = [
        f"https://sa.aqar.fm/{city}",
        f"https://www.bayut.sa/{city}",
        f"https://haraj.com.sa/{city}",
        f"https://www.propertyfinder.sa/ar/buy/{city}",
        f"https://www.zillow.com/{city}-real-estate/"
    ]
    
    prices = []
    
    for url in urls:
        try:
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                text = soup.get_text()
                numbers = [int(n.replace(',', '')) for n in text.split() if n.replace(',', '').isdigit()]
                # فلترة الأسعار الواقعية
                prices += [n for n in numbers if 100000 < n < 10000000]
        except Exception as e:
            print("⚠️ فشل الجلب من:", url, "| الخطأ:", e)

    if len(prices) < 10:
        return None  # نرجع None إذا فشل الجلب
    
    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)

    return {
        "متوسط_السعر": round(avg_price, 2),
        "نطاق_السعر": [min_price, max_price],
        "عدد_النتائج": len(prices),
    }
