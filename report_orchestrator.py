# report_orchestrator.py

from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.units import cm


def build_report_story(chapters_texts: list, styles: dict, ar_func):
    """
    يبني محتوى التقرير (Story) من نصوص الفصول
    - يحافظ على الفراغات
    - يفصل الفصول في صفحات مستقلة
    - يدعم العربية بشكل كامل
    """

    arabic_style = styles["body"]
    title_style = styles["title"]
    subtitle_style = styles["subtitle"]

    story = []
    first_chapter = True

    for chapter_text in chapters_texts:
        # فصل جديد = صفحة جديدة (إلا الأول)
        if not first_chapter:
            story.append(PageBreak())
        first_chapter = False

        lines = chapter_text.split("\n")

        for line in lines:
            clean_line = line.rstrip()

            # فراغات → مسافة عمودية (نحافظ على الإحساس الصفحي)
            if clean_line.strip() == "":
                story.append(Spacer(1, 0.45 * cm))
                continue

            # عنوان فصل
            if clean_line.strip().startswith("الفصل"):
                story.append(Paragraph(ar_func(clean_line), title_style))
                story.append(Spacer(1, 1 * cm))
                continue

            # عناوين فرعية مرقمة (1.2 / 3.1 / إلخ)
            if clean_line.strip()[0].isdigit() and "." in clean_line[:4]:
                story.append(Spacer(1, 0.6 * cm))
                story.append(Paragraph(ar_func(clean_line), subtitle_style))
                story.append(Spacer(1, 0.4 * cm))
                continue

            # نص عادي
            story.append(Paragraph(ar_func(clean_line), arabic_style))
            story.append(Spacer(1, 0.3 * cm))

    return story
