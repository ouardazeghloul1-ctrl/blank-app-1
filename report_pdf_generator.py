# report_pdf_generator.py
from io import BytesIO
import os
import tempfile
import re
import unicodedata
from datetime import datetime

import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    PageBreak, Image, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
import plotly.graph_objects as go


# =========================
# الحل النهائي: تقسيم الفقرة العربية إلى أسطر متعددة
# مع KeepTogether للفقرات متعددة الأسطر فقط
# =========================
def arabic_paragraph_flowables(text, style, available_width):
    """
    تقسيم الفقرة العربية إلى أسطر متعددة وكل سطر يصبح Paragraph مستقل
    هذا يمنع Bug ترتيب الأسطر من الأسفل في ReportLab مع RTL
    تقوم هذه الدالة بعملية reshape و bidi مرة واحدة فقط لكل سطر
    """
    if not text:
        return []
    
    text = str(text)
    words = text.split()
    
    if not words:
        return []
    
    lines = []
    current_line = []
    
    for word in words:
        # اختبار إضافة الكلمة للسطر الحالي
        test_line = " ".join(current_line + [word])
        
        # حساب العرض قبل bidi للحصول على عرض دقيق
        reshaped = arabic_reshaper.reshape(test_line)
        width = stringWidth(reshaped, style.fontName, style.fontSize)
        
        if width <= available_width:
            current_line.append(word)
        else:
            # السطر اكتمل - نضيفه كسطر منفصل
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    
    # إضافة آخر سطر
    if current_line:
        lines.append(" ".join(current_line))
    
    # إنشاء Paragraph لكل سطر على حدة مع تطبيق reshape و bidi
    flowables = []
    for i, line in enumerate(lines):
        reshaped = arabic_reshaper.reshape(line)
        bidi_line = get_display(reshaped)
        
        # إضافة Spacer بين الأسطر مع keepWithNext
        if i > 0:
            s = Spacer(1, 0.15 * cm)
            s.keepWithNext = True
            flowables.append(s)
        
        p = Paragraph(bidi_line, style)
        # ضع keepWithNext على كل سطر ما عدا الأخير
        if i < len(lines) - 1:
            p.keepWithNext = True
        flowables.append(p)
    
    # ✅ التعديل النهائي الآمن: استخدام KeepTogether فقط للفقرات متعددة الأسطر
    # لتجنب انتقال الفقرة ذات السطر الواحد إلى الصفحة التالية
    if len(flowables) > 1:
        return [KeepTogether(flowables)]
    else:
        return flowables


# =========================
# Arabic helper - للعناوين والنصوص القصيرة فقط
# =========================
def ar(text):
    if not text:
        return ""

    try:
        text = str(text)

        # إزالة الأقواس لأنها تسبب انقلاب RTL
        text = text.replace("(", " - ")
        text = text.replace(")", " - ")

        # ✅ معالجة النسب المئوية بشكل نهائي (تدعم الأرقام السالبة والموجبة)
        text = text.replace("% ", "%")
        text = text.replace(" %", "%")
        # ✅ تثبيت النسب المئوية مع دعم الإشارات السالبة والموجبة
        text = re.sub(r'(-?\d+(\.\d+)?)\s*%', r'\1%', text)

        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
        return str(text)


