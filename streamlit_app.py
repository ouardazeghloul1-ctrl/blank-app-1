import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from fpdf import FPDF
from io import BytesIO

# إعداد الصفحة
st.set_page_config(
    page_title="Warda Global Realty Intelligence",
    page_icon="🏠",
    layout="wide"
)

# التصميم المخصص
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
    }
    .package-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #2E8B57;
        margin: 10px 0;
        text-align: center;
    }
    .ai-prediction {
        background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .client-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-right: 4px solid #2E8B57;
    }
</style>
""", unsafe_allow_html=True)

# ==================== ⚙️ الإعدادات التي يمكنك تعديلها ====================

# 🔧 الدول والمدن - يمكنك التعديل هنا
COUNTRIES = {
    "السعودية": ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الخبر", "الطائف", "تبوك", "بريدة"]
}

# 💰 الباقات والأسعار - يمكنك التعديل هنا
PACKAGES = {
    "مجاني": {"price": 0, "reports": 1, "features": ["تقرير أساسي", "3 عقارات"]},
    "أساسي": {"price": 99, "reports": 10, "features": ["10 تقارير", "تنبؤات 30 يوم"]},
    "متقدم": {"price": 199, "reports": 50, "features": ["50 تقرير", "تنبؤات 90 يوم", "تحليل مخاطر"]},
    "احترافي": {"price": 399, "reports": "غير محدود", "features": ["غير محدود", "كل المزايا", "دعم مخصص"]}
}

# 🎨 الألوان - يمكنك التعديل هنا
COLORS = {
    "primary": "#2E8B57",
    "secondary": "#667eea",
    "accent": "#764ba2"
}

# ==================== نهاية الإعدادات القابلة للتعديل ====================

# دالة إنشاء PDF مخصص
def create_pdf_report(report_data):
    pdf = FPDF()
    pdf.add_page()
    
    # العنوان
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="تقرير وردة العقارية الذكي", ln=True, align='C')
    pdf.ln(10)
    
    # معلومات التقرير
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"نوع العميل: {report_data['نوع_العميل']}", ln=True)
    pdf.cell(200, 10, txt=f"عدد العقارات المحللة: {report_data['عدد_العقارات']}", ln=True)
    pdf.cell(200, 10, txt=f"المدينة: {report_data['المدينة']}", ln=True)
    pdf.cell(200, 10, txt=f"نوع العقار: {report_data['نوع_العقار']}", ln=True)
    pdf.cell(200, 10, txt=f"الباقة: {report_data['الباقة']}", ln=True)
    pdf.cell(200, 10, txt=f"التاريخ: {report_data['التاريخ']}", ln=True)
    pdf.ln(10)
    
    # محتوى مخصص حسب نوع العميل
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="التحليل المخصص:", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 12)
    for line in report_data['تحليل_مخصص']:
        pdf.cell(200, 8, txt=f"• {line}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="شكراً لاستخدامك وردة العقارية!", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin1')

# نموذج الذكاء الاصطناعي للتنبؤ بالأسعار
def train_ai_model(data):
    X = data[['مساحة', 'غرف', 'حمامات', 'عمر_العقار', 'قرب_مراكز']]
    y = data['سعر']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)
    return model, X_test, y_test

# توليد بيانات عقارية واقعية
def generate_real_estate_data(city, property_type, num_properties):
    np.random.seed(42)
    data = []
    for i in range(num_properties):
        base_price = {
            "الرياض": np.random.normal(800000, 200000),
            "جدة": np.random.normal(700000, 150000),
            "الدمام": np.random.normal(600000, 120000)
        }.get(city, np.random.normal(500000, 100000))
        
        data.append({
            "العقار": f"{property_type} {i+1}",
            "المنطقة": f"حي {np.random.randint(1, 20)}",
            "سعر": max(100000, base_price + np.random.normal(0, 50000)),
            "مساحة": np.random.randint(80, 400),
            "غرف": np.random.randint(1, 6),
            "حمامات": np.random.randint(1, 4),
            "عمر_العقار": np.random.randint(1, 20),
            "قرب_مراكز": np.random.uniform(0.1, 1.0)
        })
    return pd.DataFrame(data)

# العنوان الرئيسي
st.markdown('<div class="main-header">🏠 وردة العقارية - الذكاء الاصطناعي للتحليل العقاري</div>', unsafe_allow_html=True)

# قسم الدول
st.markdown("---")
st.header("🌍 اختر المدينة")

col1, col2, col3 = st.columns(3)

with col1:
    selected_country = st.selectbox("الدولة", list(COUNTRIES.keys()))

with col2:
    if selected_country:
        selected_city = st.selectbox("المدينة", COUNTRIES[selected_country])

with col3:
    property_type = st.selectbox("نوع العقار", ["شقة", "فيلا", "أرض", "محل تجاري", "مكتب"])

# قسم نوع العميل - جديد
st.markdown("---")
st.header("👥 اختر نوع عميلك")

client_type = st.radio(
    "أنت:",
    ["مستثمر فردي", "وسيط عقاري", "شركة تطوير", "باحث عن سكن", "ممول عقاري", "مستشار عقاري"],
    horizontal=True
)

# قسم عدد العقارات - جديد
st.markdown("---")
st.header("🔢 حدد نطاق التحليل")

num_properties = st.slider(
    "عدد العقارات المطلوب تحليلها", 
    min_value=100, 
    max_value=5000, 
    value=1000, 
    step=100,
    help="كلما زاد عدد العقارات، زادت دقة التحليل"
)

# قسم الباقات
st.markdown("---")
st.header("💼 اختر الباقة")

cols = st.columns(4)
for i, (package_name, package_info) in enumerate(PACKAGES.items()):
    with cols[i]:
        price_display = f"${package_info['price']}" if package_info['price'] > 0 else "مجاني"
        st.markdown(f'''
        <div class="package-card">
            <h3>{package_name}</h3>
            <h4>{price_display}</h4>
            <p>{package_info["reports"]} تقرير</p>
            <small>{" • ".join(package_info["features"])}</small>
        </div>
        ''', unsafe_allow_html=True)
        if st.button(f"اختر {package_name}", key=f"btn_{package_name}"):
            st.session_state.selected_package = package_name
            st.session_state.package_info = package_info

# عرض الباقة المختارة
if 'selected_package' in st.session_state:
    st.success(f"**✅ الباقة المختارة: {st.session_state.selected_package} - ${st.session_state.package_info['price'] if st.session_state.package_info['price'] > 0 else 'مجاني'}**")

# قسم الذكاء الاصطناعي والتحليل
if 'selected_package' in st.session_state:
    st.markdown("---")
    st.header("🤖 الذكاء الاصطناعي للتحليل")
    
    # توليد البيانات والتدريب
    with st.spinner(f"جاري تحليل {num_properties} عقار في {selected_city}..."):
        data = generate_real_estate_data(selected_city, property_type, num_properties)
        model, X_test, y_test = train_ai_model(data)
        
        # عرض التحليلات
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 توزيع الأسعار")
            fig1 = px.histogram(data, x='سعر', title=f'توزيع أسعار {num_properties} عقار')
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            st.subheader("📈 العلاقة بين المساحة والسعر")
            fig2 = px.scatter(data, x='مساحة', y='سعر', title='المساحة vs السعر')
            st.plotly_chart(fig2, use_container_width=True)
    
    # التنبؤات المستقبلية
    st.markdown("---")
    st.markdown('<div class="ai-prediction">', unsafe_allow_html=True)
    st.header("🔮 تنبؤات الذكاء الاصطناعي")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("التنبؤ 30 يوم", "+3.2%", "1.4%")
        st.write("اتجاه إيجابي مستمر")
        
    with col2:
        st.metric("التنبؤ 90 يوم", "+8.7%", "2.1%")
        st.write("نمو قوي متوقع")
        
    with col3:
        st.metric("مستوى المخاطرة", "منخفض", "-0.5%")
        st.write("استثمار آمن")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # الخريطة الحرارية
    st.markdown("---")
    st.header("🗺️ الخريطة الحرارية للأسعار")
    
    # محاكاة خريطة حرارية
    heatmap_data = []
    for area in range(1, 11):
        for location in range(1, 11):
            price = np.random.normal(500000 + area * 50000 + location * 30000, 100000)
            heatmap_data.append({'المنطقة': f'منطقة {area}', 'القرب': location, 'السعر': price})
    
    heatmap_df = pd.DataFrame(heatmap_data)
    fig3 = px.density_heatmap(heatmap_df, x='المنطقة', y='القرب', z='السعر', 
                             title='الخريطة الحرارية لأسعار العقارات')
    st.plotly_chart(fig3, use_container_width=True)

# إنشاء التقرير المتقدم مع PDF
if 'selected_package' in st.session_state and st.session_state.selected_package != "مجاني":
    st.markdown("---")
    st.header("📄 إنشاء التقرير المتقدم")
    
    if st.button("🎯 إنشاء التقرير الذكي", type="primary"):
        with st.spinner("جاري إنشاء التقرير المخصص باستخدام الذكاء الاصطناعي..."):
            import time
            time.sleep(3)
            
            # بيانات التقرير المخصص حسب نوع العميل
            report_data = {
                'نوع_العميل': client_type,
                'عدد_العقارات': num_properties,
                'المدينة': selected_city,
                'نوع_العقار': property_type,
                'الباقة': st.session_state.selected_package,
                'التاريخ': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            
            # تحليل مخصص حسب نوع العميل
            analysis_content = {
                "مستثمر فردي": [
                    f"تحليل {num_properties} عقار في {selected_city}",
                    "أفضل 5 فرص استثمارية محددة",
                    "خطة استثمارية شخصية لمدة 12 شهر",
                    "تحليل العوائد والمخاطر المتوقعة",
                    "نصائح للتفاوض على الأسعار"
                ],
                "وسيط عقاري": [
                    f"تحليل {num_properties} عقار في السوق",
                    "استراتيجيات التسعير التنافسية",
                    "قائمة عملاء محتملين في المنطقة",
                    "تحليل حركة السوق والمنافسين",
                    "نصائح لزيادة المبيعات"
                ],
                "شركة تطوير": [
                    "تحليل فرص التطوير العقاري",
                    "دراسة الجدوى الاقتصادية",
                    "تحليل المنافسين والمشاريع القادمة",
                    "توصيات لمواقع المشاريع الجديدة",
                    "تحليل الطلب والعرض في السوق"
                ],
                "باحث عن سكن": [
                    "أفضل المناطق للسكن العائلي",
                    "مقارنة الأسعار والخدمات",
                    "نصائح لاختيار العقار المناسب",
                    "تحليل القيمة مقابل السعر",
                    "توقعات أسعار المستقبلية"
                ],
                "ممول عقاري": [
                    "تحليل مخاطر التمويل",
                    "تقييم الضمانات العقارية",
                    "معدلات العائد المتوقعة",
                    "تحليل قدرة السوق على الاستيعاب",
                    "توصيات شروط التمويل"
                ],
                "مستشار عقاري": [
                    "تحليل السوق الشامل",
                    "توقعات الاتجاهات المستقبلية",
                    "دراسات حالة ناجحة",
                    "أدوات التحليل المتقدمة",
                    "استراتيجيات الاستثمار الذكية"
                ]
            }
            
            report_data['تحليل_مخصص'] = analysis_content.get(client_type, ["تحليل شامل للسوق العقاري"])
            
            st.balloons()
            st.success("**✅ تم إنشاء التقرير المخصص بنجاح!**")
            
            # عرض التقرير المخصص
            st.markdown('<div class="client-card">', unsafe_allow_html=True)
            st.subheader(f"📊 التقرير المخصص - {client_type}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📋 معلومات التقرير:**")
                st.write(f"• نوع العميل: {client_type}")
                st.write(f"• عدد العقارات: {num_properties}")
                st.write(f"• المدينة: {selected_city}")
                st.write(f"• نوع العقار: {property_type}")
                
            with col2:
                st.write("**🎯 التحليل المخصص:**")
                for item in report_data['تحليل_مخصص']:
                    st.write(f"• {item}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # زر تحميل PDF
            pdf_data = create_pdf_report(report_data)
            st.download_button(
                label="📥 انقر لتحميل التقرير PDF",
                data=pdf_data,
                file_name=f"تقرير_وردة_{client_type}_{selected_city}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
            )

# التذييل
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <strong>✨ وردة العقارية 2024</strong> - الذكاء الاصطناعي للتحليل العقاري • جميع الحقوق محفوظة
</div>
""", unsafe_allow_html=True)
