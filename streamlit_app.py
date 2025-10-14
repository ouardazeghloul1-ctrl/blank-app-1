# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import json
import uuid
from datetime import datetime, timedelta

# Attempt to import reportlab for robust Arabic PDF handling
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

# ------------------ config ------------------
OWNER_SECRET_ENV = "WARD A_OWNER_SECRET"  # you can change or use st.secrets in deployment
DEFAULT_OWNER_SECRET = "warda_secret_123"  # change this to a strong secret (or set in env / streamlit secrets)
TOKENS_FILE = "tokens.json"
REPORTS_DIR = "reports"
AMIRI_TTF = "Amiri-Regular.ttf"  # must exist in same folder

os.makedirs(REPORTS_DIR, exist_ok=True)

st.set_page_config(page_title="Warda Smart Real Estate — منصة وردة", page_icon="🏠", layout="wide")

# ---------- style (black + gold) ----------
st.markdown("""
<style>
  html, body, .stApp { background-color: #000000; color: #D4AF37; }
  .gold { color: #D4AF37; font-weight:700; }
  .card { background:#0b0b0b; padding:14px; border-radius:10px; border:1px solid rgba(212,175,55,0.14); }
  .pkg-btn>button { background: linear-gradient(90deg,#D4AF37,#c9a833); color:#050505; font-weight:700; border-radius:8px; padding:6px 12px; }
  .center { text-align:center; }
  .muted { color:#bdbdbd; font-size:13px; }
  .price-box { background:#0f0f0f; border:1px solid rgba(212,175,55,0.18); padding:14px; border-radius:10px; }
</style>
""", unsafe_allow_html=True)

