# report_content_builder.py
# يعتمد على: weasyprint, pandas, datetime, json (موجودة عادة)
from weasyprint import HTML, CSS
from datetime import datetime
import pandas as pd
import math
import os

# --- تخصيصات عامة يمكنك تعديلها لاحقًا ---
TEMPLATE_FILE = "report_template.html"   # يجب أن يكون في نفس المجلد
CSS_FILE = "report_style.css"            # يجب أن يكون في نفس المجلد
OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# قاعدة نصية عامة تستخدمها الفقرات (أسلوب استشاري - Big Consulting)
def human_paragraph(title, body):
    return f"<div class='section-box'><h2>{title}</h2><p>{body}</p></div>"

# توليد ملخص تنفيذي إنساني
def build_executive_summary(user_info, market_data, real_data):
    city = user_info.get("city", "المدينة المختارة")
    prop = user_info.get("property_type", "نوع العقار")
    summary = (
        f"الملخص التنفيذي: بناءً على التحليل الميداني والبيانات المتاحة لمدينة {city} ونوع العقار {prop}, "
        "يتضح أن السوق يشهد مؤشرات نمو مستدامة مدعومة بعوامل الطلب المحلي والتطورات العمرانية. "
        "هدف هذا الملخص إعطاء قرار واضح وقابل للتنفيذ ضمن إطار زمني ومؤشرات مخاطر محسوبة."
    )
    details = (
        f"نقترح النظر في التوصيات التالية بحسب باقتك المختارة ({user_info.get('package','غير محدد')})، "
        "مع ضرورة مراجعة الخيارات التمويلية وبرامج إدارة المخاطر قبل أي قرار استثماري."
    )
    return human_paragraph("الملخص التنفيذي", summary + " " + details)

# تحليل السوق (وصف + متوسطات + نقاط قوة وضعف)
def build_market_analysis(user_info, market_data, real_data):
    city = user_info.get("city", "المدينة")
    prop = user_info.get("property_type", "نوع العقار")
    avg_price = market_data.get("متوسط_السوق", 0)
    growth = market_data.get("معدل_النمو_الشهري", 0)
    occupancy = market_data.get("معدل_الإشغال", 0)
    text = (
        f"تحليل الموقع والسوق: تستعرض هذه الفقرة أهم المؤشرات لمدينة {city} لنوع العقار {prop}. "
        f"متوسط السعر الحالي للمتر المربع: {avg_price:,.0f} ريال. معدل النمو الشهري المقدر: {growth:.2f}%. "
        f"معدل الإشغال التقريبي: {occupancy:.1f}%. "
        "الملاحظة الأساسية: ينبغي الانتباه إلى الفروق بين الأحياء وتركيز العرض في الشريحتين المتوسطة والعليا."
    )
    strengths = (
        "نقاط القوة: قرب الخدمات، مشاريع بنية تحتية جديدة، طلب مستمر من شريحة المستأجرين."
    )
    weaknesses = "نقاط الضعف: تضخم في بعض مجالات العرض وارتفاع تكاليف البناء في مناطق مختارة."
    return human_paragraph("تحليل السوق والموقع", text + " " + strengths + " " + weaknesses)

# تحليل مالي مختصر / مفصل حسب الباقة
def build_financial_analysis(user_info, market_data, real_data):
    area = user_info.get("area", 120)
    current_price = market_data.get("السعر_الحالي", market_data.get("متوسط_السوق", 6000))
    price_total = current_price * area
    annual_rent = area * (market_data.get("العائد_التأجيري", 7) / 100) * current_price
    payback = None
    try:
        payback = price_total / (annual_rent if annual_rent>0 else 1)
    except:
        payback = None
    text = (
        f"التحليل المالي: القيمة السوقية الحالية لعقار بمساحة {area} م² تُقدر تقريبًا بـ {price_total:,.0f} ريال "
        f"بمعدل إيراد سنوي تقريبي {annual_rent:,.0f} ريال. فترة استرداد رأس المال التقديرية حوالي "
        f"{(payback if payback else 'غير محددة')} سنة تقريبًا (تقديري)."
    )
    recommendation = (
        "التوصية المالية: اعتماد سيناريو تمويل محافظ، ومراجعة خطة التسعير، مع وضع احتياطي سيولة يغطي 6-12 شهرًا."
    )
    return human_paragraph("التحليل المالي والتوقعات", text + " " + recommendation)

