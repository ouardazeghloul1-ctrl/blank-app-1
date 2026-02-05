# report_pdf_generator.py
from io import BytesIO
from datetime import datetime
import os
import tempfile
import streamlit as st
import re
import unicodedata

import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    PageBreak, Image, KeepTogether, HRFlowable,
    Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import plotly.graph_objects as go


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
# Clean text
# =========================
def clean_text(text: str) -> str:
    if not text:
        return ""

    cleaned = []
    for ch in text:
        if unicodedata.category(ch).startswith(("L", "N", "P", "Z")):
            cleaned.append(ch)

    text = "".join(cleaned)
    text = re.sub(r"^[\-\*\d\.\)]\s*", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# =========================
# Executive Decision Box
# =========================
def executive_decision_box(text, width_cm=16):
    return Table(
        [[Paragraph(ar(text), ParagraphStyle(
            "DecisionText",
            fontName="Amiri",
            fontSize=15,
            leading=30,
            alignment=TA_RIGHT,
            textColor=colors.HexColor("#1f1f1f"),
        ))]],
        colWidths=[width_cm * cm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F3F4F6")),
            ("BOX", (0, 0), (-1, -1), 2, colors.HexColor("#7a0000")),
            ("INNERPADDING", (0, 0), (-1, -1), 22),
        ])
    )


def elegant_divider():
    return HRFlowable(
        width="50%",
        thickness=1,
        color=colors.HexColor("#7a0000"),
        spaceBefore=18,
        spaceAfter=22,
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

    # FONT
    font_path = "Amiri-Regular.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError("Amiri-Regular.ttf not found")

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
        fontSize=14.5,
        leading=28,
        alignment=TA_RIGHT,
        spaceAfter=18,
    )

    chapter = ParagraphStyle(
        "Chapter",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=18,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#9c1c1c"),
        spaceBefore=32,
        spaceAfter=16,
        keepWithNext=1
    )

    title = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Amiri",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        spaceAfter=50
    )

    executive_title = ParagraphStyle(
        "ExecutiveTitle",
        parent=styles["Heading1"],
        fontName="Amiri",
        fontSize=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#5a0000"),
        spaceAfter=20
    )

    story = []

    # COVER
    story.append(Spacer(1, 7 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), title))
    story.append(PageBreak())

    # CONTENT
    decision_buffer = []
    decision_mode = False

    for raw in content_text.split("\n"):
        line = clean_text(raw)

        # ===== FINAL DECISION ONLY =====
        if line.startswith("🏁"):
            story.append(PageBreak())
            story.append(Spacer(1, 2 * cm))
            story.append(Paragraph(
                ar("القرار الاستشاري النهائي: موقفك الصحيح الآن"),
                executive_title
            ))
            story.append(elegant_divider())
            decision_mode = True
            decision_buffer = []
            continue

        if decision_mode:
            if line:
                decision_buffer.append(line)
            continue

        if line:
            story.append(Paragraph(ar(line), body))

    if decision_buffer:
        story.append(Spacer(1, 1.5 * cm))
        story.append(executive_decision_box("\n\n".join(decision_buffer)))

    doc.build(story)
    buffer.seek(0)
    return buffer
