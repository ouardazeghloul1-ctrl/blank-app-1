# report_orchestrator.py

from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.units import cm

# استيراد دوال الفصول النصية
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

def build_report_story(user_info, styles):
    """
    يبني القصة الكاملة للتقرير (Story)
    حسب خريطة الصفحات المعتمدة (120 صفحة)
    """
    story = []

    # -----------------------------
    # الصفحات الافتتاحية
    # -----------------------------
    story.append(Paragraph("تقرير وردة الذكاء العقاري", styles["title"]))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("النسخة: الماسية المتميزة", styles["subtitle"]))
    story.append(PageBreak())

    story.append(Paragraph("كيف تقرأ هذا التقرير؟", styles["subtitle"]))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        "هذا التقرير مبني لمساعدتك على اتخاذ قرار استثماري هادئ ومدروس، "
        "بعيدًا عن الضجيج والتوقعات السريعة.",
        styles["body"]
    ))
    story.append(PageBreak())

    # -----------------------------
    # الفصل الأول
    # -----------------------------
    story.append(Paragraph(chapter_1_text(user_info), styles["body"]))
    story.append(PageBreak())

    # -----------------------------
    # الفصل الثاني
    # -----------------------------
    story.append(Paragraph(chapter_2_text(user_info), styles["body"]))
    story.append(PageBreak())

    # -----------------------------
    # الفصل الثالث
    # -----------------------------
    story.append(Paragraph(chapter_3_text(user_info), styles["body"]))
    story.append(PageBreak())

    # -----------------------------
    # الفصل الرابع
    # -----------------------------
    story.append(Paragraph(chapter_4_text(user_info), styles["body"]))
    story.append(PageBreak())

    # -----------------------------
    # الفصل الخامس
    # -----------------------------
    story.append(Paragraph(chapter_5_text(user_info), styles["body"]))
    story.append(PageBreak())

    # -----------------------------
    # الفصل السادس
    # -----------------------------
    story.append(Paragraph(chapter_6_text(user_info), styles["body"]))
    story.append(PageBreak())

    # -----------------------------
    # الفصل السابع
    # -----------------------------
    story.append(Paragraph(chapter_7_text(user_info), styles["body"]))
    story.append(PageBreak())

    # -----------------------------
    # الفصل الثامن
    # -----------------------------
    story.append(Paragraph(chapter_8_text(user_info), styles["body"]))
    story.append(PageBreak())

    # -----------------------------
    # الفصل التاسع
    # -----------------------------
    story.append(Paragraph(chapter_9_text(user_info), styles["body"]))
    story.append(PageBreak())

    # -----------------------------
    # الفصل العاشر
    # -----------------------------
    story.append(Paragraph(chapter_10_text(user_info), styles["body"]))
    story.append(PageBreak())

    # -----------------------------
    # الصفحات الختامية
    # -----------------------------
    story.append(Paragraph("رسالة ختامية", styles["subtitle"]))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        "شكراً لاستخدامك Warda Intelligence. "
        "هذا التقرير صُمم ليكون أداة قرار تعيش معك، "
        "لا مجرد ملف يُقرأ مرة واحدة.",
        styles["body"]
    ))

    return story
