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

# ✅ دالة معالجة العربية - النسخة النهائية (بدون شروط)
def ar(text):
    """تحويل النص العربي للعرض الصحيح - الإصدار النهائي"""
    if not text:
        return ""
    try:
        reshaped = arabic_reshaper.reshape(str(text))
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
    النسخة النهائية - التقرير العربي الكامل
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
        
        # ✅ أنماط النص - النسخة النهائية
        arabic_style = ParagraphStyle(
            'Arabic',
            parent=styles['Normal'],
            fontName='Amiri',
            fontSize=12,
            leading=18,
            alignment=2,  # محاذاة لليمين
            textColor=colors.black
        )
        
        arabic_table_style = ParagraphStyle(
            'ArabicTable',
            parent=styles['Normal'],
            fontName='Amiri',
            fontSize=11,
            leading=16,
            alignment=1,  # CENTER
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
        
        # ✅ 2. معلومات التقرير
        story.append(Paragraph(ar("معلومات التقرير"), subtitle_style))
        
        city = user_info.get('city', 'غير محدد')
        property_type = user_info.get('property_type', 'غير محدد')
        
        story.append(Paragraph(ar(f"المدينة: {city}"), arabic_style))
        story.append(Paragraph(ar(f"نوع العقار: {property_type}"), arabic_style))
        story.append(Paragraph(ar(f"الباقة: {package_level}"), arabic_style))
        story.append(Paragraph(ar(f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), arabic_style))
        
        property_count = len(real_data) if not real_data.empty else 0
        story.append(Paragraph(ar(f"عدد العقارات المحللة: {property_count}"), arabic_style))
        
        story.append(Spacer(1, 1.5*cm))
        
        # ✅ 3. الملخص التنفيذي
        story.append(Paragraph(ar("الملخص التنفيذي"), subtitle_style))
        
        if not real_data.empty:
            summary_text = ar(f"""
            تم تحليل {len(real_data)} عقار في مدينة {city}. 
            متوسط أسعار السوق: {safe_num(real_data['السعر'].mean())} ريال.
            متوسط العوائد المتوقعة: {safe_num(real_data['العائد_المتوقع'].mean(), '.1f')}%.
            """)
            story.append(Paragraph(summary_text, arabic_style))
        else:
            story.append(Paragraph(ar("لا توجد بيانات عقارية متاحة للتحليل"), arabic_style))
        
        story.append(Spacer(1, 1.5*cm))
        
        # ✅ 4. التوصيات الاستثمارية
        story.append(Paragraph(ar("التوصيات الاستثمارية"), subtitle_style))
        
        recommendations = ar("""
        1. الاستثمار في المناطق ذات النمو المرتفع في سوق العقارات السعودي.
        2. التنويع بين أنواع العقارات المختلفة لتحقيق عوائد مستقرة.
        3. متابعة اتجاهات السوق باستمرار من خلال أدوات التحليل المتقدمة.
        4. الاستفادة من فرص النمو الحالية في المناطق الواعدة.
        """)
        story.append(Paragraph(recommendations, arabic_style))
        
        story.append(Spacer(1, 1.5*cm))
        
        # ✅ 5. الإحصائيات الرئيسية (جدول)
        if not real_data.empty:
            story.append(Paragraph(ar("الإحصائيات الرئيسية"), subtitle_style))
            
            stats_data = [
                [
                    Paragraph(ar("المؤشر"), arabic_table_style),
                    Paragraph(ar("القيمة"), arabic_table_style)
                ],
                [
                    Paragraph(ar("متوسط السعر"), arabic_table_style),
                    Paragraph(ar(f"{safe_num(real_data['السعر'].mean())} ريال"), arabic_table_style)
                ],
                [
                    Paragraph(ar("أعلى سعر"), arabic_table_style),
                    Paragraph(ar(f"{safe_num(real_data['السعر'].max())} ريال"), arabic_table_style)
                ],
                [
                    Paragraph(ar("أقل سعر"), arabic_table_style),
                    Paragraph(ar(f"{safe_num(real_data['السعر'].min())} ريال"), arabic_table_style)
                ],
                [
                    Paragraph(ar("متوسط العائد"), arabic_table_style),
                    Paragraph(ar(f"{safe_num(real_data['العائد_المتوقع'].mean(), '.1f')}%"), arabic_table_style)
                ],
                [
                    Paragraph(ar("عدد العقارات"), arabic_table_style),
                    Paragraph(ar(str(len(real_data))), arabic_table_style)
                ]
            ]
            
            table = Table(stats_data, colWidths=[6*cm, 6*cm])
            
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E4053')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F2F4F4')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D5D8DC'))
            ]))
            
            story.append(table)
        
        story.append(Spacer(1, 2*cm))
        
        # ✅ 6. الخاتمة
        story.append(Paragraph(ar("خاتمة التقرير"), subtitle_style))
        
        conclusion = ar("""
        هذا التقرير الشامل يقدم تحليلاً مفصلاً لسوق العقارات السعودي، 
        ويحتوي على توصيات استثمارية ذكية مدعومة بالبيانات الحقيقية. 
        وردة الذكاء العقاري - شريكك الموثوق في القرارات الاستثمارية.
        """)
        story.append(Paragraph(conclusion, arabic_style))
        
        # ✅ بناء PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        print(f"PDF Error: {e}")
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
