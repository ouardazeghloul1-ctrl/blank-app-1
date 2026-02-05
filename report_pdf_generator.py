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
        cat = unicodedata.category(ch)
        if cat.startswith(("L", "N", "P", "Z")):
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
        [[Paragraph(
            ar(text),
            ParagraphStyle(
                "DecisionText",
                fontName="Amiri",
                fontSize=14.5,
                leading=28,
                alignment=TA_RIGHT,
                textColor=colors.HexColor("#222222"),
            )
        )]],
        colWidths=[width_cm * cm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F3F5")),
            ("BOX", (0, 0), (-1, -1), 1.8, colors.HexColor("#7a0000")),
            ("INNERPADDING", (0, 0), (-1, -1), 20),
            ("TOPPADDING", (0, 0), (-1, -1), 22),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
            ("LEFTPADDING", (0, 0), (-1, -1), 18),
            ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ])
    )


def elegant_divider():
    return HRFlowable(
        width="60%",
        thickness=0.8,
        color=colors.HexColor("#7a0000"),
        spaceBefore=14,
        spaceAfter=16,
        lineCap="round"
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
    # FONT (correct & robust)
    # -------------------------
    font_path = None
    for p in [
        "Amiri-Regular.ttf",
        os.path.join(os.getcwd(), "Amiri-Regular.ttf"),
    ]:
        if os.path.exists(p):
            font_path = p
            break

    if not font_path:
        raise FileNotFoundError("Amiri-Regular.ttf not found in project root")

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
        spaceAfter=22,
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
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=19,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#5a0000"),
        spaceAfter=18
    )

    story = []

    # =========================
    # COVER
    # =========================
    story.append(Spacer(1, 7 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), title))
    story.append(PageBreak())

    # =========================
    # META PAGE
    # =========================
    report_date = datetime.now().strftime("%Y-%m-%d")

    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph(
        ar(f"<b>تاريخ إنشاء التقرير:</b> {report_date}"),
        body
    ))
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph(
        ar("<b>هذا التقرير مبني على بيانات سوقية فعلية تم تحليلها آليًا.</b>"),
        body
    ))
    story.append(PageBreak())

    # =========================
    # CONTENT + DECISION
    # =========================
    decision_buffer = []
    decision_mode = False

    for raw in content_text.split("\n"):
        clean = clean_text(raw)

        if clean.startswith("🏁"):
            story.append(PageBreak())
            story.append(Spacer(1, 1.2 * cm))
            story.append(Paragraph(
                ar("القرار الاستشاري النهائي: موقفك الصحيح الآن"),
                executive_header
            ))
            story.append(elegant_divider())
            decision_mode = True
            decision_buffer = []
            continue

        if decision_mode:
            if clean:
                decision_buffer.append(clean)
            continue

        if clean:
            story.append(Paragraph(ar(clean), body))

    if decision_buffer:
        story.append(Spacer(1, 1 * cm))
        story.append(executive_decision_box("\n\n".join(decision_buffer)))

    doc.build(story)
    buffer.seek(0)
    return buffer
