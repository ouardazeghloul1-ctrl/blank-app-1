import pandas as pd


def compute_advanced_metrics(df, city, district):

    df = df.copy()

    # تأكد من وجود سعر المتر
    if "price_per_sqm" not in df.columns:
        df["price_per_sqm"] = df["price"] / df["area"]

    city_df = df[df["city"] == city]
    district_df = city_df[city_df["district"] == district]

    if district_df.empty:
        return {}

    metrics = {}

    # حجم السوق
    metrics["market_value"] = district_df["price"].sum()

    # متوسط قيمة الصفقة
    metrics["avg_transaction_value"] = district_df["price"].mean()

    # متوسط المساحة
    metrics["avg_area"] = district_df["area"].mean()

    # أقل سعر متر
    metrics["min_price_sqm"] = district_df["price_per_sqm"].min()

    # أعلى سعر متر
    metrics["max_price_sqm"] = district_df["price_per_sqm"].max()

    # كثافة السوق
    if "transaction_date" in district_df.columns:

        months = (
            district_df["transaction_date"].max() -
            district_df["transaction_date"].min()
        ).days / 30

        months = max(months, 1)

        metrics["transactions_per_month"] = len(district_df) / months

    else:
        metrics["transactions_per_month"] = None

    return metrics
