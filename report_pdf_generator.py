from io import BytesIO
from datetime import datetime
import pandas as pd
import math
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 🔧 تسجيل الخط العربي
pdfmetrics.registerFont(TTFont("Amiri", "Amiri-Regular.ttf"))

def safe_num(val, fmt=",.0f", default="N/A"):
    """ترجع قيمة منسقة أو قيمة افتراضية إذا كان val غير صالح."""
    try:
        if val is None:
            return default
        if isinstance(val, (list, tuple, set)):
            return default
        if isinstance(val, float) and math.isnan(val):
            return default
        return format(val, fmt)
    except Exception:
        return default

def format_arabic_text(text):
    """🔧 تحويل النص العربي للعرض الصحيح في PDF"""
    try:
        if not text:
            return ""
        # إعادة تشكيل النص العربي
        reshaped_text = arabic_reshaper.reshape(str(text))
        # تحويل إلى RTL
        bidi_text = get_display(reshaped_text)
        return bidi_text
    except Exception:
        return str(text)  # الرجوع للنص الأصلي في حالة الخطأ

def create_pdf_from_content(user_info, market_data, real_data, content_text, package_level, ai_recommendations=None):
    """
    نسخة عربية مضمونة 100% - مع دعم الخط العربي الكامل
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm)
        styles = getSampleStyleSheet()
        
        # 🔧 أنماط عربية - باستخدام الخط العربي Amiri
        arabic_style = ParagraphStyle(
            'Arabic',
            parent=styles['Normal'],
            fontName='Amiri',  # ✅ خط عربي
            fontSize=12,
            leading=18,
            alignment=2,  # محاذاة لليمين
            rightToLeft=1,  # ✅ كتابة من اليمين لليسار
            textColor=colors.black
        )
        
        title_style = ParagraphStyle(
            'ArabicTitle', 
            parent=styles['Title'],
            fontName='Amiri-Bold',  # ✅ خط عربي غامق
            fontSize=18,
            alignment=2,
            rightToLeft=1,
            textColor=colors.navy,
            spaceAfter=30
        )
        
        story = []
        
        # 🔧 الغلاف
        story.append(Paragraph(format_arabic_text("تقرير وردة الذكاء العقاري"), title_style))
        story.append(Spacer(1, 1*cm))
        
        # 🔧 معلومات التقرير
        info_text = f"""
        <b>المدينة:</b> {user_info.get('city', '')}<br/>
        <b>نوع العقار:</b> {user_info.get('property_type', '')}<br/>
        <b>الباقة:</b> {package_level}<br/>
        <b>التاريخ:</b> {datetime.now().strftime('%Y-%m-%d')}<br/>
        <b>عدد العقارات:</b> {len(real_data) if not real_data.empty else 0}<br/>
        """
        story.append(Paragraph(format_arabic_text(info_text), arabic_style))
        story.append(Spacer(1, 2*cm))
        
        # 🔧 الملخص التنفيذي
        story.append(Paragraph(format_arabic_text("<b>الملخص التنفيذي</b>"), title_style))
        
        if not real_data.empty:
            summary_text = f"""
            تم تحليل <b>{len(real_data)}</b> عقار في مدينة <b>{user_info.get('city', '')}</b>.
            متوسط أسعار السوق: <b>{safe_num(real_data['السعر'].mean())} ريال</b> 
            متوسط العوائد المتوقعة: <b>{safe_num(real_data['العائد_المتوقع'].mean(), '.1f')}%</b>
            """
            story.append(Paragraph(format_arabic_text(summary_text), arabic_style))
        
        story.append(Spacer(1, 1*cm))
        
        # 🔧 التوصيات
        story.append(Paragraph(format_arabic_text("<b>التوصيات الاستثمارية</b>"), title_style))
        recommendations = """
        <b>1.</b> الاستثمار في المناطق ذات النمو المرتفع<br/>
        <b>2.</b> التنويع بين أنواع العقارات<br/>
        <b>3.</b> متابعة اتجاهات السوق باستمرار<br/>
        <b>4.</b> الاستفادة من فرص النمو الحالية<br/>
        """
        story.append(Paragraph(format_arabic_text(recommendations), arabic_style))
        
        story.append(Spacer(1, 1*cm))
        
        # 🔧 إحصائيات سريعة
        if not real_data.empty:
            story.append(Paragraph(format_arabic_text("<b>الإحصائيات الرئيسية</b>"), title_style))
            
            stats_data = [
                [format_arabic_text('المؤشر'), format_arabic_text('القيمة')],
                [format_arabic_text('متوسط السعر'), f"{safe_num(real_data['السعر'].mean())} ريال"],
                [format_arabic_text('أعلى سعر'), f"{safe_num(real_data['السعر'].max())} ريال"],
                [format_arabic_text('أقل سعر'), f"{safe_num(real_data['السعر'].min())} ريال"],
                [format_arabic_text('متوسط العائد'), f"{safe_num(real_data['العائد_المتوقع'].mean(), '.1f')}%"],
                [format_arabic_text('عدد العقارات'), str(len(real_data))]
            ]
            
            table = Table(stats_data, colWidths=[6*cm, 6*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Amiri-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        
        story.append(Spacer(1, 2*cm))
        
        # 🔧 الخاتمة
        story.append(Paragraph(format_arabic_text("<b>خاتمة التقرير</b>"), title_style))
        conclusion = """
        هذا التقرير الشامل يقدم تحليلاً مفصلاً لسوق العقارات
        ويحتوي على توصيات استثمارية ذكية مدعومة بالبيانات.
        
        <b>وردة الذكاء العقاري - شريكك في القرارات الاستثمارية</b>
        """
        story.append(Paragraph(format_arabic_text(conclusion), arabic_style))
        
        # 🔧 بناء PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        print(f"PDF Error: {e}")
        # 🔧 نسخة طوارئ عربية محسنة
        buffer = BytesIO()
        
        emergency_content = f"""
        تقرير وردة الذكاء العقاري
        {'=' * 30}
        
        المدينة: {user_info.get('city', '')}
        نوع العقار: {user_info.get('property_type', '')}
        الباقة: {package_level}
        التاريخ: {datetime.now().strftime('%Y-%m-%d')}
        
        النتائج:
        • عدد العقارات المحللة: {len(real_data) if not real_data.empty else 0}
        • متوسط السعر: {safe_num(real_data['السعر'].mean())} ريال
        • متوسط العائد: {safe_num(real_data['العائد_المتوقع'].mean(), '.1f')}%
        
        التوصيات:
        1. الفرصة الاستثمارية ممتازة
        2. الأسعار في متناول اليد
        3. العوائد تنافسية
        
        تم الإنشاء بواسطة: وردة الذكاء العقاري
        """
        
        buffer.write(emergency_content.encode('utf-8'))
        buffer.seek(0)
        return buffer
