import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hashlib
import time

# إعداد الصفحة
st.set_page_config(page_title="التحليل العقاري الذهبي | Warda Intelligence", layout="wide")

# تنسيق واجهة فاخرة
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: gold; }
    .stApp { background-color: #0E1117; }
    h1, h2, h3, h4, h5, h6 { color: gold !important; }
    .stSelectbox label, .stSlider label, .stRadio label { color: gold !important; }
    .stButton>button {
        background-color: gold; color: black; font-weight: bold;
        border-radius: 10px; padding: 0.6em 1.2em; border: none;
        width: 100%;
    }
    .analysis-card {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        padding: 20px; border-radius: 15px; border: 1px solid gold;
        margin: 10px 0; color: white;
    }
    .price-up { color: #00ff00; font-weight: bold; }
    .price-down { color: #ff4444; font-weight: bold; }
    .package-card {
        background: linear-gradient(135deg, #2d2d2d, #1a1a1a);
        padding: 15px; border-radius: 10px; border: 2px solid #d4af37;
        margin: 10px 0; text-align: center;
    }
    .admin-panel {
        background: linear-gradient(135deg, #1a2a3a, #2a3a4a);
        padding: 20px; border-radius: 15px; border: 2px solid #00ff00;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: gold;'>🏙️ منصة التحليل العقاري الذهبي - Warda Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37;'>تحليل ذكي مخصص لكل فئة - قرارات استثمارية مدروسة</p>", unsafe_allow_html=True)

# === نظام الباقات والأسعار ===
PACKAGES = {
    "مجانية": {
        "price": 0,
        "features": [
            "تحليل سوق أساسي",
            "أسعار متوسطة للمنطقة", 
            "تقرير نصي بسيط",
            "صالح لعقار واحد"
        ]
    },
    "فضية": {
        "price": 29,
        "features": [
            "كل مميزات المجانية +",
            "تحليل تنبؤي 6 أشهر",
            "مقارنة مع مشاريع مشابهة",
            "نصائح استثمارية مبدئية",
            "تقرير PDF متقدم"
        ]
    },
    "ذهبية": {
        "price": 79,
        "features": [
            "كل مميزات الفضية +", 
            "تحليل ذكاء اصطناعي متقدم",
            "تنبؤات لمدة سنة كاملة",
            "دراسة الجدوى الاقتصادية",
            "تحليل المنافسين",
            "نصائح مخصصة حسب الفئة"
        ]
    },
    "ماسية": {
        "price": 149,
        "features": [
            "كل مميزات الذهبية +",
            "تحليل شمولي متكامل", 
            "تقارير مقارنة مع كل المدن",
            "تحليل المخاطرة المتقدم",
            "خطة استثمارية تفصيلية"
        ]
    }
}

# === تحليلات مخصصة لكل فئة ===
def get_analysis_by_user_type(user_type, city, property_type, area):
    """تحليل مخصص حسب فئة المستخدم"""
    
    analyses = {
        "مستثمر": {
            "title": "📊 تحليل استثماري متقدم",
            "focus": ["العائد على الاستثمار", "فترة الاسترداد", "مخاطر السوق", "فرص النمو"],
            "questions": [
                "ما هو العائد المتوقع على استثماري؟",
                "كم تبلغ فترة استرداد رأس المال؟", 
                "ما هي أفضل استراتيجية للخروج؟",
                "كيف أحمي استثماري من تقلبات السوق؟"
            ],
            "advice": "ركز على التنويع وامتلاك محفظة عقارية متوازنة"
        },
        "وسيط عقاري": {
            "title": "🤝 تحليل سوق للوساطة",
            "focus": ["حركة السوق", "هوامش الربح", "المنافسة", "فرص جديدة"],
            "questions": [
                "ما هي أفضل المناطق للوساطة؟",
                "كيف أزيد من هامش ربحى؟",
                "ما هي استراتيجية التسعير المنافسة؟",
                "كيف أجد عملاء جدد؟"
            ],
            "advice": "تخصص في منطقة معينة وابن سمعة قوية"
        },
        "شركة تطوير": {
            "title": "🏗️ تحليل تطويري شامل", 
            "focus": ["جدوى المشروع", "تكاليف التطوير", "العقبات القانونية", "معدلات الإشغال"],
            "questions": [
                "ما هي جدوى المشروع التطويري؟",
                "كيف أقلل من تكاليف التطوير؟",
                "ما هي المتطلبات القانونية؟",
                "ما هي معدلات الإشغال المتوقعة؟"
            ],
            "advice": "اهتم بدراسة الجدوى التفصيلية قبل البدء"
        },
        "فرد": {
            "title": "🏠 تحليل شراء سكني",
            "focus": ["الملاءة المالية", "التمويل", "الموقع المناسب", "القيمة المستقبلية"],
            "questions": [
                "هل السعر مناسب لقدرتي المالية؟",
                "ما هي أفضل options التمويل؟",
                "كيف أختار الموقع المناسب؟",
                "هل ستزيد قيمة العقار مستقبلاً؟"
            ],
            "advice": "لا تشتري بأكثر من 30% من دخلك الشهري للسكن"
        },
        "باحث عن فرصة": {
            "title": "🔍 تحليل فرص الاستثمار",
            "focus": ["الفرص السريعة", "استثمارات صغيرة", "عوائد سريعة", "مخاطرة منخفضة"],
            "questions": [
                "أين توجد أفضل الفرص حالياً؟",
                "ما هي استثمارات المدى القصير؟",
                "كيف أبدأ بميزانية محدودة؟", 
                "ما هي أقل الفرص مخاطرة؟"
            ],
            "advice": "ابدأ صغيراً وتعلم من كل صفقة"
        },
        "مالك عقار": {
            "title": "💰 تحليل إدارة الممتلكات",
            "focus": ["تحسين القيمة", "زيادة الإيرادات", "الصيانة والتطوير", "البيع أو التأجير"],
            "questions": [
                "كيف أزيد من قيمة عقاري؟",
                "ما هو أفضل وقت للبيع؟",
                "كيف أزيد من إيرادات التأجير؟",
                "ما هي التحسينات المطلوبة؟"
            ],
            "advice": "حافظ على عقارك فهو استثمار طويل الأجل"
        }
    }
    
    return analyses.get(user_type, analyses["فرد"])

# === توليد التقرير ===
def generate_comprehensive_report(user_type, city, property_type, area, package, property_count):
    """توليد تقرير شامل حسب الباقة المختارة"""
    
    # حساب السعر الديناميكي
    base_price = PACKAGES[package]["price"]
    total_price = base_price * property_count
    
    # تحليل مخصص للفئة
    user_analysis = get_analysis_by_user_type(user_type, city, property_type, area)
    
    # إنشاء محتوى التقرير
    report_content = f"""
    🏙️ تقرير Warda Intelligence المتقدم
    =================================
    
    👤 معلومات العميل:
    - الفئة: {user_type}
    - المدينة: {city} 
    - نوع العقار: {property_type}
    - المساحة: {area} م²
    - عدد العقارات: {property_count}
    
    💎 الباقة المختارة: {package}
    💰 السعر الإجمالي: {total_price} دولار
    
    {user_analysis['title']}
    ========================
    
    🎯 الأسئلة الرئيسية:
    """
    
    for i, question in enumerate(user_analysis['questions'], 1):
        report_content += f"\n{i}. {question}"
    
    report_content += f"""
    
    📊 مجالات التركيز:
    """
    for focus in user_analysis['focus']:
        report_content += f"\n   • {focus}"
    
    report_content += f"""
    
    💡 النصيحة الذهبية:
    {user_analysis['advice']}
    
    📈 تحليل السوق في {city}:
    - متوسط الأسعار: {np.random.randint(1000, 5000):,} دولار/م²
    - اتجاه السوق: {'صاعد ↗️' if np.random.random() > 0.5 else 'هابط ↘️'}
    - السيولة: {'عالية 💧' if np.random.random() > 0.3 else 'متوسطة ⚖️'}
    - المنافسة: {'عالية 🔥' if np.random.random() > 0.6 else 'متوسطة 📊'}
    
    🔮 توقعات الذكاء الاصطناعي:
    - فرص النمو: {np.random.randint(5, 25)}%
    - مستوى المخاطرة: {np.random.randint(10, 40)}%
    - التوصية: {'شراء 🟢' if np.random.random() > 0.4 else 'انتظار 🟡'}
    - الفترة المثلى: {np.random.randint(1, 12)} أشهر
    
    📋 خطة العمل المقترحة:
    1. دراسة السوق المحلي لمدة أسبوع
    2. تحديد 3-5 عقارات محتملة
    3. التفاوض على السعر
    4. المراجعة القانونية
    5. إتمام الصفقة
    
    💎 مميزات الباقة {package}:
    """
    
    for feature in PACKAGES[package]["features"]:
        report_content += f"\n   ✅ {feature}"
    
    report_content += f"""
    
    🕒 تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    📞 للاستفسار: +213779888140
    🌐 Warda Intelligence - التحليل العقاري الذكي
    """
    
    return report_content, total_price

# === لوحة التحكم للمسؤول ===
def admin_panel():
    """لوحة تحكم المسؤول"""
    st.markdown("---")
    st.markdown("### 🛠️ لوحة تحكم المسؤول")
    
    with st.expander("🔗 إنشاء رابط مؤثرين جديد"):
        days_valid = st.number_input("مدة الصلاحية (أيام):", min_value=1, max_value=30, value=1)
        
        if st.button("إنشاء رابط جديد"):
            today = datetime.now().strftime("%Y%m%d")
            influencer_token = hashlib.md5(f"FREE1_{today}_{np.random.randint(1000,9999)}".encode()).hexdigest()[:10]
            expiry_date = datetime.now() + timedelta(days=days_valid)
            
            st.session_state.influencer_url = f"https://warda-intelligence.streamlit.app/?promo={influencer_token}"
            st.session_state.expiry_date = expiry_date
            
            st.success(f"✅ تم إنشاء الرابط الجديد")
    
    if hasattr(st.session_state, 'influencer_url'):
        st.markdown(f"""
        <div class='admin-panel'>
        <h4>🎯 رابط المؤثرين الحالي:</h4>
        <code style='background: black; padding: 10px; border-radius: 5px; display: block; margin: 10px; font-size: 16px;'>{st.session_state.influencer_url}</code>
        <p>📅 ينتهي في: {st.session_state.expiry_date.strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)

# === الواجهة الرئيسية ===
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👤 بيانات المستخدم")
    
    user_type = st.selectbox("اختر فئتك:", 
                           ["مستثمر", "وسيط عقاري", "شركة تطوير", "فرد", "باحث عن فرصة", "مالك عقار"])
    
    city = st.selectbox("المدينة:", 
                       ["الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة", "الخبر", "تبوك", "الطائف"])
    
    property_type = st.selectbox("نوع العقار:", 
                                ["شقة", "فيلا", "أرض", "محل تجاري"])
    
    area = st.slider("المساحة (م²):", 50, 1000, 120)

with col2:
    st.markdown("### 💎 اختيار الباقة")
    
    # عدد العقارات مع تحديث السعر تلقائياً
    property_count = st.slider("🔢 عدد العقارات للتحليل:", 1, 50, 1,
                              help="كلما زاد عدد العقارات، زادت دقة التحليل والسعر")
    
    # عرض الباقات
    chosen_pkg = st.radio("اختر باقتك:", list(PACKAGES.keys()))
    
    # حساب السعر الديناميكي
    base_price = PACKAGES[chosen_pkg]["price"]
    total_price = base_price * property_count
    
    # عرض تفاصيل الباقة
    st.markdown(f"""
    <div class='package-card'>
    <h3>باقة {chosen_pkg}</h3>
    <h4>{total_price} دولار</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # عرض المميزات
    st.markdown("**المميزات:**")
    for feature in PACKAGES[chosen_pkg]["features"]:
        st.write(f"✅ {feature}")

# === زر إنشاء التقرير ===
st.markdown("---")
st.markdown(f"### 💰 السعر النهائي: **{total_price} دولار**")

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("🚀 إنشاء التقرير الآن", use_container_width=True):
        with st.spinner("🔄 جاري إنشاء التقرير المتقدم..."):
            time.sleep(2)
            
            # إنشاء التقرير
            report, final_price = generate_comprehensive_report(
                user_type, city, property_type, area, chosen_pkg, property_count
            )
            
            # حفظ التقرير في الجلسة
            st.session_state.current_report = report
            st.session_state.report_generated = True

with col2:
    # زر لتحميل أي تقرير سابق
    if st.button("📥 تحميل آخر تقرير", use_container_width=True):
        if hasattr(st.session_state, 'current_report'):
            st.success("✅ تم تحميل آخر تقرير")
        else:
            st.warning("⚠️ لا يوجد تقرير سابق")

# === عرض التقرير وزر التحميل ===
if st.session_state.get('report_generated', False):
    st.markdown("---")
    st.markdown("## 📊 التقرير النهائي")
    
    # عرض التقرير
    st.text_area("محتوى التقرير:", st.session_state.current_report, height=400)
    
    # زر تحميل التقرير
    st.download_button(
        label="📥 تحميل التقرير الكامل",
        data=st.session_state.current_report,
        file_name=f"تقرير_{user_type}_{city}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.success("✅ تم إنشاء التقرير بنجاح!")
    st.balloons()

# === لوحة المسؤول (تظهر فقط للمسؤول) ===
admin_password = st.sidebar.text_input("كلمة مرور المسؤول:", type="password")
if admin_password == "WardaAdmin2024":  # كلمة السر الخاصة بك
    admin_panel()

# === رابط المؤثرين (للزوار العاديين) ===
st.markdown("---")
st.markdown("### 🎁 عرض المؤثرين")

# التحقق من رابط المؤثرين
query_params = st.experimental_get_query_params()
if query_params.get('promo'):
    promo_token = query_params['promo'][0]
    st.success("🎉 تم تفعيل العرض المجاني للمؤثرين!")
    
    # استخدام بيانات افتراضية للتقرير المجاني
    free_user_type = "مؤثر"
    free_city = "الرياض" 
    free_property_type = "شقة"
    free_area = 120
    free_package = "ذهبية"
    free_count = 1
    
    if st.button("🎁 الحصول على التقرير المجاني", use_container_width=True):
        report, _ = generate_comprehensive_report(
            free_user_type, free_city, free_property_type, free_area, free_package, free_count
        )
        
        st.download_button(
            label="📥 تحميل التقرير المجاني",
            data=report,
            file_name=f"تقرير_مجاني_لمؤثر_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
else:
    st.info("""
    **للمؤثرين:** 
    للحصول على تقرير مجاني، يرجى استخدام الرابط الخاص الذي تم توفيره من إدارة المنصة.
    """)

# === معلومات الاتصال ===
st.markdown("---")
st.markdown("### 📞 للتواصل مع Warda Intelligence")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **💬 واتساب:**
    +213779888140
    
    **📧 البريد:**
    info@warda-intelligence.com
    """)

with col2:
    st.markdown("""
    **🌐 الموقع:**
    www.warda-intelligence.com
    
   
