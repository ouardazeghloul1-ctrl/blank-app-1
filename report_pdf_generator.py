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
from reportlab.lib.enums import TA_RIGHT, TA_CENTER  # ✅ تحسين نظافة الكود
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# Charts system
from advanced_charts import AdvancedCharts


# =========================
# Arabic text helper
# =========================
def ar(text):
    """تحويل النص العربي للتنسيق الصحيح"""
    if not text:
        return ""
    try:
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)


def safe_num(val, fmt=",.0f", default="N/A"):
    """تنسيق رقم بأمان"""
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
    """
    إنشاء PDF احترافي مع دعم كامل للعربية
    """
    buffer = BytesIO()

    # ---- 1️⃣ تسجيل الخط الداعم للعربية
    try:
        # الخط الأكثر استقرارًا للعربية في ReportLab
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        font_name = "STSong-Light"
        print("✅ تم تسجيل الخط الصيني الداعم للعربية (STSong-Light)")
    except Exception as e:
        print(f"⚠️ خطأ في تسجيل الخط الصيني: {e}")
        try:
            # البديل الأول
            pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
            font_name = "HeiseiMin-W3"
            print("⚠️ استخدام الخط الياباني كبديل")
        except:
            # البديل النهائي
            font_name = "Helvetica"
            print("⚠️ استخدام Helvetica كبديل نهائي")

    # ---- 2️⃣ إنشاء المستند
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    # ---- 3️⃣ تعريف الأنماط مع التحسينات
    body_style = ParagraphStyle(
        "ArabicBody",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=12,
        leading=18,
        alignment=TA_RIGHT,  # ✅ استخدام الثابت بدلاً من الرقم
        rightIndent=10,
        leftIndent=10,
        spaceAfter=6
    )

    title_style = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=20,
        alignment=TA_CENTER,  # ✅ تحسين
        textColor=colors.HexColor("#1A5276"),
        spaceAfter=30
    )

    subtitle_style = ParagraphStyle(
        "ArabicSubtitle",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=15,
        alignment=TA_RIGHT,  # ✅ تحسين
        textColor=colors.HexColor("#2874A6"),
        spaceBefore=20,
        spaceAfter=15
    )

    story = []

    # =========================
    # 1️⃣ صفحة الغلاف
    # =========================
    story.append(Spacer(1, 6 * cm))
    story.append(Paragraph(ar("تقرير وردة الذكاء العقاري"), title_style))
    story.append(Spacer(1, 1 * cm))
    
    # معلومات المستخدم
    story.append(Paragraph(ar(f"المدينة: {user_info.get('city', 'غير محدد')}"), body_style))
    story.append(Paragraph(ar(f"نوع العقار: {user_info.get('property_type', 'غير محدد')}"), body_style))
    story.append(Paragraph(ar(f"الباقة: {package_level}"), body_style))
    story.append(Paragraph(ar(f"التاريخ: {datetime.now().strftime('%Y-%m-%d')}"), body_style))
    
    story.append(PageBreak())

    # =========================
    # 2️⃣ محتوى النص (الفصول)
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
                story.append(Spacer(1, 0.4 * cm))
                continue

            if clean.startswith("الفصل"):
                story.append(PageBreak())
                story.append(Paragraph(ar(clean), title_style))
                story.append(Spacer(1, 0.8 * cm))
                continue

            if clean[:2].isdigit() and "." in clean[:4]:
                story.append(Paragraph(ar(clean), subtitle_style))
                story.append(Spacer(1, 0.3 * cm))
                continue

            story.append(Paragraph(ar(clean), body_style))
            story.append(Spacer(1, 0.15 * cm))
    
    else:
        print(f"⚠️ نوع غير معروف للمحتوى: {type(content_text)}")
        story.append(Paragraph(ar("عذرًا، لم يتم العثور على محتوى التقرير."), body_style))

    # =========================
    # 3️⃣ قسم الرسومات البيانية
    # =========================

    try:
        charts_engine = AdvancedCharts()
        charts = charts_engine.generate_all_charts(
            df=market_data,
            user_info=user_info,
            real_data=real_data
        )

        if charts and isinstance(charts, dict) and len(charts) > 0:
            story.append(PageBreak())
            story.append(Paragraph(ar("التحليل البياني المتقدم"), title_style))
            story.append(Spacer(1, 1 * cm))

            for chapter, figures in charts.items():
                if not figures:
                    continue

                # عنوان الفصل البياني
                story.append(Paragraph(ar(chapter.replace("_", " ").title()), subtitle_style))
                story.append(Spacer(1, 0.5 * cm))

                for fig in figures:
                    try:
                        # حفظ الرسم البياني كصورة مؤقتة
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                            if hasattr(fig, 'write_image'):
                                fig.write_image(tmp.name, width=1200, height=700, scale=2)
                            else:
                                import plotly.io as pio
                                pio.write_image(fig, tmp.name, width=1200, height=700, scale=2)
                            img_path = tmp.name

                        story.append(Image(img_path, width=16 * cm, height=9 * cm))
                        story.append(Spacer(1, 0.5 * cm))

                    except Exception as e:
                        print(f"[Chart Render Error] {e}")
                        story.append(Paragraph(ar(f"ملاحظة: تعذر عرض رسم بياني معين"), body_style))
                        story.append(Spacer(1, 0.3 * cm))

        else:
            print("[PDF] لا توجد رسومات بيانية - تخطي القسم")
            
    except Exception as e:
        print(f"[Charts Error] {e}")
        story.append(Paragraph(ar("ملاحظة: تعذر تحميل الرسومات البيانية"), body_style))

    # =========================
    # 4️⃣ توصيات الذكاء الاصطناعي
    # =========================
    if ai_recommendations:
        story.append(PageBreak())
        story.append(Paragraph(ar("التوصيات الذكية المتقدمة"), title_style))
        story.append(Spacer(1, 1 * cm))

        if isinstance(ai_recommendations, dict):
            for key, value in ai_recommendations.items():
                story.append(Paragraph(ar(f"🎯 {key}: {value}"), body_style))
                story.append(Spacer(1, 0.3 * cm))
        elif isinstance(ai_recommendations, list):
            for i, rec in enumerate(ai_recommendations, 1):
                story.append(Paragraph(ar(f"{i}. {rec}"), body_style))
                story.append(Spacer(1, 0.3 * cm))

    # =========================
    # 5️⃣ صفحة الختام
    # =========================
    story.append(PageBreak())
    story.append(Spacer(1, 8 * cm))
    story.append(Paragraph(ar("نهاية التقرير"), subtitle_style))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(ar("ورد الذكاء العقاري"), body_style))
    story.append(Paragraph(ar(f"نُشر هذا التقرير بتاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), body_style))
    story.append(Paragraph(ar("جميع الحقوق محفوظة © 2024"), body_style))

    # =========================
    # 6️⃣ بناء PDF النهائي
    # =========================
    try:
        print(f"📄 جاري بناء PDF مع {len(story)} عنصر...")
        doc.build(story)
        print("✅ تم بناء PDF بنجاح")
    except Exception as e:
        print(f"[PDF Build Error] {e}")
        buffer = BytesIO()
        buffer.write(f"خطأ في إنشاء الـ PDF: {str(e)}".encode("utf-8"))
        buffer.seek(0)
        return buffer

    buffer.seek(0)
    return buffer
