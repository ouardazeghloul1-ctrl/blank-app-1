from io import BytesIO
from datetime import datetime
import os
import math
import tempfile

import pandas as pd

# Arabic support
import arabic_reshaper
from bidi.algorithm import get_display

# ReportLab
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Charts system
from advanced_charts import AdvancedCharts


# =========================
# Arabic text helper
# =========================
def ar(text):
    if not text:
        return ""
    try:
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)


def safe_num(val, fmt=",.0f", default="N/A"):
    try:
        if val is None:
            return default
        if isinstance(val, float) and math.isnan(val):
            return default
        return format(val, fmt)
    except Exception:
        return default


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

    # ---- Font
    font_path = "Amiri-Regular.ttf"
    if not os.path.exists(font_path):
        buffer.write("Arabic font missing".encode("utf-8"))
        buffer.seek(0)
        return buffer

    pdfmetrics.registerFont(TTFont("Amiri", font_path))

    # ---- Document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        "ArabicBody",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=12,
        leading=18,
        alignment=2
    )

    title_style = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName="Amiri",
        fontSize=20,
        alignment=2,
        textColor=colors.HexColor("#1A5276"),
        spaceAfter=30
    )

    subtitle_style = ParagraphStyle(
        "ArabicSubtitle",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=15,
        alignment=2,
        textColor=colors.HexColor("#2874A6"),
        spaceBefore=20,
        spaceAfter=15
    )

    story = []

    # =========================
    # 1️⃣ COVER PAGE
    # =========================
    story.append(Spacer(1, 6 * cm))
    story.append(Paragraph(ar("تقرير وردة الذكاء العقاري"), title_style))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(ar(f"المدينة: {user_info.get('city')}"), body_style))
    story.append(Paragraph(ar(f"نوع العقار: {user_info.get('property_type')}"), body_style))
    story.append(Paragraph(ar(f"الباقة: {package_level}"), body_style))
    story.append(Paragraph(ar(datetime.now().strftime("%Y-%m-%d")), body_style))
    story.append(PageBreak())

    # =========================
    # 2️⃣ TEXT CONTENT (الفصول)
    # =========================
    lines = content_text.split("\n")
    for line in lines:
        clean = line.strip()

        if clean == "":
            story.append(Spacer(1, 0.6 * cm))
            continue

        if clean.startswith("الفصل"):
            story.append(PageBreak())
            story.append(Paragraph(ar(clean), title_style))
            story.append(Spacer(1, 1 * cm))
            continue

        if clean[:2].isdigit():
            story.append(Paragraph(ar(clean), subtitle_style))
            continue

        story.append(Paragraph(ar(clean), body_style))
        story.append(Spacer(1, 0.3 * cm))

    # =========================
    # 3️⃣ CHARTS SECTION (🔥 المرحلة 1)
    # =========================
    story.append(PageBreak())
    story.append(Paragraph(ar("التحليل البياني المتقدم"), title_style))
    story.append(Spacer(1, 1 * cm))

    charts_engine = AdvancedCharts()

    charts = charts_engine.generate_all_charts(
        market_data=market_data,
        real_data=real_data,
        user_info=user_info
    )

    for chart_title, fig in charts.items():
        # حفظ الرسم مؤقتًا
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            fig.savefig(tmp.name, dpi=200, bbox_inches="tight")
            img_path = tmp.name

        story.append(PageBreak())
        story.append(Paragraph(ar(chart_title), subtitle_style))
        story.append(Spacer(1, 0.5 * cm))
        story.append(Image(img_path, width=16 * cm, height=9 * cm))

    # =========================
    # 4️⃣ BUILD
    # =========================
    doc.build(story)
    buffer.seek(0)
    return buffer
