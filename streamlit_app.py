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
    .premium { border-color: #ffd700; background: linear-gradient(135deg, #3d2e1a, #2d1f0f); }
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
        ],
        "color": "white"
    },
    "فضية": {
        "price": 29,
        "features": [
            "كل مميزات المجانية +",
            "تحليل تنبؤي 6 أشهر",
            "مقارنة مع مشاريع مشابهة",
            "نصائح استثمارية مبدئية",
            "تقرير PDF متقدم"
        ],
        "color": "silver"
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
        ],
        "color": "gold"
    },
    "ماسية": {
        "price": 149,
        "features": [
            "كل مميزات الذهبية +",
            "تحليل شمولي متكامل", 
            "متابعة شهرية لمدة 3 أشهر",
            "استشارة مباشرة مع خبير",
            "تحليل المخاطرة المتقدم",
            "خطة استثمارية تفصيلية",
            "تقارير مقارنة مع كل المدن"
        ],
        "color": "diamond"
    }
}

# === تحليلات مخصصة لكل فئة ===
def get_analysis_by_user_type(user_type, city, property_type, area, budget):
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

# === نظام الدفع والتقارير ===
def generate_comprehensive_report(user_type, city, property_type, area, budget, package, property_count):
    """توليد تقرير شامل حسب الباقة المختارة"""
    
    # حساب السعر الديناميكي
    base_price = PACKAGES[package]["price"]
    total_price = base_price * property_count
    
    # تحليل مخصص للفئة
    user_analysis = get_analysis_by_user_type(user_type, city, property_type, area, budget)
    
    report = f"""
    🏙️ تقرير Warda Intelligence المتقدم
    =================================
    
    👤 معلومات العميل:
    - الفئة: {user_type}
    - المدينة: {city} 
    - نوع العقار: {property_type}
    - المساحة: {area} م²
    - الميزانية: {budget:,.0f} دولار
    - عدد العقارات: {property_count}
    
    💎 الباقة المختارة: {package}
    💰 السعر الإجمالي: {total_price} دولار
    
    {user_analysis['title']}
    ========================
    
    🎯 الأسئلة الرئيسية:
    """
    
    for i, question in enumerate(user_analysis['questions'], 1):
        report += f"\n{i}. {question}"
    
    report += f"""
    
    📊 مجالات التركيز:
    """
    for focus in user_analysis['focus']:
        report += f"\n   • {focus}"
    
    report += f"""
    
    💡 النصيحة الذهبية:
    {user_analysis['advice']}
    
    📈 تحليل السوق:
    - متوسط الأسعار في {city}: {np.random.randint(1000, 5000):,} دولار/م²
    - اتجاه السوق: {'صاعد' if np.random.random() > 0.5 else 'هابط'}
    - السيولة: {'عالية' if np.random.random() > 0.3 else 'متوسطة'}
    
    🔮 توقعات الذكاء الاصطناعي:
    - فرص النمو: {np.random.randint(5, 25)}%
    - المخاطر: {np.random.randint(10, 40)}%
    - التوصية: {'شراء' if np.random.random() > 0.4 else 'انتظار'}
    
    📋 خطة العمل:
    1. دراسة السوق المحلي لمدة أسبوع
    2. تحديد 3-5 عقارات محتملة
    3. التفاوض على السعر
    4. المراجعة القانونية
    5. إتمام الصفقة
    
    🕒 تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    📞 للاستفسار: +213779888140
    """
    
    return report, total_price

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
    budget = st.number_input("الميزانية (دولار):", min_value=10000, max_value=5000000, value=100000, step=10000)
    
    # عدد العقارات مع تحديث السعر تلقائياً
    property_count = st.slider("🔢 عدد العقارات للتحليل:", 1, 50, 1, 
                              help="كلما زاد عدد العقارات، زادت دقة التحليل والسعر")

