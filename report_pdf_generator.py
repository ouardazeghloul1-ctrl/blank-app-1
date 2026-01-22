from io import BytesIO
from datetime import datetime
import os
import tempfile
import streamlit as st  # ✅ تمت الإضافة هنا

import arabic_reshaper
from bidi.algorithm import get_display
import plotly.io as pio

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from advanced_charts import AdvancedCharts


# =========================
# Arabic helper (نهائي)
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
# Plotly to Image Helper
# =========================
def plotly_to_image(fig, width_cm, height_cm):
    if fig is None:
        return None

    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            pio.write_image(
                fig,
                tmp.name,
                format="png",
                width=int(width_cm * 37.8),
                height=int(height_cm * 37.8),
                engine="kaleido"  # 🔥 مهم جدًا لـ Streamlit Cloud
            )
            return Image(tmp.name, width=width_cm * cm, height=height_cm * cm)
    except Exception as e:
        # ❌ لا نكسر إنشاء التقرير لو فشل رسم
        print("⚠️ فشل توليد رسم:", e)
        return None


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

    # -------------------------------------------------
    # FONT
    # -------------------------------------------------
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
        raise FileNotFoundError("❌ Amiri-Regular.ttf غير موجود")

    pdfmetrics.registerFont(TTFont("Amiri", font_path))

    # -------------------------------------------------
    # DOCUMENT
    # -------------------------------------------------
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        "ArabicBody",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=12,
        leading=18,
        alignment=TA_RIGHT,
        spaceAfter=6
    )

    title_style = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName="Amiri",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        spaceAfter=30
    )

    chapter_style = ParagraphStyle(
        "ArabicChapter",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=16,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#9c1c1c"),
        spaceBefore=24,
        spaceAfter=14
    )

    story = []

    # -------------------------------------------------
    # COVER
    # -------------------------------------------------
    story.append(Spacer(1, 5 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), title_style))
    story.append(Spacer(1, 1 * cm))

    story.append(Paragraph(ar(f"المدينة: {user_info.get('city', '')}"), body_style))
    story.append(Paragraph(ar(f"نوع العقار: {user_info.get('property_type', '')}"), body_style))
    story.append(Paragraph(ar(f"الباقة: {package_level}"), body_style))
    story.append(Paragraph(ar(f"التاريخ: {datetime.now().strftime('%Y-%m-%d')}"), body_style))

    # الغلاف يجب أن ينتهي بـ PageBreak
    story.append(PageBreak())

    # -------------------------------------------------
    # CONTENT TEXT (منظم + فراغات + رسومات حسب الفصل)
    # -------------------------------------------------
    chapter_index = 0  # تم إضافة هذا المتغير لتتبع الفصول
    
    if isinstance(content_text, str):
        lines = content_text.split("\n")
        paragraph_counter = 0
        first_chapter = True

        for line in lines:
            clean = line.strip()

            if not clean:
                story.append(Spacer(1, 0.4 * cm))
                continue

            if clean.startswith("الفصل"):
                if not first_chapter:
                    story.append(PageBreak())
                first_chapter = False

                story.append(Paragraph(ar(clean), chapter_style))
                story.append(Spacer(1, 0.3 * cm))

                # -----------------------------
                # 🖼️ إدراج الرسومات حسب الفصل
                # -----------------------------
                charts_by_chapter = st.session_state.get("charts_by_chapter", {})
                chapter_index += 1
                chapter_key = f"chapter_{chapter_index}"
                chapter_charts = charts_by_chapter.get(chapter_key, [])

                # تحديد نوع الباقة
                premium = package_level in ["ذهبية", "ماسية", "ماسية متميزة"]

                if chapter_charts:
                    # 🔹 الرسم الرئيسي (كبير)
                    main_chart = chapter_charts[0]
                    img = plotly_to_image(
                        main_chart,
                        width_cm=14 if premium else 16,
                        height_cm=9 if premium else 10,
                    )
                    if img:
                        story.append(img)
                        story.append(Spacer(1, 0.6 * cm))

                    # 🔹 الرسومات الثانوية (للباقات العليا فقط)
                    if premium and len(chapter_charts) > 1:
                        for fig in chapter_charts[1:]:
                            img = plotly_to_image(fig, width_cm=7, height_cm=5)
                            if img:
                                story.append(img)
                                story.append(Spacer(1, 0.4 * cm))

                paragraph_counter = 0
                continue

            story.append(Paragraph(ar(clean), body_style))
            paragraph_counter += 1

            # فراغ ذكي كل 2 فقرة (للمحتوى الثقيل فكريًا)
            if paragraph_counter % 2 == 0:
                story.append(Spacer(1, 0.6 * cm))

    # -------------------------------------------------
    # AI RECOMMENDATIONS
    # -------------------------------------------------
    if ai_recommendations:
        story.append(PageBreak())
        story.append(Paragraph(ar("التوصيات الذكية المتقدمة"), title_style))

        for k, v in ai_recommendations.items():
            story.append(Paragraph(ar(str(k)), chapter_style))
            story.append(Paragraph(ar(str(v)), body_style))
            story.append(Spacer(1, 0.6 * cm))

    # -------------------------------------------------
    # FOOTER
    # -------------------------------------------------
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph(ar("نهاية التقرير"), chapter_style))
    story.append(Paragraph(ar("Warda Intelligence © 2024"), body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
