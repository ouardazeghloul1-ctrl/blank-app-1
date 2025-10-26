# report_pdf_generator.py
from io import BytesIO
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

def arabic(text):
    return get_display(arabic_reshaper.reshape(str(text)))

def create_pdf_from_content(user_info, market_data, df, content_text, package_level, ai_recommendations=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm)

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    body_style = styles["BodyText"]
    body_style.fontSize = 12
    body_style.leading = 18

    story = []

    # غلاف
    story.append(Paragraph(arabic("تقرير Warda Intelligence"), title_style))
    story.append(Spacer(1, 12))
    meta = f"المدينة: {user_info.get('city','-')} | نوع العقار: {user_info.get('property_type','-')} | الباقة: {package_level} | تاريخ: {datetime.now().strftime('%Y-%m-%d')}"
    story.append(Paragraph(arabic(meta), body_style))
    story.append(PageBreak())

    # نص التقرير كامل بدون تكرار
    for line in content_text.split("\n"):
        if line.strip():
            story.append(Paragraph(arabic(line), body_style))
            story.append(Spacer(1, 8))

    story.append(PageBreak())

    # الرسوم البيانية
    def add_chart(fig):
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format="png", bbox_inches="tight")
        img_buffer.seek(0)
        story.append(Image(img_buffer, width=16*cm, height=10*cm))
        story.append(PageBreak())
        plt.close(fig)

    # 1) توزيع الأسعار
    if not df.empty:
        fig, ax = plt.subplots()
        prices = pd.to_numeric(df['السعر'], errors='coerce').dropna() / 1000
        ax.hist(prices, bins=15)
        ax.set_title(arabic("توزيع الأسعار (بالآلاف)"))
        add_chart(fig)

    # 2) توقع الأسعار
    if market_data:
        fig, ax = plt.subplots()
        months = ['حالي', '1م', '3م', '6م', 'سنة']
        growth = market_data.get('معدل_النمو_الشهري', 0)
        current = market_data.get('السعر_الحالي', df['السعر'].mean())
        values = [current * (1 + growth*i/100) for i in [0, 1, 3, 6, 12]]
        ax.plot(months, values, marker='o')
        ax.set_title(arabic("توقع حركة الأسعار"))
        add_chart(fig)

    doc.build(story)
    buffer.seek(0)
    return buffer
