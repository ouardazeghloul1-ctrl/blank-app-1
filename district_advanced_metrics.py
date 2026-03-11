# =========================================
# Warda Intelligence
# Advanced District Metrics Engine
# =========================================

import pandas as pd


def compute_advanced_metrics(df, city, district):

    city_df = df[df["city"] == city]
    district_df = city_df[city_df["district"] == district]

    if district_df.empty:
        return {}

    metrics = {}

    # ----------------------------------
    # حجم السوق
    # ----------------------------------

    metrics["market_value"] = district_df["price"].sum()

    # ----------------------------------
    # متوسط قيمة الصفقة
    # ----------------------------------

    metrics["avg_transaction_value"] = district_df["price"].mean()

    # ----------------------------------
    # متوسط المساحة
    # ----------------------------------

    metrics["avg_area"] = district_df["area"].mean()

    # ----------------------------------
    # أقل سعر متر
    # ----------------------------------

    metrics["min_price_sqm"] = district_df["price_per_sqm"].min()

    # ----------------------------------
    # أعلى سعر متر
    # ----------------------------------

    metrics["max_price_sqm"] = district_df["price_per_sqm"].max()

    # ----------------------------------
    # كثافة السوق
    # ----------------------------------

    months = (
        district_df["transaction_date"].max() -
        district_df["transaction_date"].min()
    ).days / 30

    if months == 0:
        metrics["transactions_per_month"] = len(district_df)
    else:
        metrics["transactions_per_month"] = len(district_df) / months

    return metrics
