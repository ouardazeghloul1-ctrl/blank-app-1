import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import plotly.express as px
import time
import io
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display

# إعداد الصفحة
st.set_page_config(page_title="Warda Intelligence", layout="wide")

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
    .metric-card {
        background: linear-gradient(135deg, #2a2a2a, #3a3a3a);
        padding: 15px; border-radius: 10px; border: 1px solid #d4af37;
        margin: 10px; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: gold;'>🏙️ منصة التحليل العقاري الذهبي - Warda Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37;'>تحليل ذكي مخصص لكل فئة - قرارات استثمارية مدروسة</p>", unsafe_allow_html=True)

# === نظام الباقات والأسعار ===
PACKAGES = {
    "مجانية": {"price": 0, "features": ["تحليل سوق أساسي", "أسعار متوسطة للمنطقة", "تقرير نصي بسيط", "صالح لعقار واحد"]},
    "فضية": {"price": 29, "features": ["كل مميزات المجانية +", "تحليل تنبؤي 6 أشهر", "مقارنة مع 5 مشاريع مشابهة", "نصائح استثمارية متقدمة", "تقرير PDF تفاعلي", "رسوم بيانية متحركة", "تحليل المنافسين", "دراسة الجدوى المبدئية"]},
    "ذهبية": {"price": 79, "features": ["كل مميزات الفضية +", "تحليل ذكاء اصطناعي متقدم", "تنبؤات لمدة سنة كاملة", "دراسة الجدوى الاقتصادية الشاملة", "تحليل 10 منافسين رئيسيين", "نصائح مخصصة حسب الفئة", "مؤشرات أداء مفصلة", "تحليل المخاطر المتقدم"]},
    "ماسية": {"price": 149, "features": ["كل مميزات الذهبية +", "تحليل شمولي متكامل", "تقارير مقارنة مع كل المدن", "تحليل المخاطرة المتقدم", "خطة استثمارية تفصيلية", "محاكاة سيناريوهات متعددة", "تحليل توقيت السوق", "توصيات استراتيجية شاملة"]}
}

# === بيانات سوقية متقدمة ===
def generate_advanced_market_data(city, property_type, status):
    base_prices = {
        "الرياض": {"شقة": {"سكني": 4500, "فاخر": 6500, "اقتصادي": 3200}, "فيلا": {"سكني": 3200, "فاخر": 4800, "اقتصادي": 2400}, "أرض": {"سكني": 1800, "تجاري": 3500, "استثماري": 2200}, "محل تجاري": {"مركزي": 8000, "تجاري": 6000, "حيوي": 4500}},
        "جدة": {"شقة": {"سكني": 3800, "فاخر": 5500, "اقتصادي": 2800}, "فيلا": {"سكني": 2800, "فاخر": 4200, "اقتصادي": 2000}, "أرض": {"سكني": 1500, "تجاري": 2800, "استثماري": 1800}, "محل تجاري": {"مركزي": 6500, "تجاري": 5000, "حيوي": 3800}}
    }
    city_data = base_prices.get(city, base_prices["الرياض"])
    property_data = city_data.get(property_type, {"سكني": 3000})
    avg_price = np.mean(list(property_data.values()))
    price_multiplier = 1.12 if status == "للبيع" else 0.88 if status == "للشراء" else 0.95
    return {
        'السعر_الحالي': avg_price * price_multiplier,
        'متوسط_السوق': avg_price,
        'أعلى_سعر': avg_price * 1.35,
        'أقل_سعر': avg_price * 0.75,
        'حجم_التداول_شهري': np.random.randint(150, 600),
        'معدل_النمو_الشهري': np.random.uniform(0.8, 3.5),
        'عرض_العقارات': np.random.randint(80, 250),
        'طالب_الشراء': np.random.randint(120, 400),
        'معدل_الإشغال': np.random.uniform(75, 95),
        'العائد_التأجيري': np.random.uniform(6, 12),
        'مؤشر_السيولة': np.random.uniform(60, 90)
    }

# === تحليلات متقدمة ===
def get_advanced_analysis_by_user_type(user_type, city, property_type, area, status):
    analyses = {
        "مستثمر": {
            "title": "📊 التحليل الاستثماري الشامل",
            "sections": {
                "التحليل_المالي": """
عزيزي المستثمر، في هذا التحليل المالي، سأقدم لك نظرة شاملة تساعدك على اتخاذ قرار استثماري موفق. بناءً على بيانات السوق، العائد على الاستثمار (ROI) يبلغ 9.5% سنويًا، وهو مؤشر قوي يعكس جودة الفرص الحالية. صافي القيمة الحالية (NPV) يقترب من +$45,000، مما يعني أن استثمارك سيدر ربحًا واضحًا على المدى البعيد. معدل العائد الداخلي (IRR) عند 11.2% يعد جيدًا جدًا، بينما فترة استرداد رأس المال 8.2 سنة متوسطة، ويمكن تحسينها إذا ركزت على مناطق مثل القدية. نسبة الدين إلى الحقوق عند 65% مريحة وتتيح لك مرونة في التمويل.

بالنسبة للتدفقات النقدية، في السنة الأولى، يمكنك توقع إيرادات شهرية حوالي $2,800 مقابل مصروفات $1,200، مما يعني صافي تدفق $1,600 شهريًا و$19,200 سنويًا. على مدى 5 سنوات، الإيرادات الإجمالية قد تصل إلى $168,000 بينما المصروفات $72,000، لتترك لك ربحًا تراكميًا $96,000. أنصحك بمراجعة هذه الأرقام مع خبير مالي لتأكيدها حسب وضعك الشخصي، لكن النتيجة تبدو مشجعة جدًا!
                """,
                "استراتيجيات_الاستثمار": """
عزيزي المستثمر، الاستراتيجية الأمثل في الوقت الحالي هي الشراء والتأجير طويل الأجل، وهي طريقة أثبتت نجاحها في السوق العقاري. هذه الخطة توفر تدفقات نقدية ثابتة شهريًا، وتحمي استثمارك من التضخم، بل وتفتح الباب لإعفاءات ضريبية محتملة. من تجربتي، ارتفاع القيمة السوقية مع الزمن يجعل هذا الخيار استثمارًا ذكيًا. لتنفيذها، ابدأ بالبحث عن 3-5 عقارات وتفاوض عليها في الشهور الأولى (1-3)، ثم ركز على التمويل والتجهيزات في (4-6)، وانتقل للتأجير وإدارة الممتلكات في (7-9)، وأخيرًا قم بتقييم الأداء وإجراء التعديلات في (10-12).

أما بالنسبة لتوزيع محفظتك، أقترح تخصيص 40% لشقق سكنية ($200,000، عائد 8-10%) لاستقرارها، 30% لمحلات تجارية ($150,000، عائد 10-12%) لارتفاع الطلب، 20% لفيلات ($100,000، عائد 7-9%) للتنويع، و10% لأراضي ($50,000، عائد 12-15%) للنمو العالي. يمكنك تعديل هذا التوزيع حسب ميزانيتك، لكن التنويع سيقلل المخاطر ويزيد الأرباح.
                """,
                "إدارة_المخاطر": """
عزيزي المستثمر، إدارة المخاطر هي مفتاح النجاح في أي استثمار. بناءً على تحليلي، مخاطر السوق تشكل 30%، مثل تقلبات الأسعار أو التغيرات الاقتصادية أو المنافسة الجديدة، وأنصحك باختيار مناطق مستقرة مثل المربع لتجنبها. مخاطر التشغيل 25%، مثل صعوبة إيجاد مستأجرين أو تكاليف صيانة غير متوقعة أو مشاكل قانونية، يمكن تقليلها بتوظيف شركة إدارة ممتلكات موثوقة. أما مخاطر التمويل 20%، مثل ارتفاع الفائدة أو صعوبة إعادة التمويل، فيمكن مواجهتها بقروض ذات فائدة ثابتة.

للتخفيف، أقترح التنويع في 3 مناطق جغرافية مختلفة، واستخدام عقود خيارات لتحوط السعر، وضع احتياطي نقدي يغطي 6 أشهر، وتأمين شامل ضد المخاطر. بهذه الطريقة، ستكون استثماراتك محمية ومستدامة.
                """,
                "الفرص_المستقبلية": """
عزيزي المستثمر، السوق العقاري في السعودية يشهد نموًا كبيرًا بفضل رؤية 2030، وهناك فرص ذهبية تنتظرك. في الرياض، المنطقة الشمالية (مشروع القدية) تقدم معدل نمو 15% سنويًا، مع مشاريع تطوير ضخمة وطلب متزايد على الوحدات السكنية، وأنصحك بالاستثمار المبكر هنا لتحقيق أرباح كبيرة. أما المنطقة المركزية (المربع) فتوفر استقرارًا في الأسعار وطلبًا دائمًا من الموظفين الحكوميين، مع إشغال مرتفع على مدار العام، مما يجعلها خيارًا آمنًا للتدفق النقدي.

وفقًا لتوقعات الذكاء الاصطناعي، نمو السوق 7.8% في 2024، مع ارتفاع أسعار المواد 4.2% وزيادة الطلب السكني 12.5%، وهذا يعني أن الوقت مناسب جدًا للشراء. إذا أردت، يمكننا مناقشة خطة مخصصة تناسب أهدافك!
                """
            }
        }
    }
    return analyses.get(user_type, analyses["مستثمر"])

# === توليد تقرير مع PDF ورسوم ===
def generate_advanced_report(user_type, city, property_type, area, status, package, property_count):
    base_price = PACKAGES[package]["price"]
    total_price = base_price * property_count
    market_data = generate_advanced_market_data(city, property_type, status)
    advanced_analysis = get_advanced_analysis_by_user_type(user_type, city, property_type, area, status)
    
    report_content = []
    cover_page = f"""
    🏙️ تقرير Warda Intelligence المتقدم
    {'=' * 60}
    
    📊 **التقرير الاستثماري الشامل**
    🎯 مخصص لفئة: {user_type}
    🏙️ المنطقة: {city}
    🏠 نوع العقار: {property_type}
    
    📅 تاريخ الإصدار: {datetime.now().strftime('%Y-%m-%d')}
    ⏰ وقت الإنشاء: {datetime.now().strftime('%H:%M')}
    🔢 رقم التقرير: WR-{datetime.now().strftime('%Y%m%d%H%M')}
    
    💼 **معلومات العميل:**
    ┌─ 🏷️ الفئة: {user_type}
    ├─ 🏙️ المدينة: {city} 
    ├─ 🏠 نوع العقار: {property_type}
    ├─ 📏 المساحة: {area} م²
    ├─ 📌 الحالة: {status}
    ├─ 🔢 عدد العقارات: {property_count}
    ├─ 💎 الباقة: {package}
    └─ 💰 القيمة: {total_price} دولار
    
    📈 **ملخص الأداء:**
    ├─ 📊 تصنيف الاستثمار: {'🟢 ممتاز' if market_data['العائد_التأجيري'] > 8 else '🟡 جيد'}
    ├─ 💸 العائد المتوقع: {market_data['العائد_التأجيري']:.1f}% سنوياً
    ├─ 📈 نمو رأس المال: {market_data['معدل_النمو_الشهري']*12:.1f}% سنوياً
    ├─ 🛡️ مستوى المخاطرة: {np.random.randint(15, 35)}%
    └─ ⭐ التوصية: {'🟢 شراء مستعجل' if market_data['معدل_النمو_الشهري'] > 2 else '🟡 شراء مدروس'}
    
    {'=' * 60}
    """
    report_content.append(cover_page)
    
    for section_title, section_content in advanced_analysis["sections"].items():
        report_content.append(f"""
    📑 الصفحة {report_content.count('=') // 2 + 2}: {section_title.replace('_', ' ').title()}
    {'=' * 60}
    
    {section_content}
    
    {'=' * 60}
    """)

    # توليد الرسوم
    fig1 = px.line(x=[2024, 2025, 2026], y=[market_data['متوسط_السوق']*0.95, market_data['السعر_الحالي'], market_data['أعلى_سعر']], 
                   title="نمو أسعار العقارات", color_discrete_sequence=['gold'])
    fig2 = px.pie(values=[market_data['العائد_التأجيري'], 100-market_data['العائد_التأجيري']], names=['عائد', 'مخاطر'], 
                  title="توزيع العوائد", color_discrete_sequence=['gold', 'gray'])
    fig3 = px.bar(x=['شقق', 'محلات', 'فيلات', 'أراضي'], y=[40, 30, 20, 10], 
                  title="محفظة الاستثمار", color_discrete_sequence=['gold'])
    fig4 = px.pie(values=[30, 25, 20], names=['سوق', 'تشغيل', 'تمويل'], 
                  title="مستويات المخاطر", color_discrete_sequence=['gold', 'gray', 'lightgray'])
    fig5 = px.bar(x=['نيوم', 'الدرعية', 'المالي'], y=[18, 14, 12], 
                  title="الفرص الإقليمية", color_discrete_sequence=['gold'])
    
    figs = [fig1, fig2, fig3, fig4, fig5]
    
    return "\n\n".join(report_content), total_price, figs, market_data

# === إنشاء PDF مع خط Amiri ===
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('Amiri', '', os.path.join('fonts', 'Amiri-Regular.ttf'), uni=True)

    def header(self):
        self.set_font('Amiri', 'B', 16)
        self.cell(0, 10, "🏙️ تقرير Warda Intelligence", 0, 1, "C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Amiri', 'B', 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Amiri', '', 10)
        reshaped_text = arabic_reshaper.reshape(body)
        displayed_text = get_display(reshaped_text)
        self.multi_cell(0, 5, displayed_text)
        self.ln()

    def add_image(self, img_buffer):
        self.image(img_buffer, x=10, y=self.get_y(), w=190)
        self.ln(10)

# === الواجهة الرئيسية ===
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👤 بيانات المستخدم")
    user_type = st.selectbox("اختر فئتك:", ["مستثمر", "وسيط عقاري", "شركة تطوير", "فرد", "باحث عن فرصة", "مالك عقار"])
    city = st.selectbox("المدينة:", ["الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة", "الخبر", "تبوك", "الطائف"])
    property_type = st.selectbox("نوع العقار:", ["شقة", "فيلا", "أرض", "محل تجاري"])
    status = st.selectbox("الحالة:", ["للبيع", "للشراء", "للإيجار"])
    area = st.slider("المساحة (م²):", 50, 1000, 120)

with col2:
    st.markdown("### 💎 اختيار الباقة")
    property_count = st.slider("🔢 عدد العقارات للتحليل:", 1, 50, 1, help="كلما زاد عدد العقارات، زادت دقة التحليل والسعر")
    chosen_pkg = st.radio("اختر باقتك:", list(PACKAGES.keys()))
    base_price = PACKAGES[chosen_pkg]["price"]
    total_price = base_price * property_count
    st.markdown(f"<div class='package-card'><h3>باقة {chosen_pkg}</h3><h4>{total_price} دولار</h4></div>", unsafe_allow_html=True)
    st.markdown("**المميزات:**")
    for feature in PACKAGES[chosen_pkg]["features"]:
        st.write(f"✅ {feature}")

# === نظام الدفع ===
st.markdown("---")
st.markdown(f"### 💰 السعر النهائي: **{total_price} دولار**")
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

# === زر إنشاء التقرير ===
st.markdown("---")
st.markdown("### 🚀 إنشاء التقرير")
col1, col2 = st.columns(2)
with col1:
    if st.button("🎯 إنشاء التقرير (للمسؤول)", use_container_width=True):
        with st.spinner("🔄 جاري إنشاء التقرير المتقدم..."):
            time.sleep(3)
            report, final_price, figs, market_data = generate_advanced_report(user_type, city, property_type, area, status, chosen_pkg, property_count)
            st.session_state.current_report = report
            st.session_state.figs = figs
            st.session_state.report_generated = True
            st.success("✅ تم إنشاء التقرير المتقدم!")

with col2:
    if st.button("📥 تحميل التقرير (بعد الدفع)", use_container_width=True):
        if hasattr(st.session_state, 'current_report'):
            st.success("✅ تم تحميل التقرير")
        else:
            st.warning("⚠️ يرجى إتمام عملية الدفع أولاً")

# === عرض التقرير وتحميل PDF ===
if st.session_state.get('report_generated', False):
    st.markdown("---")
    st.markdown("## 📊 التقرير النهائي المتقدم")
    st.text_area("محتوى التقرير:", st.session_state.current_report, height=600)
    
    # إنشاء PDF
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    for page in st.session_state.current_report.split("\n\n"):
        if "📑" in page:
            pdf.chapter_title(page.split("\n")[0].replace("📑", "").strip())
            pdf.chapter_body("\n".join(page.split("\n")[1:]).strip())
        else:
            pdf.chapter_body(page)
    
    for i, fig in enumerate(st.session_state.figs):
        img_buffer = io.BytesIO()
        fig.write_image(img_buffer, format='png', width=600, height=400, scale=2)
        img_buffer.seek(0)
        pdf.add_page()
        pdf.add_image(img_buffer)
    
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    st.download_button(
        label="📥 تحميل التقرير الكامل (PDF)",
        data=pdf_buffer,
        file_name=f"تقرير_متقدم_{user_type}_{city}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
    st.success("🎉 تم إنشاء التقرير المتقدم بنجاح! يحتوي على 5 صفحات و5 رسوم بيانية")
    st.balloons()

# === لوحة المسؤول ===
admin_password = st.sidebar.text_input("كلمة مرور المسؤول:", type="password")
if admin_password == "WardaAdmin2024":
    st.sidebar.success("🎉 مرحباً بك في لوحة التحكم!")
    st.sidebar.markdown("### 🛠️ لوحة تحكم المسؤول")
    if st.sidebar.button("🔗 إنشاء رابط مؤثرين جديد"):
        today = datetime.now().strftime("%Y%m%d")
        influencer_token = np.random.randint(1000, 9999)
        st.session_state.influencer_url = f"https://warda-intelligence.streamlit.app/?promo={influencer_token}"
        st.sidebar.success("✅ تم إنشاء الرابط الجديد")
    if hasattr(st.session_state, 'influencer_url'):
        st.sidebar.markdown(f"**رابط المؤثرين:**")
        st.sidebar.code(st.session_state.influencer_url)

# === عرض المؤثرين ===
st.markdown("---")
st.markdown("### 🎁 عرض المؤثرين")
query_params = st.experimental_get_query_params()
if query_params.get('promo'):
    promo_token = query_params['promo'][0]
    st.success("🎉 تم تفعيل العرض المجاني للمؤثرين!")
    free_user_type, free_city, free_property_type, free_area, free_status, free_package, free_count = "مؤثر", "الرياض", "شقة", 120, "للبيع", "ذهبية", 1
    if st.button("🎁 الحصول على التقرير المجاني", use_container_width=True):
        report, _, figs, _ = generate_advanced_report(free_user_type, free_city, free_property_type, free_area, free_status, free_package, free_count)
        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        for page in report.split("\n\n"):
            if "📑" in page:
                pdf.chapter_title(page.split("\n")[0].replace("📑", "").strip())
                pdf.chapter_body("\n".join(page.split("\n")[1:]).strip())
            else:
                pdf.chapter_body(page)
        for i, fig in enumerate(figs):
            img_buffer = io.BytesIO()
            fig.write_image(img_buffer, format='png', width=600, height=400, scale=2)
            img_buffer.seek(0)
            pdf.add_page()
            pdf.add_image(img_buffer)
        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        st.download_button(
            label="📥 تحميل التقرير المجاني (PDF)",
            data=pdf_buffer,
            file_name=f"تقرير_مجاني_لمؤثر_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
else:
    st.info("**للمؤثرين:** للحصول على تقرير مجاني، يرجى استخدام الرابط الخاص الذي تم توفيره من إدارة المنصة.")

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
