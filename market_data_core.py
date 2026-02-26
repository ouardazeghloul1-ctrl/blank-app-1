# ==============================================
# market_data_core.py
# المصدر الوحيد للبيانات: ملف وزارة العدل
# ==============================================

import pandas as pd
from government_data_provider import load_government_data


def get_market_data(city=None, property_type=None):
    """
    الدالة الوحيدة لجلب بيانات السوق
    الآن تعتمد فقط على بيانات وزارة العدل
    """
    
    df = load_government_data(selected_city=city)

    if df.empty:
        raise Exception(f"❌ لا توجد بيانات متاحة لـ {city}")

    # توحيد الأعمدة لتتوافق مع بقية المنصة
    df = df.rename(columns={
        "السعر": "price",
        "المساحة": "area"
    })

    # تأكد من وجود الحقول الأساسية
    if "price" not in df.columns:
        df["price"] = 0

    if "area" not in df.columns:
        df["area"] = 0

    return df.reset_index(drop=True)
