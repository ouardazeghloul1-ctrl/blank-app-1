import os
import streamlit as st
import subprocess
import json

# ======================
# إنشاء المجلدات التلقائية
# ======================
for folder in ["outputs", "logs", "models"]:
    os.makedirs(folder, exist_ok=True)

# ======================
# إعداد الواجهة ثنائية اللغة
# ======================
LANGUAGES = {"🇸🇦 العربية": "ar", "🇬🇧 English": "en"}
lang_choice = st.sidebar.selectbox("🌐 اختر اللغة | Choose language", list(LANGUAGES.keys()))
lang = LANGUAGES[lang_choice]

# ======================
# النصوص حسب اللغة
# ======================
TEXTS = {
    "ar": {
        "title": "منصة وِردة العقارية - Warda Realty",
        "intro": "ابحث عن فرص عقارية واستثمر بثقة 💼",
        "city": "أدخل المدينة",
        "property_type": "نوع العقار",
        "goal": "الهدف من البحث",
        "individual": "فرد",
        "investor": "مستثمر",
        "search": "ابدأ البحث",
        "result": "نتائج البحث",
        "downloading": "جارٍ استخراج النتائج...",
        "no_data": "لم يتم العثور على بيانات بعد، تأكد من اتصال الإنترنت.",
    },
    "en": {
        "title": "Warda Realty Platform",
        "intro": "Find Real Estate Opportunities & Invest Smartly 💼",
        "city": "Enter City",
        "property_type": "Property Type",
        "goal": "Search Goal",
        "individual": "Individual",
        "investor": "Investor",
        "search": "Start Search",
        "result": "Search Results",
        "downloading": "Fetching real data, please wait...",
        "no_data": "No data found yet. Please check your internet connection.",
    }
}

T = TEXTS[lang]

# ======================
# واجهة التطبيق
# ======================
st.set_page_config(page_title=T["title"], page_icon="🏠", layout="centered")

st.title(T["title"])
st.write(T["intro"])

city = st.text_input(T["city"])
property_type = st.selectbox(T["property_type"], ["", "شقة / Apartment", "فيلا / Villa", "قطعة أرض / Land"])
goal = st.radio(T["goal"], [T["individual"], T["investor"]])

if st.button(T["search"]):
    if city.strip() == "":
        st.warning("⚠️ يرجى إدخال المدينة أولاً." if lang == "ar" else "⚠️ Please enter the city first.")
    else:
        st.info(T["downloading"])
        try:
            # تشغيل سكربت استخراج البيانات الحقيقي
            result = subprocess.run(
                ["python", "run_scraping.py", city, property_type, goal],
                capture_output=True, text=True
            )
            st.success(T["result"])
            
            # عرض النتائج
            output_file = os.path.join("outputs", "results.json")
            if os.path.exists(output_file):
                with open(output_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data:
                    for i, item in enumerate(data, 1):
                        st.write(f"### {i}. {item.get('title', 'بدون عنوان')}")
                        st.write(item.get('description', ''))
                        st.write(f"📍 {item.get('location', '')} | 💰 {item.get('price', '')}")
                        st.markdown("---")
                else:
                    st.warning(T["no_data"])
            else:
                st.warning(T["no_data"])
        except Exception as e:
            st.error(f"حدث خطأ أثناء تشغيل الكود: {e}")
