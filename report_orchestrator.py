# report_orchestrator.py

from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.units import cm
import arabic_reshaper
from bidi.algorithm import get_display


# =========================
# Arabic text helper
# =========================
def ar(text):
    """
    إعادة تشكيل النص العربي ليظهر بشكل صحيح في ReportLab
    """
    if not text:
        return ""
    try:
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)


# =========================
# Import chapter builders
# =========================
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


# =========================
# MAIN ORCHESTRATOR
# =========================
def build_report_story(user_info: dict, styles: dict):
    """
    تبني محتوى التقرير الكامل (Story) للفصول العشرة
    ❗ بدون صفحات فارغة
    ❗ تحكم كامل في PageBreak
    """

    body_style = styles["body"]
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
        if not chapter_text:
            continue

        lines = chapter_text.split("\n")

        for line in lines:
            clean = line.strip()

            # سطر فارغ = مسافة عمودية
            if not clean:
                story.append(Spacer(1, 0.35 * cm))
                continue

            # ===== عنوان فصل =====
            if clean.startswith("الفصل"):
                # 🔥 الحل الجذري: لا PageBreak إذا كان هذا أول محتوى
                if story:
                    story.append(PageBreak())

                story.append(Paragraph(ar(clean), title_style))
                story.append(Spacer(1, 0.8 * cm))
                continue

            # ===== عنوان فرعي مرقم =====
            if clean[0].isdigit() and "." in clean[:4]:
                story.append(Spacer(1, 0.4 * cm))
                story.append(Paragraph(ar(clean), subtitle_style))
                story.append(Spacer(1, 0.25 * cm))
                continue

            # ===== نص عادي =====
            story.append(Paragraph(ar(clean), body_style))
            story.append(Spacer(1, 0.25 * cm))

    return story