with col2:
    st.markdown("### 💎 اختيار الباقة")
    
    # عرض الباقات
    chosen_pkg = st.radio("اختر باقتك:", list(PACKAGES.keys()), horizontal=True)
    
    # حساب السعر الديناميكي
    base_price = PACKAGES[chosen_pkg]["price"]
    total_price = base_price * property_count
    
    # عرض تفاصيل الباقة
    st.markdown(f"""
    <div class='package-card'>
    <h3>{chosen_pkg} - {total_price} دولار</h3>
    <p>{PACKAGES[chosen_pkg]['features'][0]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # عرض المميزات
    st.markdown("**المميزات:**")
    for feature in PACKAGES[chosen_pkg]["features"]:
        st.write(f"✅ {feature}")
    
    # تحديث السعر مباشرة
    st.markdown(f"### 💰 السعر النهائي: **{total_price} دولار**")
    
    # زر الدفع
    if st.button("💳 proceed to payment", use_container_width=True):
        st.session_state.payment_ready = True

# === نظام الدفع ===
if st.session_state.get('payment_ready', False):
    st.markdown("---")
    st.markdown("### 💳 معلومات الدفع")
    
    col1, col2 = st.columns(2)
    
    with col1:
        email = st.text_input("البريد الإلكتروني:")
        card_number = st.text_input("رقم البطاقة:")
        
    with col2:
        expiry = st.text_input("تاريخ الانتهاء (MM/YY):")
        cvv = st.text_input("CVV:")
    
    if st.button("✅ تأكيد الدفع وإنشاء التقرير", use_container_width=True):
        with st.spinner("🔄 جاري إنشاء التقرير المتقدم..."):
            time.sleep(2)
            
            # إنشاء التقرير
            report, final_price = generate_comprehensive_report(
                user_type, city, property_type, area, budget, chosen_pkg, property_count
            )
            
            # عرض التقرير
            st.markdown("---")
            st.markdown("## 📊 التقرير النهائي")
            st.text_area("محتوى التقرير:", report, height=400)
            
            # زر تحميل التقرير
            st.download_button(
                label="📥 تحميل التقرير الكامل",
                data=report,
                file_name=f"تقرير_{user_type}_{city}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
            
            st.success("✅ تم الدفع وإنشاء التقرير بنجاح!")
            st.balloons()

# === رابط المؤثرين ===
st.markdown("---")
st.markdown("### 🎁 نظام المؤثرين")

# إنشاء رابط مؤقت صالح ليوم واحد
today = datetime.now().strftime("%Y%m%d")
influencer_token = hashlib.md5(f"FREE1_{today}".encode()).hexdigest()[:8]
influencer_url = f"https://warda-intelligence.streamlit.app/?promo={influencer_token}"

st.markdown(f"""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1a3a1a, #2d5a2d); border-radius: 10px;'>
<h4>🎯 رابط خاص بالمؤثرين</h4>
<p>هذا الرابط صالح ليوم واحد فقط ويوفر تقرير مجاني كامل:</p>
<code style='background: black; padding: 10px; border-radius: 5px; display: block; margin: 10px;'>{influencer_url}</code>
<p>📅 ينتهي في: {(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M')}</p>
</div>
""", unsafe_allow_html=True)

# === التحقق من رابط المؤثرين ===
if st.experimental_get_query_params().get('promo', [''])[0] == influencer_token:
    st.success("🎉 تم تفعيل العرض المجاني للمؤثرين! يمكنك الحصول على تقرير مجاني كامل.")
    
    if st.button("🎁 الحصول على التقرير المجاني", use_container_width=True):
        report, _ = generate_comprehensive_report(
            "مؤثر", "الرياض", "شقة", 120, 100000, "ذهبية", 1
        )
        st.download_button(
            label="📥 تحميل التقرير المجاني",
            data=report,
            file_name=f"تقرير_مجاني_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# === معلومات الاتصال ===
st.markdown("---")
st.markdown("### 📞 للتواصل مع Warda Intelligence")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **💬 واتساب:**
    +213779888140
    """)

with col2:
    st.markdown("""
    **📧 البريد:**
    info@warda-intelligence.com
    """)

with col3:
    st.markdown("""
    **🌐 الموقع:**
    www.warda-intelligence.com
    """)
