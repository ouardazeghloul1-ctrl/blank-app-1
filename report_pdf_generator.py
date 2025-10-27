from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_pdf_from_content(user_info, market_data, df, content_text, package_level, ai_recommendations=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm)
    
    # أنماط النص
    styles = getSampleStyleSheet()
    
    # إنشاء أنماط عربية
    arabic_style = ParagraphStyle(
        'ArabicStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        alignment=2,  # محاذاة لليمين
        rightIndent=0,
        wordWrap='CJK'  # دعم النص العربي
    )
    
    title_style = ParagraphStyle(
        'ArabicTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        alignment=2,
        textColor=colors.darkblue,
        spaceAfter=30
    )
    
    story = []
    
    # الصفحة الأولى - الغلاف
    story.append(Paragraph("تقرير Warda Intelligence", title_style))
    story.append(Spacer(1, 2*cm))
    
    # معلومات التقرير
    info_text = f"""
    <b>المدينة:</b> {user_info.get('city', '')}<br/>
    <b>نوع العقار:</b> {user_info.get('property_type', '')}<br/>
    <b>الباقة:</b> {package_level}<br/>
    <b>التاريخ:</b> {datetime.now().strftime('%Y-%m-%d')}<br/>
    """
    story.append(Paragraph(info_text, arabic_style))
    story.append(PageBreak())
    
    # محتوى التقرير
    lines = content_text.split("\n")
    for line in lines:
        if line.strip():
            story.append(Paragraph(line.strip(), arabic_style))
            story.append(Spacer(1, 12))
    
    story.append(PageBreak())
    
    # إضافة رسوم بيانية
    if not df.empty:
        # الرسم البياني 1: توزيع الأسعار
        fig, ax = plt.subplots(figsize=(10, 6))
        prices = pd.to_numeric(df['السعر'], errors='coerce').dropna()
        if not prices.empty:
            ax.hist(prices / 1000, bins=10, color='skyblue', edgecolor='black')
            ax.set_xlabel('السعر (بالآلاف)')
            ax.set_ylabel('عدد العقارات')
            ax.set_title('توزيع الأسعار')
            
            # حفظ الرسم
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
            img_buffer.seek(0)
            
            from reportlab.platypus import Image
            story.append(Paragraph("<b>الرسم البياني: توزيع الأسعار</b>", arabic_style))
            story.append(Image(img_buffer, width=15*cm, height=10*cm))
            story.append(PageBreak())
            plt.close()
    
    # صفحة الختام
    story.append(Paragraph("<b>خلاصة التقرير</b>", title_style))
    story.append(Spacer(1, 1*cm))
    
    summary_text = f"""
    تم تحليل {len(df) if not df.empty else 0} عقار في {user_info.get('city', '')}.
    هذا التقرير يقدم رؤية شاملة لسوق العقارات ويحتوي على توصيات استثمارية ذكية.
    
    <b>Warda Intelligence</b><br/>
    الذكاء الاستثماري المتقدم
    """
    story.append(Paragraph(summary_text, arabic_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
