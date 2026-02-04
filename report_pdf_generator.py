# report_pdf_generator.py
from io import BytesIO
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
# Clean text (NO TAG DAMAGE)
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
def plotly_to_image(fig, w_cm, h_cm):
    if fig is None:
        return None
    try:
        img_bytes = fig.to_image(
            format="png",
            width=int(w_cm * 38),
            height=int(h_cm * 38)
        )
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.write(img_bytes)
        tmp.close()
        return Image(tmp.name, width=w_cm * cm, height=h_cm * cm)
    except Exception:
        return None


# =========================
# Divider
# =========================
def elegant_divider():
    return HRFlowable(
        width="60%",
        thickness=0.7,
        color=colors.HexColor("#B0B0B0"),
        spaceBefore=12,
        spaceAfter=14,
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
        fontSize=14.5,
        leading=28,
        alignment=TA_RIGHT,
        spaceAfter=18,
    )

    chapter = ParagraphStyle(
        "Chapter",
        fontName="Amiri",
        fontSize=18,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#9c1c1c"),
        spaceBefore=30,
        spaceAfter=16,
        keepWithNext=1
    )

    ai_box = ParagraphStyle(
        "AIBox",
        parent=body,
        backColor=colors.HexColor("#F2F4F7"),
        leftIndent=14,
        rightIndent=14,
        spaceBefore=12,
        spaceAfter=18,
    )

    caption_style = ParagraphStyle(
        "Caption",
        parent=body,
        fontSize=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#666666"),
        spaceAfter=14,
    )

    story = []

    # COVER
    story.append(Spacer(1, 7 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), ParagraphStyle(
        "Title",
        fontName="Amiri",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        spaceAfter=40
    )))
    story.append(PageBreak())

    charts_by_chapter = st.session_state.get("charts_by_chapter", {})
    chapter_index = 0
    chart_cursor = {}
    decision_buffer = []
    decision_mode = False
    ai_mode = False

    lines = iter(content_text.split("\n"))

    for raw in lines:
        raw_strip = raw.strip()

        # EMPTY
        if not raw_strip:
            story.append(Spacer(1, 0.5 * cm))
            continue

        # FINAL DECISION
        if raw_strip.startswith("🏁"):
            story.append(PageBreak())
            story.append(Paragraph(ar("الخلاصة الاستشارية النهائية"), chapter))
            story.append(elegant_divider())
            decision_mode = True
            decision_buffer = []
            continue

        # CHAPTER
        if raw_strip.startswith("الفصل"):
            decision_mode = False
            ai_mode = False
            chapter_index += 1
            chart_cursor[chapter_index] = 0
            story.append(PageBreak())
            story.append(Paragraph(ar(raw_strip), chapter))
            continue

        # AI TITLE
        if raw_strip.startswith(("📊", "💎", "⚠️")):
            ai_mode = True
            decision_mode = False
            story.append(elegant_divider())
            story.append(Paragraph(ar(raw_strip), ParagraphStyle(
                "AISub",
                parent=chapter,
                fontSize=15.5,
                textColor=colors.HexColor("#444444")
            )))
            continue

        # CHART CAPTION
        if raw_strip == "[[CHART_CAPTION]]":
            try:
                caption = next(lines).strip()
                story.append(Paragraph(ar(caption), caption_style))
            except StopIteration:
                pass
            continue

        # CHART
        if raw_strip in ("[[ANCHOR_CHART]]", "[[RHYTHM_CHART]]"):
            charts = charts_by_chapter.get(f"chapter_{chapter_index}", [])
            idx = chart_cursor.get(chapter_index, 0)
            if idx < len(charts):
                img = plotly_to_image(charts[idx], 16.8, 8.5)
                if img:
                    story.append(Spacer(1, 1.0 * cm))
                    story.append(img)
                    story.append(Spacer(1, 0.6 * cm))
                chart_cursor[chapter_index] += 1
            ai_mode = False
            decision_mode = False
            continue

        clean = clean_text(raw_strip)

        if decision_mode:
            decision_buffer.append(clean)
        elif ai_mode:
            story.append(Paragraph(ar(clean), ai_box))
            ai_mode = False
        else:
            story.append(Paragraph(ar(clean), body))

    # ADD FINAL DECISION BOX
    if decision_buffer:
        story.append(Spacer(1, 1.0 * cm))
        story.append(executive_decision_box("\n\n".join(decision_buffer)))

    doc.build(story)
    buffer.seek(0)
    return buffer
