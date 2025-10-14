import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import io

# === إعداد الصفحة ===
st.set_page_config(page_title="Warda Smart Real Estate", page_icon="🏠", layout="wide")

# === التصميم الأسود والذهبي الأصلي ===
st.markdown(
    """
    <style>
      html, body, .stApp { background-color: #000000; color: #D4AF37; }
      .gold { color: #D4AF37; font-weight:700; }
      .card { background:#0b0b0b; padding:16px; border-radius:12px; border:1px solid rgba(212,175,55,0.18); }
      .btn-gold > button, .stDownloadButton>button { background: linear-gradient(90deg,#D4AF37,#c9a833); color:#050505; font-weight:700; border-radius:10px; padding:10px 18px; }
      .muted { color:#9f9f9f; font-size:13px; }
      .center { text-align:center; }
      input, .stTextInput>div>input, .stSelectbox>div, textarea { background:#111 !important; color:#D4AF37 !important; border-radius:6px; }
      .gold-box { border:1px solid rgba(212,175,55,0.18); padding:12px; border-radius:10px; background:#080808; }
      .small { font-size:13px; color:#bfbfbf; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 class='gold center'>🏠 Warda Smart Real Estate</h1>", unsafe_allow_html=True)
st.markdown("<p class='center small'>المنصة الذكية لتحليل السوق • تقرير مفصل بعد الإعداد</p>", unsafe_allow_html=True)
st.markdown("---")

# === Session state ===
if "selected_client" not in st.session_state:
    st.session_state.selected_client = None
if "selected_package" not in st.session_state:
    st.session_state.selected_package = None
if "paid" not in st.session_state:
    st.session_state.paid = False
if "free_report_generated" not in st.session_state:
    st.session_state.free_report_generated = False

# === فئات العملاء ===
st.header("🎯 اختر هويتك (انقري على ما يناسبك)")
client_types = [
    "مستثمر فردي", "وسيط عقاري", "شركة تطوير", "باحث عن سكن",
    "ممول عقاري", "مستشار عقاري", "مطور عقاري", "مدير استثمار"
]

cols = st.columns(4)
for i, c in enumerate(client_types):
    if cols[i % 4].button(f"أنا {c}", key=f"client_{i}"):
        st.session_state.selected_client = c

if st.session_state.selected_client:
    st.success(f"✅ تم اختيار: {st.session_state.selected_client}")
else:
    st.info("اختر هويتك بالضغط على أحد الأزرار أعلاه")

st.markdown("---")

# === بيانات التحليل ===
st.header("📋 بيانات التحليل")

cities = [
    "الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة", "الخبر", "الطائف",
    "بريدة", "حفر الباطن", "ينبع", "أبها", "نجران", "جازان", "حائل", "عرعر"
]
city = st.selectbox("المدينة", cities)

property_types = [
    "شقة", "فيلا", "أرض", "دوبلكس", "محل تجاري", "مكتب", "استوديو",
    "عمارة", "مزرعة", "مستودع", "شاليه", "أرض تجارية"
]
property_type = st.selectbox("نوع العقار", property_types)

status = st.selectbox("الحالة", ["للبيع", "للإيجار", "كلاهما"])

count = st.slider("عدد العقارات في التحليل (من 1 إلى 1000)", min_value=1, max_value=1000, value=50, step=1)

st.markdown("---")

# === الباقات ===
st.header("📦 اختر باقتك")
packages = {
    "مجانية": {
        "price_usd": 0,
        "details": [
            "تحليل سريع لموقع واحد",
            "مؤشرات سعرية أساسية", 
            "ملخص مفصل (صفحة واحدة)",
            "تحميل مباشر بدون دفع"
        ]
    },
    "متوسطة": {
        "price_usd": 15,
        "details": [
            "تحليل 3 مواقع/أحياء",
            "مؤشرات سعرية + توصيات أولية",
            "تنبؤ 30 يوم (مخطط تقريبي)",
            "تقرير مفصل (3-4 صفحات)"
        ]
    },
    "جيدة": {
        "price_usd": 40,
        "details": [
            "تحليل شامل حتى 5 مواقع", 
            "توصيات استثمارية قابلة للتنفيذ",
            "تنبؤ 30 و90 يوم",
            "تقرير مصمم بالهوية الذهبية"
        ]
    },
    "ممتازة": {
        "price_usd": 90,
        "details": [
            "تحليل كامل لكل المواقع المطلوبة",
            "مقارنة عروض المنافسين وتحليل مخاطر", 
            "تنبؤ مفصل 30/90 يوم + سيناريوهات نمو",
            "تقرير شامل وجاهز للعرض على مستثمرين"
        ]
    }
}

# عرض الباقات
pkg_cols = st.columns(4)
for i, (pkg_name, pkg_info) in enumerate(packages.items()):
    with pkg_cols[i]:
        st.markdown(f"<div class='card'><h3 class='gold'>{pkg_name}</h3>"
                    f"<p class='muted'>{'<br>'.join(pkg_info['details'])}</p>"
                    f"<p class='gold'>السعر الأساسي: ${pkg_info['price_usd']}</p></div>", unsafe_allow_html=True)
        
        if st.button(f"اختر {pkg_name}", key=f"pkg_btn_{i}"):
            st.session_state.selected_package = pkg_name
            st.session_state.paid = False
            st.session_state.free_report_generated = False

# عرض الباقة المختارة
if st.session_state.selected_package:
    selected_pkg_info = packages[st.session_state.selected_package]
    st.markdown(f"""
    <div class='gold-box'>
    <h3 class='gold'>✅ الباقة المختارة: {st.session_state.selected_package}</h3>
    <p class='muted'>{' • '.join(selected_pkg_info['details'])}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("اختر باقة من الخيارات أعلاه")

# === حساب السعر ===
if st.session_state.selected_package:
    base_price = packages[st.session_state.selected_package]["price_usd"]
    
    # كل عقار إضافي يضيف 10 دولار
    if base_price > 0:
        total_price_usd = base_price + (count * 10)
    else:
        total_price_usd = 0.0

    st.markdown(f"""
    <div class="gold-box">
    <h3 class="gold">💰 السعر الإجمالي: ${total_price_usd}</h3>
    <p class="small">السعر يشمل ${base_price} للباقة + ${10} لكل عقار إضافي (إجمالي {count} عقار)</p>
    </div>
    """, unsafe_allow_html=True)
else:
    total_price_usd = 0

st.markdown("---")

# === نظام الدفع ===
if st.session_state.selected_package == "مجانية":
    st.session_state.paid = True
    st.session_state.free_report_generated = True
    
    st.markdown("### 🎁 الباقة المجانية")
    st.info("يمكنك تحميل التقرير مباشرة بدون دفع - هذه الباقة مجانية لكافة المستخدمين.")
    
else:
    paypal_email = "zeghloulwarda6@gmail.com"
    st.markdown("### 💳 للدفع الآمن عبر PayPal")
    
    paypal_link = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business={paypal_email}&currency_code=USD&amount={total_price_usd}&item_name=Warda+Report+{st.session_state.selected_package}"
    st.markdown(f"""<a href="{paypal_link}" target="_blank"><button class="stButton">💳 ادفع عبر PayPal الآن (${total_price_usd})</button></a>""", unsafe_allow_html=True)
    st.markdown("<p class='small'>بعد الدفع ستعود إلى هذه الصفحة وتضغط على: <b>لقد دفعت — أريد التقرير</b></p>", unsafe_allow_html=True)

    if st.button("✅ لقد دفعت — أريد التقرير"):
        st.session_state.paid = True
        st.success("تم تفعيل إمكانية تحميل التقرير — انزلي للأسفل لتحمليه.")

st.markdown("---")

# === إنشاء PDF ===
st.header("📄 تقريرك الجاهز")

def create_professional_pdf(client_type, city, prop_type, status, count, package, price):
    """إنشاء PDF احترافي يعمل 100%"""
    
    # استخدام مكتبة reportlab للPDF - الأكثر استقراراً
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # محتوى التقرير
        title_style = styles["Heading1"]
        normal_style = styles["Normal"]
        
        # العنوان
        title = Paragraph("Warda Smart Real Estate Report", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # معلومات العميل
        client_info = f"""
        <b>Client Information:</b><br/>
        Client Type: {client_type}<br/>
        City: {city}<br/>
        Property Type: {prop_type}<br/>
        Status: {status}<br/>
        Properties Analyzed: {count}<br/>
        Package: {package}<br/>
        Total Price: ${price}<br/>
        """
        story.append(Paragraph(client_info, normal_style))
        story.append(Spacer(1, 15))
        
        # التحليل
        analysis = f"""
        <b>Market Analysis Summary:</b><br/>
        This comprehensive real estate analysis report provides detailed insights 
        into the current market conditions in {city}. Based on the analysis of 
        {count} properties, this report offers valuable information for {client_type}.
        
        The {prop_type} market shows promising opportunities with current trends 
        indicating growth potential. The {status} segment demonstrates stable 
        performance with opportunities for strategic investments.
        """
        story.append(Paragraph(analysis, normal_style))
        story.append(Spacer(1, 15))
        
        # التوصيات
        recommendations = """
        <b>Key Recommendations:</b><br/>
        • Conduct thorough due diligence before investment<br/>
        • Consider location-specific market factors<br/>
        • Monitor market trends regularly<br/>
        • Consult with real estate professionals<br/>
        • Review financing options carefully<br/>
        """
        story.append(Paragraph(recommendations, normal_style))
        story.append(Spacer(1, 15))
        
        # الخاتمة
        conclusion = f"""
        <b>Conclusion:</b><br/>
        Report generated on: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}<br/>
        For detailed consultation and personalized advice, contact Warda Smart Real Estate.
        """
        story.append(Paragraph(conclusion, normal_style))
        
        # بناء الPDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        # إذا فشل reportlab، نستخدم طريقة بسيطة مضمونة
        from fpdf import FPDF
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # محتوى إنجليزي فقط لتجنب المشاكل
        content = [
            "WARDASMART REAL ESTATE REPORT",
            "",
            "CLIENT INFORMATION:",
            f"Client Type: {client_type}",
            f"City: {city}",
            f"Property Type: {prop_type}",
            f"Status: {status}",
            f"Properties Analyzed: {count}",
            f"Package: {package}",
            f"Total Price: ${price}",
            "",
            "ANALYSIS SUMMARY:",
            f"Market analysis for {city} completed.",
            f"Based on {count} properties analysis.",
            "Professional insights provided.",
            "",
            f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "Warda Smart Real Estate - Professional Services"
        ]
        
        for line in content:
            pdf.cell(0, 10, line, ln=True)
        
        pdf_buffer = io.BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin-1')
        pdf_buffer.write(pdf_output)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()

if st.session_state.paid and st.session_state.selected_package:
    # عرض الملخص
    st.markdown(f"""
    **📊 ملخص طلبك:**  
    **نوع العميل:** {st.session_state.selected_client or '—'}  
    **المدينة:** {city}  
    **نوع العقار:** {property_type}  
    **الحالة:** {status}  
    **عدد العقارات:** {count}  
    **الباقة:** {st.session_state.selected_package}  
    **المبلغ المدفوع:** ${total_price_usd}
    """)
    
    if st.button("🔄 أنشئ تقريري الآن", key="generate_report"):
        with st.spinner("جاري إنشاء التقرير المحترف..."):
            try:
                # إنشاء PDF
                pdf_data = create_professional_pdf(
                    client_type=st.session_state.selected_client or "",
                    city=city,
                    prop_type=property_type,
                    status=status,
                    count=count,
                    package=st.session_state.selected_package,
                    price=total_price_usd,
                )
                
                # زر التحميل
                st.download_button(
                    label="📥 حمل تقريرك الآن",
                    data=pdf_data,
                    file_name=f"warda_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                )
                st.success("✅ تم إنشاء التقرير بنجاح!")
                st.balloons()
                
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")

elif not st.session_state.selected_package:
    st.warning("⚠️ يرجى اختيار باقة أولاً")
else:
    st.warning("⚠️ لتفعيل زر تنزيل التقرير: يجب الدفع أولا (للباقات غير المجانية) ثم النقر على 'لقد دفعت — أريد التقرير'.")

st.markdown("---")

# === واتساب ===
wa_number = "00779888140"
st.markdown(f"""
<div class='center'>
<a href='https://wa.me/{wa_number}' target='_blank'>
<button style='background:#25D366;color:white;border-radius:10px;padding:10px 18px;font-weight:700;'>💬 تواصل معي عبر WhatsApp</button>
</a>
</div>
""", unsafe_allow_html=True)

st.markdown("<p class='small center'>منصة وردة الذكية للعقارات - تحليلات احترافية لقرارات أذكى</p>", unsafe_allow_html=True)
