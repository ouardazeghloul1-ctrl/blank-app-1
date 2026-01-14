from io import BytesIO
from datetime import datetime
import os
import math
import pandas as pd

# ========= ReportLab =========
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ========= orchestrator =========
from report_orchestrator import build_report_story

# ========= أدوات =========
def safe_num(val, fmt=",.0f", default="N/A"):
    try:
        if val is None:
            return default
        if isinstance(val, float) and math.isnan(val):
            return default
        return format(val, fmt)
    except Exception:
        return default


def create_pdf_from_content(
    user_info,
    market_data,
    real_data,
    content_text,
    package_level,
    ai_recommendations=None
):
    buffer = BytesIO()

    # ========= الخط العربي =========
    font_path = "Amiri-Regular.ttf"
    if not os.path.exists(font_path):
        buffer.write("❌ ملف الخط العربي غير موجود".encode("utf-8"))
        buffer.seek(0)
        return buffer

    pdfmetrics.registerFont(TTFont("Amiri", font_path))

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
        alignment=2
    )

    title_style = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName="Amiri",
        fontSize=18,
        alignment=2,
        textColor=colors.HexColor("#1A5276"),
        spaceAfter=20
    )

    subtitle_style = ParagraphStyle(
        "ArabicSubtitle",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=14,
        alignment=2,
        textColor=colors.HexColor("#2874A6"),
        spaceAfter=12
    )

    styles_bundle = {
        "body": arabic_style,
        "title": title_style,
        "subtitle": subtitle_style
    }

    # ========= هنا النقطة الحاسمة =========
    story = build_report_story(user_info, styles_bundle)

    doc.build(story)
    buffer.seek(0)
    return buffer