# =========================
# Clean bullets & junk - معدلة لدعم الرموز المالية بشكل آمن
# =========================
def clean_text(text: str) -> str:
    if not text:
        return ""

    text = str(text)
    cleaned = []
    for ch in text:
        cat = unicodedata.category(ch)
        # ✅ السماح بالحروف والأرقام وعلامات الترقيم والرموز المالية المحددة
        if cat.startswith(("L", "N", "P", "Z")) or ch in "%$▲▼":
            cleaned.append(ch)

    text = "".join(cleaned)
    text = re.sub(r"^[\-\*\d\.\)]\s*", "", text)
    text = text.replace(":", " : ")
    text = text.replace("،", " ، ")
    text = text.replace("؛", " ؛ ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# =========================
# Plotly → Image - النسخة النهائية مع scale=2 لجودة عالية
# =========================
def plotly_to_image(fig, width_cm, height_cm):
    if fig is None:
        return None

    tmp = None
    try:
        img_bytes = fig.to_image(
            format="png",
            width=1200,
            height=700,
            scale=2,
            engine="kaleido"
        )

        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.write(img_bytes)
        tmp.close()

        img_obj = Image(tmp.name, width=width_cm * cm, height=height_cm * cm)
        
        # ✅ إضافة معلومات الملف المؤقت للكائن ليتم حذفه لاحقاً
        img_obj._temp_file = tmp.name
        
        return img_obj

    except Exception as e:
        print("Chart export error:", e)
        if tmp and os.path.exists(tmp.name):
            try:
                os.unlink(tmp.name)
            except:
                pass
        return None


# =========================
# Elegant divider - نسخة نهائية بمسافات مثالية
# =========================
def elegant_divider(width="80%", thickness=0.6, color=colors.HexColor("#C8C8C8")):
    return HRFlowable(
        width=width,
        thickness=thickness,
        color=color,
        spaceBefore=6,
        spaceAfter=8,
        lineCap='round'
    )


# =========================
# FOOTER
# =========================
def add_footer(canvas, doc):
    canvas.saveState()
    
    # رسم خط خفيف فوق الفوتر
    canvas.setStrokeColor(colors.HexColor("#DDDDDD"))
    canvas.line(2.4 * cm, 2 * cm, A4[0] - 2.4 * cm, 2 * cm)
    
    canvas.setFont("Amiri", 9)
    canvas.setFillColor(colors.HexColor("#777777"))
    
    page_number = canvas.getPageNumber()
    
    # ✅ تعديل الفوتر لإضافة السنة
    canvas.drawRightString(
        A4[0] - 2.4 * cm, 
        1.5 * cm, 
        ar(f"Warda Intelligence | منصة الذكاء العقاري | {datetime.now().year}")
    )
    
    canvas.drawString(
        2.4 * cm, 
        1.5 * cm, 
        ar(f"الصفحة {page_number}")
    )
    
    canvas.restoreState()


# =========================
# MAIN PDF GENERATOR - النسخة النهائية مع حل مشكلة النص العربي
# =========================
def create_pdf_from_content(
    user_info,
    content_text,
    executive_decision,
    charts_by_chapter,
    package_level,
    ai_recommendations=None
):
    buffer = BytesIO()

    # -------------------------
    # FONT
    # -------------------------
    font_path = None
    for p in [
        "Amiri-Regular.ttf",
        "fonts/Amiri-Regular.ttf",
        os.path.join(os.getcwd(), "Amiri-Regular.ttf"),
        os.path.join(os.getcwd(), "fonts", "Amiri-Regular.ttf"),
    ]:
        if os.path.exists(p):
            font_path = p
            break

    if not font_path:
        raise FileNotFoundError("Amiri font not found")

    pdfmetrics.registerFont(TTFont("Amiri", font_path))

    # -------------------------
    # DOCUMENT
    # -------------------------
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2.4 * cm,
        leftMargin=2.4 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm
    )

    styles = getSampleStyleSheet()

    # ✅ التعديل: منع Widow و Orphan lines بجعل allowWidows و allowOrphans = 0
    body = ParagraphStyle(
        "ArabicBody",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=14,
        leading=24,
        alignment=TA_RIGHT,
        wordWrap='RTL',
        spaceAfter=12,
        allowWidows=0,
        allowOrphans=0,
    )

    chapter = ParagraphStyle(
        "ArabicChapter",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=19,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#8B0000"),
        spaceBefore=24,
        spaceAfter=12,
        keepWithNext=1
    )

    ai_sub_title = ParagraphStyle(
        "AISubTitle",
        parent=styles["Heading3"],
        fontName="Amiri",
        fontSize=15.5,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#444444"),
        spaceBefore=14,
        spaceAfter=8,
    )

    title = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName="Amiri",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        spaceAfter=40
    )

    ai_executive_header = ParagraphStyle(
        "AIExecutiveHeader",
        parent=chapter,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        fontSize=17,
        spaceBefore=24,
        spaceAfter=12,
    )

    # ✅ نمط خاص للتاريخ في الغلاف (مركز)
    date_style = ParagraphStyle(
        "DateStyle",
        parent=body,
        alignment=TA_CENTER,
        fontSize=14,
        textColor=colors.HexColor("#555555"),
        spaceBefore=6,
        spaceAfter=12,
    )

    # ✅ إضافة نمط للإحصائيات الرئيسية
    stats_style = ParagraphStyle(
        "StatsStyle",
        parent=body,
        fontSize=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1B5E20"),
        spaceBefore=16,
        spaceAfter=16,
    )

    SPECIAL_TAGS = {"[[ANCHOR_CHART]]", "[[RHYTHM_CHART]]", "[[CHART_CAPTION]]"}

    story = []
    
    # حساب العرض المتاح للنص (هامش أيمن + أيسر = 4.8 سم، عرض A4 = 21 سم)
    # العرض الصافي = 21 - 4.8 = 16.2 سم
    AVAILABLE_WIDTH = A4[0] - (2.4 * cm) - (2.4 * cm)
    
    # =========================
    # ✅ DYNAMIC CHAPTER CHART MAP - حسب نوع التقرير
    # =========================
    report_kind = user_info.get("report_kind", "district") if user_info else "district"
    
    if report_kind == "city":
        # خريطة رسومات المدن - كل الفصول من 1 إلى 8
        CHAPTER_CHART_MAP = {
            1: 1, 2: 2, 3: 3, 4: 4,
            5: 5, 6: 6, 7: 7, 8: 8
        }
    else:
        # خريطة رسومات الأحياء (كما كانت من قبل)
        CHAPTER_CHART_MAP = {
            4: 4, 7: 7, 11: 11, 16: 16, 21: 21
        }

    # =========================
    # COVER - مع العنوان الكامل والتاريخ
    # =========================
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), title))
    
    # ✅ 1️⃣ إضافة عنوان التقرير الحقيقي
    if user_info:
        district = user_info.get("district_name", "")
        city = user_info.get("city_name", "")
        property_type = user_info.get("property_type", "")
        
        # تخصيص العنوان حسب نوع التقرير
        if report_kind == "city":
            subtitle = f"التقرير الاستثماري العقاري\nمدينة {city}\nتحليل سوق {property_type}"
        else:
            subtitle = f"التقرير الاستثماري العقاري\nحي {district} – مدينة {city}\nتحليل سوق {property_type}"
        
        story.append(Spacer(1, 0.6 * cm))
        story.append(Paragraph(ar(subtitle), ai_executive_header))
    
    # ✅ 2️⃣ إضافة تاريخ التقرير (باستخدام نمط مركزي)
    date_text = f"تاريخ التقرير: {datetime.now().strftime('%B %Y')}"
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(ar(date_text), date_style))
    
    # ✅ 3️⃣ إضافة جدول المؤشرات مع تحسينات التنسيق وفاصلة الآلاف
    if user_info:
        district = user_info.get("district_name", "")
        city = user_info.get("city_name", "")
        property_type = user_info.get("property_type", "")
        
        # ✅ استخدام قيم افتراضية آمنة مع شرطة "--" في حالة عدم وجود بيانات
        price = user_info.get("district_avg_price", "—")
        city_price = user_info.get("city_avg_price", "—")
        transactions = user_info.get("transactions_count", "—")
        dpi = user_info.get("dpi_score", "—")
        
        # ✅ تحويل القيم الرقمية إلى نص مع فاصلة الآلاف (بدون أرقام عشرية للأعداد الصحيحة)
        def format_number_with_commas(value):
            if value == "—":
                return "—"
            try:
                # محاولة تحويل القيمة إلى رقم
                num = float(value)
                # إذا كان الرقم عدداً صحيحاً (أو قريب جداً من الصحيح)
                if abs(num - round(num)) < 0.01:
                    return f"{int(round(num)):,}"
                else:
                    return f"{num:,.2f}"
            except (ValueError, TypeError):
                return str(value)
        
        price_formatted = format_number_with_commas(price)
        city_price_formatted = format_number_with_commas(city_price)
        transactions_formatted = format_number_with_commas(transactions)
        
        # تخصيص جدول المؤشرات حسب نوع التقرير
        if report_kind == "city":
            table_data = [
                [ar("المؤشر"), ar("القيمة")],
                [ar("المدينة"), ar(city)],
                [ar("نوع العقار"), ar(property_type)],
                [ar("متوسط سعر المتر"), ar(f"{price_formatted} ريال") if price != "—" else ar("—")],
                [ar("عدد الصفقات"), ar(f"{transactions_formatted} صفقة") if transactions != "—" else ar("—")],
                [ar("مؤشر قوة السوق"), ar(f"{dpi} / 100") if dpi != "—" else ar("—")]
            ]
        else:
            table_data = [
                [ar("المؤشر"), ar("القيمة")],
                [ar("المدينة"), ar(city)],
                [ar("الحي"), ar(district)],
                [ar("نوع العقار"), ar(property_type)],
                [ar("متوسط سعر المتر"), ar(f"{price_formatted} ريال") if price != "—" else ar("—")],
                [ar("متوسط المدينة"), ar(f"{city_price_formatted} ريال") if city_price != "—" else ar("—")],
                [ar("عدد الصفقات"), ar(f"{transactions_formatted} صفقة") if transactions != "—" else ar("—")],
                [ar("مؤشر قوة الحي"), ar(f"{dpi} / 100") if dpi != "—" else ar("—")]
            ]
        
        table = Table(table_data, colWidths=[7*cm, 9*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Amiri'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#8B0000")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F9F9F9")),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F9F9F9"), colors.white]),
        ]))
        story.append(Spacer(1, 1*cm))
        story.append(table)
    
    # ✅ إضافة إجمالي عدد الصفقات من user_info إذا كان متوفراً
    if user_info and "total_transactions" in user_info:
        total = user_info["total_transactions"]
        if total is not None:
            story.append(Spacer(1, 0.8 * cm))
            try:
                total_formatted = f"{int(float(total)):,}" if total else "0"
            except (ValueError, TypeError):
                total_formatted = str(total)
            story.append(Paragraph(
                ar(f"إجمالي الصفقات المستخدمة في التحليل: {total_formatted} صفقة"),
                stats_style
            ))
    
    story.append(PageBreak())

    # =========================
    # EXECUTIVE DECISION (INDEPENDENT)
    # =========================
    DECISION_BLOCK_TITLES = {
        "DECISION_DEFINITION": "تعريف القرار التنبؤي",
        "MARKET_STATUS": "وضع السوق الحالي",
        "PREDICTIVE_SIGNALS": "الإشارات التنبؤية",
        "SCENARIOS": "السيناريوهات المحتملة",
        "OPTIMAL_POSITION": "القرار التنفيذي",
        "DECISION_GUARANTEE": "ضمان القرار"
    }

    if executive_decision and executive_decision.strip():
        story.append(Spacer(1, 1.2 * cm))
        story.append(Paragraph(ar("الخلاصة التنفيذية للقرار"), ai_executive_header))
        story.append(elegant_divider("60%"))
        story.append(Spacer(1, 0.6 * cm))

        for line in executive_decision.split("\n"):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.2 * cm))
                continue

            # عناوين الكتل
            if line.startswith("[DECISION_BLOCK:"):
                key = line.replace("[DECISION_BLOCK:", "").replace("]", "")
                title_text = DECISION_BLOCK_TITLES.get(key, "")
                if title_text:
                    story.append(Spacer(1, 0.6 * cm))
                    story.append(Paragraph(ar(title_text), chapter))
                    story.append(elegant_divider("50%"))
                continue

            if line == "[END_DECISION_BLOCK]":
                continue

            # ✅ التعديل: إزالة ar() المزدوج - تمرير النص الخام مباشرة
            story.extend(arabic_paragraph_flowables(line, body, AVAILABLE_WIDTH))
            story.append(Spacer(1, 0.2 * cm))

        story.append(Spacer(1, 1.0 * cm))
        story.append(elegant_divider("30%"))
        story.append(PageBreak())

    # =========================
    # TRANSITION PAGE – HOW TO READ THIS REPORT
    # =========================
    story.append(Spacer(1, 2.5 * cm))

    story.append(Paragraph(
        ar("كيف تقرأ هذا التقرير بناءً على القرار أعلاه"),
        ai_executive_header
    ))

    story.append(elegant_divider("55%"))
    story.append(Spacer(1, 1.0 * cm))

    # ✅ التعديل: إزالة ar() المزدوج - تمرير النص الخام مباشرة
    transition_texts = [
        "الخلاصة التنفيذية للقرار تمثل القرار المعتمد لهذا التقرير، "
        "وقد تم اشتقاقه بناءً على مؤشرات رقمية ومعايير تحليلية محددة.",
        
        "الفصول التالية لا تُقرأ كتحليل عام للسوق، ولا كمسار للوصول إلى قرار جديد، "
        "بل كشرح منهجي للأسس التي بُني عليها القرار الصادر.",
        
        "كل فصل يفسر جانبًا محددًا من القرار، ويبيّن السياق السوقي، "
        "وحدود المخاطر، وطبيعة الفرص، وشروط التوقيت والتنفيذ، "
        "بهدف توضيح لماذا جاء القرار بهذه الصيغة تحديدًا.",
        
        "القرار موجود في الأعلى، "
        "وما يلي هو الإطار التحليلي الذي يبرره، "
        "ويحدّد نطاق صلاحيته، ويضبط تطبيقه."
    ]
    
    for text in transition_texts:
        story.extend(arabic_paragraph_flowables(text, body, AVAILABLE_WIDTH))
        story.append(Spacer(1, 0.15 * cm))

    story.append(Spacer(1, 1.2 * cm))
    story.append(elegant_divider("30%"))
    story.append(PageBreak())

    # =========================
    # PROCESS CONTENT WITH DYNAMIC CHART MAPPING
    # =========================
    chapter_index = 0
    chart_cursor = {}
    
    first_chapter_processed = False
    
    # قائمة لتتبع الملفات المؤقتة لحذفها لاحقاً
    temp_files = []

    for raw in content_text.split("\n"):
        raw_stripped = raw.strip()

        # ✅ إزالة Spacer للأسطر الفارغة لمنع الصفحات الفارغة
        if not raw_stripped:
            continue

        clean = raw_stripped if raw_stripped in SPECIAL_TAGS else clean_text(raw)

        if clean.startswith(("📊", "💎", "⚠️")):
            story.append(Spacer(1, 0.6 * cm))
            story.append(elegant_divider())
            story.append(Paragraph(ar(clean), ai_sub_title))
            story.append(Spacer(1, 0.3 * cm))
            continue

        if raw_stripped.startswith("الفصل"):
            if first_chapter_processed:
                story.append(PageBreak())
            chapter_index += 1
            chart_cursor[chapter_index] = 0
            story.append(Paragraph(ar(clean), chapter))
            story.append(Spacer(1, 0.3 * cm))
            story.append(elegant_divider("40%"))
            story.append(Spacer(1, 0.6 * cm))
            first_chapter_processed = True
            continue

        if clean == "[[ANCHOR_CHART]]":
            real_chapter = CHAPTER_CHART_MAP.get(chapter_index)
            if real_chapter:
                charts = charts_by_chapter.get(f"chapter_{real_chapter}", [])
                cursor = chart_cursor.get(chapter_index, 0)

                if cursor < len(charts):
                    img = plotly_to_image(charts[cursor], 16.8, 9)
                    if img:
                        if hasattr(img, '_temp_file'):
                            temp_files.append(img._temp_file)
                        
                        story.append(Spacer(1, 0.8 * cm))
                        story.append(img)
                        story.append(Spacer(1, 0.4 * cm))
                    chart_cursor[chapter_index] += 1
            continue

        if clean == "[[RHYTHM_CHART]]":
            real_chapter = CHAPTER_CHART_MAP.get(chapter_index)
            if real_chapter:
                charts = charts_by_chapter.get(f"chapter_{real_chapter}", [])
                cursor = chart_cursor.get(chapter_index, 0)

                if cursor < len(charts):
                    fig = charts[cursor]
                    is_indicator = (
                        fig is not None
                        and hasattr(fig, 'data')
                        and len(fig.data) > 0
                        and isinstance(fig.data[0], go.Indicator)
                    )
                    img = plotly_to_image(fig, 17.5 if is_indicator else 16.8,
                                           9.5 if is_indicator else 9)
                    if img:
                        if hasattr(img, '_temp_file'):
                            temp_files.append(img._temp_file)
                        
                        story.append(Spacer(1, 0.8 * cm if is_indicator else 0.7 * cm))
                        story.append(img)
                        story.append(Spacer(1, 0.4 * cm))
                    chart_cursor[chapter_index] += 1
            continue

        # ✅ التعديل الأساسي: إزالة ar() المزدوج - تمرير النص الخام مباشرة
        # هذا هو الحل النهائي لمشكلة انقلاب النص من الأسفل إلى الأعلى
        if clean and clean not in SPECIAL_TAGS:
            story.extend(arabic_paragraph_flowables(clean, body, AVAILABLE_WIDTH))
            story.append(Spacer(1, 0.15 * cm))
        elif clean not in SPECIAL_TAGS:
            story.extend(arabic_paragraph_flowables(clean, body, AVAILABLE_WIDTH))
            story.append(Spacer(1, 0.15 * cm))

    doc.build(
        story, 
        onFirstPage=add_footer, 
        onLaterPages=add_footer
    )
    
    buffer.seek(0)
    
    # حذف جميع الملفات المؤقتة بعد بناء PDF
    unique_temp_files = list(set(temp_files))
    for temp_file in unique_temp_files:
        try:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        except Exception as e:
            print(f"Error deleting temp file {temp_file}: {e}")
    
    return buffer
