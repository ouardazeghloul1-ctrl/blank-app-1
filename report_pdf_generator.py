from io import BytesIO
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
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


# =========================
# تنظيف القوائم والمربعات
# =========================
def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.strip()

    # تحويل النقاط الغريبة
    text = re.sub(r"[•◦▪▫]", "–", text)

    # تحويل أرقام الإيموجي
    text = re.sub(r"[0-9]️⃣", lambda m: m.group(0)[0] + ".", text)

    # تصحيح الأخطاء الإملائية للماركر
    text = text.replace("[[RYTHM_CHART]]", "[[RHYTHM_CHART]]")

    return text


# =========================
# Plotly → Image
# =========================
def plotly_to_image(fig, width_cm, height_cm):
    if fig is None:
        return None

    img_bytes = fig.to_image(
        format="png",
        width=int(width_cm * 38),
        height=int(height_cm * 38)
    )

    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.write(img_bytes)
    tmp.close()

    return Image(tmp.name, width=width_cm * cm, height=height_cm * cm)


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
        rightMargin=2.2 * cm,
        leftMargin=2.2 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2.2 * cm
    )

    styles = getSampleStyleSheet()

    body = ParagraphStyle(
        "ArabicBody",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=14,
        leading=26,
        alignment=TA_RIGHT,
        spaceBefore=6,
        spaceAfter=22,
        allowWidows=0,
        allowOrphans=0
    )

    chapter = ParagraphStyle(
        "ArabicChapter",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=17,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#9c1c1c"),
        spaceBefore=34,
        spaceAfter=20
    )

    title = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName="Amiri",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        spaceAfter=42
    )

    story = []

    # COVER
    story.append(Spacer(1, 5 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), title))
    story.append(PageBreak())

    charts_by_chapter = st.session_state.get("charts_by_chapter", {})
    chapter_index = 0
    chart_cursor = {}
    text_since_last_chart = 0

    lines = content_text.split("\n")

    for raw in lines:
        clean = normalize_text(raw)

        if not clean:
            story.append(Spacer(1, 0.9 * cm))
            continue

        # -------- CHAPTER TITLE --------
        if clean.startswith("الفصل"):
            story.append(PageBreak())
            chapter_index += 1
            chart_cursor[chapter_index] = 0
            text_since_last_chart = 0
            story.append(Paragraph(ar(clean), chapter))
            continue

        # منع الرسومات في الفصل 9 و10
        if chapter_index >= 9:
            if clean.startswith("[[") and "CHART" in clean:
                continue
            story.append(Paragraph(ar(clean), body))
            continue

        charts = charts_by_chapter.get(f"chapter_{chapter_index}", [])
        cursor = chart_cursor.get(chapter_index, 0)

        # -------- ANCHOR --------
        if clean == "[[ANCHOR_CHART]]":
            if cursor < len(charts) and text_since_last_chart >= 6:
                img = plotly_to_image(charts[cursor], 16.8, 8.8)
                if img:
                    story.append(Spacer(1, 1.5 * cm))
                    story.append(KeepTogether([img]))
                    story.append(Spacer(1, 1.8 * cm))
                chart_cursor[chapter_index] += 1
                text_since_last_chart = 0
            continue

        # -------- RHYTHM --------
        if clean == "[[RHYTHM_CHART]]":
            if cursor < len(charts) and text_since_last_chart >= 4:
                img = plotly_to_image(charts[cursor], 15.8, 6.5)
                if img:
                    story.append(Spacer(1, 1.3 * cm))
                    story.append(KeepTogether([img]))
                    story.append(Spacer(1, 1.6 * cm))
                chart_cursor[chapter_index] += 1
                text_since_last_chart = 0
            continue

        if clean.startswith("[[") and "CHART" in clean:
            continue

        story.append(Paragraph(ar(clean), body))
        text_since_last_chart += 1

    doc.build(story)
    buffer.seek(0)
    return buffer
