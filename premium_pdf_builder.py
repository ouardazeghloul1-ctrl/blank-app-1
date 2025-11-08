# premium_pdf_builder.py - منشئ التقارير الفاخرة للباقات المميزة
from io import BytesIO
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

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
class PremiumPDFBuilder:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_arabic_styles()
    
    def _setup_arabic_styles(self):
        """إعداد الأنماط للغة العربية"""
        self.arabic_style = ParagraphStyle(
            'ArabicStyle',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            leading=16,
            alignment=2,  # Right alignment
            rightIndent=0,
            wordWrap='RTL'
        )
        
        self.arabic_title_style = ParagraphStyle(
            'ArabicTitle',
            parent=self.styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=24,
            alignment=2,
            textColor=colors.HexColor('#b30000')
        )
    
    def arabic(self, text):
        """تحويل النص العربي"""
        return get_display(arabic_reshaper.reshape(str(text)))
    
    def create_premium_pdf(self, user_info, market_data, real_data, package_level, ai_recommendations=None):
    """إنشاء تقرير PDF فاخر للباقات المميزة"""
    buffer = BytesIO()
    
    # 🎯🎯🎯 اضافة جديدة - ابدأ النسخ من هنا 🎯🎯🎯
    print(f"🎯 إنشاء تقرير للباقة: {package_level}")
    print(f"📊 بيانات المستخدم: {user_info}")
    print(f"📈 بيانات السوق: {market_data}")
    print(f"🏠 عدد العقارات: {len(real_data) if not real_data.empty else 'لا توجد بيانات'}")
    # 🎯🎯🎯 نهاية الاضافة - انتهى النسخ 🎯🎯🎯
    
    if package_level == "فضية":
        return self._create_silver_pdf(user_info, market_data, real_data, buffer)
    elif package_level == "ذهبية":
        return self._create_gold_pdf(user_info, market_data, real_data, ai_recommendations, buffer)
    elif package_level == "ماسية":
        return self._create_diamond_pdf(user_info, market_data, real_data, ai_recommendations, buffer)
    else:
        return self._create_basic_pdf(user_info, market_data, real_data, buffer)
    
    def _create_silver_pdf(self, user_info, market_data, real_data, buffer):
        """تقرير الباقة الفضية - 35 صفحة"""
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm)
        story = []
        
        # 🎨 الغلاف الفاخر
        story.extend(self._create_premium_cover(user_info, "فضية", "التقرير المتقدم"))
        story.append(PageBreak())
        
        # 📊 الملخص التنفيذي المتقدم
        story.extend(self._create_executive_summary(user_info, market_data, real_data, "متقدم"))
        story.append(PageBreak())
        
        # 📈 تحليل السوق المتعمق
        story.extend(self._create_market_analysis(real_data, market_data, "متقدم"))
        story.append(PageBreak())
        
        # 🎯 التحليل التنبؤي 18 شهراً
        story.extend(self._create_18month_forecast(market_data, real_data))
        story.append(PageBreak())
        
        # 🏢 مقارنة المنافسين
        story.extend(self._create_competitor_analysis(real_data))
        story.append(PageBreak())
        
        # 💼 دراسة الجدوى المتقدمة
        story.extend(self._create_feasibility_study(real_data, market_data))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _create_gold_pdf(self, user_info, market_data, real_data, ai_recommendations, buffer):
        """تقرير الباقة الذهبية - 60 صفحة"""
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm)
        story = []
        
        # 🎨 غلاف VIP
        story.extend(self._create_premium_cover(user_info, "ذهبية", "تقرير الذكاء الاصطناعي"))
        story.append(PageBreak())
        
        # 🤖 تحليل الذكاء الاصطناعي
        if ai_recommendations:
            story.extend(self._create_ai_analysis(ai_recommendations))
            story.append(PageBreak())
        
        # 📈 توقعات 5 سنوات
        story.extend(self._create_5year_forecast(market_data, real_data))
        story.append(PageBreak())
        
        # 🎯 تحليل المخاطر المتقدم
        story.extend(self._create_risk_analysis(real_data, market_data))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _create_diamond_pdf(self, user_info, market_data, real_data, ai_recommendations, buffer):
        """تقرير الباقة الماسية - 90 صفحة"""
        # استخدام النظام الذهبي مع إضافات
        return self._create_gold_pdf(user_info, market_data, real_data, ai_recommendations, buffer)
    
    def _create_basic_pdf(self, user_info, market_data, real_data, buffer):
        """تقرير أساسي للباقة المجانية"""
        from report_pdf_generator import create_pdf_from_content
        content = f"تقرير {user_info.get('city', '')} - {user_info.get('property_type', '')}"
        return create_pdf_from_content(user_info, market_data, real_data, content, "مجانية", None)
    
    def _create_premium_cover(self, user_info, package_level, report_type):
        """إنشاء غلاف فاخر"""
        cover_elements = []
        
        # العنوان الرئيسي
        title_text = f"<b>تقرير {report_type}</b>"
        cover_elements.append(Paragraph(self.arabic(title_text), self.arabic_title_style))
        cover_elements.append(Spacer(1, 2*cm))
        
        # معلومات الباقة
        package_text = f"""
        <b>الباقة:</b> {package_level}<br/>
        <b>العميل:</b> {user_info.get('user_type', 'مستثمر')}<br/>
        <b>المدينة:</b> {user_info.get('city', 'الرياض')}<br/>
        <b>نوع العقار:</b> {user_info.get('property_type', 'شقة')}<br/>
        <b>تاريخ التقرير:</b> {datetime.now().strftime('%Y-%m-%d')}
        """
        cover_elements.append(Paragraph(self.arabic(package_text), self.arabic_style))
        cover_elements.append(Spacer(1, 3*cm))
        
        # شعار الشركة
        company_text = "<b>Warda Intelligence</b><br/>الذكاء الاستثماري المتقدم"
        cover_elements.append(Paragraph(self.arabic(company_text), self.arabic_title_style))
        
        return cover_elements
    
    def _create_executive_summary(self, user_info, market_data, real_data, level):
        """إنشاء ملخص تنفيذي متقدم"""
        elements = []
        
        title = "الملخص التنفيذي - نظرة شاملة على السوق"
        elements.append(Paragraph(self.arabic(f"<b>{title}</b>"), self.arabic_title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # إحصائيات رئيسية
        if not real_data.empty:
            avg_price = real_data['السعر'].mean()
            avg_roi = real_data['العائد_المتوقع'].mean()
            market_growth = market_data.get('معدل_النمو_الشهري', 0)
            
            summary_text = f"""
            <b>أبرز المؤشرات:</b><br/>
            • متوسط أسعار السوق: {safe_num(avg_price)} ريال<br/>
            • متوسط العوائد: {avg_roi:.1f}% سنوياً<br/>
            • معدل نمو السوق: {market_growth:.1f}% شهرياً<br/>
            • عدد العقارات المحللة: {len(real_data)} عقار<br/>
            <br/>
            <b>التوقعات العامة:</b><br/>
            السوق في حالة { 'نمو إيجابي' if market_growth > 2 else 'استقرار' } مع فرص استثمارية متعددة<br/>
            في قطاع {user_info.get('property_type', 'العقارات')} بمدينة {user_info.get('city', 'المدينة')}
            """
        else:
            summary_text = "لا توجد بيانات كافية لتحليل السوق الحالي"
        
        elements.append(Paragraph(self.arabic(summary_text), self.arabic_style))
        return elements
    
    def _create_market_analysis(self, real_data, market_data, level):
        """تحليل السوق المتقدم"""
        elements = []
        
        elements.append(Paragraph(self.arabic("<b>📈 تحليل السوق المتقدم</b>"), self.arabic_title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        if not real_data.empty:
            analysis_text = f"""
            <b>مؤشرات السوق الرئيسية:</b><br/>
            • حجم السوق: {len(real_data)} عقار<br/>
            • توزيع المناطق: {real_data['المنطقة'].nunique()} منطقة<br/>
            • متوسط المساحة: {safe_num(real_data['المساحة'].mean(), '.0f')} م²<br/>
            • نطاق الأسعار: {safe_num(real_data['السعر'].min())} - {safe_num(real_data['السعر'].max())} ريال<br/>
            """
        else:
            analysis_text = "لا توجد بيانات كافية لتحليل السوق"
        
        elements.append(Paragraph(self.arabic(analysis_text), self.arabic_style))
        return elements
    
    def _create_18month_forecast(self, market_data, real_data):
        """تحليل تنبؤي 18 شهراً"""
        elements = []
        
        elements.append(Paragraph(self.arabic("<b>📈 التحليل التنبؤي 18 شهراً</b>"), self.arabic_title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        growth_rate = market_data.get('معدل_النمو_الشهري', 2.5)
        current_avg_price = real_data['السعر'].mean() if not real_data.empty else 1000000
        
        forecast_text = "<b>توقعات الأسعار للأشهر القادمة:</b><br/>"
        
        months = [6, 12, 18]
        for months_ahead in months:
            future_price = current_avg_price * (1 + growth_rate/100) ** months_ahead
            increase = ((future_price / current_avg_price) - 1) * 100
            
            forecast_text += f"""
            • بعد {months_ahead} شهر: {safe_num(future_price)} ريال (+{safe_num(increase, fmt='.1f')}%)<br/>
            """
        
        forecast_text += f"""
        <br/><b>التوصيات الاستثمارية:</b><br/>
        {'الاستثمار الفوري موصى به' if growth_rate > 3 else 'الاستثمار التدريجي أفضل'}
        """
        
        elements.append(Paragraph(self.arabic(forecast_text), self.arabic_style))
        return elements
    
    def _create_competitor_analysis(self, real_data):
        """تحليل المنافسين"""
        elements = []
        
        elements.append(Paragraph(self.arabic("<b>🏢 تحليل المنافسين</b>"), self.arabic_title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        if not real_data.empty:
            top_areas = real_data['المنطقة'].value_counts().head(10)
            analysis_text = "<b>أكثر المناطق نشاطاً:</b><br/>"
            
            for area, count in top_areas.items():
                avg_price = real_data[real_data['المنطقة'] == area]['السعر'].mean()
                analysis_text += f"• {area}: {count} عقار - متوسط السعر {safe_num(avg_price)} ريال<br/>"
        else:
            analysis_text = "لا توجد بيانات كافية لتحليل المنافسة"
        
        elements.append(Paragraph(self.arabic(analysis_text), self.arabic_style))
        return elements
    
    def _create_feasibility_study(self, real_data, market_data):
        """دراسة الجدوى المتقدمة"""
        elements = []
        
        elements.append(Paragraph(self.arabic("<b>💼 دراسة الجدوى المتقدمة</b>"), self.arabic_title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        if not real_data.empty:
            roi = real_data['العائد_المتوقع'].mean()
            payback_period = 100 / roi if roi > 0 else 0
            
            feasibility_text = f"""
            <b>مؤشرات الجدوى:</b><br/>
            • متوسط العائد على الاستثمار: {roi:.1f}%<br/>
            • فترة استرداد رأس المال: {payback_period:.1f} سنة<br/>
            • مؤشر الربحية: {'ممتاز' if roi > 8 else 'جيد' if roi > 6 else 'متوسط'}<br/>
            <br/>
            <b>التوصية:</b> {'مشروع مجدي' if roi > 7 else 'يحتاج دراسة إضافية'}
            """
        else:
            feasibility_text = "لا توجد بيانات كافية لدراسة الجدوى"
        
        elements.append(Paragraph(self.arabic(feasibility_text), self.arabic_style))
        return elements
    
    def _create_ai_analysis(self, ai_recommendations):
        """تحليل الذكاء الاصطناعي"""
        elements = []
        
        elements.append(Paragraph(self.arabic("<b>🤖 تحليل الذكاء الاصطناعي المتقدم</b>"), self.arabic_title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        if ai_recommendations:
            ai_text = f"""
            <b>ملف المخاطر:</b> {ai_recommendations.get('ملف_المخاطر', 'غير متوفر')}<br/>
            <b>الاستراتيجية المقترحة:</b> {ai_recommendations.get('استراتيجية_الاستثمار', 'غير متوفر')}<br/>
            <b>التوقيت المثالي:</b> {ai_recommendations.get('التوقيت_المثالي', 'غير متوفر')}<br/>
            """
        else:
            ai_text = "لا توجد توصيات من الذكاء الاصطناعي"
        
        elements.append(Paragraph(self.arabic(ai_text), self.arabic_style))
        return elements
    
    def _create_5year_forecast(self, market_data, real_data):
        """توقعات 5 سنوات"""
        elements = []
        
        elements.append(Paragraph(self.arabic("<b>📊 توقعات 5 سنوات</b>"), self.arabic_title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        forecast_text = """
        <b>التوقعات طويلة المدى:</b><br/>
        • السنة 1: نمو متسارع في المناطق الناشئة<br/>
        • السنة 2-3: استقرار مع فرص في القطاع التجاري<br/>
        • السنة 4-5: نضوج السوق وفرص التحسين<br/>
        <br/>
        <b>استراتيجية طويلة المدى:</b><br/>
        التركيز على التنويع والاستثمار في البنية التحتية
        """
        
        elements.append(Paragraph(self.arabic(forecast_text), self.arabic_style))
        return elements
    
    def _create_risk_analysis(self, real_data, market_data):
        """تحليل المخاطر المتقدم"""
        elements = []
        
        elements.append(Paragraph(self.arabic("<b>🛡️ تحليل المخاطر المتقدم</b>"), self.arabic_title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        risk_text = """
        <b>أنواع المخاطر المحتملة:</b><br/>
        • مخاطر السوق: تقلبات الأسعار والطلب<br/>
        • مخاطر التشغيل: تكاليف الصيانة والإدارة<br/>
        • مخاطر السيولة: صعوبة البيع في الأوقات الحرجة<br/>
        • مخاطر الاقتصاد الكلي: تغير السياسات الاقتصادية<br/>
        <br/>
        <b>استراتيجيات إدارة المخاطر:</b><br/>
        • التنويع الجغرافي والنوعي<br/>
        • الاحتفاظ باحتياطي نقدي<br/>
        • التأمين على العقارات<br/>
        """
        
        elements.append(Paragraph(self.arabic(risk_text), self.arabic_style))
        return elements

# اختبار النظام
if __name__ == "__main__":
    builder = PremiumPDFBuilder()
    print("✅ نظام التقارير الفاخرة جاهز!")
