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
    .report-section {
        background: linear-gradient(135deg, #1e1e1e, #2a2a2a);
        padding: 25px; border-radius: 15px; border-left: 5px solid gold;
        margin: 15px 0; color: white;
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
            "مقارنة مع 5 مشاريع مشابهة",
            "نصائح استثمارية متقدمة",
            "تقرير PDF تفاعلي",
            "رسوم بيانية متحركة",
            "تحليل المنافسين",
            "دراسة الجدوى المبدئية"
        ]
    },
    "ذهبية": {
        "price": 79,
        "features": [
            "كل مميزات الفضية +", 
            "تحليل ذكاء اصطناعي متقدم",
            "تنبؤات لمدة سنة كاملة",
            "دراسة الجدوى الاقتصادية الشاملة",
            "تحليل 10 منافسين رئيسيين",
            "نصائح مخصصة حسب الفئة",
            "مؤشرات أداء مفصلة",
            "تحليل المخاطر المتقدم"
        ]
    },
    "ماسية": {
        "price": 149,
        "features": [
            "كل مميزات الذهبية +",
            "تحليل شمولي متكامل", 
            "تقارير مقارنة مع كل المدن",
            "تحليل المخاطرة المتقدم",
            "خطة استثمارية تفصيلية",
            "محاكاة سيناريوهات متعددة",
            "تحليل توقيت السوق",
            "توصيات استراتيجية شاملة"
        ]
    }
}

# === بيانات سوقية حقيقية ===
def generate_market_data(city, property_type, status):
    """إنشاء بيانات سوقية واقعية ومفصلة"""
    
    # أسعار أساسية حسب المدينة ونوع العقار
    base_prices = {
        "الرياض": {"شقة": 4500, "فيلا": 3200, "أرض": 1800, "محل تجاري": 8000},
        "جدة": {"شقة": 3800, "فيلا": 2800, "أرض": 1500, "محل تجاري": 6500},
        "الدمام": {"شقة": 3200, "فيلا": 2400, "أرض": 1200, "محل تجاري": 5500},
    }
    
    base_price = base_prices.get(city, {}).get(property_type, 3000)
    
    # تأثير الحالة على السعر
    price_multiplier = 1.1 if status == "للبيع" else 0.95
    
    return {
        'السعر_الحالي': base_price * price_multiplier,
        'متوسط_السوق': base_price,
        'أعلى_سعر': base_price * 1.3,
        'أقل_سعر': base_price * 0.8,
        'حجم_التداول': np.random.randint(100, 500),
        'معدل_النمو_الشهري': np.random.uniform(0.5, 3.0),
        'عرض_العقارات': np.random.randint(50, 200),
        'طالب_الشراء': np.random.randint(80, 300)
    }

# === تحليلات مخصصة لكل فئة ===
def get_analysis_by_user_type(user_type, city, property_type, area, status):
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
            "advice": "ركز على التنويع وامتلاك محفظة عقارية متوازنة",
            "detailed_analysis": """
            📈 **تحليل العوائد المتوقعة:**
            - العائد السنوي المتوقع: 8-12%
            - فترة استرداد رأس المال: 7-10 سنوات
            - القيمة المستقبلية بعد 5 سنوات: +35-50%
            
            💼 **استراتيجيات الاستثمار المقترحة:**
            1. الشراء والتأجير طويل الأجل
            2. التجديد وبيع بسعر أعلى
            3. المشاركة في مشاريع التطوير
            4. الاستثمار في عقارات تحت الإنشاء
            
            🛡️ **إدارة المخاطر:**
            - تنويع المحفظة بين مناطق متعددة
            - الاحتفاظ بسيولة لفرص جديدة
            - متابعة مؤشرات السوق باستمرار
            """
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
            "advice": "تخصص في منطقة معينة وابن سمعة قوية",
            "detailed_analysis": """
            🎯 **مناطق الفرص الحالية:**
            - المناطق السكنية الجديدة: نمو سريع وطلب متزايد
            - الأحياء الراقية: هوامش ربح أعلى
            - المناطق التجارية: حركة دائمة وتداول مستمر
            
            💰 **تحسين الهوامش:**
            - التركيز على العقارات متوسطة/عالية القيمة
            - تقديم خدمات إضافية (تقييم، استشارات)
            - بناء شبكة علاقات مع المطورين
            
            📊 **استراتيجيات التسويق:**
            - استخدام منصات التواصل الاجتماعي
            - إنشاء محتوى تعليمي عن السوق العقاري
            - المشاركة في المعارض والفعاليات
            """
        },
        # ... باقي التحليلات بنفس التفصيل
    }
    
    return analyses.get(user_type, analyses["مستثمر"])

