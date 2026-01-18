# report_pdf_generator.py
from io import BytesIO
from datetime import datetime
import os
import tempfile

import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from advanced_charts import AdvancedCharts


# =========================
# Arabic helper - بسيطة جداً كما كانت
# =========================
def ar(text):
    """
    دالة بسيطة: تأخذ نصاً عربياً وتعطيه شكلاً صحيحاً
    لا تحلل، لا تتخمين، لا ذكاء
    """
    if not text:
        return ""
    
    # حاول معالجة النص العربي، وإلا ارجع النص كما هو
    try:
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        # إذا فشلت المعالجة، ارجع النص كما هو
        return str(text)


# =========================
# MAIN PDF GENERATOR
# =========================
def create_pdf_from_content(
    user_info,
    market_data,
    real_data,
    content_text,
    package_level,
    ai_recommendations=None
):
    buffer = BytesIO()

    # -------------------------------------------------
    # 1) LOAD AMIRI FONT
    # -------------------------------------------------
    FONT_CANDIDATES = [
        "Amiri-Regular.ttf",
        os.path.join("fonts", "Amiri-Regular.ttf"),
        os.path.join(os.getcwd(), "Amiri-Regular.ttf"),
        os.path.join(os.getcwd(), "fonts", "Amiri-Regular.ttf"),
    ]

    font_path = None
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            font_path = path
            break

    if not font_path:
        raise FileNotFoundError(
            "❌ Amiri-Regular.ttf غير موجود. "
            "ضع الملف في نفس مجلد main.py أو داخل مجلد fonts/"
        )

    pdfmetrics.registerFont(TTFont("Amiri", font_path))

    # -------------------------------------------------
    # 2) DOCUMENT
    # -------------------------------------------------
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    # ستايل للنصوص العربية
    arabic_style = ParagraphStyle(
        "ArabicBody",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=12,
        leading=18,
        alignment=TA_RIGHT,
        spaceAfter=6
    )

    # ستايل للقيم والأرقام (لا معالجة عربية)
    value_style = ParagraphStyle(
        "ValueStyle",
        parent=styles["Normal"],
        fontName="Amiri",  # نفس الخط لكن لا معالجة
        fontSize=12,
        leading=18,
        alignment=TA_RIGHT,
        spaceAfter=6
    )

    title_style = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName="Amiri",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#b30000"),
        spaceAfter=30
    )

    subtitle_style = ParagraphStyle(
        "ArabicSubtitle",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=16,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#7a0000"),
        spaceBefore=20,
        spaceAfter=12
    )

    story = []

    # -------------------------------------------------
    # 3) COVER PAGE - فصل يدوي صريح
    # -------------------------------------------------
    story.append(Spacer(1, 5 * cm))
    story.append(Paragraph(ar("تقرير وردة الذكاء العقاري"), title_style))
    story.append(Spacer(1, 1 * cm))
    
    # ✅ فصل صريح: نص عربي + قيمة منفصلة
    story.append(Paragraph(ar("المدينة:"), arabic_style))
    story.append(Paragraph(str(user_info.get('city', '')), value_style))
    
    story.append(Paragraph(ar("نوع العقار:"), arabic_style))
    story.append(Paragraph(str(user_info.get('property_type', '')), value_style))
    
    story.append(Paragraph(ar("الباقة:"), arabic_style))
    story.append(Paragraph(str(package_level), value_style))
    
    story.append(Paragraph(ar("التاريخ:"), arabic_style))
    story.append(Paragraph(datetime.now().strftime('%Y-%m-%d'), value_style))
    
    # فاصل كبير بدلاً من PageBreak فوري
    story.append(Spacer(1, 3 * cm))

    # -------------------------------------------------
    # 4) TEXT CONTENT - حل مؤقت بسيط
    # -------------------------------------------------
    if isinstance(content_text, list):
        # إذا كان content_text قائمة من Paragraphs جاهزة
        story.extend(content_text)
    elif isinstance(content_text, str):
        # ✅ حل بسيط ومضمون:
        # نعرض كل المحتوى كقيمة واحدة (بدون معالجة عربية)
        # ونترك تنظيفه للمرحلة القادمة (orchestrator)
        
        # نقسم إلى أسطر للحفاظ على التنسيق
        lines = content_text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.3 * cm))
                continue
            
            # ❌ لا نحلل، لا نتخمين
            # ✅ نعرض الخط كما هو (سيتحمله ReportLab)
            story.append(Paragraph(line, value_style))
    
    # فاصل قبل الرسومات
    story.append(Spacer(1, 2 * cm))
    
    # -------------------------------------------------
    # 5) CHARTS
    # -------------------------------------------------
    try:
        charts_engine = AdvancedCharts()
        charts = charts_engine.generate_all_charts(
            df=market_data,
            user_info=user_info,
            real_data=real_data
        )

        if charts:
            # PageBreak فقط إذا كان هناك محتوى كافٍ
            story.append(PageBreak())
            story.append(Paragraph(ar("التحليل البياني المتقدم"), title_style))

            for chapter, figures in charts.items():
                if not figures:
                    continue

                story.append(Spacer(1, 0.5 * cm))
                # ✅ نص عربي صرف فقط
                story.append(Paragraph(ar(chapter.replace("_", " ")), subtitle_style))

                for fig in figures:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                        fig.write_image(tmp.name, width=1200, height=700, scale=2)
                        story.append(Image(tmp.name, width=16 * cm, height=9 * cm))
                        story.append(Spacer(1, 0.5 * cm))
    except Exception as e:
        story.append(Paragraph(ar("تعذر تحميل الرسومات البيانية"), arabic_style))
        story.append(Paragraph(str(e), value_style))

    # -------------------------------------------------
    # 6) AI RECOMMENDATIONS - فصل يدوي صريح
    # -------------------------------------------------
    if ai_recommendations:
        # نضيف عنوان القسم أولاً
        story.append(Paragraph(ar("التوصيات الذكية المتقدمة"), title_style))
        story.append(Spacer(1, 1 * cm))
        
        # إذا كان هناك توصيات كثيرة، نضيف PageBreak
        if isinstance(ai_recommendations, dict) and len(ai_recommendations) > 3:
            story.append(PageBreak())
        
        if isinstance(ai_recommendations, dict):
            for k, v in ai_recommendations.items():
                # ✅ فصل صريح: عنوان + محتوى
                story.append(Paragraph(ar(str(k)), subtitle_style))
                story.append(Paragraph(str(v), value_style))
                story.append(Spacer(1, 0.5 * cm))
    
    # -------------------------------------------------
    # 7) FOOTER - بدون PageBreak غير ضروري
    # -------------------------------------------------
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph(ar("نهاية التقرير"), subtitle_style))
    story.append(Paragraph(ar("Warda Intelligence © 2024"), arabic_style))

    # -------------------------------------------------
    # 8) BUILD
    # -------------------------------------------------
    doc.build(story)
    buffer.seek(0)
    return buffer