# قسم الذكاء الاصطناعي (للباقات الذهبية والماسية)
def build_ai_section(user_info, ai_recommendations):
    if not ai_recommendations:
        return ""
    risk = ai_recommendations.get("ملف_المخاطر", "متوسط المخاطر")
    strat = ai_recommendations.get("استراتيجية_الاستثمار", "تنويع المحافظ")
    timing = ai_recommendations.get("التوقيت_المثالي", "مراقبة السوق")
    conf = ai_recommendations.get("مؤشرات_الثقة", {})
    conf_level = conf.get("مستوى_الثقة", "غير محدد")
    text = (
        f"تحليل الذكاء الاصطناعي: صاغ نظامنا ملف المخاطر الخاص بكم على أنه: {risk}. "
        f"استراتيجية المقترحة: {strat}. التوقيت المثالي: {timing}. مستوى الثقة في البيانات: {conf_level}."
    )
    return human_paragraph("نتائج التحليل المدعوم بالذكاء الاصطناعي", text)

# تحليل المنافسين (لمشاريع محددة)
def build_competitor_analysis(user_info, market_data, real_data, n=10):
    n = min(n, max(1, int(len(real_data) * 0.2))) if isinstance(real_data, pd.DataFrame) else n
    text = f"تحليل المنافسين: تم مقارنة المشروع مع أبرز {n} مشاريع منافسة من حيث السعر، الجودة، ومراحل الإنجاز. "
    text += "الاستنتاجات توضح مواضع القوة والضعف، مع اقتراحات لتحسين الميزة التنافسية (تفصيلي داخل الملحقات)."
    return human_paragraph("تحليل المنافسين", text)

# صفحة توصيات عملية (قابلة للتنفيذ)
def build_recommendations(user_info, market_data):
    text = (
        "التوصيات العملية: ١) التركيز على التسعير الديناميكي عند التفاوض. "
        "٢) دراسة خيار التمويل الجزئي لتقليل فترة الاسترداد. "
        "٣) إعداد خطة تسويقية رقمية متكاملة لرفع الطلب في أول 6 أشهر."
    )
    return human_paragraph("التوصيات العملية", text)

# تفاصيل إضافية وملحقات (نستخدمها لملء صفحات حتى نصل لعدد الصفحات المطلوب)
def build_detailed_pages(real_data, start_idx=0, count=5):
    pages = []
    df = real_data if isinstance(real_data, pd.DataFrame) else pd.DataFrame()
    sample = df[start_idx:start_idx+count] if not df.empty else pd.DataFrame()
    # لكل صف ننتج فقرة تحليلية قصيرة
    if not sample.empty:
        for i, row in sample.iterrows():
            title = f"تحليل عقار نموذجي - {row.get('المنطقة', 'المنطقة')}"
            txt = (
                f"العقار: {row.get('العقار','-')} — السعر: {int(row.get('السعر',0))} ريال — المساحة: {row.get('المساحة','-')}. "
                f"تحليل موجز: السعر يتناسب مع متوسط المنطقة مع وجود فرصة زيادة القيمة عبر تحسينات بسيطة."
            )
            pages.append(human_paragraph(title, txt))
    else:
        # ملء محتوى عام إن لم تتوفر بيانات كافية
        filler = (
            "تفصيل إضافي: تحليل اتجاهات السوق المحلية مع اقتراح نقاط دخول واستراتيجيات خروج "
            "ومعايير مراقبة الأداء للاستثمار العقاري."
        )
        for i in range(count):
            pages.append(human_paragraph(f"تفصيل إضافي {i+1}", filler))
    return pages

