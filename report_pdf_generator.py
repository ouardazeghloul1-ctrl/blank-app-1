from io import BytesIO
from datetime import datetime
import os
import tempfile
import streamlit as st
import re

import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    PageBreak, Image, KeepTogether
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
# Normalize markers + bullets
# =========================
def normalize(text: str) -> str:
    if not text:
        return ""
    t = text.strip()

    # توحيد الماركرات
    t = t.replace("[[RYTHM_CHART]]", "[[RHYTHM_CHART]]")

    # إزالة أي مربعات أو ترقيم غريب
    t = re.sub(r"[■▪◼◾]", "", t)

    return t.strip()


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
# MAIN PDF GENERATOR (FINAL)
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
        topMargin=2.4 * cm,
        bottomMargin=2.4 * cm
    )

    styles = getSampleStyleSheet()

    # =========================
    # STYLES – PREMIUM
    # =========================
    body = ParagraphStyle(
        "ArabicBody",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=14.2,
        leading=27,                 # تنفّس واضح
        alignment=TA_RIGHT,
        spaceBefore=6,
        spaceAfter=22,
        allowWidows=0,
        allowOrphans=0,
    )

    chapter = ParagraphStyle(
        "ArabicChapter",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=17.5,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#9c1c1c"),
        spaceBefore=36,
        spaceAfter=28,
    )

    title = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName="Amiri",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        spaceAfter=44
    )

    story = []

    # =========================
    # COVER
    # =========================
    story.append(Spacer(1, 5 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), title))
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph(ar(f"التاريخ: {datetime.now().strftime('%Y-%m-%d')}"), body))
    story.append(PageBreak())

    charts_by_chapter = st.session_state.get("charts_by_chapter", {})
    chapter_index = 0
    chart_cursor = {}
    text_since_chart = 0

    lines = content_text.split("\n")
    i = 0

    while i < len(lines):
        raw = normalize(lines[i])
        i += 1

        if not raw:
            story.append(Spacer(1, 0.8 * cm))
            continue

        # =====================
        # CHAPTER TITLE
        # =====================
        if raw.startswith("الفصل"):
            story.append(PageBreak())
            chapter_index += 1
            chart_cursor[chapter_index] = 0
            text_since_chart = 0

            # العنوان + أول فقرة معًا (ممنوع الانفصال)
            block = [Paragraph(ar(raw), chapter)]

            # حاول جلب أول فقرة حقيقية
            if i < len(lines):
                peek = normalize(lines[i])
                if peek and not peek.startswith("[["):
                    block.append(Paragraph(ar(peek), body))
                    i += 1

            story.append(KeepTogether(block))
            continue

        # =====================
        # NO CHARTS CH 9–10
        # =====================
        if chapter_index >= 9:
            if raw.startswith("[["):
                continue
            story.append(Paragraph(ar(raw), body))
            continue

        charts = charts_by_chapter.get(f"chapter_{chapter_index}", [])
        cursor = chart_cursor.get(chapter_index, 0)

        # =====================
        # ANCHOR CHART
        # =====================
        if raw == "[[ANCHOR_CHART]]":
            if cursor < len(charts) and text_since_chart >= 6:
                img = plotly_to_image(charts[cursor], 16.8, 8.8)
                if img:
                    story.append(Spacer(1, 1.6 * cm))
                    story.append(KeepTogether([img]))
                    story.append(Spacer(1, 2.0 * cm))
                chart_cursor[chapter_index] += 1
                text_since_chart = 0
            continue

        # =====================
        # RHYTHM CHART
        # =====================
        if raw == "[[RHYTHM_CHART]]":
            if cursor < len(charts) and text_since_chart >= 4:
                img = plotly_to_image(charts[cursor], 15.8, 6.5)
                if img:
                    story.append(Spacer(1, 1.4 * cm))
                    story.append(KeepTogether([img]))
                    story.append(Spacer(1, 1.8 * cm))
                chart_cursor[chapter_index] += 1
                text_since_chart = 0
            continue

        # =====================
        # IGNORE UNKNOWN MARKERS
        # =====================
        if raw.startswith("[["):
            continue

        # =====================
        # NORMAL TEXT
        # =====================
        story.append(Paragraph(ar(raw), body))
        text_since_chart += 1

    # =========================
    # BUILD
    # =========================
    doc.build(story)
    buffer.seek(0)
    return buffer
