# =========================================
# Warda Intelligence
# District Metrics Engine
# المرحلة 1: تجهيز البيانات
# =========================================

import pandas as pd


def prepare_district_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    تجهيز بيانات الصفقات العقارية للأحياء
    """

    df = df.copy()

    # حساب سعر المتر
    df["price_per_sqm"] = df["price"] / df["area"]

    # تحويل التاريخ
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    return df


def calculate_basic_district_metrics(df: pd.DataFrame, city_name: str, district_name: str):
    """
    حساب المؤشرات الأساسية لحي معين
    """

    # بيانات المدينة
    city_df = df[df["city"] == city_name]

    # بيانات الحي
    district_df = city_df[city_df["district"] == district_name]

    # متوسط سعر المتر في المدينة
    city_avg_price = city_df["price_per_sqm"].mean()

    # متوسط سعر المتر في الحي
    district_avg_price = district_df["price_per_sqm"].mean()

    # عدد الصفقات
    transactions_count = len(district_df)

    # الانحراف عن متوسط المدينة
    deviation = ((district_avg_price - city_avg_price) / city_avg_price) * 100

    return {
        "district_name": district_name,
        "city_name": city_name,
        "district_avg_price": round(district_avg_price, 2),
        "city_avg_price": round(city_avg_price, 2),
        "transactions_count": transactions_count,
        "price_deviation_percent": round(deviation, 2)
    }


def calculate_dpi_score(metrics: dict):
    """
    حساب مؤشر قوة الحي DPI
    """

    deviation = abs(metrics["price_deviation_percent"])
    transactions = metrics["transactions_count"]

    # استقرار السعر
    stability_score = max(0, 100 - deviation * 2)

    # قوة الطلب
    demand_score = min(100, transactions * 2)

    # السيولة
    liquidity_score = min(100, transactions * 1.5)

    # حساب المؤشر النهائي
    dpi = (
        0.30 * stability_score +
        0.40 * demand_score +
        0.30 * liquidity_score
    )

    return round(dpi, 2)
