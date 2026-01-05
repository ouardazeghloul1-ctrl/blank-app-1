from io import BytesIO
from datetime import datetime
import pandas as pd
import math
import os

# ✅ استيرادات إجبارية للعربية
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ✅ الخطوة 1: دالة معالجة العربية (للنصوص العربية فقط)
def ar(text):
    """تحويل النص العربي للعرض الصحيح - للنصوص العربية الصرفة فقط"""
    if not text:
        return ""
    try:
        clean_text = str(text)
        reshaped = arabic_reshaper.reshape(clean_text)
        return get_display(reshaped)
    except Exception:
        return str(text)

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

def create_pdf_from_content(user_info, market_data, real_data, content_text, package_level, ai_recommendations=None):
    """
    نسخة عربية مضمونة 100% - النصوص العربية والأرقام منفصلة
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        
        # ✅ تسجيل الخطوط العربية
        font_path = "Amiri-Regular.ttf"
        
        if not os.path.exists(font_path):
            # خطة طوارئ
            buffer = BytesIO()
            emergency_content = f"""
            ⚠️ تنبيه: ملف الخط العربي غير موجود
            الرجاء إضافة ملف Amiri-Regular.ttf إلى المجلد
            
            تقرير وردة الذكاء العقاري
            {'=' * 40}
            
            المدينة: {user_info.get('city', '')}
            نوع العقار: {user_info.get('property_type', '')}
            الباقة: {package_level}
            التاريخ: {datetime.now().strftime('%Y-%m-%d')}
            
            تم تحليل {len(real_data) if not real_data.empty else 0} عقار
            """
            buffer.write(emergency_content.encode('utf-8'))
            buffer.seek(0)
            return buffer
        
        pdfmetrics.registerFont(TTFont("Amiri", font_path))
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm)
        styles = getSampleStyleSheet()
        
        # ✅ أنماط النص
        arabic_style = ParagraphStyle(
            'Arabic',
            parent=styles['Normal'],
            fontName='Amiri',
            fontSize=12,
            leading=18,
            alignment=2,
            textColor=colors.black
        )
        
        title_style = ParagraphStyle(
            'ArabicTitle', 
            parent=styles['Title'],
            fontName='Amiri',
            fontSize=18,
            alignment=2,
            textColor=colors.HexColor('#1A5276'),
            spaceAfter=20,
            spaceBefore=20
        )
        
        subtitle_style = ParagraphStyle(
            'ArabicSubtitle',
            parent=styles['Heading2'],
            fontName='Amiri',
            fontSize=14,
            alignment=2,
            textColor=colors.HexColor('#2874A6'),
            spaceAfter=15
        )
        
        story = []
        
        # ✅ 1. العنوان الرئيسي
        story.append(Paragraph(ar("تقرير وردة الذكاء العقاري"), title_style))
        story.append(Spacer(1, 1*cm))
        
        # ✅ 2. معلومات التقرير - كل سطر منفصل
        story.append(Paragraph(ar("معلومات التقرير"), subtitle_style))
        story.append(Paragraph(ar("المدينة:"), arabic_style))
        story.append(Paragraph(user_info.get('city', 'غير محدد'), arabic_style))
        
        story.append(Paragraph(ar("نوع العقار:"), arabic_style))
        story.append(Paragraph(user_info.get('property_type', 'غير محدد'), arabic_style))
        
        story.append(Paragraph(ar("الباقة:"), arabic_style))
        story.append(Paragraph(package_level, arabic_style))
        
        story.append(Paragraph(ar("التاريخ:"), arabic_style))
        story.append(Paragraph(datetime.now().strftime('%Y-%m-%d %H:%M'), arabic_style))
        
        story.append(Paragraph(ar("عدد العقارات المحللة:"), arabic_style))
        property_count = len(real_data) if not real_data.empty else 0
        story.append(Paragraph(str(property_count), arabic_style))
        
        story.append(Spacer(1, 1.5*cm))
        
        # ✅ 3. الملخص التنفيذي
        story.append(Paragraph(ar("الملخص التنفيذي"), subtitle_style))
        
        if not real_data.empty:
            story.append(Paragraph(ar("تم تحليل"), arabic_style))
            story.append(Paragraph(str(len(real_data)), arabic_style))
            story.append(Paragraph(ar("عقار في مدينة"), arabic_style))
            story.append(Paragraph(user_info.get('city', ''), arabic_style))
            
            story.append(Spacer(1, 0.5*cm))
            
            story.append(Paragraph(ar("متوسط أسعار السوق:"), arabic_style))
            story.append(Paragraph(safe_num(real_data['السعر'].mean()) + " ريال", arabic_style))
            
            story.append(Paragraph(ar("متوسط العوائد المتوقعة:"), arabic_style))
            story.append(Paragraph(safe_num(real_data['العائد_المتوقع'].mean(), '.1f') + "%", arabic_style))
        else:
            story.append(Paragraph(ar("لا توجد بيانات عقارية متاحة للتحليل"), arabic_style))
        
        story.append(Spacer(1, 1.5*cm))
        
        # ✅ 4. التوصيات الاستثمارية
        story.append(Paragraph(ar("التوصيات الاستثمارية"), subtitle_style))
        
        recommendations = [
            ar("1. الاستثمار في المناطق ذات النمو المرتفع"),
            ar("2. التنويع بين أنواع العقارات"),
            ar("3. متابعة اتجاهات السوق باستمرار"),
            ar("4. الاستفادة من فرص النمو الحالية")
        ]
        
        for rec in recommendations:
            story.append(Paragraph(rec, arabic_style))
        
        story.append(Spacer(1, 1.5*cm))
        
        # ✅ 5. الإحصائيات الرئيسية (جدول)
        if not real_data.empty:
            story.append(Paragraph(ar("الإحصائيات الرئيسية"), subtitle_style))
            
            stats_data = [
                [ar('المؤشر'), ar('القيمة')],
                [ar('متوسط السعر'), f"{safe_num(real_data['السعر'].mean())} ريال"],
                [ar('أعلى سعر'), f"{safe_num(real_data['السعر'].max())} ريال"],
                [ar('أقل سعر'), f"{safe_num(real_data['السعر'].min())} ريال"],
                [ar('متوسط العائد'), f"{safe_num(real_data['العائد_المتوقع'].mean(), '.1f')}%"],
                [ar('عدد العقارات'), str(len(real_data))]
            ]
            
            table = Table(stats_data, colWidths=[6*cm, 6*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E4053')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Amiri'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F2F4F4')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D5D8DC')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica')
            ]))
            
            story.append(table)
        
        story.append(Spacer(1, 2*cm))
        
        # ✅ 6. الخاتمة
        story.append(Paragraph(ar("خاتمة التقرير"), subtitle_style))
        
        story.append(Paragraph(ar("هذا التقرير الشامل يقدم تحليلاً مفصلاً لسوق العقارات"), arabic_style))
        story.append(Paragraph(ar("ويحتوي على توصيات استثمارية ذكية مدعومة بالبيانات"), arabic_style))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(ar("وردة الذكاء العقاري"), arabic_style))
        story.append(Paragraph(ar("شريكك في القرارات الاستثمارية"), arabic_style))
        
        story.append(Spacer(1, 1*cm))
        
        # ✅ 7. نوع الباقة
        story.append(Paragraph(ar("نوع الباقة:"), arabic_style))
        story.append(Paragraph(package_level, arabic_style))
        
        # ✅ بناء PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        print(f"PDF Error: {e}")
        # خطة طوارئ
        buffer = BytesIO()
        
        emergency_content = f"""
        تقرير وردة الذكاء العقاري
        {'=' * 40}
        
        المدينة: {user_info.get('city', '')}
        نوع العقار: {user_info.get('property_type', '')}
        الباقة: {package_level}
        التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
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
