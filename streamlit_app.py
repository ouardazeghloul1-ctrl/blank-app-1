import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
from realfetcher import fetch_real_estate_data  # ✅ تعديل الاسم هنا

# -------------------------------------
# إعداد الصفحة
# -------------------------------------
st.set_page_config(page_title="منصة Warda Realty", layout="wide")

st.title("🏠 منصة تحليل أسعار العقارات - Warda Realty")
st.markdown("### السوق العقاري السعودي - بيانات حقيقية من الإنترنت")

# -------------------------------------
# تحديد مسار ملف CSV
# -------------------------------------
OUTPUT_DIR = "outputs"
CSV_PATH = os.path.join(OUTPUT_DIR, "data.csv")

# -------------------------------------
# زر تحديث البيانات
# -------------------------------------
if st.button("🔄 تحديث البيانات من المواقع"):
    with st.spinner("جاري جلب البيانات الحقيقية..."):
        try:
            # ✅ تعديل الدالة المستدعاة هنا أيضًا
            df = fetch_real_estate_data()
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            df.to_csv(CSV_PATH, index=False)
            st.success("✅ تم جلب البيانات وتحديث الملف بنجاح!")
        except Exception as e:
            st.error(f"حدث خطأ أثناء الجلب: {e}")

# -------------------------------------
# قراءة البيانات من الملف
# -------------------------------------
if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)

    st.subheader("📊 نظرة عامة على البيانات")
    st.dataframe(df.head(20))

    # -------------------------------------
    # اختيار المدينة أو المنطقة
    # -------------------------------------
    if "المدينة" in df.columns:
        city_list = df["المدينة"].dropna().unique().tolist()
        selected_city = st.selectbox("اختر المدينة:", ["الكل"] + city_list)

        if selected_city != "الكل":
            df = df[df["المدينة"] == selected_city]

    # -------------------------------------
    # رسم بياني للأسعار
    # -------------------------------------
    if "السعر" in df.columns:
        st.subheader("📈 توزيع الأسعار")
        fig = px.histogram(df, x="السعر", nbins=30, title="توزيع أسعار العقارات")
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------
    # ملخص إحصائي
    # -------------------------------------
    st.subheader("📋 ملخص الأسعار")
    st.write(df.describe())

else:
    st.warning("⚠️ لم يتم العثور على ملف البيانات. اضغط زر **تحديث البيانات** لجلبها أول مرة.")
