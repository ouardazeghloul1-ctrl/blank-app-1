import streamlit as st
from io import BytesIO
from datetime import datetime
from fpdf import FPDF
import pandas as pd
import numpy as np

# ----------------- إعداد الصفحة -----------------
st.set_page_config(page_title="Warda Smart Real Estate", layout="wide")
st.markdown("""
<style>
body { background-color: #050505; color: #f0f0f0; }
.gold { color: #D4AF37; font-weight:700; }
.card { background:#0f0f0f; padding:20px; border-radius:12px; border:1px solid rgba(212,175,55,0.25); text-align:center; }
.btn-gold > button { background: linear-gradient(90deg,#D4AF37,#c9a833); color:#0a0a0a; font-weight:700; border-radius:12px; padding:12px 20px; font-size:16px; }
.small-muted { color:#bfbfbf; font-size:13px; }
.package-title { font-size:18px; font-weight:700; margin-bottom:6px; }
.package-desc { font-size:14px; color:#ddd; margin-bottom:10px; }
.btn-paypal { background:#ffc439; color:#050505; padding:10px 16px; border-radius:10px; font-weight:700; text-decoration:none; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center' class='gold'>🏠 Warda Smart Real Estate</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ddd; margin-top:-10px'>✨ ذكاء عقاري، تحليل شامل، تقارير فخمة</p>", unsafe_allow_html=True)
st.markdown("---")

# ----------------- فئات العملاء -----------------
st.header("🎯 أخبرنا من أنت")
client_types = [
    "مستثمر فردي", "وسيط عقاري", "شركة تطوير", "باحث عن سكن",
    "ممول عقاري", "مستشار عقاري", "مالك عقار", "مستأجر",
    "مطور صغير", "مدير صندوق استثمار", "خبير تقييم", "طالب دراسة جدوى"
]

# استخدم Session State للاحتفاظ بالاختيار
if 'selected_client' not in st.session_state:
    st.session_state.selected_client = client_types[0]

cols = st.columns(4)
for idx, client in enumerate(client_types):
    if cols[idx % 4].button(f"أنا {client}", key=f"client_{idx}"):
        st.session_state.selected_client = client

st.info(f"✅ نوع العميل الحالي: **{st.session_state.selected_client}**", icon="ℹ️")

# ----------------- اختيار الباقة -----------------
st.header("📦 اختر باقتك")
packages = {
    "مجانية": {"base_price": 0, "description": ["تحليل سريع لموقع واحد","مخطط رسوم بيانية مبسط","تقرير PDF مختصر"]},
    "متوسطة": {"base_price": 150, "description": ["تحليل 3 مواقع","تنبؤ 30 يوم","تقرير PDF مفصل"]},
    "جيدة": {"base_price": 300, "description": ["تحليل 5 مواقع","تنبؤ 30 و90 يوم","تقرير PDF فخم"]},
    "ممتازة": {"base_price": 500, "description": ["تحليل شامل كل المواقع","توصيات استثمارية دقيقة","تقرير PDF شامل"]}
}

if 'selected_package' not in st.session_state:
    st.session_state.selected_package = "مجانية"

package_cols = st.columns(4)
for idx, (pkg, info) in enumerate(packages.items()):
    with package_cols[idx]:
        st.markdown(f"<div class='card'><div class='package-title'>{pkg}</div>"
                    f"<div class='package-desc'>{'<br>'.join(info['description'])}</div></div>", unsafe_allow_html=True)
        if st.button(f"اختر {pkg}", key=f"pkg_{idx}"):
            st.session_state.selected_package = pkg

st.info(f"✅ الباقة المختارة: **{st.session_state.selected_package}**", icon="✨")

# ----------------- إعدادات التحليل -----------------
st.header("🔍 إعدادات التحليل")
city = st.selectbox("💠 اختر المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الخبر", "الطائف"])
property_type = st.selectbox("🏷️ نوع العقار", ["شقة","فيلا","أرض","دوبلكس","محل تجاري","مكتب"])
num_properties = st.slider("📊 عدد العقارات في التحليل", min_value=100, max_value=5000, value=500, step=100)

# حساب السعر تلقائي حسب الباقة وعدد العقار
price_sar = packages[st.session_state.selected_package]['base_price']
if price_sar > 0:
    price_sar += int(num_properties/500) * 50  # كل 500 عقار يزيد السعر 50 ريال
st.info(f"💰 السعر الحالي للباقة: **{price_sar} ريال**", icon="💵")

# ----------------- زر التحليل -----------------
if st.button("💎 اطلب التحليل الآن"):
    # بيانات وهمية للتجربة
    df = pd.DataFrame({
        "العقار": [f"عقار {i+1}" for i in range(num_properties)],
        "المساحة": np.random.randint(50,500,num_properties),
        "السعر": np.random.randint(100000,1000000,num_properties)
    })

    avg_price = int(df['السعر'].mean())
    st.success(f"تم التحليل! متوسط سعر العقارات: {avg_price:,} ريال")

    # ----------------- PDF -----------------
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Warda Smart Real Estate - {st.session_state.selected_client}", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(5)
    pdf.cell(0, 8, f"الباقة: {st.session_state.selected_package}", ln=True)
    pdf.cell(0, 8, f"المدينة: {city}", ln=True)
    pdf.cell(0, 8, f"نوع العقار: {property_type}", ln=True)
    pdf.cell(0, 8, f"عدد العقارات: {num_properties}", ln=True)
    pdf.cell(0, 8, f"متوسط السعر: {avg_price:,} ريال", ln=True)
    pdf.ln(5)
    pdf.cell(0, 8, "أول 10 سجلات:", ln=True)
    for i, row in df.head(10).iterrows():
        pdf.multi_cell(0, 6, str(row.to_dict()))
    pdf_file = BytesIO()
    pdf.output(pdf_file)
    pdf_file.seek(0)

    st.download_button(
        label="📥 حمل تقريرك الآن",
        data=pdf_file,
        file_name=f"warda_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mime="application/pdf"
    )

    # زر PayPal
    paypal_email = "zeghloulwarda6@gmail.com"
    paypal_link = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business={paypal_email}&currency_code=SAR&amount={price_sar}&item_name=Warda+Smart+Real+Estate+{st.session_state.selected_package}"
    st.markdown(f"<a class='btn-paypal' href='{paypal_link}' target='_blank'>💳 ادفع الآن عبر PayPal</a>", unsafe_allow_html=True)

    # زر WhatsApp
    st.markdown("<br>")
    st.markdown("<a class='btn-paypal' style='background:#25D366;' href='https://wa.me/213000000000' target='_blank'>💬 تواصل معنا عبر WhatsApp</a>", unsafe_allow_html=True)
