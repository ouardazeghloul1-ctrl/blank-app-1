# =========================================
# Warda Intelligence
# District Neighbor Finder
# استخراج الأحياء المشابهة أو المجاورة
# =========================================

import pandas as pd


def find_nearby_districts(df, city, district, n=4):
    """
    استخراج الأحياء الأقرب سعرياً داخل نفس المدينة
    """

    if df is None or df.empty:
        return []

    # فلترة المدينة
    city_df = df[df["city"] == city]

    if city_df.empty:
        return []

    # متوسط السعر لكل حي
    district_prices = (
        city_df.groupby("district")["price_per_sqm"]
        .mean()
        .reset_index()
    )

    # سعر الحي الحالي
    target_row = district_prices[district_prices["district"] == district]

    if target_row.empty:
        return []

    target_price = target_row.iloc[0]["price_per_sqm"]

    # حساب الفرق
    district_prices["price_diff"] = abs(
        district_prices["price_per_sqm"] - target_price
    )

    # ترتيب حسب الأقرب
    nearest = district_prices.sort_values("price_diff")

    # حذف الحي نفسه
    nearest = nearest[nearest["district"] != district]

    # أخذ أقرب أحياء
    nearest = nearest.head(n)

    results = []

    for _, row in nearest.iterrows():

        results.append(
            {
                "district_name": row["district"],
                "avg_price": round(row["price_per_sqm"], 2),
            }
        )

    return results
