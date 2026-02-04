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
# Clean text (SAFE)
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
            ("BOX", (0, 0), (-1, -1), 1.8, colors.HexColor("#7a0000")),
            ("INNERPADDING", (0, 0), (-1, -1), 20),
            ("TOPPADDING", (0, 0), (-1, -1), 22),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
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
# Elegant divider
# =========================
def elegant_divider(width="60%", thickness=0.7, color=colors.HexColor("#9c1c1c")):
    return HRFlowable(
        width=width,
        thickness=thickness,
        color=color,
        spaceBefore=14,
        spaceAfter=18,
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
    # FONT (SAFE SEARCH)
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
        raise FileNotFoundError("Amiri-Regular.ttf not found")

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
        "Body",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=14.5,
        leading=28,
        alignment=TA_RIGHT,
        spaceAfter=22,
    )

    chapter = ParagraphStyle(
        "Chapter",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=18,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#9c1c1c"),
        spaceBefore=36,
        spaceAfter=18,
        keepWithNext=1
    )

    ai_box = ParagraphStyle(
        "AIBox",
        parent=body,
        backColor=colors.HexColor("#F2F4F7"),
        leftIndent=14,
        rightIndent=14,
        spaceBefore=14,
        spaceAfter=18,
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

    ai_exec_title = ParagraphStyle(
        "AIExecTitle",
        parent=chapter,
        alignment=TA_CENTER,
        fontSize=19,
        textColor=colors.HexColor("#5a0000"),
        spaceBefore=30,
        spaceAfter=18,
    )

    # =========================
    # BUILD STORY
    # =========================
    story = []

    # COVER
    story.append(Spacer(1, 7 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), title))
    story.append(PageBreak())

    charts_by_chapter = st.session_state.get("charts_by_chapter", {})
    chapter_index = 0
    chart_cursor = {}
    first_chapter = False

    ai_mode = False
    decision_mode = False
    decision_buffer = []

    lines = content_text.split("\n")
    lines_iter = iter(lines)

    for raw in lines_iter:
        raw_strip = raw.strip()
        clean = raw_strip if raw_strip.startswith("[[") else clean_text(raw)

        if not raw_strip:
            story.append(Spacer(1, 0.7 * cm))
            continue

        # ===== FINAL DECISION =====
        if clean.startswith("🏁"):
            story.append(PageBreak())
            story.append(Spacer(1, 1.5 * cm))
            story.append(Paragraph(ar("🧠 الخلاصة الاستشارية النهائية"), ai_exec_title))
            story.append(elegant_divider())
            decision_mode = True
            ai_mode = False
            decision_buffer = []
            continue

        # ===== AI SUB HEADERS =====
        if clean.startswith(("📊", "💎", "⚠️")):
            story.append(elegant_divider())
            story.append(Paragraph(ar(clean), chapter))
            ai_mode = True
            decision_mode = False
            continue

        # ===== CHAPTER =====
        if clean.startswith("الفصل"):
            if first_chapter:
                story.append(PageBreak())
            chapter_index += 1
            chart_cursor[chapter_index] = 0
            story.append(Paragraph(ar(clean), chapter))
            first_chapter = True
            ai_mode = False
            decision_mode = False
            continue

        # ===== CHART =====
        if clean == "[[ANCHOR_CHART]]":
            charts = charts_by_chapter.get(f"chapter_{chapter_index}", [])
            idx = chart_cursor.get(chapter_index, 0)
            if idx < len(charts):
                img = plotly_to_image(charts[idx], 16.8, 8.8)
                if img:
                    story.append(Spacer(1, 1.2 * cm))
                    story.append(img)
                    story.append(Spacer(1, 0.6 * cm))
                chart_cursor[chapter_index] += 1
            continue

        # ===== TEXT FLOW =====
        if decision_mode:
            decision_buffer.append(clean)
            continue

        if ai_mode:
            story.append(Paragraph(ar(clean), ai_box))
            continue  # ✅ AI MODE يبقى مفتوح

        story.append(Paragraph(ar(clean), body))

    # ===== FINAL DECISION BOX =====
    if decision_buffer:
        story.append(Spacer(1, 1 * cm))
        decision_text = "\n\n".join(
            clean_text(p) for p in decision_buffer if p.strip()
        )
        story.append(executive_decision_box(decision_text))
        story.append(Spacer(1, 1.5 * cm))

    doc.build(story)
    buffer.seek(0)
    return buffer
