# report_pdf_generator.py
# ==========================================
# FINAL CLEAN PDF GENERATOR (SAFE & STABLE)
# ==========================================

from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    PageBreak, Image, Table, TableStyle
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import arabic_reshaper
from bidi.algorithm import get_display
import tempfile
import plotly.graph_objects as go
import os


# =========================
# Arabic helper
# =========================
def ar(text):
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


# =========================
# Plotly → Image
# =========================
def plotly_to_image(fig, w=16.5, h=8.5):
    img_bytes = fig.to_image(
        format="png",
        width=int(w * 38),
        height=int(h * 38)
    )
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    tmp.write(img_bytes)
    tmp.close()
    return Image(tmp.name, width=w * cm, height=h * cm)


# =========================
# Executive Decision Box
# =========================
def executive_decision_box(text):
    return Table(
        [[Paragraph(ar(text), ParagraphStyle(
            "DecisionText",
            fontName="Amiri",
            fontSize=14.5,
            leading=28,
            alignment=TA_RIGHT
        ))]],
        colWidths=[16 * cm],
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F2F3F5")),
            ("BOX", (0,0), (-1,-1), 1.8, colors.HexColor("#7a0000")),
            ("INNERPADDING", (0,0), (-1,-1), 18),
        ])
    )


# =========================
# MAIN PDF BUILDER
# =========================
def create_pdf_from_blocks(blocks, charts_by_chapter):
    buffer = BytesIO()

    # ---- SAFE FONT PATH ----
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FONT_PATH = os.path.join(BASE_DIR, "Amiri-Regular.ttf")

    pdfmetrics.registerFont(
        TTFont("Amiri", FONT_PATH)
    )

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2.4 * cm,
        leftMargin=2.4 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm
    )

    body = ParagraphStyle(
        "Body",
        fontName="Amiri",
        fontSize=14.5,
        leading=28,
        alignment=TA_RIGHT,
        spaceAfter=18
    )

    chapter = ParagraphStyle(
        "Chapter",
        fontName="Amiri",
        fontSize=18,
        textColor=colors.HexColor("#9c1c1c"),
        alignment=TA_RIGHT,
        spaceBefore=32,
        spaceAfter=16
    )

    ai_box = ParagraphStyle(
        "AIBox",
        parent=body,
        backColor=colors.HexColor("#F2F4F7"),
        leftIndent=12,
        rightIndent=12
    )

    title_exec = ParagraphStyle(
        "ExecTitle",
        fontName="Amiri",
        fontSize=19,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        spaceAfter=24
    )

    story = []
    chart_cursor = {}

    # =========================
    # RENDER BLOCKS
    # =========================
    for block in blocks:
        btype = block["type"]

        if btype == "chapter_title":
            if story:
                story.append(PageBreak())
            story.append(Paragraph(ar(block["content"]), chapter))

        elif btype == "text":
            story.append(Paragraph(ar(block["content"]), body))

        elif btype == "ai_insight":
            story.append(Spacer(1, 0.3 * cm))
            story.append(Paragraph(ar(block["content"]), ai_box))

        elif btype == "chart":
            ch = block["chapter"]
            chart_cursor.setdefault(ch, 0)
            fig = charts_by_chapter.get(f"chapter_{ch}", [])[chart_cursor[ch]]
            story.append(Spacer(1, 0.8 * cm))
            story.append(plotly_to_image(fig))
            chart_cursor[ch] += 1

        elif btype == "chart_caption":
            story.append(Paragraph(ar(block["content"]), ParagraphStyle(
                "Caption",
                parent=body,
                alignment=TA_CENTER,
                fontSize=13,
                textColor=colors.HexColor("#666666")
            )))

        elif btype == "final_decision":
            story.append(PageBreak())
            story.append(Paragraph(ar(block["title"]), title_exec))
            story.append(executive_decision_box(block["content"]))

    doc.build(story)
    buffer.seek(0)
    return buffer
