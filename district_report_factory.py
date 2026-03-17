# district_report_factory.py

import pandas as pd
import os

from advanced_charts import AdvancedCharts
from report_pdf_generator import create_pdf_from_content
from district_narrative_engine import generate_district_narrative


def generate_all_district_reports(df):

    cities = df["city"].dropna().unique()

    charts_engine = AdvancedCharts()

    os.makedirs("reports_store", exist_ok=True)

    for city in cities:

        city_data = df[df["city"] == city]

        districts = (
            city_data["district"]
            .dropna()
            .str.split("/")
            .str[-1]
            .str.strip()
            .unique()
        )

        for district in districts:

            district_data = city_data[
                city_data["district"]
                .str.contains(district, na=False)
            ]

            if len(district_data) < 5:
                continue

            print("Creating report:", city, district)

            # حساب سعر المتر
            valid = district_data[
                (district_data["price"].notna()) &
                (district_data["area"].notna()) &
                (district_data["area"] > 0)
            ]

            if valid.empty:
                continue

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
                "total_transactions": transactions,

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
                package_level="ذهبية"
            )

            file_name = f"{city}_{district}_report.pdf"

            with open(f"reports_store/{file_name}", "wb") as f:
                f.write(pdf_buffer.getvalue())

    print("All reports generated!")
  # -----------------------------------------
# استخراج التصنيفات الاستثمارية
# -----------------------------------------

def get_market_rankings(df):

    ranking = rank_districts(df)

    if ranking.empty:
        return {}

    best = ranking.sort_values("dpi", ascending=False).head(10)

    cheapest = ranking.sort_values(
        "median_price_sqm",
        ascending=True
    ).head(10)

    expensive = ranking.sort_values(
        "median_price_sqm",
        ascending=False
    ).head(10)

    active = ranking.sort_values(
        "transactions",
        ascending=False
    ).head(10)

    return {
        "best_investment": best,
        "cheapest": cheapest,
        "most_expensive": expensive,
        "most_active": active,
          }
