from io import BytesIO
from datetime import datetime
import pandas as pd
import math
import os

# ✅ استيرادات إجبارية للعربية
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ✅ استيراد المنسّق
from report_orchestrator import build_report_story

# ✅ دالة معالجة العربية
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
        if isinstance(val, (list, tuple, set)):
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
    """
    مولد PDF النهائي
    يعتمد كليًا على report_orchestrator
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors

        # -----------------------------
        # الخط العربي
        # -----------------------------
        font_path = "Amiri-Regular.ttf"
        if not os.path.exists(font_path):
            buffer = BytesIO()
            buffer.write("Arabic font missing".encode("utf-8"))
            buffer.seek(0)
            return buffer

        pdfmetrics.registerFont(TTFont("Amiri", font_path))

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )

        # -----------------------------
        # الأنماط
        # -----------------------------
        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(
            name="body",
            parent=styles["Normal"],
            fontName="Amiri",
            fontSize=12,
            leading=18,
            alignment=2,
            textColor=colors.black
        ))

        styles.add(ParagraphStyle(
            name="title",
            parent=styles["Title"],
            fontName="Amiri",
            fontSize=20,
            alignment=2,
            textColor=colors.HexColor("#1A5276"),
            spaceAfter=20
        ))

        styles.add(ParagraphStyle(
            name="subtitle",
            parent=styles["Heading2"],
            fontName="Amiri",
            fontSize=14,
            alignment=2,
            textColor=colors.HexColor("#2874A6"),
            spaceAfter=15
        ))

        # -----------------------------
        # بناء التقرير عبر المنسّق
        # -----------------------------
        story = build_report_story(user_info, styles)

        # -----------------------------
        # توليد PDF
        # -----------------------------
        doc.build(story)
        buffer.seek(0)
        return buffer

    except Exception as e:
        print("PDF Error:", e)
        buffer = BytesIO()
        buffer.write("PDF generation failed".encode("utf-8"))
        buffer.seek(0)
        return buffer
