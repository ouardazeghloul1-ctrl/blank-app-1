# =========================================
# FINAL EXECUTIVE PDF GENERATOR – WARDA
# نسخة مستقرة – تقرير فاخر مبني على بيانات حقيقية
# =========================================

from io import BytesIO
import os
import tempfile
import re
import unicodedata

import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    PageBreak, Image, KeepTogether,
    Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import plotly.graph_objects as go

# 🔑 الخلاصة الاستشارية الحقيقية
from ai_executive_summary import generate_executive_summary


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
# Clean text (محافظ – بدون تخريب)
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
# Executive Decision Box (فاخر – ثابت)
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
            ("TOPPADDING", (0, 0), (-1, -1), 22),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
            ("LEFTPADDING", (0, 0), (-1, -1), 18),
            ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ])
    )


# =========================
# MAIN PDF GENERATOR
# =========================
def create_pdf_from_blocks(
    blocks,
    charts_by_chapter,
    user_info,
    market_data,
    real_data
):
    buffer = BytesIO()

    # -------------------------
    # FONT (SAFE)
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
        "Body",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=14.5,
        leading=28,
        alignment=TA_RIGHT,
        spaceAfter=18,
        allowWidows=0,
        allowOrphans=0,
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

    story = []
    chart_cursor = {}
    chapter_index = 0

    # =========================
    # CONTENT RENDER
    # =========================
    for block in blocks:
        btype = block.get("type")

        # -------- CHAPTER --------
        if btype == "chapter_title":
            chapter_index += 1
            chart_cursor[chapter_index] = 0

            if chapter_index > 1:
                story.append(PageBreak())

            story.append(
                KeepTogether([
                    Paragraph(ar(block["content"]), chapter),
                    Spacer(1, 0.6 * cm)
                ])
            )
            continue

        # -------- TEXT --------
        if btype == "text":
            clean = clean_text(block.get("content", ""))
            if clean:
                story.append(Paragraph(ar(clean), body))
            continue

        # -------- CHART --------
        if btype == "chart":
            charts = charts_by_chapter.get(f"chapter_{chapter_index}", [])
            idx = chart_cursor.get(chapter_index, 0)

            if idx < len(charts):
                img = plotly_to_image(charts[idx], 16.8, 8.8)
                if img:
                    story.append(Spacer(1, 1.2 * cm))
                    story.append(img)
                    story.append(Spacer(1, 0.8 * cm))
                chart_cursor[chapter_index] += 1
            continue

        # -------- CHART CAPTION --------
        if btype == "chart_caption":
            story.append(Paragraph(ar(block.get("content", "")), ParagraphStyle(
                "Caption",
                parent=body,
                alignment=TA_CENTER,
                fontSize=13,
                textColor=colors.HexColor("#666666")
            )))
            story.append(Spacer(1, 1.0 * cm))
            continue

    # =========================
    # 🧠 EXECUTIVE FINAL DECISION
    # =========================
    story.append(PageBreak())
    story.append(Spacer(1, 1.5 * cm))

    story.append(Paragraph(
        ar("الخلاصة الاستشارية النهائية"),
        ParagraphStyle(
            "FinalTitle",
            parent=chapter,
            alignment=TA_CENTER,
            fontSize=19,
            textColor=colors.HexColor("#5a0000"),
            spaceAfter=24
        )
    ))

    executive_text = generate_executive_summary(
        user_info=user_info,
        market_data=market_data,
        real_data=real_data
    )

    story.append(executive_decision_box(executive_text))
    story.append(Spacer(1, 1.5 * cm))

    # =========================
    # BUILD
    # =========================
    doc.build(story)
    buffer.seek(0)
    return buffer


# =========================
# SAFE ALIAS (حل ImportError)
# =========================
def create_pdf_from_content(*args, **kwargs):
    """
    Alias آمن للحفاظ على التوافق مع streamlit_app.py
    """
    return create_pdf_from_blocks(*args, **kwargs)
