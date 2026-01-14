# report_orchestrator.py

from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.units import cm
from arabic_reshaper import reshape
from bidi.algorithm import get_display


def ar(text):
    """
    دالة لمعالجة النصوص العربية (نفس الدالة الموجودة في report_pdf_generator)
    """
    if not text:
        return ""
    try:
        reshaped = reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)


def build_report_story(
    chapters_texts: list,
    arabic_style,
    title_style,
    subtitle_style
):
    """
    يبني محتوى التقرير (Story) بطريقة آمنة 100%
    chapters_texts: قائمة نصوص الفصول (كما هي من Word)
    """

    story = []

    for chapter_text in chapters_texts:
        lines = chapter_text.split("\n")

        for line in lines:
            clean_line = line.strip()

            # فراغ = مسافة عمودية
            if clean_line == "":
                story.append(Spacer(1, 0.5 * cm))
                continue

            # عنوان فصل
            if clean_line.startswith("الفصل"):
                story.append(PageBreak())
                story.append(Paragraph(ar(clean_line), title_style))
                story.append(Spacer(1, 1 * cm))
                continue

            # عناوين فرعية مرقمة
            if clean_line[0].isdigit() and "." in clean_line[:4]:
                story.append(Spacer(1, 0.5 * cm))
                story.append(Paragraph(ar(clean_line), subtitle_style))
                story.append(Spacer(1, 0.5 * cm))
                continue

            # نص عادي
            story.append(Paragraph(ar(clean_line), arabic_style))
            story.append(Spacer(1, 0.3 * cm))

    return story
