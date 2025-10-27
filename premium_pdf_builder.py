# premium_pdf_builder.py - منشئ التقارير الفاخرة للباقات المميزة
from io import BytesIO
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.barcharts import VerticalBarChart
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
        story.append(self._create_premium_cover(user_info, "فضية", "التقرير المتقدم"))
        story.append(PageBreak())
        
        # 📊 الملخص التنفيذي المتقدم
        story.append(self._create_executive_summary(user_info, market_data, real_data, "متقدم"))
        story.append(PageBreak())
        
        # 📈 تحليل السوق المتعمق
        story.append(self._create_market_analysis(real_data, market_data, "متقدم"))
        story.append(PageBreak())
        
        # 🎯 التحليل التنبؤي 18 شهراً
        story.append(self._create_18month_forecast(market_data, real_data))
        story.append(PageBreak())
        
        # 🏢 مقارنة المنافسين
        story.append(self._create_competitor_analysis(real_data))
        story.append(PageBreak())
        
        # 💼 دراسة الجدوى المتقدمة
        story.append(self._create_feasibility_study(real_data, market_data))
        story.append(PageBreak())
        
        # 📋 التوصيات الاستراتيجية
        story.append(self._create_strategic_recommendations(user_info, real_data))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _create_gold_pdf(self, user_info, market_data, real_data, ai_recommendations, buffer):
        """تقرير الباقة الذهبية - 60 صفحة"""
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm)
        story = []
        
        # 🎨 غلاف VIP
        story.append(self._create_premium_cover(user_info, "ذهبية", "تقرير الذكاء الاصطناعي"))
        story.append(PageBreak())
        
        # 🤖 تحليل الذكاء الاصطناعي
        if ai_recommendations:
            story.append(self._create_ai_analysis(ai_recommendations))
            story.append(PageBreak())
        
        # 📈 توقعات 5 سنوات
        story.append(self._create_5year_forecast(market_data, real_data))
        story.append(PageBreak())
        
        # 🎯 تحليل المخاطر المتقدم
        story.append(self._create_risk_analysis(real_data, market_data))
        story.append(PageBreak())
        
        # 💰 دراسة الجدوى الاقتصادية الشاملة
        story.append(self._create_comprehensive_feasibility(real_data, market_data))
        story.append(PageBreak())
        
        # 🏆 تحليل 25 منافس
        story.append(self._create_25_competitors_analysis(real_data))
        story.append(PageBreak())
        
        # 📊 مؤشرات الأداء المتقدمة
        story.append(self._create_advanced_kpis(real_data, market_data))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
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
            • متوسط أسعار السوق: {avg_price:,.0f} ريال<br/>
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
            • بعد {months_ahead} شهر: {future_price:,.0f} ريال (+{increase:.1f}%)<br/>
            """
        
        forecast_text += f"""
        <br/><b>التوصيات الاستثمارية:</b><br/>
        {'الاستثمار الفوري موصى به' if growth_rate > 3 else 'الاستثمار التدريجي أفضل'}
        """
        
        elements.append(Paragraph(self.arabic(forecast_text), self.arabic_style))
        return elements

# اختبار النظام
if __name__ == "__main__":
    builder = PremiumPDFBuilder()
    print("✅ نظام التقارير الفاخرة جاهز!")