# ---------- helper: tokens ----------
def load_tokens():
    if not os.path.exists(TOKENS_FILE):
        return {}
    try:
        with open(TOKENS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_tokens(tokens):
    with open(TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(tokens, f, ensure_ascii=False, indent=2)

def generate_single_use_token(allowed_package=None, valid_hours=48):
    tokens = load_tokens()
    t = str(uuid.uuid4())
    tokens[t] = {
        "created_at": datetime.utcnow().isoformat(),
        "used": False,
        "used_by": None,
        "used_at": None,
        "allowed_package": allowed_package,
        "expires_at": (datetime.utcnow() + timedelta(hours=valid_hours)).isoformat()
    }
    save_tokens(tokens)
    return t

def validate_token(token):
    tokens = load_tokens()
    info = tokens.get(token)
    if not info:
        return False, "غير موجود"
    if info.get("used"):
        return False, "مُستخدم سابقاً"
    if info.get("expires_at"):
        try:
            if datetime.fromisoformat(info["expires_at"]) < datetime.utcnow():
                return False, "منتهي الصلاحية"
        except:
            pass
    return True, info

def mark_token_used(token, user_identifier=None):
    tokens = load_tokens()
    if token in tokens:
        tokens[token]["used"] = True
        tokens[token]["used_by"] = user_identifier
        tokens[token]["used_at"] = datetime.utcnow().isoformat()
        save_tokens(tokens)
        return True
    return False

# ---------- Owner check ----------
if "is_owner" not in st.session_state:
    st.session_state.is_owner = False
if "owner_authenticated" not in st.session_state:
    st.session_state.owner_authenticated = False

# ---------- UI: Header ----------
st.markdown("<h1 class='center gold'>🏠 Warda Smart Real Estate — منصة وردة</h1>", unsafe_allow_html=True)
st.markdown("<p class='center muted'>اختار(ي) هويتك، اختر باقتك، وحمّل تقريرك المفصل — يمكنك إعطاء رابط لمرة واحدة لمؤثر.</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------- Left: Client selection ----------
st.header("🎯 من أنتِ / أنت؟ (اختار(ي))")
client_types = [
    "مستثمر فردي", "وسيط عقاري", "شركة تطوير", "باحث عن سكن",
    "ممول عقاري", "مستشار عقاري", "مطور عقاري", "مالك عقار", "خبير تسويق"
]
cols = st.columns(4)
if "selected_client" not in st.session_state:
    st.session_state.selected_client = None
for i, c in enumerate(client_types):
    if cols[i % 4].button(f"أنا {c}", key=f"client_btn_{i}"):
        st.session_state.selected_client = c

if st.session_state.selected_client:
    st.success(f"✅ تم اختيار: {st.session_state.selected_client}")
else:
    st.info("اضغطي على الزر الذي يطابق هويتك")

st.markdown("---")

# ---------- Analysis inputs ----------
st.header("📋 إعدادات التحليل")
left, right = st.columns([2, 1])
with left:
    cities = [
        "الرياض","جدة","الدمام","مكة المكرمة","المدينة المنورة","الخبر","تبوك","الطائف",
        "بريدة","حفر الباطن","ينبع","أبها","نجران","جازان","حائل","عرعر"
    ]
    city = st.selectbox("🏙️ المدينة", cities)
    property_types = [
        "شقة","فيلا","أرض","دوبلكس","محل تجاري","مكتب","استوديو","عمارة","مزرعة","مستودع","شاليه","أرض تجارية"
    ]
    property_type = st.selectbox("🏠 نوع العقار", property_types)
    status = st.selectbox("📌 الحالة", ["للبيع","للإيجار","كلاهما"])
    count = st.slider("🔢 عدد العقارات في التحليل (1 - 1000)", min_value=1, max_value=1000, value=50, step=1)
    area = st.number_input("📏 المساحة (م²)", min_value=10, max_value=20000, value=120, step=1)
    rooms = st.number_input("🚪 عدد الغرف", min_value=0, max_value=20, value=3, step=1)
with right:
    st.markdown("<div class='card'><h4 class='gold'>بيانات مساعدة</h4><p class='muted'>يمكنك رفع ملف بيانات CSV (اختياري) لاستخدامه في التقرير. إن لم تفعلِي، يستخدم النظام بيانات عيّنة للتوضيح.</p></div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("رفع ملف CSV (اختياري)", type=["csv"])
    sample_df = pd.DataFrame()
    if uploaded:
        try:
            sample_df = pd.read_csv(uploaded)
            st.success(f"تم رفع الملف — {len(sample_df)} صفاً.")
            # save a local copy for reuse
            sample_df.to_csv("latest_data.csv", index=False, encoding="utf-8-sig")
        except Exception as e:
            st.error("فشل قراءة CSV: " + str(e))
    else:
        # if local file exists, try to load it
        if os.path.exists("latest_data.csv"):
            try:
                sample_df = pd.read_csv("latest_data.csv")
            except:
                sample_df = pd.DataFrame()

st.markdown("---")

# ---------- Packages (small buttons that reveal details) ----------
st.header("📦 باقاتنا")
packages = {
    "مجانية": {"price": 0, "details": [
        "تحليل سريع لعقار واحد",
        "ملخص صفحة واحدة",
        "تحميل مباشر"}
    },
    "فضية": {"price": 10, "details": [
        "تحليل دقيق + متوسط الأسعار في المنطقة",
        "نصائح استثمارية عملية"]},
    "ذهبية": {"price": 25, "details": [
        "كل ما في الفضية + تنبؤ بالسعر المستقبلي",
        "اقتراح أفضل وقت للبيع"]},
    "ماسية": {"price": 50, "details": [
        "تحليل شامل + مقارنة مع مشاريع مماثلة",
        "تقرير PDF مصمم وفاخر"]}
}

# display package small buttons
pkg_cols = st.columns(len(packages))
if "selected_package" not in st.session_state:
    st.session_state.selected_package = None

for i, (pname, pinfo) in enumerate(packages.items()):
    with pkg_cols[i]:
        if st.button(pname, key=f"pkg_small_{i}", help="اضغطي لاختيار هذه الباقة"):
            st.session_state.selected_package = pname
            st.session_state.paid = False  # reset payment flag
            st.session_state.free_token_used = False

# show selected package big box
if st.session_state.get("selected_package"):
    sel = st.session_state.selected_package
    pinfo = packages[sel]
    price_display = pinfo["price"]
    st.markdown(f"""
    <div class='price-box'>
      <h3 class='gold'>الباقة المختارة: {sel} — السعر: ${price_display}</h3>
      <p class='muted'>{'<br>'.join(pinfo['details'])}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("اضغطي على أزرار الباقات أعلاه لاختيار الباقة وعرض مميزاتها")

# ---------- Payment logic (PayPal link) ----------
if "paid" not in st.session_state:
    st.session_state.paid = False

if st.session_state.get("selected_package") is None:
    total_price_usd = 0
else:
    total_price_usd = packages[st.session_state.selected_package]["price"]

# If package is free, allow immediate download (but owner can download anything)
if st.session_state.get("selected_package") == "مجانية":
    st.success("هذه الباقة مجانية — يمكنك تحميل التقرير مباشرة.")
    st.session_state.paid = True

# PayPal for paid packages
if st.session_state.get("selected_package") and st.session_state.get("selected_package") != "مجانية":
    paypal_email = "zeghloulwarda6@gmail.com"
    paypal_link = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business={paypal_email}&currency_code=USD&amount={total_price_usd}&item_name=Warda+Report+{st.session_state.selected_package}"
    st.markdown(f"<a href='{paypal_link}' target='_blank'><button class='pkg-btn'>💳 ادفع عبر PayPal — ${total_price_usd}</button></a>", unsafe_allow_html=True)
    st.caption("بعد الدفع، اضغطي على 'لقد دفعت — أريد التقرير' لتفعيل التحميل.")
    if st.button("✅ لقد دفعت — أريد التقرير"):
        st.session_state.paid = True
        st.success("تم تفعيل التحميل. أنقري زر إنشاء التقرير أدناه.")

st.markdown("---")

# ---------- Tokens (single-use links) handling ----------
params = st.experimental_get_query_params()
free_token = params.get("free_token", [None])[0]
token_valid = False
token_info = None
if free_token:
    ok, info = validate_token(free_token)
    if ok:
        token_valid = True
        token_info = info
        st.success("✅ تم تفعيل رابط التقرير المجاني (يعمل لمرة واحدة).")
    else:
        st.error(f"رابط غير صالح: {info}")

# ---------- Owner admin area (generate tokens etc.) ----------
st.sidebar.header("🔐 لوحة المالك")
owner_pass = st.sidebar.text_input("كلمة سر المالك (أدخلها لتفعيل الأدوات)", type="password")
# Owner secret — in production, use st.secrets or env var
owner_secret = os.environ.get("WARDA_OWNER_SECRET", DEFAULT_OWNER_SECRET)
if owner_pass and owner_pass == owner_secret:
    st.sidebar.success("تم التحقق — أنتِ المالك")
    st.session_state.owner_authenticated = True
    st.session_state.is_owner = True
else:
    if owner_pass:
        st.sidebar.error("كلمة السر خاطئة")

if st.session_state.get("owner_authenticated"):
    st.sidebar.markdown("### توليد رابط مجاني لمرة واحدة")
    allowed_pkg = st.sidebar.selectbox("الباقة المسموحة (اختياري)", [None] + list(packages.keys()))
    hours = st.sidebar.number_input("صلاحية الرابط (ساعة)", min_value=1, max_value=168, value=48)
    if st.sidebar.button("🔑 توليد رابط لمرة واحدة"):
        t = generate_single_use_token(allowed_package=allowed_pkg, valid_hours=hours)
        base_url = st.experimental_get_url()
        free_link = f"{base_url}?free_token={t}"
        st.sidebar.success("تم إنشاء الرابط (مرة واحدة). انسخي وشاركيه مع المؤثر:")
        st.sidebar.code(free_link)
    st.sidebar.markdown("---")
    st.sidebar.markdown("### إدارة التوكنات")
    if st.sidebar.button("عرض التوكنات الحالية"):
        tok = load_tokens()
        st.sidebar.write(tok)

# ---------- Helper: can user download (owner, token, or free package) ----------
def user_can_download():
    if st.session_state.get("is_owner"):
        return True, None
    if token_valid:
        # if token restricts package, check allowed_package
        allowed = token_info.get("allowed_package")
        if allowed and st.session_state.get("selected_package") and allowed != st.session_state.get("selected_package"):
            return False, None
        return True, free_token
    if st.session_state.get("selected_package") == "مجانية":
        return True, None
    if st.session_state.get("paid"):
        return True, None
    return False, None

# ---------- Generate report function (reportlab if available, else fallback) ----------
def generate_report_bytes(client_type, city, prop_type, status, count, area, rooms, package_name):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Use sample data if none uploaded
    df = sample_df if not sample_df.empty else pd.DataFrame({
        "السعر":[300000 + i*5000 for i in range(min(count,50))],
        "المساحة":[area for _ in range(min(count,50))],
        "الغرف":[int(rooms) for _ in range(min(count,50))]
    })
    # Prepare simple stats
    try:
        prices = pd.to_numeric(df.get("السعر", df.get("price", df["السعر"] if "السعر" in df.columns else df.iloc[:,0])), errors='coerce').dropna()
    except Exception:
        prices = pd.Series([300000 + i*1000 for i in range(min(count,50))])
    avg_price = int(prices.mean()) if len(prices)>0 else 0
    min_price = int(prices.min()) if len(prices)>0 else 0
    max_price = int(prices.max()) if len(prices)>0 else 0

    # If reportlab available and Amiri font exists -> create bilingual PDF with Arabic using Amiri
    if REPORTLAB_AVAILABLE and os.path.exists(AMIRI_TTF):
        # register Amiri
        try:
            pdfmetrics.registerFont(TTFont('Amiri', AMIRI_TTF))
            # create canvas
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=A4)
            width, height = A4
            # Header
            c.setFont("Amiri", 18)
            c.drawCentredString(width/2, height - 2*cm, "تقرير منصة وردة الذكية للتحليل العقاري")
            c.setFont("Amiri", 11)
            c.drawString(2*cm, height - 3*cm, f"العميل: {client_type} | الباقة: {package_name} | التاريخ: {now}")
            # Arabic analysis block
            y = height - 4*cm
            lines_ar = [
                f"المدينة: {city}",
                f"نوع العقار: {prop_type}",
                f"الحالة: {status}",
                f"المساحة المطلوبة: {area} م²",
                f"عدد الغرف المطلوب: {rooms}",
                f"عدد العقارات المحللة: {count}",
                "",
                f"إحصاءات سريعة (من عيّنة البيانات): المتوسط: {avg_price:,} ريال، الأدنى: {min_price:,} ريال، الأعلى: {max_price:,} ريال.",
                "",
                "التوصيات (عنصرية ومباشرة):",
                "- راجعي العروض الأقل من المتوسط للتأكد من توافرها.",
                "- في حال كانت باقة 'ذهبية' أو أعلى، ننصح بدراسة مقارنة مع مشاريع مماثلة قبل الشراء.",
            ]
            for ln in lines_ar:
                c.drawString(2*cm, y, ln)
                y -= 0.7*cm
                if y < 4*cm:
                    c.showPage()
                    y = height - 3*cm
                    c.setFont("Amiri", 11)
            # add a chart image (matplotlib)
            # generate histogram
            plt.figure(figsize=(6,2.5))
            plt.hist(prices.fillna(0), bins=15)
            plt.title("توزيع الأسعار (عينة)")
            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='PNG', bbox_inches='tight')
            plt.close()
            img_buf.seek(0)
            c.drawImage(ImageReader(img_buf), 2*cm, y-6*cm, width=16*cm, preserveAspectRatio=True)
            c.showPage()
            # English summary page
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(width/2, height - 2*cm, "Warda Smart Real Estate — Analysis Report")
            c.setFont("Helvetica", 11)
            english_lines = [
                f"Client: {client_type}",
                f"City: {city}",
                f"Property Type: {prop_type}",
                f"Area (m2): {area}",
                f"Rooms: {rooms}",
                f"Properties analyzed: {count}",
                "",
                f"Quick stats: Avg: {avg_price:,} SAR, Min: {min_price:,} SAR, Max: {max_price:,} SAR"
            ]
            y2 = height - 3*cm
            for ln in english_lines:
                c.drawString(2*cm, y2, ln)
                y2 -= 0.7*cm
            c.save()
            buf.seek(0)
            return buf.getvalue()
        except Exception as e:
            # fallback to simple English FPDF output if unexpected error
            pass

    # fallback: simple PDF via reportlab without Amiri or via string-based approach
    # Use reportlab (if available) for English only
    if REPORTLAB_AVAILABLE:
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height - 2*cm, "Warda Smart Real Estate — Report")
        c.setFont("Helvetica", 11)
        y = height - 3*cm
        content = [
            f"Client: {client_type}",
            f"City: {city}",
            f"Property Type: {prop_type}",
            f"Status: {status}",
            f"Area: {area} sqm",
            f"Rooms: {rooms}",
            f"Properties analyzed: {count}",
            "",
            f"Avg price: {avg_price:,} SAR | Min: {min_price:,} | Max: {max_price:,}",
            "",
            "Recommendations:",
            "- Use local comparables to validate bargains.",
            "- Consider financing options and legal checks."
        ]
        for ln in content:
            c.drawString(2*cm, y, ln)
            y -= 0.7*cm
            if y < 3*cm:
                c.showPage()
                y = height - 3*cm
        c.save()
        buf.seek(0)
        return buf.getvalue()

    # final fallback: plain text PDF using FPDF (English only)
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Warda Smart Real Estate Report", ln=True, align='C')
        pdf.ln(6)
        lines = [
            f"Client: {client_type}",
            f"City: {city}",
            f"Property Type: {prop_type}",
            f"Status: {status}",
            f"Area: {area} sqm",
            f"Rooms: {rooms}",
            f"Properties analyzed: {count}",
            "",
            f"Avg price: {avg_price:,} SAR"
        ]
        for ln in lines:
            pdf.cell(0, 8, ln, ln=True)
        return pdf.output(dest='S').encode('latin-1', errors='replace')
    except Exception as e:
        st.error("لا توجد مكتبة PDF متاحة على السيرفر. الرجاء تثبيت reportlab أو fpdf.")
        return None

# ---------- Download / Generate logic ----------
st.header("📄 أنشئ تقريرك الآن")
can_download, token_for_mark = user_can_download()
if not st.session_state.get("selected_package"):
    st.info("اختر باقة أولاً من الأعلى")
else:
    st.markdown(f"**الباقة المختارة:** {st.session_state.get('selected_package')} — **السعر:** ${total_price_usd}")

if can_download:
    if st.button("📥 إنشاء وتحميل تقرير PDF الآن"):
        st.info("📂 جاري إنشاء التقرير...")
        pdf_bytes = generate_report_bytes(
            client_type=st.session_state.get("selected_client") or "عميل",
            city=city,
            prop_type=property_type,
            status=status,
            count=count,
            area=area,
            rooms=rooms,
            package_name=st.session_state.get("selected_package") or "مجانية"
        )
        if pdf_bytes:
            # mark token used if applicable
            if token_for_mark:
                mark_token_used(token_for_mark, user_identifier="anonymous")
            # save to reports folder
            fname = f"warda_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            path = os.path.join(REPORTS_DIR, fname)
            with open(path, "wb") as f:
                f.write(pdf_bytes)
            st.success(f"✅ تم إنشاء التقرير وحفظه داخل `{path}`")
            st.download_button("📥 حمل تقريرك الآن", data=pdf_bytes, file_name=fname, mime="application/pdf")
        else:
            st.error("فشل إنشاء التقرير — تأكدي أن المكتبات المطلوبة مثبتة (reportlab أو fpdf).")
else:
    st.warning("⛔ لا تملك صلاحية تحميل التقرير حالياً — يمكنك اختيار باقة مجانية أو الدفع أو استخدام رابط مجاني صالح.")

st.markdown("---")
st.markdown("<div class='center muted'>للمساعدة أو تعديل الإعدادات، تواصلي عبر WhatsApp أو عدّلي كلمة سر المالك في إعدادات البيئة.</div>", unsafe_allow_html=True)

# ---------- Footer / contact ----------
wa_number = "213779888140"  # your real number (without +)
st.markdown(f"<div class='center'><a href='https://wa.me/{wa_number}' target='_blank'><button style='background:#25D366;color:white;border-radius:10px;padding:10px 18px;font-weight:700;'>💬 تواصل عبر WhatsApp</button></a></div>", unsafe_allow_html=True)
st.markdown("<p class='muted center'>© Warda Smart Real Estate — جميع الحقوق محفوظة</p>", unsafe_allow_html=True)
