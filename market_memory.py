# market_memory.py
# =========================================
# Market Memory Layer – Warda Intelligence
# تخزين السوق ومقارنته زمنيًا
# =========================================
# ملاحظة معمارية:
# هذا الملف مخصص فقط لنظام التنبيهات (AlertEngine)
# لا يُستخدم في التقارير أو الخلاصة التنفيذية
# لا يُستدعى من orchestrator
# الذاكرة فقط - لا تحليل ولا قرار
# =========================================

import os
import pandas as pd
from datetime import datetime

MEMORY_FOLDER = "market_memory"
os.makedirs(MEMORY_FOLDER, exist_ok=True)


def _build_filename(city, property_type):
    date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
    return f"{city}_{property_type}_{date_str}.csv"


def store_snapshot(df: pd.DataFrame, city: str, property_type: str):
    """
    تخزين لقطة السوق مع ختم زمني داخلي
    """
    if df is None or df.empty:
        return None

    # 🔒 إضافة وقت اللقطة داخل البيانات نفسها
    snapshot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = df.copy()
    df["__snapshot_time__"] = snapshot_time

    filename = _build_filename(city, property_type)
    path = os.path.join(MEMORY_FOLDER, filename)

    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def load_last_snapshots(city: str, property_type: str, limit=2):
    """
    تحميل آخر لقطتين للسوق
    
    Args:
        city: اسم المدينة
        property_type: نوع العقار
        limit: عدد اللقطات المطلوبة (افتراضي: 2)
    
    Returns:
        list: قائمة بالـ DataFrames للقطات المطلوبة
    """
    files = [
        f for f in os.listdir(MEMORY_FOLDER)
        if f.startswith(f"{city}_{property_type}")
    ]

    # ترتيب حسب وقت التعديل (الأحدث أولاً) لضمان السلامة حتى لو تغير تنسيق الاسم
    files = sorted(
        files,
        key=lambda f: os.path.getmtime(os.path.join(MEMORY_FOLDER, f)),
        reverse=True
    )[:limit]

    snapshots = []
    for f in files:
        try:
            df = pd.read_csv(os.path.join(MEMORY_FOLDER, f))
            snapshots.append(df)
        except Exception as e:
            print(f"⚠️ خطأ في تحميل اللقطة {f}: {e}")
            continue

    return snapshots


# للاختبار المستقل (اختياري)
if __name__ == "__main__":
    # بيانات تجريبية للاختبار
    test_data = pd.DataFrame({
        "price": [500000, 750000, 1000000, 1250000, 1500000],
        "area": [80, 100, 120, 150, 180],
        "date": [datetime.now().strftime("%Y-%m-%d")] * 5
    })
    
    # تخزين لقطة اختبار
    path = store_snapshot(test_data, "الرياض", "شقة")
    print(f"✅ تم تخزين اللقطة في: {path}")
    
    # تحميل آخر لقطتين
    snapshots = load_last_snapshots("الرياض", "شقة", limit=2)
    print(f"📊 تم تحميل {len(snapshots)} لقطة")
