# integrated_pdf_system.py - نظام PDF المتكامل مع النظام الذكي
from smart_report_system import SmartReportSystem
from io import BytesIO
import arabic_reshaper
from bidi.algorithm import get_display

class IntegratedPDFSystem:
    def __init__(self):
        self.smart_system = SmartReportSystem()
    
    def create_smart_pdf(self, user_info, market_data, real_data, package_level):
        """إنشاء PDF ذكي مع المحتوى المخصص لكل فئة"""
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # إنشاء التقرير الذكي الموسع
        smart_report = self.smart_system.generate_extended_report(user_info, market_data, real_data, package_level)
        
        # تحويل التقرير إلى فقرات PDF
        story.extend(self._convert_to_pdf_elements(smart_report, user_info))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _convert_to_pdf_elements(self, report_text, user_info):
        """تحويل النص إلى عناصر PDF"""
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, Spacer
        from reportlab.lib.units import cm
        
        elements = []
        styles = getSampleStyleSheet()
        
        # أنماط عربية
        arabic_style = ParagraphStyle(
            'Arabic',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            alignment=2,
            textColor=colors.black
        )
        
        title_style = ParagraphStyle(
            'ArabicTitle',
            parent=styles['Title'],
            fontName='Helvetica-Bold', 
            fontSize=16,
            alignment=2,
            textColor=colors.navy
        )
        
        # تقسيم التقرير إلى فقرات
        paragraphs = report_text.split('\n\n')
        
        for paragraph in paragraphs:
            if paragraph.strip():
                if any(marker in paragraph for marker in ['🎯', '📊', '💎', '👤']):
                    elements.append(Paragraph(self._ar(paragraph), title_style))
                else:
                    elements.append(Paragraph(self._ar(paragraph), arabic_style))
                elements.append(Spacer(1, 0.2*cm))
        
        return elements
    
    def _ar(self, text):
        """تحويل النص العربي"""
        try:
            reshaped = arabic_reshaper.reshape(str(text))
            return get_display(reshaped)
        except:
            return str(text)

# دالة الاستخدام
def create_integrated_pdf(user_info, market_data, real_data, package_level, ai_recommendations):
    system = IntegratedPDFSystem()
    return system.create_smart_pdf(user_info, market_data, real_data, package_level)
