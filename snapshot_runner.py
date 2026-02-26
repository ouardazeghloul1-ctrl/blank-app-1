import pandas as pd
from government_data_provider import load_government_data
from market_memory import store_snapshot

def collect_and_store(city, property_type):

    df = load_government_data(
        selected_city=city,
        selected_property_type=property_type
    )

    if df is None or df.empty:
        print(f"⚠️ لا توجد بيانات لـ {city} - {property_type}")
        return df

    # ❌ لا نضيف __snapshot_time__ هنا
    # المسؤولية بالكامل داخل market_memory

    store_snapshot(df, city, property_type)

    print(f"✅ تم حفظ لقطة سوق جديدة: {city} - {property_type}")

    return df
