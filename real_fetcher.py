import requests
import pandas as pd

def جلب_الأسعار_الحقيقية():
    """
    يحاول جلب بيانات حديثة من مصدر مفتوح، وإن فشل يعيد None
    """
    try:
        # مثال تجريبي لمصدر بيانات عقارية مفتوحة (يمكن تغييره لاحقًا)
        url = "https://raw.githubusercontent.com/datasets/house-prices-us/master/data.csv"
        df = pd.read_csv(url)
        
        # تنظيف وتبسيط البيانات
        df = df[['City', 'State', 'MedianListingPrice']].dropna().head(20)
        return df
    except Exception as e:
        print("خطأ أثناء جلب البيانات:", e)
        return None
