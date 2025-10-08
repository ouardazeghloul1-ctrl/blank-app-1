# app.py (final)
import streamlit as st
import pandas as pd
import os
import traceback
from realfetcher import fetch_data  # يدعم وضع "open" و "scraper"
from ai_predictor import predict_prices
from payment import process_payment
from pdf_report import generate_pdf
from utils import render_header

st.set_page_config(page_title="Warda", layout="wide")
render_header(short=True)  # تابع في utils يعرض الشعار المصغر / سنضمن وجوده

# --- Language selector ---
lang = st.selectbox("Language / اللغة:", ["English", "عربي"], index=0)

# --- Labels bilingual ---
if lang == "English":
    title_app = "Warda — Real Estate Price Insights"
    city_label = "City"
    district_label = "District (optional)"
    prop_label = "Property Type"
    goal_label = "Goal"
    package_label = "Choose Package"
    use_real_data_label = "Use real market data (scraper)"
    test_scraper_label = "Test scraper now"
    get_report_label = "Get Report"
    download_label = "Download PDF Report"
    no_data_msg = "No data available for the selected filters."
    error_msg = "An error occurred:"
else:
    title_app = "وردة — تحليلات أسعار العقارات"
    city_label = "المدينة"
    district_label = "الحي (اختياري)"
    prop_label = "نوع العقار"
    goal_label = "الغرض"
    package_label = "اختر الباقة"
    use_real_data_label = "استخدام بيانات السوق الحقيقية (Scraper)"
    test_scraper_label = "اختبار السكيرابر الآن"
    get_report_label = "احصل على التقرير"
    download_label = "تحميل التقرير"
    no_data_msg = "لا توجد بيانات لهذا الاختيار."

st.title(title_app)
st.markdown("**Warda** — concise, modern, trusted." if lang == "English" else "**وردة** — محترفة، سريعة، موثوقة.")

# --- Inputs ---
package = st.selectbox(package_label, ["Quick", "Accurate", "VIP 999$"])
city = st.selectbox(city_label, ["Riyadh", "Jeddah", "Dammam", "Makkah", "Madinah"])
district = st.text_input(district_label)
property_type = st.selectbox(prop_label, ["Apartment", "Villa", "Land"])
goal = st.selectbox(goal_label, ["Buy", "Rent", "Invest"] if lang == "English" else ["شراء", "إيجار", "استثمار"])
prediction_days = st.selectbox("Prediction Days / أيام التنبؤ:", [14, 30])

st.write("---")

# --- Options for data source ---
use_real = st.checkbox(use_real_data_label, value=False)
colA, colB = st.columns([1,1])

with colA:
    test_scrape = st.button(test_scraper_label)

with colB:
    run_button = st.button(get_report_label)

# --- Area to show logs / messages ---
log_container = st.container()

def show_error(e):
    with log_container:
        st.error(f"{error_msg} {str(e)}")
        st.text(traceback.format_exc())

# --- Handle test scraper ---
if test_scrape:
    with st.spinner("Testing scraper..."):
        try:
            # call fetch_data in a small sample mode (it should handle mode env var)
            sample_df = fetch_data(city=city, district=district, property_type=property_type)
            if sample_df is None or getattr(sample_df, "empty", False):
                st.warning(no_data_msg)
            else:
                st.success(f"Sample fetched: {len(sample_df)} rows")
                st.dataframe(sample_df.head(10))
        except Exception as e:
            show_error(e)

# --- Main run: generate report after payment ---
if run_button:
    try:
        with st.spinner("Processing payment..."):
            paid = process_payment(package)
        if not paid:
            st.warning("Payment failed or not completed.")
        else:
            with st.spinner("Collecting data..."):
                # If user wants real data, fetch_data will check REALFETCHER_MODE env var
                df = None
                try:
                    if use_real:
                        df = fetch_data(city=city, district=district, property_type=property_type)
                        if df is None or getattr(df, "empty", False):
                            st.warning("Using fallback sample data because real fetch returned no rows.")
                            df = fetch_data(city="", district="", property_type="")  # fallback
                    else:
                        df = fetch_data(city="", district="", property_type="")  # sample/open mode
                except Exception as e:
                    st.warning("Error while fetching data; falling back to sample data.")
                    st.text(str(e))
                    df = fetch_data(city="", district="", property_type="")

            if df is None or getattr(df, "empty", False):
                st.error(no_data_msg)
            else:
                st.success("Data ready. Running prediction...")
                prediction = predict_prices(df, prediction_days)
                st.subheader("Prediction / التنبؤ")
                st.line_chart(prediction["Prediction"])
                st.write("Sample data preview / عرض بيانات تجريبية:")
                st.dataframe(df.head(10))

                # Generate PDF and offer download
                pdf_bytes = generate_pdf(city, district, property_type, prediction, package, df)
                st.success("Report generated.")
                st.download_button(download_label, pdf_bytes, file_name="Warda_Report.pdf")
    except Exception as e:
        show_error(e)

# --- Footer with quick debug help ---
st.write("---")
if lang == "English":
    st.info("If scraper returns no data: 1) ensure REALFETCHER_MODE=scraper in .env and run locally; 2) test the scraper with the sample button; 3) check logs/ for scraping.log")
else:
    st.info("إن لم يجلب السكرايبر بيانات: 1) تأكدي من وضع REALFETCHER_MODE=scraper في .env وتشغيله محلياً; 2) جرّبي زر الاختبار; 3) راجعي logs/scraping.log")
