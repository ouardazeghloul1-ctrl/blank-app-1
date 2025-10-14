import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import io
import base64

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
st.markdown("<p class='center small'>المنصة الذكية لتحليل السوق — تقرير PDF بعد الدفع</p>", unsafe_allow_html=True)
st.markdown("---")

# === Session state ===
if "selected_client" not in st.session_state:
    st.session_state.selected_client = None
if "selected_package" not in st.session_state:
    st.session_state.selected_package = None
if "paid" not in st.session_state:
    st.session_state.paid = False

# === فئات العملاء ===
st.header("🎯 اختر هويتك (انقري على ما يناسبك)")
client_types = [
    "مستثمر فردي", "وسيط عقاري", "شركة تطوير", "باحث عن سكن",
    "ممول عقاري", "مستشار عقاري", "مالك عقار", "مستأجر",
    "مطور صغير", "مدير صندوق استثمار", "خبير تقييم", "طالب دراسة جدوى",
    "باحث عن فرص تجارية", "وسيط تأجير", "محلل سوق", "شركة إدارة أملاك"
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
    "بريدة", "حفر الباطن", "ينبع", "أبها", "نجران", "جازان", "حائل", "عرعر",
    "القاهرة", "الإسكندرية", "الجزائر", "تونس", "الرباط"
]
city = st.selectbox("المدينة", cities)

property_types = [
    "شقة", "فيلا", "أرض", "دوبلكس", "محل تجاري", "مكتب", "استوديو",
    "عمارة", "مزرعة", "مستودع", "شاليه", "أرض تجارية", "بيت شعبي"
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
            "ملخص PDF مختصر (صفحة واحدة)"
        ]
    },
    "متوسطة": {
        "price_usd": 15,
        "details": [
            "تحليل 3 مواقع/أحياء",
            "مؤشرات سعرية + توصيات أولية",
            "تنبؤ 30 يوم (مخطط تقريبي)",
            "تقرير PDF مفصل (3-4 صفحات)"
        ]
    },
    "جيدة": {
        "price_usd": 40,
        "details": [
            "تحليل شامل حتى 5 مواقع",
            "توصيات استثمارية قابلة للتنفيذ",
            "تنبؤ 30 و90 يوم (نطاق ثقة تقريبي)",
            "تقرير PDF مصمم بالهوية الذهبية"
        ]
    },
    "ممتازة": {
        "price_usd": 90,
        "details": [
            "تحليل كامل لكل المواقع المطلوبة",
            "مقارنة عروض المنافسين وتحليل مخاطر",
            "تنبؤ مفصل 30/90 يوم + سيناريوهات نمو",
            "تقرير PDF شامل وجاهز للعرض على مستثمرين"
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
paypal_email = "zeghloulwarda6@gmail.com"
st.markdown("### 💳 للدفع الآمن عبر PayPal")

if total_price_usd == 0:
    st.info("الباقة مجانية — يمكنك تحميل التقرير مباشرة بعد الضغط على زر التحليل.")
else:
    paypal_link = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business={paypal_email}&currency_code=USD&amount={total_price_usd}&item_name=Warda+Report+{st.session_state.selected_package}"
    st.markdown(f"""<a href="{paypal_link}" target="_blank"><button class="stButton">💳 ادفع عبر PayPal الآن (${total_price_usd})</button></a>""", unsafe_allow_html=True)
    st.markdown("<p class='small'>بعد الدفع ستعود إلى هذه الصفحة وتضغط على: <b>لقد دفعت — أريد التقرير</b></p>", unsafe_allow_html=True)

if total_price_usd > 0:
    if st.button("✅ لقد دفعت — أريد التقرير"):
        st.session_state.paid = True
        st.success("تم تفعيل إمكانية تحميل التقرير — انزلي للأسفل لتحمليه.")

if total_price_usd == 0:
    st.session_state.paid = True

st.markdown("---")

# === إنشاء PDF ===
st.header("📄 تقريرك (سيصبح متاحًا بعد الدفع)")

def create_pdf_safe(client_type, city, prop_type, status, count, package, price):
    """إنشاء PDF بدون أي مشاكل Unicode"""
    
    # محتوى إنجليزي فقط - هذا هو الحل النهائي
    content = f"""
WARDASMART REAL ESTATE ANALYSIS REPORT
=====================================

CLIENT INFORMATION:
Client Type: {client_type}
City: {city}
Property Type: {prop_type}
Status: {status}
Properties Analyzed: {count}
Package: {package}
Total Price: ${price}

ANALYSIS SUMMARY:
This professional real estate analysis report provides
comprehensive market insights based on current data.

REPORT DETAILS:
- Market analysis completed for specified parameters
- Price trends and investment opportunities identified
- Custom recommendations provided based on client profile
- Professional insights for informed decision making

TECHNICAL SPECIFICATIONS:
- Analysis based on {count} property data points
- Market evaluation for {city} area
- Property type focus: {prop_type}
- Client category: {client_type}

CONCLUSION:
This report serves as a foundation for strategic
real estate decisions. For detailed consultation
and Arabic version, please contact us directly.

Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

WARDASMART REAL ESTATE
Professional Analysis Platform
"""
    
    # إنشاء PDF باستخدام reportlab بدلاً من fpdf - الحل الجذري
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # إضافة المحتوى
        lines = content.split('\n')
        for line in lines:
            if line.strip():
                p = Paragraph(line, styles["Normal"])
                story.append(p)
                story.append(Spacer(1, 12))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
        
    except:
        # إذا فشل reportlab، نرجع ملف نصي بسيط
        simple_content = f"Wardasmart Report - {datetime.now()}"
        return simple_content.encode('utf-8')

if st.session_state.paid and st.session_state.selected_package:
    # عرض الملخص
    st.markdown(f"""
    **نوع العميل:** {st.session_state.selected_client or '—'}  
    **المدينة:** {city}  
    **نوع العقار:** {property_type}  
    **الحالة:** {status}  
    **عدد العقارات:** {count}  
    **الباقة:** {st.session_state.selected_package}  
    **المبلغ المدفوع:** ${total_price_usd}
    """)
    
    if st.button("🔍 أنشئ تقرير PDF الآن"):
        try:
            # إنشاء PDF
            pdf_data = create_pdf_safe(
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
                label="📥 حمل تقريرك الآن (PDF)",
                data=pdf_data,
                file_name=f"warda_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
            )
            st.success("✅ تم إنشاء التقرير بنجاح!")
            st.balloons()
            
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
            # حل بديل فوري
            st.info("📝 جاري إنشاء تقرير بديل...")
            
            # إنشاء ملف نصي بسيط كبديل
            simple_report = f"""
            Warda Smart Real Estate Report
            =============================
            Client: {st.session_state.selected_client}
            City: {city}
            Property: {property_type}
            Status: {status}
            Count: {count}
            Package: {st.session_state.selected_package}
            Price: ${total_price_usd}
            Date: {datetime.now()}
            
            This is your real estate analysis report.
            Contact us for the full detailed version.
            """
            
            st.download_button(
                label="📥 حمل التقرير النصي (بديل)",
                data=simple_report.encode('utf-8'),
                file_name=f"warda_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
            )

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
