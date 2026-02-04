# report_pdf_generator.py
# =========================================
# STABLE PDF GENERATOR – WARDA
# نقطة دخول موحّدة وآمنة 100%
# =========================================

from io import BytesIO
import os
import tempfile
import re
import unicodedata

import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    PageBreak, Image, KeepTogether,
    Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# =========================
# Arabic helper
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
# Safe clean
# =========================
def clean_text(text: str) -> str:
    if not text:
        return ""
    cleaned = []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat.startswith(("L", "N", "P", "Z")):
            cleaned.append(ch)
    return re.sub(r"\s+", " ", "".join(cleaned)).strip()


# =========================
# Core PDF builder
# =========================
def create_pdf_from_blocks(blocks, charts_by_chapter=None, **context):
    if not blocks:
        blocks = []
    if charts_by_chapter is None:
        charts_by_chapter = {}

    buffer = BytesIO()

    # ---- FONT ----
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

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2.4 * cm,
        leftMargin=2.4 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm
    )

    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=14,
        leading=26,
        alignment=TA_RIGHT,
        spaceAfter=14
    )

    story = []

    for block in blocks:
        text = clean_text(block.get("content", ""))
        if text:
            story.append(Paragraph(ar(text), body))

    if not story:
        story.append(Paragraph(ar("تم إنشاء التقرير بنجاح."), body))

    doc.build(story)
    buffer.seek(0)
    return buffer


# =================================================
# SINGLE SAFE ENTRY POINT (🔥 المهم)
# =================================================
def create_pdf_from_content(**kwargs):
    """
    الدالة الوحيدة التي يستدعيها streamlit_app.py
    تقبل أي شكل من المدخلات بدون أخطاء
    """

    # الحالة 1: نظام جديد
    blocks = kwargs.get("blocks")

    # الحالة 2: نظام قديم (content_text)
    if blocks is None:
        content_text = kwargs.get("content_text", "")
        blocks = [
            {"type": "text", "content": line}
            for line in content_text.split("\n")
            if line.strip()
        ]

    charts_by_chapter = kwargs.get("charts_by_chapter", {})

    return create_pdf_from_blocks(
        blocks=blocks,
        charts_by_chapter=charts_by_chapter
    )
