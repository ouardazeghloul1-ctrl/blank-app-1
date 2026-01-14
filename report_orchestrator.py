# report_orchestrator.py

from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.units import cm
import arabic_reshaper
from bidi.algorithm import get_display

# ========= دعم العربية =========
def ar(text):
    if not text:
        return ""
    try:
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)

# ========= استيراد نصوص الفصول =========
from report_content_builder import (
    chapter_1_text,
    chapter_2_text,
    chapter_3_text,
    chapter_4_text,
    chapter_5_text,
    chapter_6_text,
    chapter_7_text,
    chapter_8_text,
    chapter_9_text,
    chapter_10_text
)

# ========= الدالة الوحيدة المسؤولة عن بناء التقرير =========
def build_report_story(user_info: dict, styles: dict):
    """
    تبني محتوى التقرير الكامل (Story) من الفصول العشرة
    """

    arabic_style = styles["body"]
    title_style = styles["title"]
    subtitle_style = styles["subtitle"]

    chapters = [
        chapter_1_text(user_info),
        chapter_2_text(user_info),
        chapter_3_text(user_info),
        chapter_4_text(user_info),
        chapter_5_text(user_info),
        chapter_6_text(user_info),
        chapter_7_text(user_info),
        chapter_8_text(user_info),
        chapter_9_text(user_info),
        chapter_10_text(user_info),
    ]

    story = []

    for chapter_text in chapters:
        lines = chapter_text.split("\n")

        for line in lines:
            clean = line.strip()

            # فراغ = مسافة عمودية (نحافظ على التقسيم)
            if clean == "":
                story.append(Spacer(1, 0.4 * cm))
                continue

            # عنوان فصل
            if clean.startswith("الفصل"):
                story.append(PageBreak())
                story.append(Paragraph(ar(clean), title_style))
                story.append(Spacer(1, 1 * cm))
                continue

            # عنوان فرعي مرقم
            if clean[0].isdigit() and "." in clean[:4]:
                story.append(Spacer(1, 0.5 * cm))
                story.append(Paragraph(ar(clean), subtitle_style))
                story.append(Spacer(1, 0.3 * cm))
                continue

            # نص عادي
            story.append(Paragraph(ar(clean), arabic_style))
            story.append(Spacer(1, 0.25 * cm))

    return story
