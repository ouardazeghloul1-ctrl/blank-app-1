# realfetcher.py
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) WardaFetcher/1.0"
}

# خريطة روابط أساسية (نتعامل مع صفحات نتائج عامة؛ إن فشلنا في استخراج بعض الصفحات فذلك لسبب تحميل جافاسكربت)
URL_MAP = {
    "الرياض": [
        "https://www.bayut.sa/للبيع/العقارات/الرياض/",
        "https://sa.aqar.fm/شقق-للبيع/الرياض",
        "https://www.propertyfinder.sa/ar/search?l=4&c=1&t=1&fu=0&ob=mr",
        "https://haraj.com.sa/tags/الرياض_شقق%20للبيع"
    ],
    "جدة": [
        "https://www.bayut.sa/للبيع/العقارات/جدة/",
        "https://sa.aqar.fm/شقق-للبيع/جدة",
        "https://www.propertyfinder.sa/ar/search?l=2658&c=1&t=1&fu=0&ob=mr",
        "https://haraj.com.sa/tags/جده_شقق%20للبيع"
    ],
    "الدمام": [
        "https://www.bayut.sa/للبيع/العقارات/الدمام/",
        "https://sa.aqar.fm/شقق-للبيع/الدمام",
        "https://www.propertyfinder.sa/ar/search?l=3278&c=1&t=1&fu=0&ob=mr",
        "https://haraj.com.sa/tags/الدمام_شقق%20للبيع"
    ]
}

def _clean_num(s):
    if not s: 
        return None
    s = re.sub(r'[^\d]', '', s)
    try:
        return int(s)
    except:
        return None

def _extract_prices_from_text(text):
    # يبحث عن أرقام تبدو كأسعار (≥ 10,000)
    nums = re.findall(r'\d{4,9}', text.replace(',', '').replace('٬',''))
    out = []
    for n in nums:
        val = _clean_num(n)
        if val and 10000 <= val <= 200000000:
            out.append(val)
    return out

def fetch_from_url(url, limit=200):
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
    except Exception as e:
        # فشل الاتصال
        return []
    if r.status_code != 200:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    text = soup.get_text(separator=" ", strip=True)
    prices = _extract_prices_from_text(text)
    # بعض الصفحات تحتوي بيانات ضمن سكربتات JSON — نجرب البحث داخل سكربتات ايضا
    if len(prices) < 8:
        scripts = soup.find_all("script")
        for sc in scripts:
            try:
                st = sc.string or ""
                if st:
                    p2 = _extract_prices_from_text(st)
                    prices += p2
            except:
                continue
    # تقليل الضوضاء
    prices = [p for p in prices if 10000 <= p <= 200000000]
    prices = prices[:limit]
    return prices

def fetch_properties(city: str, mode: str = "quick"):
    """
    city: 'الرياض'|'جدة'|'الدمام'
    mode: 'quick' (سريع) أو 'deep' (دقيق)
    يعيد DataFrame مع عمود price وsource وsample_url (قد تكون None)
    """
    city = city.strip()
    urls = URL_MAP.get(city, [])
    all_records = []
    all_prices = []

    for idx, url in enumerate(urls):
        # كل رابط نأخذ منه عينات
        pages_to_try = 1 if mode == "quick" else 2  # في الوضع العميق نجرب أكثر
        for p in range(pages_to_try):
            u = url
            if p > 0:
                # بعض المواقع تستخدم ?page=
                if "?" in u:
                    u = f"{u}&page={p+1}"
                else:
                    u = f"{u}?page={p+1}"
            try:
                prices = fetch_from_url(u, limit=300 if mode == "deep" else 100)
                # نحول الأسعار إلى سجلات
                for pr in prices:
                    all_prices.append(pr)
                    all_records.append({
                        "title": None,
                        "price": pr,
                        "location": city,
                        "url": u,
                        "source": u.split("/")[2] if "//" in u else u
                    })
            except Exception as e:
                continue
            # تأخير بسيط للدخول بلطف على المواقع
            time.sleep(0.6 + random.random()*0.6)

    if not all_prices:
        return pd.DataFrame()  # فشل جلب أي بيانات

    # فلترة وإزالة الشواذ بناءً على z-score بسيط
    prices = all_prices.copy()
    mean = sum(prices)/len(prices)
    std = (sum((x-mean)**2 for x in prices)/len(prices))**0.5 if len(prices)>1 else 0
    if std > 0:
        filtered_prices = [p for p in prices if abs(p-mean) <= 3*std]
    else:
        filtered_prices = prices

    # إذا الوضع السريع نقلل العيّنة
    if mode == "quick":
        sample_prices = filtered_prices[:min(len(filtered_prices), 80)]
        records_sample = [r for r in all_records if r["price"] in sample_prices][:len(sample_prices)]
    else:
        sample_prices = filtered_prices
        records_sample = all_records

    # إنشاء DataFrame نهائي
    df = pd.DataFrame(records_sample)
    # ضمان وجود عمود price كعدد صحيح
    df = df.dropna(subset=["price"])
    df["price"] = df["price"].astype(int)
    df = df.sort_values("price").reset_index(drop=True)
    return df
