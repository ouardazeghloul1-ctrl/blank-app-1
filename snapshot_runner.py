# snapshot_runner.py
# =========================================
# Snapshot Runner – الجسر بين البيانات الحية والتنبيهات
# =========================================

from market_data_core import get_market_data
from market_memory import store_snapshot

def collect_and_store(city, property_type):
    """
    1️⃣ يجلب البيانات الحقيقية من السوق
    2️⃣ يخزنها كلقطة سوق زمنية
    3️⃣ يرجع DataFrame للاستخدام الفوري
    """
    df = get_market_data(city, property_type)
    store_snapshot(df, city, property_type)
    return df
