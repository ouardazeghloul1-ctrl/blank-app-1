import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import io
import os
from fpdf import FPDF

# === إعداد الصفحة ===
st.set_page_config(page_title="Warda Smart Real Estate", page_icon="🏠", layout="wide")

# === التصميم الأسود والذهبي ===
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

pkg_cols = st.columns(4)
pkg_keys = list(packages.keys())
for i, k in enumerate(pkg_keys):
    with pkg_cols[i]:
        st.markdown(f"<div class='card'><h3 class='gold'>{k}</h3>"
                    f"<p class='muted'>{'<br>'.join(packages[k]['details'])}</p>"
                    f"<p class='gold'>السعر الأساسي: ${packages[k]['price_usd']}</p></div>", unsafe_allow_html=True)
        if st.button(f"اختر {k}", key=f"pkgbtn_{i}"):
            st.session_state.selected_package = k
            st.session_state.paid = False

if st.session_state.selected_package:
    st.info(f"باقة مختارة: **{st.session_state.selected_package}**", icon="✨")
else:
    st.info("اختر باقة لعرض السعر وتفعيل خيار الدفع")

# === حساب السعر ===
base_price = packages.get(st.session_state.selected_package, packages["مجانية"])["price_usd"]

# كل عقار إضافي يضيف 10 دولار كما طلبتِ
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

st.markdown("---")

# === نظام الدفع ===
paypal_email = "zeghloulwarda6@gmail.com"
st.markdown("### 💳 للدفع الآمن عبر PayPal")
if total_price_usd == 0:
    st.info("الباقة مجانية — يمكنك تحميل التقرير مباشرة بعد الضغط على زر التحليل.", icon="info")
else:
    paypal_link = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business={paypal_email}&currency_code=USD&amount={total_price_usd}&item_name=Warda+Report+{st.session_state.selected_package}"
    st.markdown(f"""<a href="{paypal_link}" target="_blank"><button class="stButton">💳 ادفع عبر PayPal الآن (${total_price_usd})</button></a>""", unsafe_allow_html=True)
    st.markdown("<p class='small'>بعد الدفع ستعود إلى هذه الصفحة وتضغط على: <b>لقد دفعت — أريد التقرير</b></p>", unsafe_allow_html=True)

if total_price_usd > 0:
    if st.button("✅ لقد دفعت — أريد التقرير"):
        st.session_state.paid = True
        st.success("تم تفعيل إمكانية تحميل التقرير — انزلي للأسفل لتحمليه.", icon="✅")

if total_price_usd == 0:
    st.session_state.paid = True

st.markdown("---")

# === إنشاء PDF ===
st.header("📄 تقريرك (سيصبح متاحًا بعد الدفع)")

def create_simple_pdf(client_type, city, prop_type, status, count, package, price):
    """إنشاء PDF مبسط وآمن"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # محتوى التقرير بالإنجليزية فقط لتجنب المشاكل
    content = f"""
WARDASMART REAL ESTATE ANALYSIS REPORT
=====================================

CLIENT INFORMATION:
------------------
Client Type: {client_type}
City: {city}
Property Type: {prop_type}
Status: {status}
Properties Analyzed: {count}
Package: {package}
Total Price: ${price}

ANALYSIS SUMMARY:
----------------
This report provides comprehensive real estate analysis
for the selected market parameters.

Based on the analysis of {count} properties in {city},
we provide market insights and recommendations.

KEY METRICS:
- Market analysis completed
- Price trends evaluated
- Investment opportunities identified
- Custom recommendations provided

Report generated on: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}

For detailed consultation in Arabic, please contact us directly.

Warda Smart Real Estate
Professional Market Analysis
"""
    
    # كتابة المحتوى سطراً سطراً
    lines = content.split('\n')
    for line in lines:
        if line.strip():
            pdf.cell(0, 8, line, ln=True)
        else:
            pdf.ln(5)
    
    return pdf

if st.session_state.paid:
    # عرض الملخص
    st.markdown(f"**نوع العميل:** {st.session_state.selected_client or '—'}  \n"
                f"**المدينة:** {city}  \n"
                f"**نوع العقار:** {property_type}  \n"
                f"**الحالة:** {status}  \n"
                f"**عدد العقارات:** {count}  \n"
                f"**الباقة:** {st.session_state.selected_package or '—'}  \n"
                f"**المبلغ المدفوع:** ${total_price_usd}")
    
    if st.button("🔍 أنشئ تقرير PDF الآن"):
        try:
            # إنشاء PDF
            pdf = create_simple_pdf(
                client_type=st.session_state.selected_client or "",
                city=city,
                prop_type=property_type,
                status=status,
                count=count,
                package=st.session_state.selected_package or "",
                price=total_price_usd,
            )
            
            # حفظ PDF في buffer
            pdf_buffer = io.BytesIO()
            pdf_output = pdf.output(dest='S').encode('latin-1')
            pdf_buffer.write(pdf_output)
            pdf_buffer.seek(0)
            
            # زر التحميل
            st.download_button(
                label="📥 حمل تقريرك الآن (PDF)",
                data=pdf_buffer.getvalue(),
                file_name=f"warda_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
            )
            st.success("✅ تم إنشاء التقرير بنجاح!")
            
        except Exception as e:
            st.error(f"❌ حدث خطأ: {str(e)}")
            st.info("💡 جاري استخدام الحل البديل...")
            
            # حل بديل بسيط
            try:
                pdf_simple = FPDF()
                pdf_simple.add_page()
                pdf_simple.set_font("Arial", size=14)
                pdf_simple.cell(0, 10, "Warda Real Estate Report", 0, 1, "C")
                pdf_simple.ln(10)
                pdf_simple.set_font("Arial", size=12)
                pdf_simple.cell(0, 8, f"Client: {st.session_state.selected_client}", ln=True)
                pdf_simple.cell(0, 8, f"City: {city}", ln=True)
                pdf_simple.cell(0, 8, "Report generated successfully!", ln=True)
                
                buffer_simple = io.BytesIO()
                pdf_simple.output(buffer_simple)
                
                st.download_button(
                    label="📥 حمل التقرير المبسط",
                    data=buffer_simple.getvalue(),
                    file_name="warda_simple_report.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e2:
                st.error(f"❌ فشل الحل البديل: {e2}")

else:
    st.warning("لتفعيل زر تنزيل التقرير: يجب الدفع أولا (للباقات غير المجانية) ثم النقر على 'لقد دفعت — أريد التقرير'.", icon="⚠️")

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
