from io import BytesIO
from datetime import datetime
import os
import math
import tempfile

import pandas as pd

# Arabic support
import arabic_reshaper
from bidi.algorithm import get_display

# ReportLab
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Charts system
from advanced_charts import AdvancedCharts


# =========================
# Arabic text helper
# =========================
def ar(text):
    if not text:
        return ""
    try:
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)


def safe_num(val, fmt=",.0f", default="N/A"):
    try:
        if val is None:
            return default
        if isinstance(val, float) and math.isnan(val):
            return default
        return format(val, fmt)
    except Exception:
        return default


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

    # ---- Font
    font_path = "Amiri-Regular.ttf"
    if not os.path.exists(font_path):
        buffer.write("Arabic font missing".encode("utf-8"))
        buffer.seek(0)
        return buffer

    pdfmetrics.registerFont(TTFont("Amiri", font_path))

    # ---- Document
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
        alignment=2
    )

    title_style = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName="Amiri",
        fontSize=20,
        alignment=2,
        textColor=colors.HexColor("#1A5276"),
        spaceAfter=30
    )

    subtitle_style = ParagraphStyle(
        "ArabicSubtitle",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=15,
        alignment=2,
        textColor=colors.HexColor("#2874A6"),
        spaceBefore=20,
        spaceAfter=15
    )

    story = []

    # =========================
    # 1️⃣ COVER PAGE
    # =========================
    story.append(Spacer(1, 6 * cm))
    story.append(Paragraph(ar("تقرير وردة الذكاء العقاري"), title_style))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(ar(f"المدينة: {user_info.get('city')}"), body_style))
    story.append(Paragraph(ar(f"نوع العقار: {user_info.get('property_type')}"), body_style))
    story.append(Paragraph(ar(f"الباقة: {package_level}"), body_style))
    story.append(Paragraph(ar(datetime.now().strftime("%Y-%m-%d")), body_style))
    story.append(PageBreak())

    # =========================
    # 2️⃣ TEXT CONTENT (الفصول) - الإصدار المحسن
    # =========================

    # 🔴 إذا كان المحتوى Story جاهز (من report_orchestrator)
    if isinstance(content_text, list):
        story.extend(content_text)
        print(f"✅ تم إضافة Story جاهز ({len(content_text)} عنصر)")

    # 🟡 إذا كان المحتوى نصيًا (Smart / ملخص)
    elif isinstance(content_text, str):
        print(f"📝 معالجة نص تقرير ({len(content_text)} حرف)")
        lines = content_text.split("\n")
        for line in lines:
            clean = line.strip()

            if clean == "":
                story.append(Spacer(1, 0.6 * cm))
                continue

            if clean.startswith("الفصل"):
                story.append(PageBreak())
                story.append(Paragraph(ar(clean), title_style))
                story.append(Spacer(1, 1 * cm))
                continue

            if clean[:2].isdigit():
                story.append(Paragraph(ar(clean), subtitle_style))
                continue

            story.append(Paragraph(ar(clean), body_style))
            story.append(Spacer(1, 0.3 * cm))
    
    else:
        print(f"⚠️ نوع غير معروف للمحتوى: {type(content_text)}")
        story.append(Paragraph(ar("عذرًا، لم يتم العثور على محتوى التقرير."), body_style))

    # =========================
    # 3️⃣ CHARTS SECTION
    # =========================

    charts_engine = AdvancedCharts()

    charts = charts_engine.generate_all_charts(
        df=market_data,
        user_info=user_info,
        real_data=real_data
    )

    # لا نفتح قسم الرسومات إلا إذا كان فيه محتوى فعلي
    if charts and isinstance(charts, dict):
        story.append(PageBreak())
        story.append(Paragraph(ar("التحليل البياني المتقدم"), title_style))
        story.append(Spacer(1, 1 * cm))

        for chapter, figures in charts.items():
            if not figures:
                continue

            # عنوان الفصل
            story.append(Paragraph(ar(chapter.replace("_", " ").title()), subtitle_style))
            story.append(Spacer(1, 0.5 * cm))

            for fig in figures:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                        # ✅ الطريقة الصحيحة لتحويل Plotly إلى صورة
                        if hasattr(fig, 'write_image'):
                            fig.write_image(tmp.name, width=1200, height=700, scale=2)
                        else:
                            # Fallback for any other chart type
                            import plotly.io as pio
                            pio.write_image(fig, tmp.name, width=1200, height=700, scale=2)
                        img_path = tmp.name

                    story.append(Image(img_path, width=16 * cm, height=9 * cm))
                    story.append(Spacer(1, 0.5 * cm))

                except Exception as e:
                    print(f"[Chart Render Error] {e}")
                    # وضع نص بديل في حالة فشل الرسم
                    story.append(Paragraph(ar(f"لم يتمكن النظام من عرض الرسم البياني: {str(e)[:50]}"), body_style))
                    story.append(Spacer(1, 0.5 * cm))

    else:
        print("[PDF] No charts generated – skipping chart section")
        # لا نضيف صفحة بيضاء إذا لم توجد رسوم

    # =========================
    # 4️⃣ AI RECOMMENDATIONS SECTION (إذا وجدت)
    # =========================
    if ai_recommendations and isinstance(ai_recommendations, dict) and len(ai_recommendations) > 0:
        story.append(PageBreak())
        story.append(Paragraph(ar("التوصيات الذكية المتقدمة"), title_style))
        story.append(Spacer(1, 1 * cm))

        for key, value in ai_recommendations.items():
            story.append(Paragraph(ar(f"🎯 {key}: {value}"), body_style))
            story.append(Spacer(1, 0.3 * cm))
    elif ai_recommendations and isinstance(ai_recommendations, list) and len(ai_recommendations) > 0:
        story.append(PageBreak())
        story.append(Paragraph(ar("التوصيات الذكية المتقدمة"), title_style))
        story.append(Spacer(1, 1 * cm))

        for i, rec in enumerate(ai_recommendations, 1):
            story.append(Paragraph(ar(f"{i}. {rec}"), body_style))
            story.append(Spacer(1, 0.3 * cm))

    # =========================
    # 5️⃣ FOOTER PAGE
    # =========================
    story.append(PageBreak())
    story.append(Spacer(1, 8 * cm))
    story.append(Paragraph(ar("نهاية التقرير"), subtitle_style))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(ar("ورد الذكاء العقاري"), body_style))
    story.append(Paragraph(ar("نُشر هذا التقرير بتاريخ: " + datetime.now().strftime("%Y-%m-%d %H:%M")), body_style))
    story.append(Paragraph(ar("جميع الحقوق محفوظة © 2024"), body_style))

    # =========================
    # 6️⃣ BUILD
    # =========================
    try:
        print(f"📄 جاري بناء PDF مع {len(story)} عنصر...")
        doc.build(story)
        print("✅ تم بناء PDF بنجاح")
    except Exception as e:
        # في حالة فشل البناء، نعيد buffer نظيف
        print(f"[PDF Build Error] {e}")
        buffer = BytesIO()
        buffer.write(f"خطأ في إنشاء الـ PDF: {str(e)}".encode("utf-8"))
        buffer.seek(0)
        return buffer

    buffer.seek(0)
    return buffer