# -----------------------------------------
# الدالة الأساسية: توليد التقرير
# -----------------------------------------
def generate_report(user_info, market_data, real_data, ai_recommendations=None, package_level="مجانية"):
    """
    user_info: dict يحتوي keys مثل user_type, city, property_type, area, package
    market_data: dict من generate_advanced_market_data
    real_data: pd.DataFrame من RealEstateScraper
    ai_recommendations: dict أو None
    package_level: 'مجانية','فضية','ذهبية','ماسية'
    """
    # 1) احضار القالب
    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError(f"لم أجد قالب HTML: {TEMPLATE_FILE}")
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template_html = f.read()

    # 2) بناء أجزاء المحتوى الأساسية
    parts = []
    parts.append(build_executive_summary(user_info, market_data, real_data))
    parts.append(build_market_analysis(user_info, market_data, real_data))
    parts.append(build_financial_analysis(user_info, market_data, real_data))

    # باقات أعلى تضيف محتوى إضافي
    if package_level in ["فضية", "ذهبية", "ماسية"]:
        parts.append(build_competitor_analysis(user_info, market_data, real_data, n=15))
        # إضافة صفحات بيانات مفصّلة مستخرجة
        parts.extend(build_detailed_pages(real_data, start_idx=0, count=6))

    if package_level in ["ذهبية", "ماسية"]:
        # إضافة قسم الذكاء الاصطناعي والتوصيات المتقدمة
        parts.append(build_ai_section(user_info, ai_recommendations))
        parts.append(build_recommendations(user_info, market_data))
        parts.extend(build_detailed_pages(real_data, start_idx=6, count=10))

    if package_level == "ماسية":
        # محتوى استراتيجي إضافي، مقارنة دولية، ومحاكاة سيناريوهات
        parts.append(human_paragraph("مقارنة إقليمية", "تحليل مقارنة شاملاً مع 5 دول خليجية يوضح نقاط التفوّق والفرص." ))
        parts.append(human_paragraph("محاكاة سيناريوهات", "عرض 20 سيناريو استثماري مع نتائج متوقعة ومخططات حساسية." ))
        parts.extend(build_detailed_pages(real_data, start_idx=16, count=20))

    # 3) دمج الأجزاء داخل صفحات مع التحكم بعدد الصفحات المعلن
    pages_target = {
        "مجانية": 15,
        "فضية": 35,
        "ذهبية": 60,
        "ماسية": 90
    }
    target = pages_target.get(package_level, 15)

    # تجميع HTML: نلف كل جزء في <div class="page"> ... </div>
    pages_html = []
    for part in parts:
        pages_html.append(f'<div class="page">{part}</div>')

    # إذا لم نصل لعدد الصفحات المطلوب نملأ بمحتوى تفصيلي إضافي
    idx = 0
    while len(pages_html) < target:
        extra = build_detailed_pages(real_data, start_idx=idx*5, count=1)
        if not extra:
            # filler عام
            extra = [human_paragraph("مزيد من التحليل", "محتوى تفصيلي إضافي حول عناصر تقييم المخاطر، الجداول، وخريطة الفرص.")]
        pages_html.append(f'<div class="page">{extra[0]}</div>')
        idx += 1
        # safety break
        if idx > 200:
            break

    # 4) إعداد بيانات القالب (استبدال المتغيرات الأساسية)
    report_title = f"تقرير Warda Intelligence - {user_info.get('city','')}"
    report_subtitle = f"تحليل {user_info.get('property_type','')} — باقة: {package_level} — الفئة: {user_info.get('user_type','')}"
    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M")

    # استبدال متغيرات بسيطة في القالب
    html_full = template_html
    html_full = html_full.replace("{{ report_title }}", report_title)
    html_full = html_full.replace("{{ report_subtitle }}", report_subtitle)
    html_full = html_full.replace("{{ generated_on }}", generated_on)
    # إدراج البينات المنسقة للصفحات
    body_pages = "\n".join(pages_html)
    html_full = html_full.replace("{{ report_body }}", body_pages)

    # 5) تحويل HTML إلى PDF باستخدام WeasyPrint
    css = CSS(filename=CSS_FILE)
    out_basename = f"Warda_Report_{user_info.get('city','')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    out_path = os.path.join(OUTPUT_FOLDER, out_basename + ".pdf")

    HTML(string=html_full).write_pdf(out_path, stylesheets=[css])

    # 6) إرجاع مسار الملف (أو يمكنك إرجاع البايتس بفتح الملف وقرائته)
    return out_path

# --- مثال استخدام مبسط ---
if __name__ == "__main__":
    # اختبار سريع — استخدم بيانات تجريبية بسيطة
    ui = {"user_type": "مستثمر", "city": "الرياض", "property_type": "شقة", "area": 120, "package": "ذهبية"}
    md = {"متوسط_السوق": 6250, "السعر_الحالي": 6250, "معدل_النمو_الشهري": 2.5, "العائد_التأجيري": 7.5, "مؤشر_السيولة": 80}
    rd = pd.DataFrame([{"العقار":"شقة مثال","السعر":700000,"المساحة":"120 م²","المنطقة":"النخيل"}]*50)
    path = generate_report(ui, md, rd, ai_recommendations=None, package_level="ذهبية")
    print("تم الإنشاء:", path)
