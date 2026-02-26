# snapshot_runner.py
# =========================================
# Snapshot Runner – الجسر بين بيانات الوزارة والتنبيهات
# =========================================

import pandas as pd
from government_data_provider import load_government_data
from market_memory import store_snapshot

def collect_and_store(city, property_type):
    """
    1️⃣ يجلب البيانات من ملف وزارة العدل
    2️⃣ يضيف وقت اللقطة
    3️⃣ يخزنها في Market Memory
    4️⃣ يرجع DataFrame للاستخدام الفوري
    """

    # جلب البيانات من المصدر الحكومي
    df = load_government_data(
        selected_city=city,
        selected_property_type=property_type
    )

    if df is None or df.empty:
        print(f"⚠️ لا توجد بيانات لـ {city} - {property_type}")
        return df

    # إضافة وقت اللقطة (ضروري للمقارنة الزمنية)
    df["__snapshot_time__"] = pd.Timestamp.now()

    # تخزين اللقطة
    store_snapshot(df, city, property_type)

    print(f"✅ تم حفظ لقطة سوق جديدة: {city} - {property_type}")

    return df
