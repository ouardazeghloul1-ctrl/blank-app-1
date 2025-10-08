import requests
from bs4 import BeautifulSoup
import json

def fetch_real_estate_data(city, property_type, goal):
    """
    كود تجريبي مبدئي لجلب بيانات عقارية من موقع عقار.كوم.
    """
    try:
        url = f"https://sa.aqar.fm/{city}"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.find_all("div", {"class": "sc-bdnylx-0"})

        results = []
        for item in listings[:10]:  # نأخذ فقط أول 10 نتائج للتجريب
            title = item.text.strip()[:100]
            results.append({
                "title": title or "إعلان بدون عنوان",
                "description": "تم جمع هذا الإعلان تجريبياً من موقع عقار.",
                "location": city,
                "price": "غير محدد"
            })

        with open("outputs/results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        return results

    except Exception as e:
        print(f"❌ خطأ أثناء جلب البيانات: {e}")
        return []
