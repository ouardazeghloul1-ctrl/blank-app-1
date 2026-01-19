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
# Arabic helper (واحد فقط – نهائي)
# =========================
def ar(text):
    if not text:
        return ""
    try:
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)


# =========================
# Cover Line Function
# =========================
def cover_line(label, value, style):
    return Paragraph(
        ar(f"{label}: {value}"),
        style
    )


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
    # FONT
    # -------------------------------------------------
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
        raise FileNotFoundError("❌ Amiri-Regular.ttf غير موجود")

    pdfmetrics.registerFont(TTFont("Amiri", font_path))

    # -------------------------------------------------
    # DOCUMENT
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

    arabic_style = ParagraphStyle(
        "ArabicBody",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=12,
        leading=18,
        alignment=TA_RIGHT,
        spaceAfter=8
    )

    value_style = ParagraphStyle(
        "ValueStyle",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=12,
        leading=18,
        alignment=TA_RIGHT,
        spaceAfter=8
    )

    title_style = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName="Amiri",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        spaceAfter=30
    )

    subtitle_style = ParagraphStyle(
        "ArabicSubtitle",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=16,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#9c1c1c"),
        spaceBefore=18,
        spaceAfter=12
    )

    story = []

    # -------------------------------------------------
    # COVER
    # -------------------------------------------------
    story.append(Spacer(1, 5 * cm))
    story.append(Paragraph(ar("تقرير وردة الذكاء العقاري"), title_style))
    story.append(Spacer(1, 1 * cm))

    story.append(cover_line("المدينة", user_info.get("city", ""), arabic_style))
    story.append(cover_line("نوع العقار", user_info.get("property_type", ""), arabic_style))
    story.append(cover_line("الباقة", package_level, arabic_style))
    story.append(cover_line("التاريخ", datetime.now().strftime("%Y-%m-%d"), arabic_style))
    
    # ⚠️ PageBreak تم حذفه هنا تمامًا - هذا كان يسبب صفحة فارغة

    # -------------------------------------------------
    # CONTENT TEXT (التعديل النهائي - الأهم)
    # -------------------------------------------------
    if isinstance(content_text, str):
        lines = content_text.split("\n")
        for line in lines:
            clean = line.strip()
            if not clean:
                story.append(Spacer(1, 0.4 * cm))
                continue

            if clean.startswith("الفصل"):
                story.append(Spacer(1, 1 * cm))
                story.append(Paragraph(ar(clean), subtitle_style))
                story.append(Spacer(1, 0.6 * cm))
            else:
                story.append(Paragraph(ar(clean), arabic_style))

    # -------------------------------------------------
    # CHARTS
    # -------------------------------------------------
    try:
        charts_engine = AdvancedCharts()
        charts = charts_engine.generate_all_charts(df=market_data)

        if charts:
            story.append(PageBreak())
            story.append(Paragraph(ar("التحليل البياني المتقدم"), title_style))

            for chapter, figures in charts.items():
                if not figures:
                    continue

                story.append(Paragraph(ar(chapter.replace("_", " ")), subtitle_style))

                for fig in figures:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                        fig.write_image(tmp.name, width=1200, height=700, scale=2)
                        story.append(Image(tmp.name, width=16 * cm, height=9 * cm))
                        story.append(Spacer(1, 0.5 * cm))
    except Exception as e:
        story.append(Paragraph(ar("تعذر تحميل الرسومات"), arabic_style))
        story.append(Paragraph(str(e), value_style))

    # -------------------------------------------------
    # AI RECOMMENDATIONS
    # -------------------------------------------------
    if ai_recommendations:
        story.append(PageBreak())
        story.append(Paragraph(ar("التوصيات الذكية المتقدمة"), title_style))

        for k, v in ai_recommendations.items():
            story.append(Paragraph(ar(str(k)), subtitle_style))
            story.append(Paragraph(ar(str(v)), arabic_style))
            story.append(Spacer(1, 0.5 * cm))

    # -------------------------------------------------
    # FOOTER (التعديل النهائي)
    # -------------------------------------------------
    # ⚠️ PageBreak تم حذفه هنا أيضًا
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph(ar("نهاية التقرير"), subtitle_style))
    story.append(Paragraph(ar("Warda Intelligence © 2024"), arabic_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
