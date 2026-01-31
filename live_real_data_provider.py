# live_real_data_provider.py
# =========================================
# مزود البيانات الحية – Warda Intelligence
# المصدر المباشر للبيانات العقارية
# =========================================

import pandas as pd
from datetime import datetime

from realfetcher import fetch_data


def get_live_real_data(city: str, property_type: str, district: str = "") -> pd.DataFrame:
    """
    يجلب بيانات حقيقية وحية مباشرة من السوق.
    في حال الفشل، يعتمد على fallback داخلي ذكي.
    """

    try:
        df = fetch_data(
            city=city,
            district=district or "",
            property_type=property_type
        )

        if df is None or df.empty:
            raise ValueError("لا توجد بيانات حية متاحة")

        # إضافة ختم زمني واضح
        df["تاريخ_التقرير"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        return df.reset_index(drop=True)

    except Exception as e:
        # فشل آمن — لا نكسر التقرير
        print(f"⚠️ تعذر جلب البيانات الحية: {e}")

        return pd.DataFrame({
            "السعر": [],
            "المساحة": [],
            "المدينة": [],
            "نوع_العقار": [],
            "مصدر_البيانات": ["fallback"],
            "تاريخ_التقرير": [datetime.now().strftime("%Y-%m-%d %H:%M")]
        })
