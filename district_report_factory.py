# =========================================
# District Report Factory
# Warda Intelligence
# يولد جميع تقارير الأحياء تلقائياً
# =========================================

import os
import pandas as pd

from advanced_charts import AdvancedCharts
from report_pdf_generator import create_pdf_from_content
from district_narrative_engine import generate_district_narrative
from district_ranking_engine import rank_districts


# -----------------------------------------
# المدن المستهدفة فقط
# -----------------------------------------

TARGET_CITIES = [
    "الرياض",
    "جدة",
    "مكة المكرمة",
    "المدينة المنورة",
    "الدمام"
]


# -----------------------------------------
# أنواع التقارير
# -----------------------------------------

REPORT_PACKAGES = {
    "basic": {
        "name": "اقتصادي",
        "price": 9
    },
    "pro": {
        "name": "استثماري",
        "price": 29
    },
    "premium": {
        "name": "احترافي",
        "price": 39
    }
}


# -----------------------------------------
# تنظيف اسم الحي
# -----------------------------------------

def extract_district_name(text):
    if pd.isna(text):
        return None

    return str(text).split("/")[-1].strip()


# -----------------------------------------
# حساب سعر المتر
# -----------------------------------------

def prepare_price_per_sqm(df):

    df = df.copy()

    if "price_per_sqm" not in df.columns:
        df["price_per_sqm"] = df["price"] / df["area"].replace(0, 1)

    return df


# -----------------------------------------
# إنشاء مجلد التقارير
# -----------------------------------------

def ensure_directories():

    os.makedirs("reports_store", exist_ok=True)

    for package in REPORT_PACKAGES:
        os.makedirs(f"reports_store/{package}", exist_ok=True)


# -----------------------------------------
# استخراج الأحياء النشطة
# -----------------------------------------

def get_active_districts(city_data):

    districts = (
        city_data["district"]
        .dropna()
        .apply(extract_district_name)
        .value_counts()
    )

    active = districts[districts >= 5]

    return active.index.tolist()


# -----------------------------------------
# إنشاء تقرير حي واحد
# -----------------------------------------

def generate_single_report(
        city,
        district,
        city_data,
        charts_engine,
        package_level):

    district_data = city_data[
        city_data["district"].str.contains(district, na=False)
    ]

    if len(district_data) < 5:
        return

    valid = district_data[
        (district_data["price"].notna()) &
        (district_data["area"].notna()) &
        (district_data["area"] > 0)
    ]

    if valid.empty:
        return

    district_price = (valid["price"] / valid["area"]).median()

    valid_city = city_data[
        (city_data["price"].notna()) &
        (city_data["area"].notna()) &
        (city_data["area"] > 0)
    ]

    city_price = (valid_city["price"] / valid_city["area"]).median()

    transactions = len(district_data)

    dpi = min(95, 40 + transactions)

    user_info = {

        "city_name": city,
        "district_name": district,
        "property_type": "شقة",

        "district_avg_price": district_price,
        "city_avg_price": city_price,

        "transactions_count": transactions,
        "dpi_score": dpi,
        "total_transactions": transactions
    }

    report_text = generate_district_narrative(
        user_info=user_info,
        district_metrics={},
        nearby_districts=[],
        dpi_score=dpi,
        market_data=city_data,
        real_data=city_data
    )

    charts = charts_engine.generate_all_district_charts(
        city_data,
        district
    )

    charts_by_chapter = {
        "chapter_4": [charts.get("price_trend")],
        "chapter_7": [charts.get("district_comparison")],
        "chapter_11": [charts.get("transactions_over_time")],
        "chapter_16": [charts.get("price_distribution")],
        "chapter_21": [charts.get("property_type_analysis")],
    }

    pdf_buffer = create_pdf_from_content(
        user_info=user_info,
        content_text=report_text,
        executive_decision="",
        charts_by_chapter=charts_by_chapter,
        package_level=package_level
    )

    file_name = f"{city}_{district}_{package_level}.pdf"

    with open(f"reports_store/{package_level}/{file_name}", "wb") as f:
        f.write(pdf_buffer.getvalue())


# -----------------------------------------
# المصنع الرئيسي للتقارير
# -----------------------------------------

def generate_all_district_reports(df):

    print("\n🚀 Starting District Report Factory")

    ensure_directories()

    charts_engine = AdvancedCharts()

    df = prepare_price_per_sqm(df)

    df["district_clean"] = df["district"].apply(extract_district_name)

    df = df[df["city"].isin(TARGET_CITIES)]

    for city in TARGET_CITIES:

        city_data = df[df["city"] == city]

        if city_data.empty:
            continue

        print(f"\n📍 Processing city: {city}")

        districts = get_active_districts(city_data)

        print(f"Active districts: {len(districts)}")

        for district in districts:

            print(f"Generating reports for {district}")

            for package in REPORT_PACKAGES:

                generate_single_report(
                    city,
                    district,
                    city_data,
                    charts_engine,
                    package
                )

    print("\n✅ All district reports generated successfully")
