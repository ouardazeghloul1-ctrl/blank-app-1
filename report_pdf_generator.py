from io import BytesIO
from datetime import datetime
import math
import tempfile

import arabic_reshaper
from bidi.algorithm import get_display

# ReportLab core
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# Charts
from advanced_charts import AdvancedCharts


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
    PDF Generator – Root Stable Version
    - No empty first pages
    - Full Arabic support
    - Stable cover
    """

    buffer = BytesIO()

    # --------------------------------------------------
    # 1️⃣ Font (Unicode – mandatory for Arabic)
    # --------------------------------------------------
    try:
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        FONT = "STSong-Light"
    except Exception:
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
        FONT = "HeiseiMin-W3"

    # --------------------------------------------------
    # 2️⃣ BaseDocTemplate (ROOT FIX)
    # --------------------------------------------------
    doc = BaseDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="main_frame"
    )

    template = PageTemplate(id="main_template", frames=[frame])
    doc.addPageTemplates([template])

    # --------------------------------------------------
    # 3️⃣ Styles
    # --------------------------------------------------
    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        "ArabicBody",
        parent=styles["Normal"],
        fontName=FONT,
        fontSize=12,
        leading=18,
        alignment=TA_RIGHT,
        spaceAfter=6
    )

    title_style = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName=FONT,
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1A5276"),
        spaceAfter=25
    )

    subtitle_style = ParagraphStyle(
        "ArabicSubtitle",
        parent=styles["Heading2"],
        fontName=FONT,
        fontSize=15,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#2874A6"),
        spaceBefore=18,
        spaceAfter=12
    )

    story = []

    # --------------------------------------------------
    # 4️⃣ COVER PAGE (Stable – no empty pages)
    # --------------------------------------------------
    story.append(Spacer(1, 5 * cm))
    story.append(Paragraph(ar("تقرير وردة الذكاء العقاري"), title_style))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(ar(f"المدينة: {user_info.get('city', '')}"), body_style))
    story.append(Paragraph(ar(f"نوع العقار: {user_info.get('property_type', '')}"), body_style))
    story.append(Paragraph(ar(f"الباقة: {package_level}"), body_style))
    story.append(Paragraph(ar(f"التاريخ: {datetime.now().strftime('%Y-%m-%d')}"), body_style))
    story.append(PageBreak())

    # --------------------------------------------------
    # 5️⃣ TEXT CONTENT
    # --------------------------------------------------
    if isinstance(content_text, list):
        # Content from report_orchestrator (Story ready)
        story.extend(content_text)

    elif isinstance(content_text, str):
        # Fallback text
        for line in content_text.split("\n"):
            clean = line.strip()

            if not clean:
                story.append(Spacer(1, 0.3 * cm))
                continue

            if clean.startswith("الفصل"):
                story.append(PageBreak())
                story.append(Paragraph(ar(clean), title_style))
                story.append(Spacer(1, 0.8 * cm))
                continue

            story.append(Paragraph(ar(clean), body_style))

    # --------------------------------------------------
    # 6️⃣ CHARTS SECTION
    # --------------------------------------------------
    try:
        charts_engine = AdvancedCharts()
        charts = charts_engine.generate_all_charts(
            df=market_data,
            user_info=user_info,
            real_data=real_data
        )

        if charts:
            story.append(PageBreak())
            story.append(Paragraph(ar("التحليل البياني المتقدم"), title_style))
            story.append(Spacer(1, 1 * cm))

            for chapter, figures in charts.items():
                if not figures:
                    continue

                story.append(Paragraph(ar(chapter.replace("_", " ").title()), subtitle_style))
                story.append(Spacer(1, 0.4 * cm))

                for fig in figures:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                        fig.write_image(tmp.name, width=1200, height=700, scale=2)
                        story.append(Image(tmp.name, width=16 * cm, height=9 * cm))
                        story.append(Spacer(1, 0.4 * cm))

    except Exception:
        pass  # charts failure must never break report

    # --------------------------------------------------
    # 7️⃣ AI RECOMMENDATIONS
    # --------------------------------------------------
    if ai_recommendations:
        story.append(PageBreak())
        story.append(Paragraph(ar("التوصيات الذكية المتقدمة"), title_style))
        story.append(Spacer(1, 0.8 * cm))

        if isinstance(ai_recommendations, dict):
            for k, v in ai_recommendations.items():
                story.append(Paragraph(ar(f"{k}: {v}"), body_style))

        elif isinstance(ai_recommendations, list):
            for i, rec in enumerate(ai_recommendations, 1):
                story.append(Paragraph(ar(f"{i}. {rec}"), body_style))

    # --------------------------------------------------
    # 8️⃣ FOOTER
    # --------------------------------------------------
    story.append(PageBreak())
    story.append(Spacer(1, 7 * cm))
    story.append(Paragraph(ar("نهاية التقرير"), subtitle_style))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(ar("Warda Intelligence"), body_style))
    story.append(Paragraph(ar("© جميع الحقوق محفوظة 2024"), body_style))

    # --------------------------------------------------
    # 9️⃣ BUILD
    # --------------------------------------------------
    doc.build(story)
    buffer.seek(0)
    return buffer
