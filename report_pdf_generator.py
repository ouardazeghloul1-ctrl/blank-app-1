# ---- Font (SAFE PATH) ----
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

styles = getSampleStyleSheet()

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

    # ---- Chapter ----
    if btype == "chapter_title":
        story.append(PageBreak())
        story.append(Paragraph(ar(block["content"]), chapter))

    # ---- Text ----
    elif btype == "text":
        story.append(Paragraph(ar(block["content"]), body))

    # ---- AI Insight ----
    elif btype == "ai_insight":
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph(ar(block["content"]), ai_box))

    # ---- Chart ----
    elif btype == "chart":
        ch = block["chapter"]
        chart_cursor.setdefault(ch, 0)
        fig = charts_by_chapter.get(f"chapter_{ch}", [])[chart_cursor[ch]]
        story.append(Spacer(1, 0.8 * cm))
        story.append(plotly_to_image(fig))
        chart_cursor[ch] += 1

    # ---- Chart Caption ----
    elif btype == "chart_caption":
        story.append(Paragraph(ar(block["content"]), ParagraphStyle(
            "Caption",
            parent=body,
            alignment=TA_CENTER,
            fontSize=13,
            textColor=colors.HexColor("#666666")
        )))

    # ---- Final Decision ----
    elif btype == "final_decision":
        story.append(PageBreak())
        story.append(Paragraph(ar(block["title"]), title_exec))
        story.append(executive_decision_box(block["content"]))

doc.build(story)
buffer.seek(0)
return buffer
