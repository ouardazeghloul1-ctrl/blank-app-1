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
# Arabic helper - معدلة نهائياً (بدون get_display)
# =========================
def ar(text):
    if not text:
        return ""

    try:
        text = str(text)

        # إصلاح عرض النسب السالبة داخل RTL
        text = re.sub(r"(-?\d+\.\d+)%", lambda m: f"\u200E{m.group(0)}", text)

        # استخدام arabic_reshaper فقط (بدون get_display)
        reshaped = arabic_reshaper.reshape(text)

        return reshaped

    except Exception:
        return str(text)


# =========================
# Clean bullets & junk
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
# Plotly → Image - معدلة مع دعم kaleido
# =========================
def plotly_to_image(fig, width_cm, height_cm):
    if fig is None:
        return None

    try:
        img_bytes = fig.to_image(
            format="png",
            width=1200,
            height=700,
            engine="kaleido"
        )

        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.write(img_bytes)
        tmp.close()

        return Image(tmp.name, width=width_cm * cm, height=height_cm * cm)

    except Exception as e:
        print("Chart export error:", e)
        return None


# =========================
# Elegant divider
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
    content_text,
    executive_decision,
    charts_by_chapter,
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
        leading=22,
        alignment=TA_RIGHT,
        spaceAfter=22,
        allowWidows=0,
        allowOrphans=0,
    )

    chapter = ParagraphStyle(
        "ArabicChapter",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=18,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#9c1c1c"),
        spaceBefore=36,
        spaceAfter=18,
        keepWithNext=1
    )

    ai_sub_title = ParagraphStyle(
        "AISubTitle",
        parent=styles["Heading3"],
        fontName="Amiri",
        fontSize=15.5,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#444444"),
        spaceBefore=18,
        spaceAfter=10,
    )

    title = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName="Amiri",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        spaceAfter=50
    )

    ai_executive_header = ParagraphStyle(
        "AIExecutiveHeader",
        parent=chapter,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        fontSize=17,
        spaceBefore=30,
        spaceAfter=14,
    )

    SPECIAL_TAGS = {"[[ANCHOR_CHART]]", "[[RHYTHM_CHART]]", "[[CHART_CAPTION]]"}

    story = []

    # COVER
    story.append(Spacer(1, 7.5 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), title))
    story.append(PageBreak())

    # =========================
    # EXECUTIVE DECISION (INDEPENDENT)
    # =========================
    DECISION_BLOCK_TITLES = {
        "DECISION_DEFINITION": "تعريف القرار التنبؤي",
        "MARKET_STATUS": "وضع السوق الحالي",
        "PREDICTIVE_SIGNALS": "الإشارات التنبؤية",
        "SCENARIOS": "السيناريوهات المحتملة",
        "OPTIMAL_POSITION": "القرار التنفيذي",
        "DECISION_GUARANTEE": "ضمان القرار"
    }

    if executive_decision and executive_decision.strip():
        story.append(Spacer(1, 1.5 * cm))
        story.append(Paragraph(ar("الخلاصة التنفيذية للقرار"), ai_executive_header))
        story.append(elegant_divider("60%"))
        story.append(Spacer(1, 0.8 * cm))

        for line in executive_decision.split("\n"):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.4 * cm))
                continue

            # عناوين الكتل
            if line.startswith("[DECISION_BLOCK:"):
                key = line.replace("[DECISION_BLOCK:", "").replace("]", "")
                title_text = DECISION_BLOCK_TITLES.get(key, "")
                if title_text:
                    story.append(Spacer(1, 0.9 * cm))
                    story.append(Paragraph(ar(title_text), chapter))
                    story.append(elegant_divider("50%"))
                continue

            if line == "[END_DECISION_BLOCK]":
                continue

            # النص الفعلي
            story.append(Paragraph(ar(line), body))
            story.append(Spacer(1, 0.35 * cm))

        story.append(Spacer(1, 1.2 * cm))
        story.append(elegant_divider("30%"))
        story.append(PageBreak())

    # =========================
    # TRANSITION PAGE – HOW TO READ THIS REPORT
    # =========================
    story.append(Spacer(1, 3 * cm))

    story.append(Paragraph(
        ar("كيف تقرأ هذا التقرير بناءً على القرار أعلاه"),
        ai_executive_header
    ))

    story.append(elegant_divider("55%"))
    story.append(Spacer(1, 1.2 * cm))

    story.append(Paragraph(ar(
        "الخلاصة التنفيذية للقرار تمثل القرار المعتمد لهذا التقرير، "
        "وقد تم اشتقاقه بناءً على مؤشرات رقمية ومعايير تحليلية محددة."
    ), body))

    story.append(Paragraph(ar(
        "الفصول التالية لا تُقرأ كتحليل عام للسوق، ولا كمسار للوصول إلى قرار جديد، "
        "بل كشرح منهجي للأسس التي بُني عليها القرار الصادر."
    ), body))

    story.append(Paragraph(ar(
        "كل فصل يفسر جانبًا محددًا من القرار، ويبيّن السياق السوقي، "
        "وحدود المخاطر، وطبيعة الفرص، وشروط التوقيت والتنفيذ، "
        "بهدف توضيح لماذا جاء القرار بهذه الصيغة تحديدًا."
    ), body))

    story.append(Paragraph(ar(
        "القرار موجود في الأعلى، "
        "وما يلي هو الإطار التحليلي الذي يبرره، "
        "ويحدّد نطاق صلاحيته، ويضبط تطبيقه."
    ), body))

    story.append(Spacer(1, 1.5 * cm))
    story.append(elegant_divider("30%"))
    story.append(PageBreak())

    chapter_index = 0
    chart_cursor = {}
    first_chapter_processed = False

    # تقسيم النص إلى فقرات (بناءً على سطر فارغ)
    paragraphs = content_text.split("\n\n")

    for raw in paragraphs:
        raw_stripped = raw.strip()

        if not raw_stripped:
            continue

        clean = raw_stripped if raw_stripped in SPECIAL_TAGS else clean_text(raw)

        if clean.startswith(("📊", "💎", "⚠️")):
            story.append(Spacer(1, 0.8 * cm))
            story.append(elegant_divider())
            story.append(Paragraph(ar(clean), ai_sub_title))
            story.append(Spacer(1, 0.4 * cm))
            continue

        if clean.startswith("الفصل"):
            if first_chapter_processed:
                story.append(PageBreak())
            chapter_index += 1
            chart_cursor[chapter_index] = 0
            story.append(KeepTogether([
                Paragraph(ar(clean), chapter),
                Spacer(1, 0.6 * cm)
            ]))
            first_chapter_processed = True
            continue

        if clean == "[[ANCHOR_CHART]]":
            charts = charts_by_chapter.get(f"chapter_{chapter_index}", [])
            cursor = chart_cursor.get(chapter_index, 0)

            if cursor < len(charts):
                img = plotly_to_image(charts[cursor], 16.8, 8.8)
                if img:
                    story.append(Spacer(1, 1.6 * cm))
                    story.append(img)
                    story.append(Spacer(1, 0.6 * cm))
                chart_cursor[chapter_index] += 1
            continue

        if clean == "[[RHYTHM_CHART]]":
            charts = charts_by_chapter.get(f"chapter_{chapter_index}", [])
            cursor = chart_cursor.get(chapter_index, 0)

            if cursor < len(charts):
                fig = charts[cursor]
                is_indicator = (
                    fig is not None
                    and hasattr(fig, 'data')
                    and len(fig.data) > 0
                    and isinstance(fig.data[0], go.Indicator)
                )
                img = plotly_to_image(fig, 17.5 if is_indicator else 16.8,
                                       9.5 if is_indicator else 8.8)
                if img:
                    story.append(Spacer(1, 1.8 * cm if is_indicator else 1.4 * cm))
                    story.append(img)
                    story.append(Spacer(1, 0.6 * cm))
                chart_cursor[chapter_index] += 1
            continue

        story.append(Paragraph(ar(clean), body))

    doc.build(story)
    buffer.seek(0)
    return buffer