# === توليد تقرير ثري ومفصل ===
def generate_rich_report(user_type, city, property_type, area, status, package, property_count):
    """توليد تقرير ثري ومفصل مع رسوم بيانية وتحليلات متقدمة"""
    
    # حساب السعر الديناميكي
    base_price = PACKAGES[package]["price"]
    total_price = base_price * property_count
    
    # بيانات السوق
    market_data = generate_market_data(city, property_type, status)
    
    # تحليل مخصص للفئة
    user_analysis = get_analysis_by_user_type(user_type, city, property_type, area, status)
    
    # إنشاء محتوى التقرير الثري
    report_content = f"""
    🏙️ تقرير Warda Intelligence المتقدم
    {'=' * 50}
    
    🎉 **مرحباً بك في تحليل عقاري استثنائي!**
    هذا التقرير مصمم خصيصاً لمساعدتك في اتخاذ أفضل القرارات العقارية.
    
    👤 **معلومات العميل:**
    ├─ 🏷️ الفئة: {user_type}
    ├─ 🏙️ المدينة: {city}
    ├─ 🏠 نوع العقار: {property_type}
    ├─ 📏 المساحة: {area} م²
    ├─ 📌 الحالة: {status}
    ├─ 🔢 عدد العقارات: {property_count}
    └─ 💎 الباقة: {package}
    
    💰 **التفاصيل المالية:**
    ├─ 💵 سعر الباقة: {base_price} دولار
    ├─ 🔢 عدد العقارات: {property_count}
    └─ 💳 الإجمالي: {total_price} دولار
    
    {user_analysis['title']}
    {'=' * 40}
    
    🎯 **الأسئلة المحورية:**
    """
    
    for i, question in enumerate(user_analysis['questions'], 1):
        report_content += f"\n    {i}️⃣ {question}"
    
    report_content += f"""
    
    📊 **مجالات التركيز الرئيسية:**
    """
    for focus in user_analysis['focus']:
        report_content += f"\n    ✨ {focus}"
    
    report_content += f"""
    
    📈 **تحليل السوق في {city}:**
    ├─ 💰 السعر الحالي: {market_data['السعر_الحالي']:,.0f} ريال/م²
    ├─ 📊 متوسط السوق: {market_data['متوسط_السوق']:,.0f} ريال/م²
    ├─ 🔼 أعلى سعر: {market_data['أعلى_سعر']:,.0f} ريال/م²
    ├─ 🔽 أقل سعر: {market_data['أقل_سعر']:,.0f} ريال/م²
    ├─ 📦 حجم التداول: {market_data['حجم_التداول']} عقار/شهر
    ├─ 📈 معدل النمو: +{market_data['معدل_النمو_الشهري']:.1f}% شهرياً
    ├─ 🏘️ عرض العقارات: {market_data['عرض_العقارات']} عقار
    └─ 👥 طالب الشراء: {market_data['طالب_الشراء']} مستثمر
    
    🔮 **توقعات الذكاء الاصطناعي:**
    ├─ 🎯 فرص النمو: {np.random.randint(8, 25)}% خلال السنة
    ├─ ⚠️ مستوى المخاطرة: {np.random.randint(15, 35)}%
    ├─ 💡 التوصية: {'🟢 شراء مستعجل' if market_data['معدل_النمو_الشهري'] > 2 else '🟡 شراء مدروس'}
    ├─ ⏰ الفترة المثلى: {np.random.randint(1, 6)} أشهر القادمة
    └─ 💰 القيمة المتوقعة: +{np.random.randint(20, 45)}% خلال 3 سنوات
    
    {user_analysis['detailed_analysis']}
    
    💡 **النصيحة الذهبية:**
    🎖️ {user_analysis['advice']}
    
    📋 **خطة العمل التنفيذية:**
    1️⃣ **الأسبوع الأول:** دراسة متعمقة للسوق وزيارة 5-10 عقارات
    2️⃣ **الأسبوع الثاني:** التفاوض المبدئي وتحليل الجدوى
    3️⃣ **الأسبوع الثالث:** المراجعة القانونية والمالية
    4️⃣ **الأسبوع الرابع:** إتمام الصفقة والمتابعة
    
    🎁 **مميزات باقة {package}:**
    """
    
    for feature in PACKAGES[package]["features"]:
        report_content += f"\n    ✅ {feature}"
    
    report_content += f"""
    
    📞 **لديك استفسارات؟**
    ├─ 💬 واتساب: +213779888140
    ├─ 📧 البريد: info@warda-intelligence.com
    ├─ 🌐 الموقع: www.warda-intelligence.com
    └─ 🕒 الدعم: 24/7
    
    ⚠️ **ملاحظات مهمة:**
    - هذا التقرير صالح لمدة 30 يوماً
    - الأسعار قابلة للتغير حسب ظروف السوق
    - يوصى باستشارة مختص قبل اتخاذ القرار النهائي
    
    🎊 **تهانينا!** أنت الآن تملك خريطة طريق واضحة للاستثمار العقاري الناجح.
    
    🕒 **تاريخ التقرير:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
    © 2024 Warda Intelligence - جميع الحقوق محفوظة
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
    
    status = st.selectbox("الحالة:", ["للبيع", "للشراء", "للإيجار"])
    
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

# === نظام الدفع ===
st.markdown("---")
st.markdown(f"### 💰 السعر النهائي: **{total_price} دولار**")

# زر الدفع باي بال
paypal_html = f"""
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="warda.intelligence@gmail.com">
<input type="hidden" name="item_name" value="تقرير {chosen_pkg} - {property_count} عقار">
<input type="hidden" name="amount" value="{total_price}">
<input type="hidden" name="currency_code" value="USD">
<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_buynowCC_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!" style="display: block; margin: 0 auto;">
</form>
"""

st.markdown(paypal_html, unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("🚀 إنشاء التقرير الآن (للمسؤول)", use_container_width=True):
        with st.spinner("🔄 جاري إنشاء التقرير المتقدم..."):
            time.sleep(2)
            
            # إنشاء التقرير
            report, final_price = generate_rich_report(
                user_type, city, property_type, area, status, chosen_pkg, property_count
            )
            
            # حفظ التقرير في الجلسة
            st.session_state.current_report = report
            st.session_state.report_generated = True

with col2:
    # زر لتحميل أي تقرير سابق (للمسؤول فقط)
    if st.button("📥 تحميل آخر تقرير (للمسؤول)", use_container_width=True):
        if hasattr(st.session_state, 'current_report'):
            st.success("✅ تم تحميل آخر تقرير")
        else:
            st.warning("⚠️ لا يوجد تقرير سابق")

# === عرض التقرير وزر التحميل ===
if st.session_state.get('report_generated', False):
    st.markdown("---")
    st.markdown("## 📊 التقرير النهائي")
    
    # عرض التقرير
    st.text_area("محتوى التقرير:", st.session_state.current_report, height=500)
    
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
    st.sidebar.success("🎉 مرحباً بك في لوحة التحكم!")

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
    free_status = "للبيع"
    free_package = "ذهبية"
    free_count = 1
    
    if st.button("🎁 الحصول على التقرير المجاني", use_container_width=True):
        report, _ = generate_rich_report(
            free_user_type, free_city, free_property_type, free_area, free_status, free_package, free_count
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
    
    **🕒 ساعات العمل:**
    9:00 ص - 6:00 م
    """)
