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
# Clean bullets & junk - النسخة النهائية القاطعة
# =========================
def clean_text(text: str) -> str:
    if not text:
        return ""

    cleaned = []
    for ch in text:
        cat = unicodedata.category(ch)

        # نسمح فقط بالحروف والأرقام والمسافات وعلامات الترقيم الأساسية
        if cat.startswith(("L", "N", "P", "Z")):
            cleaned.append(ch)

    text = "".join(cleaned)

    # تنظيف بدايات الأسطر
    text = re.sub(r"^[\-\*\d\.\)]\s*", "", text)

    # توحيد المسافات
    text = re.sub(r"\s+", " ", text)

    return text.strip()


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
# دالة فاصل فاخر (استشاري)
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

    # =========================
    # 🧠 AI INSIGHT BOX (للفصول 1–3)
    # =========================
    ai_insight_box = ParagraphStyle(
        "AIInsightBox",
        parent=body,
        backColor=colors.HexColor("#F2F4F7"),
        leftIndent=14,
        rightIndent=14,
        spaceBefore=14,
        spaceAfter=18,
        leading=26,
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

    # =========================
    # 🧠 ستايل العنوان التنفيذي الفاخر
    # =========================
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
    chart_caption_style = ParagraphStyle(
        "ChartCaption",
        parent=body,
        fontSize=13,
        textColor=colors.HexColor("#666666"),
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=18,
        fontName="Amiri"
    )

    story = []

    # =========================
    # COVER (NO EMPTY PAGE AFTER)
    # =========================
    story.append(Spacer(1, 7.5 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), title))
    story.append(PageBreak())

    # =========================
    # CONTENT
    # =========================
    charts_by_chapter = st.session_state.get("charts_by_chapter", {})

    chapter_index = 0
    chart_cursor = {}
    first_chapter_processed = False

    # تحويل النص إلى iterator للوصول للسطور التالية
    lines_list = content_text.split("\n")
    lines_iter = iter(lines_list)

    for raw in lines_iter:
        raw_stripped = raw.strip()
        
        # 📌 PATCH B: إصلاح تنويه البيانات (إصلاح القطع نهائيًا)
            story.append(Spacer(1, 0.6 * cm))
            story.append(Paragraph(ar(raw_stripped), body))

            # 👇 التقاط الأسطر التالية كجزء من التنويه
            while True:
                try:
                    next_line = next(lines_iter)
                    if not next_line.strip():
                        break
                    story.append(Paragraph(ar(next_line.strip()), body))
                except StopIteration:
                    break

            story.append(Spacer(1, 0.8 * cm))
            continue
        
        # ⛔ الحل الأساسي: الوسوم لا تمر على clean_text
        if raw_stripped in SPECIAL_TAGS:
            clean = raw_stripped
        else:
            clean = clean_text(raw)
        
        # ✅ تحسين شرط الفراغ
        if not raw_stripped:
            story.append(Spacer(1, 0.8 * cm))
            continue

        # =========================
        # 🧠 🏁 التعديل الجوهري: عرض الاستشارة النهائية بشكل تنفيذي
        # =========================

        # 🏁 القرار الاستثماري النهائي (التعديل الذكي)
        if raw_stripped.startswith("=== EXECUTIVE_PREDICTIVE_DECISION ==="):
            # صفحة مستقلة للقرار النهائي
            story.append(PageBreak())

            # مساحة مريحة قبل العنوان
            story.append(Spacer(1, 1.2 * cm))
            story.append(Paragraph(ar("الخلاصة التنفيذية التنبؤية"), chapter))
            story.append(Spacer(1, 0.6 * cm))
            continue

        # 📊 💎 ⚠️ عناوين الذكاء الاصطناعي داخل الفصول
        if clean.startswith(("📊", "💎", "⚠️")):
            story.append(Spacer(1, 0.8 * cm))
            story.append(elegant_divider())
            story.append(Paragraph(ar(clean), ai_sub_title))
            story.append(Spacer(1, 0.4 * cm))
            continue

        # -------- CHAPTER --------
        if clean.startswith("الفصل"):
            # ✅ لا نكسر الصفحة قبل أول فصل
            if first_chapter_processed:
                story.append(PageBreak())

            chapter_index += 1
            chart_cursor[chapter_index] = 0

            story.append(
                KeepTogether([
                    Paragraph(ar(clean), chapter),
                    Spacer(1, 0.6 * cm)
                ])
            )

            first_chapter_processed = True
            continue

        # -------- NO CHARTS IN 9–10 --------
        if chapter_index >= 9:
            # ✅ الفلترة النهائية: فلترة UTF-8 قبل Paragraph
            clean = clean.encode("utf-8", "ignore").decode("utf-8")
            story.append(Paragraph(ar(clean), body))
            continue

        charts = charts_by_chapter.get(f"chapter_{chapter_index}", [])
        cursor = chart_cursor.get(chapter_index, 0)

        # -------- CHART CAPTION --------
        if clean == "[[CHART_CAPTION]]":
            try:
                next_line = next(lines_iter)
                while not next_line.strip():
                    next_line = next(lines_iter)

                caption = ar(next_line.strip())
                story.append(Paragraph(caption, chart_caption_style))
                story.append(Spacer(1, 1.2 * cm))
            except StopIteration:
                story.append(Spacer(1, 1.2 * cm))
            continue

        # -------- ANCHOR CHART --------
        if clean == "[[ANCHOR_CHART]]":
            if cursor < len(charts):
                img = plotly_to_image(charts[cursor], 16.8, 8.8)
                if img:
                    story.append(Spacer(1, 1.6 * cm))
                    story.append(img)
                    story.append(Spacer(1, 0.6 * cm))
                chart_cursor[chapter_index] += 1
            continue

        # -------- RHYTHM CHART --------
        if clean == "[[RHYTHM_CHART]]":
            if cursor < len(charts):
                # ⭐⭐ الحل الذكي: تحديد حجم الرسم بناءً على نوعها
                fig = charts[cursor]
                
                # ✅ الكشف الآمن: تجنب IndexError إذا كان fig.data فارغ
                is_donut = (
                    fig is not None
                    and hasattr(fig, 'data')
                    and len(fig.data) > 0
                    and isinstance(fig.data[0], go.Pie)
                )
                
                is_indicator = (
                    fig is not None
                    and hasattr(fig, 'data')
                    and len(fig.data) > 0
                    and isinstance(fig.data[0], go.Indicator)
                )
                
                # ⭐ تحديد الحجم بناءً على نوع الرسمة
                if is_donut:
                    # ✅ الدونت: استخدم حجم ANCHOR (كبير)
                    img = plotly_to_image(fig, 16.8, 8.8)
                elif is_indicator:
                    # ✅ المؤشر: استخدم حجم كبير تنفيذي
                    img = plotly_to_image(fig, 17.5, 9.5)
                else:
                    img = plotly_to_image(fig, 16.8, 8.8)
                
                if img:
                    if is_indicator:
                        story.append(Spacer(1, 1.8 * cm))
                    else:
                        story.append(Spacer(1, 1.4 * cm))
                    
                    story.append(img)
                    story.append(Spacer(1, 0.6 * cm))
                
                chart_cursor[chapter_index] += 1
            continue

        # -------- NORMAL TEXT --------
        # ✅ التأكد من أن هذا ليس وسمًا قبل معالجة النص
        if clean not in SPECIAL_TAGS:
            clean = clean.encode("utf-8", "ignore").decode("utf-8")
            story.append(Paragraph(ar(clean), body))

    # =========================
    # BUILD
    # =========================
    doc.build(story)
    buffer.seek(0)
    return buffer
