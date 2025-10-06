import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from data_config import الأسعار_الحالية, آخر_تحديث
from real_fetcher import fetch_real_data

st.set_page_config(page_title="منصة وردة العقارية", page_icon="🏠", layout="wide")
st.title("🏡 منصة وردة للتحليل العقاري الذكي")

st.sidebar.info(f"📅 آخر تحديث محلي: {آخر_تحديث}")

city = st.selectbox("🏙️ اختر المدينة", list(الأسعار_الحالية.keys()))
ptype = st.selectbox("🏠 نوع العقار", ["شقق", "فلل", "مكاتب"])

if st.button("🔍 تحليل السوق الآن"):
    with st.spinner("جاري جلب أحدث الأسعار من الإنترنت..."):
        data = fetch_real_data(city, ptype)
        
        if data:
            st.success("✅ تم جلب بيانات حقيقية من الإنترنت!")
            avg = data["متوسط_السعر"]
            st.metric("💰 متوسط السعر الحالي", f"{avg:,.0f} ريال")
            st.write(f"🧭 نطاق الأسعار الواقعي: {data['نطاق_السعر'][0]:,} - {data['نطاق_السعر'][1]:,} ريال")
            st.write(f"📊 عدد العقارات التي تم تحليلها: {data['عدد_النتائج']}")
        else:
            st.warning("⚠️ لم يتمكن التطبيق من جلب بيانات مباشرة، سيتم استخدام البيانات المحلية الحالية.")
            backup = الأسعار_الحالية[city][ptype]
            st.metric("💰 متوسط السعر المحلي", f"{backup['متوسط_السعر']:,} ريال")
            st.write(f"🧭 النطاق المحلي: {backup['نطاق_السعر'][0]:,} - {backup['نطاق_السعر'][1]:,} ريال")

st.markdown("---")
st.caption("💡 ملاحظة: يتم تحديث البيانات الحقيقية أسبوعيًا تلقائيًا من مواقع متعددة (حراج، بيوت، عقار السعودية، Zillow).")
