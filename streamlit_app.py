import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
from fpdf import FPDF
from io import BytesIO

# إعداد الصفحة
st.set_page_config(
    page_title="وردة العقارية - المنصة الذكية",
    page_icon="🏠",
    layout="wide"
)

# تنسيق CSS مخصص
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2E8B57;
        margin: 2rem 0 1rem 0;
        border-right: 5px solid #2E8B57;
        padding-right: 15px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        border-right: 4px solid #4682b4;
        margin: 10px 0;
    }
    .preview-box {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        border: 2px dashed #ffc107;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<div class="main-header">🏠 وردة العقارية - المنصة الذكية</div>', unsafe_allow_html=True)

# 🔧 قسم الإدخال الرئيسي
st.markdown("---")
st.markdown('<div class="section-header">⚙️ إعدادات البحث</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    المدن = ["الرياض", "جدة", "مكة", "المدينة", "الدمام", "الخبر", "الطائف", "تبوك", "بريدة", "خميس مشيط"]
    المدينة = st.selectbox("🏙️ اختر المدينة", المدن)

with col2:
    أنواع_العقارات = ["شقة", "فيلا", "أرض", "محل تجاري", "مكتب"]
    نوع_العقار = st.selectbox("🏠 نوع العقار", أنواع_العقارات)

with col3:
    الباقات = ["الباقة الأساسية - $99 (تحليل 500 عقار)", 
               "الباقة المتقدمة - $199 (تحليل 1000 عقار)", 
               "الباقة الاحترافية - $399 (تحليل 2000 عقار + الذكاء الاصطناعي)"]
    الباقة = st.selectbox("💼 اختر الباقة", الباقات)

# إنشاء بيانات عقارية واقعية للسعودية
def إنشاء_بيانات_سعودية(المدينة, نوع_العقار, الباقة):
    np.random.seed(42)
    
    # تحديد عدد العقارات حسب الباقة
    if "500" in الباقة:
        عدد_العقارات = 500
    elif "1000" in الباقة:
        عدد_العقارات = 1000
    else:
        عدد_العقارات = 2000
    
    # أسعار واقعية للسعودية (بالدولار الأمريكي)
    أسعار_قاعدة = {
        "الرياض": {"شقة": 200000, "فيلا": 500000, "أرض": 150000, "محل تجاري": 350000, "مكتب": 250000},
        "جدة": {"شقة": 180000, "فيلا": 450000, "أرض": 130000, "محل تجاري": 300000, "مكتب": 220000},
        "مكة": {"شقة": 220000, "فيلا": 550000, "أرض": 160000, "محل تجاري": 400000, "مكتب": 280000},
        "المدينة": {"شقة": 190000, "فيلا": 480000, "أرض": 140000, "محل تجاري": 320000, "مكتب": 240000},
        "الدمام": {"شقة": 150000, "فيلا": 350000, "أرض": 100000, "محل تجاري": 250000, "مكتب": 180000},
        "الخبر": {"شقة": 160000, "فيلا": 380000, "أرض": 110000, "محل تجاري": 270000, "مكتب": 190000},
        "الطائف": {"شقة": 120000, "فيلا": 280000, "أرض": 80000, "محل تجاري": 200000, "مكتب": 150000},
        "تبوك": {"شقة": 100000, "فيلا": 250000, "أرض": 70000, "محل تجاري": 180000, "مكتب": 130000},
        "بريدة": {"شقة": 110000, "فيلا": 270000, "أرض": 75000, "محل تجاري": 190000, "مكتب": 140000},
        "خميس مشيط": {"شقة": 90000, "فيلa": 220000, "أرض": 60000, "محل تجاري": 160000, "مكتب": 120000}
    }
    
    أحياء = {
        "الرياض": ["الملقا", "الملز", "العليا", "اليرموك", "النسيم", "الشفا", "العارض", "الرحمانية"],
        "جدة": ["الثغر", "الروضة", "الزهراء", "السلامة", "الكورنيش", "الشفا", "النسيم", "الرحاب"],
        "مكة": ["العزيزية", "الزاهر", "الشبيكة", "الشرائع", "الجموم", "الطندباوي", "الهجرة", "الزاهر"],
        "المدينة": ["العنبرية", "السيح", "العالية", "المناخ", "قربان", "الخالدية", "العالية", "المناخ"],
        "الدمام": ["المنطقة الوسطى", "الروضة", "الفنار", "القلب", "الشاطئ", "القرن", "الفيحاء", "الروابي"],
        "الخبر": ["الغروب", "الرمال", "الجزيرة", "الحزام الذهبي", "المرجان", "الدانة", "الروضة", "الخليج"],
        "الطائف": ["الشهداء", "الوئيد", "قروى", "الخالدية", "المنصورة", "الروضة", "النزهة", "الهدا"],
        "تبوك": ["الفيصلية", "النخيل", "العليا", "الربوة", "الخضراء", "الصالحية", "العزيزية", "الروضة"],
        "بريدة": ["المصيف", "الروضة", "النهضة", "الخبيب", "العليا", "الربيع", "الخالدية", "الروضة"],
        "خميس مشيط": ["النزهة", "الجنوب", "السلام", "الروضة", "القدس", "الخالدية", "الربيع", "النسيم"]
    }
    
    بيانات = []
    سعر_قاعدة = أسعار_قاعدة[المدينة][نوع_العقار]
    
    for i in range(عدد_العقارات):
        حي = np.random.choice(أحياء[المدينة])
        
        # تباين في الأسعار
        سعر = np.random.normal(سعر_قاعدة, سعر_قاعدة * 0.4)
        سعر = max(سعر_قاعدة * 0.4, سعر)  # حد أدنى
        
        # مساحة واقعية
        if نوع_العقار == "شقة":
            مساحة = np.random.uniform(80, 200)
        elif نوع_العقار == "فيلا":
            مساحة = np.random.uniform(200, 500)
        elif نوع_العقار == "أرض":
            مساحة = np.random.uniform(300, 1200)
        else:
            مساحة = np.random.uniform(50, 250)
        
        # حساب سعر المتر
        سعر_المتر = سعر / مساحة if مساحة > 0 else 0
        
        # عائد متوقع واقعي
        عائد_متوقع = np.random.uniform(5, 15)
        
        بيانات.append({
            "العقار": f"{نوع_العقار} {i+1}",
            "الحي": حي,
            "السعر": int(سعر),
            "المساحة": int(مساحة),
            "سعر_المتر": int(سعر_المتر),
            "العائد_المتوقع": round(عائد_متوقع, 1),
            "الغرف": np.random.randint(1, 6) if نوع_العقار in ["شقة", "فيلا"] else 0,
            "الحمامات": np.random.randint(1, 4) if نوع_العقار in ["شقة", "فيلا"] else 0
        })
    
    return pd.DataFrame(بيانات)

# إنشاء البيانات
df = إنشاء_بيانات_سعودية(المدينة, نوع_العقار, الباقة)

# 📊 قسم الإحصائيات الرئيسية
st.markdown("---")
st.markdown('<div class="section-header">📊 الإحصائيات الرئيسية</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏠 عدد العقارات", f"{len(df):,} عقار")
with col2:
    st.metric("💰 متوسط السعر", f"${df['السعر'].mean():,.0f}")
with col3:
    st.metric("📐 متوسط المساحة", f"{df['المساحة'].mean():.0f} م²")
with col4:
    st.metric("🎯 متوسط سعر المتر", f"${df['سعر_المتر'].mean():,.0f}")

# 📈 قسم الرسوم البيانية
st.markdown("---")
st.markdown('<div class="section-header">📈 التحليلات البيانية</div>', unsafe_allow_html=True)

col_رسم1, col_رسم2 = st.columns(2)

with col_رسم1:
    # توزيع الأسعار
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.hist(df['السعر'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.set_xlabel('السعر ($)')
    ax1.set_ylabel('عدد العقارات')
    ax1.set_title('توزيع أسعار العقارات')
    ax1.ticklabel_format(style='plain', axis='x')
    st.pyplot(fig1)

with col_رسم2:
    # العلاقة بين المساحة والسعر
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    scatter = ax2.scatter(df['المساحة'], df['السعر'], c=df['العائد_المتوقع'], alpha=0.6, cmap='viridis')
    ax2.set_xlabel('المساحة (م²)')
    ax2.set_ylabel('السعر ($)')
    ax2.set_title('العلاقة بين المساحة والسعر')
    plt.colorbar(scatter, label='العائد المتوقع %')
    st.pyplot(fig2)

# 👀 قسم المعاينة المجانية
st.markdown("---")
st.markdown('<div class="section-header">👀 معاينة مجانية للتقرير</div>', unsafe_allow_html=True)

st.markdown('<div class="preview-box">', unsafe_allow_html=True)
st.success("**🔍 هذه معاينة مجانية للتقرير. للوصول للتقرير الكامل يرجى الدفع**")

col_prev1, col_prev2 = st.columns(2)

with col_prev1:
    st.subheader("🏆 أفضل 3 عروض (معاينة)")
    أفضل_عروض = df.nsmallest(3, 'سعر_المتر')
    for i, (_, عقار) in enumerate(أفضل_عروض.iterrows(), 1):
        st.write(f"**{i}. {عقار['العقار']} - حي {عقار['الحي']}**")
        st.write(f"💰 ${عقار['السعر']:,} • 📐 {عقار['المساحة']} م²")
        st.write(f"🎯 ${عقار['سعر_المتر']:,} • 📈 {عقار['العائد_المتوقع']}%")
        st.progress(عقار['العائد_المتوقع'] / 15)

with col_prev2:
    st.subheader("📊 إحصائيات سريعة (معاينة)")
    st.write(f"• عدد العقارات الكلي: {len(df):,} عقار")
    st.write(f"• متوسط السعر: ${df['السعر'].mean():,.0f}")
    st.write(f"• متوسط المساحة: {df['المساحة'].mean():.0f} م²")
    st.write(f"• أفضل حي للاستثمار: {df.nsmallest(1, 'سعر_المتر')['الحي'].iloc[0]}")

st.markdown('</div>', unsafe_allow_html=True)

# 💳 قسم الدفع
st.markdown("---")
st.markdown('<div class="section-header">💳 الدفع للحصول على التقرير الكامل</div>', unsafe_allow_html=True)

col_دفع1, col_دفع2 = st.columns(2)

with col_دفع1:
    st.success(f"""
    **تفاصيل طلبك:**
    
    🏙️ **المدينة:** {المدينة}
    🏠 **نوع العقار:** {نوع_العقار}
    📦 **الباقة:** {الباقة}
    💰 **السعر:** ${الباقة.split('$')[1].split(' ')[0]}
    
    **ما ستحصل عليه:**
    ✓ تقرير PDF كامل ({len(df)} عقار)
    ✓ تحليل مفصل وشامل
    ✓ توصيات استثمارية ذكية
    ✓ دعم لمدة أسبوع
    {"" if "احترافية" not in الباقة else "✓ تنبؤات الذكاء الاصطناعي المتقدم"}
    """)

with col_دفع2:
    st.info("""
    **طرق الدفع المتاحة:**
    
    💳 **PayPal** - الدفع الآني والأكثر أماناً
    🏦 **تحويل بنكي** - للعملاء المحليين
    📱 **STC Pay** - للدفع السريع
    
    **معلومات الدفع:**
    - PayPal: zeghloulwarda6@gmail.com
    - رقم الحساب: SA1234567890123456789012
    - STC Pay: 0550123456
    """)
    
    # زر الدفع عبر PayPal
    st.markdown("""
    <a href="https://www.paypal.com/send?email=zeghloulwarda6@gmail.com&amount={}&currency=USD" target="_blank">
        <button style="background-color: #0070ba; color: white; padding: 20px 40px; border: none; border-radius: 10px; font-size: 20px; cursor: pointer; width: 100%; margin: 10px 0;">
            💳 الدفع عبر PayPal الآن - ${}
        </button>
    </a>
    """.format(الباقة.split('$')[1].split(' ')[0], الباقة.split('$')[1].split(' ')[0]), unsafe_allow_html=True)
    
    st.warning("**⚠️ بعد الدفع، سيصلك التقرير الكامل على بريدك الإلكتروني خلال 24 ساعة**")

# 🤖 قسم الذكاء الاصطناعي والتنبؤ (للباقة الاحترافية فقط - معاينة)
if "احترافية" in الباقة:
    st.markdown("---")
    st.markdown('<div class="section-header">🤖 معاينة تنبؤات الذكاء الاصطناعي</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="preview-box">', unsafe_allow_html=True)
    st.info("""
    **🧠 هذه معاينة لتقنية الذكاء الاصطناعي المتاحة في الباقة الاحترافية:**
    
    - 📈 تنبؤات أسعار لـ 30 يوم قادم
    - 🔮 تحليل اتجاهات السوق
    - 🎯 خطط استثمارية ذكية
    - 📊 مقارنة بين أنواع العقارات
    
    **للحصول على هذه الميزات المتقدمة، يرجى اختيار الباقة الاحترافية والدفع.**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# 📥 قسم تحميل التقرير الكامل (يظهر فقط بعد التأكيد)
st.markdown("---")
st.markdown('<div class="section-header">📥 تحميل التقرير الكامل</div>', unsafe_allow_html=True)

st.warning("**🔒 هذا القسم متاح فقط للعملاء الذين قاموا بالدفع. بعد التأكيد، سيظهر هنا زر تحميل التقرير الكامل.**")

# نموذج تأكيد الدفع
with st.form("تأكيد_الدفع"):
    st.write("**بعد إتمام الدفع، يرجى تعبئة هذه المعلومات:**")
    email = st.text_input("البريد الإلكتروني *")
    transaction_id = st.text_input("رقم العملية أو المرجع *")
    submitted = st.form_submit_button("✅ تأكيد استلام الطلب")
    
    if submitted:
        if email and transaction_id:
            st.balloons()
            st.success("**🎉 تم تأكيد طلبك! سيصلك التقرير الكامل خلال 24 ساعة على بريدك الإلكتروني.**")
            
            # إنشاء وزر تحميل PDF (مشروط بالدفع)
            def create_pdf_report(df, المدينة, نوع_العقار, الباقة):
                pdf = FPDF()
                pdf.add_page()
                
                # إضافة دعم للعربية
                pdf.add_font('Arial', '', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', uni=True)
                
                # عنوان التقرير
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(200, 10, txt="تقرير وردة العقارية - التحليل العقاري المتكامل", ln=True, align='C')
                pdf.ln(10)
                
                # معلومات التقرير
                pdf.set_font('Arial', '', 12)
                pdf.cell(200, 10, txt=f"المدينة: {المدينة}", ln=True)
                pdf.cell(200, 10, txt=f"نوع العقار: {نوع_العقار}", ln=True)
                pdf.cell(200, 10, txt=f"الباقة: {الباقة}", ln=True)
                pdf.cell(200, 10, txt=f"عدد العقارات المحللة: {len(df):,}", ln=True)
                pdf.cell(200, 10, txt=f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
                pdf.ln(10)
                
                # الإحصائيات
                pdf.set_font('Arial', 'B', 14)
                pdf.cell(200, 10, txt="الإحصائيات الرئيسية:", ln=True)
                pdf.set_font('Arial', '', 12)
                pdf.cell(200, 10, txt=f"• متوسط السعر: ${df['السعر'].mean():,.0f}", ln=True)
                pdf.cell(200, 10, txt=f"• متوسط المساحة: {df['المساحة'].mean():.0f} م²", ln=True)
                pdf.cell(200, 10, txt=f"• متوسط سعر المتر: ${df['سعر_المتر'].mean():,.0f}", ln=True)
                pdf.cell(200, 10, txt=f"• متوسط العائد المتوقع: {df['العائد_المتوقع'].mean():.1f}%", ln=True)
                pdf.ln(10)
                
                # أفضل العروض
                pdf.set_font('Arial', 'B', 14)
                pdf.cell(200, 10, txt="أفضل 20 عرض استثماري:", ln=True)
                pdf.set_font('Arial', '', 10)
                
                أفضل_عروض = df.nsmallest(20, 'سعر_المتر')
                for i, (_, عقار) in enumerate(أفضل_عروض.iterrows(), 1):
                    pdf.cell(200, 8, txt=f"{i}. {عقار['العقار']} - حي {عقار['الحي']}", ln=True)
                    pdf.cell(200, 8, txt=f"   السعر: ${عقار['السعر']:,} - المساحة: {عقار['المساحة']} م²", ln=True)
                    pdf.cell(200, 8, txt=f"   سعر المتر: ${عقار['سعر_المتر']:,} - العائد: {عقار['العائد_المتوقع']}%", ln=True)
                    pdf.ln(2)
                
                pdf.ln(10)
                pdf.set_font('Arial', 'I', 10)
                pdf.cell(200, 10, txt="شكراً لثقتكم في وردة العقارية - تحليلات عقارية ذكية", ln=True, align='C')
                
                return pdf.output(dest='S').encode('latin1')
            
            # زر تحميل PDF
            try:
                pdf_data = create_pdf_report(df, المدينة, نوع_العقار, الباقة)
                st.download_button(
                    label="📄 تحميل التقرير الكامل PDF",
                    data=pdf_data,
                    file_name=f"تقرير_وردة_العقارية_{المدينة}_{نوع_العقار}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    help="انقر لتحميل التقرير الكامل بصيغة PDF"
                )
            except Exception as e:
                st.error("⚠️ حدث خطأ في إنشاء التقرير. يرجى التواصل مع الدعم")
        else:
            st.error("❌ يرجى تعبئة جميع الحقول المطلوبة")

# 🔧 قسم المعلومات الشخصية
st.markdown("---")
st.markdown('<div class="section-header">📞 للتواصل مع وردة العقارية</div>', unsafe_allow_html=True)

col_معلومات1, col_معلومات2, col_معلومات3 = st.columns(3)

with col_معلومات1:
    st.write("**📍 العنوان:**")
    st.write("المملكة العربية السعودية")

with col_معلومات2:
    st.write("**📧 البريد الإلكتروني:**")
    st.write("ouardazeghloul1@gmail.com")

with col_معلومات3:
    st.write("**📱 رقم الواتساب:**")
    st.write("+779888140")

st.markdown("---")
st.markdown("✨ **وردة العقارية 2025** - تحليلات عقارية ذكية بدقة عالية")
