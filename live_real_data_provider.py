# live_real_data_provider.py
# =========================================
# مزود البيانات الحية – Warda Intelligence
# المصدر المباشر للبيانات العقارية
# =========================================

import pandas as pd
from datetime import datetime
import os

from realfetcher import fetch_data
from market_memory import store_snapshot

def get_live_real_data(city: str, property_type: str, district: str = "") -> pd.DataFrame:
    """
    يجلب بيانات حقيقية وحية مباشرة من السوق.
    في حال الفشل، يعتمد على fallback داخلي ذكي.
    """

    try:
        # 1. جلب البيانات
        df = fetch_data(
            city=city,
            district=district or "",
            property_type=property_type
        )
        
        # 2. التحقق من صحة البيانات أولاً ⬅️ قبل الحفظ
        if df is None or df.empty:
            raise ValueError("⚠️ لا توجد بيانات حية متاحة (DataFrame فارغ)")
        
        # 3. إضافة مصدر البيانات (للتمييز مستقبلاً)
        df["_snapshot_source"] = "live_fetch"
        
        # 4. الآن فقط نقوم بالحفظ بعد التأكد من وجود بيانات
        saved_path = store_snapshot(df, city, property_type)
        
        # 5. طباعة مسار الحفظ لتعرفي أين تبحثين
        if saved_path:
            print(f"📁 تم حفظ snapshot في: {saved_path}")
            # التأكد من وجود المجلد
            folder_path = os.path.dirname(saved_path)
            if os.path.exists(folder_path):
                print(f"📂 مجلد market_memory موجود في: {folder_path}")
            else:
                print(f"⚠️ المجلد لم يُنشأ بعد: {folder_path}")
        else:
            print("⚠️ لم يتم حفظ snapshot (بيانات فارغة أو خطأ)")
        
        # 6. إضافة ختم زمني واضح للتقرير
        df["تاريخ_التقرير"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        return df.reset_index(drop=True)

    except Exception as e:
        # فشل آمن — لا نكسر التقرير
        print(f"⚠️ تعذر جلب البيانات الحية: {e}")
        
        # في حالة الفشل، نرجع DataFrame فارغ مع رسالة توضيحية
        return pd.DataFrame({
            "السعر": [],
            "المساحة": [],
            "المدينة": [],
            "نوع_العقار": [],
            "مصدر_البيانات": ["fallback"],
            "تاريخ_التقرير": [datetime.now().strftime("%Y-%m-%d %H:%M")],
            "رسالة_الخطأ": [str(e)]  # مفيد للتتبع
        })
