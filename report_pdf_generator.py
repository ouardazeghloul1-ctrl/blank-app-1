# report_pdf_generator.py
from io import BytesIO
from datetime import datetime
import os
import tempfile
import re
import unicodedata

import streamlit as st
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
# Arabic helpers
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
# Clean text (no emojis)
# =========================
def clean_text(text: str) -> str:
    if not text:
        return ""

    cleaned = []
    for ch in text:
        cat = unicodedata.category(ch)
        # Allow letters, numbers, punctuation, spaces
        if cat.startswith(("L", "N", "P", "Z")):
            cleaned.append(ch)

    text = "".join(cleaned)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# =========================
# Executive decision box
# =========================
def executive_decision_box(text, width_cm=16):
    return Table(
        [[Paragraph(ar(text), ParagraphStyle(
            "DecisionText",
            fontName="Amiri",
            fontSize=14.5,
            leading=28,
            alignment=TA_RIGHT,
            textColor=colors.HexColor("#222222"),
        ))]],
        colWidths=[width_cm * cm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F3F5")),
            ("BOX", (0, 0), (-1, -1), 1.6, colors.HexColor("#7a0000")),
            ("INNERPADDING", (0, 0), (-1, -1), 18),
            ("TOPPADDING", (0, 0), (-1, -1), 20),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
            ("LEFTPADDING", (0, 0), (-1, -1), 16),
            ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ])
    )


# =========================
# Plotly → Image
# =========================
def plotly_to_image(fig, width_cm, height_cm):
    if fig is None:
        return None
    try:
        img_bytes = fig.to_image(
            format="png",
            width=int(width_cm * 38),
            height=int(height_cm * 38)
        )
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.write(img_bytes)
        tmp.close()
        return Image(tmp.name, width=width_cm * cm, height=height_cm * cm)
    except Exception:
        return None


# =========================
# Divider
# =========================
def elegant_divider(width="80%", thickness=0.6, color=colors.HexColor("#B0B0B0")):
    return HRFlowable(
        width=width,
        thickness=thickness,
        color=color,
        spaceBefore=12,
        spaceAfter=14,
        lineCap='round'
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

    body = ParagraphStyle(
        "ArabicBody",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=14.5,
        leading=28,
        alignment=TA_RIGHT,
        spaceAfter=18,
    )

    chapter = ParagraphStyle(
        "ArabicChapter",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=18,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#7a0000"),
        spaceBefore=30,
        spaceAfter=14,
        keepWithNext=1
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

    executive_header = ParagraphStyle(
        "ExecutiveHeader",
        parent=chapter,
        alignment=TA_CENTER,
        fontSize=19,
        textColor=colors.HexColor("#5a0000"),
        spaceBefore=20,
        spaceAfter=14,
    )

    story = []

    # =========================
    # COVER
    # =========================
    story.append(Spacer(1, 7 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), title))
    story.append(PageBreak())

    # =========================
    # CONTENT
    # =========================
    lines = content_text.split("\n")
    decision_buffer = []
    in_decision = False

    for raw in lines:
        clean = clean_text(raw)

        if not clean:
            story.append(Spacer(1, 0.6 * cm))
            continue

        # =========================
        # EXECUTIVE DECISION START
        # =========================
        if clean.startswith("EXECUTIVE_DECISION_START"):
            story.append(PageBreak())
            story.append(Spacer(1, 1.2 * cm))
            story.append(Paragraph(ar("الخلاصة التنفيذية التنبؤية"), executive_header))
            story.append(elegant_divider(width="50%", thickness=0.8, color=colors.HexColor("#7a0000")))
            story.append(Spacer(1, 0.6 * cm))
            in_decision = True
            decision_buffer = []
            continue

        if in_decision:
            decision_buffer.append(clean)
            continue

        # =========================
        # NORMAL TEXT
        # =========================
        story.append(Paragraph(ar(clean), body))

    # =========================
    # ADD EXECUTIVE BOX
    # =========================
    if decision_buffer:
        story.append(Spacer(1, 0.8 * cm))
        story.append(executive_decision_box("\n\n".join(decision_buffer)))
        story.append(Spacer(1, 1.2 * cm))

    # =========================
    # BUILD
    # =========================
    doc.build(story)
    buffer.seek(0)
    return buffer
