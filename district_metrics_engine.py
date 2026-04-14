# =========================================
# Warda Intelligence
# District Metrics Engine
# المرحلة 1: تجهيز البيانات
# =========================================

import pandas as pd
import numpy as np
import logging

# ---------------------------------
# إعداد نظام التسجيل (logging)
# ---------------------------------
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------------
# حدود فلترة القيم غير الواقعية (قابلة للتعديل حسب نوع العقار)
# ---------------------------------
MIN_PRICE_PER_SQM = 500
MAX_PRICE_PER_SQM = 20000


def prepare_district_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    تجهيز بيانات الصفقات العقارية للأحياء
    """

    df = df.copy()

    # التأكد من الأعمدة الأساسية
    required_columns = ["price", "area"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"العمود {col} غير موجود في البيانات")

    # منع القسمة على صفر
    df["area"] = pd.to_numeric(df["area"], errors="coerce")
    df.loc[df["area"] <= 0, "area"] = np.nan

    # حساب سعر المتر
    df["price_per_sqm"] = df["price"] / df["area"]

    # إزالة القيم غير الصالحة
    df = df[df["price_per_sqm"].notna()]

    # تحويل التاريخ إذا وجد
    if "transaction_date" in df.columns:
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

    return df


def calculate_basic_district_metrics(df: pd.DataFrame, city_name: str, district_name: str):
    """
    حساب المؤشرات الأساسية لحي معين
    """

    if df.empty:
        logging.warning("Input dataframe is empty")
        return None

    # بيانات المدينة
    city_df = df[df["city"] == city_name]

    if city_df.empty:
        logging.warning(f"No data found for city {city_name}")
        return None

    # بيانات الحي (غير مفلترة - للحصول على العدد الإجمالي للصفقات)
    total_transactions = len(city_df[city_df["district"] == district_name])

    # بيانات الحي (المستخدمة في التحليل)
    district_df = city_df[city_df["district"] == district_name]

    # ---------------------------------
    # فلترة القيم غير الواقعية لسعر المتر
    # ---------------------------------
    district_df = district_df[
        (district_df["price_per_sqm"] >= MIN_PRICE_PER_SQM) & 
        (district_df["price_per_sqm"] <= MAX_PRICE_PER_SQM)
    ]
    
    city_clean = city_df[
        (city_df["price_per_sqm"] >= MIN_PRICE_PER_SQM) & 
        (city_df["price_per_sqm"] <= MAX_PRICE_PER_SQM)
    ]

    # ---------------------------------
    # حماية من البيانات الفارغة بعد الفلترة (مع تسجيل السبب)
    # ---------------------------------
    if district_df.empty:
        logging.warning(f"No valid transactions after filtering for district {district_name}")
        return None
    if city_clean.empty:
        logging.warning(f"No valid city data after filtering for city {city_name}")
        return None

    # ---------------------------------
    # حساب المتوسط الوسيط مع حماية NaN
    # ---------------------------------
    district_avg_price = district_df["price_per_sqm"].median()
    city_avg_price = city_clean["price_per_sqm"].median()

    if pd.isna(district_avg_price):
        logging.warning(f"Median price is NaN for district {district_name}")
        return None
    if pd.isna(city_avg_price):
        logging.warning(f"Median price is NaN for city {city_name}")
        return None

    # عدد الصفقات المستخدمة في التحليل (بعد الفلترة)
    transactions_count = len(district_df)
    
    # عدد الصفقات المستبعدة بسبب الفلترة
    filtered_out_transactions = total_transactions - transactions_count

    # منع القسمة على صفر
    if city_avg_price and city_avg_price > 0:
        deviation = ((district_avg_price - city_avg_price) / city_avg_price) * 100
    else:
        deviation = 0

    return {
        "district_name": district_name,
        "city_name": city_name,
        "district_avg_price": round(float(district_avg_price), 2),
        "city_avg_price": round(float(city_avg_price), 2),
        "transactions_count": int(transactions_count),
        "total_transactions": int(total_transactions),
        "filtered_out_transactions": int(filtered_out_transactions),
        "price_deviation_percent": round(float(deviation), 2)
    }


def calculate_dpi_score(metrics: dict):
    """
    حساب مؤشر قوة الحي DPI
    """

    if not metrics:
        return 0

    deviation = abs(metrics.get("price_deviation_percent", 0))
    transactions = metrics.get("transactions_count", 0)

    # --------------------------
    # استقرار السعر
    # --------------------------
    stability_score = max(0, 100 - deviation * 1.5)

    # --------------------------
    # قوة الطلب
    # --------------------------
    if transactions >= 60:
        demand_score = 90
    elif transactions >= 40:
        demand_score = 75
    elif transactions >= 20:
        demand_score = 60
    elif transactions >= 10:
        demand_score = 45
    else:
        demand_score = 30

    # --------------------------
    # السيولة
    # --------------------------
    liquidity_score = min(100, transactions * 2)

    # --------------------------
    # حساب المؤشر النهائي
    # --------------------------
    dpi = (
        0.35 * stability_score +
        0.35 * demand_score +
        0.30 * liquidity_score
    )

    dpi = max(0, min(100, dpi))

    return round(dpi, 2)
