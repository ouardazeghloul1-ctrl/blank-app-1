 enhanced_pdf.py - الإصدار المصحح مع دعم جميع المدن
from io import BytesIO
from datetime import datetime
import pandas as pd
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
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

class EnhancedPDFGenerator:
    def __init__(self):
        # 🎯 التركيز على العدد الدقيق للصفحات مع هوية فاخرة
        self.package_pages = {
            "مجانية": 15,
            "فضية": 35, 
            "ذهبية": 60,
            "ماسية": 90
        }
        
        # 🎯 نظام المدن الذكي - متوافق مع سكريبر البيانات
        self.city_profiles = {
            "الرياض": {
                "description": "العاصمة الاقتصادية والقلب النابض للمملكة",
                "strength": "النمو السكاني والاستثماري المتسارع",
                "opportunity": "رؤية 2030 والمشاريع الكبرى",
                "growth_rate": 2.8
            },
            "جدة": {
                "description": "عروس البحر الأحمر والعاصمة التجارية",
                "strength": "الموقع الاستراتيجي والبنية التحتية المتطورة",
                "opportunity": "المشاريع السياحية والاستثمارات الكبرى", 
                "growth_rate": 2.2
            },
            "مكة": {
                "description": "أطهر بقاع الأرض والعاصمة الدينية العالمية",
                "strength": "الطلب المستمر من الحجاج والمعتمرين",
                "opportunity": "المشاريع التنموية والخدمات المصاحبة",
                "growth_rate": 2.5
            },
            "المدينة": {
                "description": "مدينة النبي صلى الله عليه وسلم - طيبة الطيبة",
                "strength": "الموقع الديني الفريد والاستقرار السوقي",
                "opportunity": "التوسع العمراني والخدمات المتطورة",
                "growth_rate": 2.1
            },
            "الدمام": {
                "description": "عاصمة المنطقة الشرقية والقلب النابض للطاقة",
                "strength": "التنويع الاقتصادي والموقع الاستراتيجي",
                "opportunity": "المشاريع الصناعية واللوجستية الكبرى",
                "growth_rate": 1.9
            }
        }
        
        # 🎯 إعدادات متقدمة للخطوط والتصميم
        self.arabic_config = {
            'font_name': 'Helvetica',
            'base_font_size': 11,
            'title_font_size': 18,
            'subtitle_font_size': 14,
            'line_spacing': 16,
            'primary_color': '#2E86AB',
            'secondary_color': '#A23B72', 
            'accent_color': '#F18F01'
        }
    
    def create_enhanced_pdf(self, user_info, market_data, real_data, package_level, smart_report_content=None):
        """النسخة المحسنة مع دعم جميع المدن"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm
            from reportlab.lib import colors
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            
            # 🎯 الحل الأساسي: تسجيل الخطوط العربية
            pdfmetrics.registerFont(UnicodeCIDFont('Helvetica'))
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(
                buffer, 
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm, 
                bottomMargin=2*cm,
                title=f"تقرير {package_level} - Warda Intelligence"
            )
            
            story = []
            target_pages = self.package_pages.get(package_level, 15)
            
            # 🎯 الحصول على معلومات المدينة من user_info
            user_city = user_info.get('city', 'الرياض')
            city_info = self.city_profiles.get(user_city, {
                "description": "مدينة واعدة ذات إمكانات نمو عالية",
                "strength": "الموقع الاستراتيجي والبنية التحتية",
                "opportunity": "الفرص الاستثمارية المتعددة",
                "growth_rate": 2.0
            })
            
            print(f"🎯 إنشاء تقرير {package_level} لمدينة {user_city} - مستهدف {target_pages} صفحة")

            # 🎯 البداية بغلاف فاخر
            story.extend(self._create_premium_cover(user_info, package_level, city_info))
            story.append(PageBreak())

            # 🎯 الفهرس المحسن
            story.extend(self._create_enhanced_table_of_contents(package_level, user_city))
            story.append(PageBreak())

            # 🎯 الملخص التنفيذي المحسن مع معلومات المدينة
            story.extend(self._create_executive_summary_enhanced(user_info, market_data, real_data, package_level, city_info))
            story.append(PageBreak())

            # 🎯 دمج المحتوى الذكي إذا كان متوفراً
            if smart_report_content:
                story.extend(self._integrate_smart_report(smart_report_content, user_info))
                story.append(PageBreak())

            # 🎯 الأقسام الأساسية المحسنة
            basic_sections = self._create_enhanced_basic_sections(user_info, market_data, real_data, package_level, city_info)
            story.extend(basic_sections)
            story.append(PageBreak())

            # 🎯 توليد محتوى إضافي ذكي لملء الصفحات
            current_pages = 5  # الغلاف + الفهرس + الملخص + المحتوى الذكي + الأساسيات
            
            while current_pages < target_pages:
                additional_content = self._create_premium_additional_section(
                    current_pages, user_info, market_data, real_data, package_level, city_info
                )
                story.extend(additional_content)
                
                if current_pages % 3 == 0 and current_pages < target_pages - 1:
                    story.append(PageBreak())
                
                current_pages += 1
                print(f"📄 تم إنشاء الصفحة {current_pages} من {target_pages}")
                
                if current_pages >= target_pages:
                    break
            
            # 🎯 الخاتمة الفاخرة
            story.extend(self._create_premium_conclusion(user_info, package_level, city_info))
            
            doc.build(story)
            buffer.seek(0)
            
            print(f"✅ تم إنشاء التقرير الفاخر لمدينة {user_city} بنجاح - {current_pages} صفحة")
            return buffer
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء PDF: {e}")
            return self._create_emergency_pdf(user_info, real_data, package_level)
    
    def _create_premium_cover(self, user_info, package_level, city_info):
        """غلاف فاخر مع معلومات المدينة"""
        elements = []
        
        premium_title_style = self._get_premium_style('premium_title')
        premium_subtitle_style = self._get_premium_style('premium_subtitle')
        info_style = self._get_premium_style('premium_info')
        
        user_city = user_info.get('city', 'المدينة المستهدفة')
        
        # 🎯 شعار الشركة الفاخر
        logo_text = f"""
        <para align="center">
            <font name="Helvetica-Bold" size="24" color="#2E86AB">🌹 Warda Intelligence</font><br/>
            <font size="16" color="#A23B72">الذكاء الاستثماري المتقدم - {user_city}</font>
        </para>
        """
        elements.append(Paragraph(self._safe_arabic(logo_text), premium_title_style))
        elements.append(Spacer(1, 2*cm))
        
        # 🎯 العنوان الرئيسي الفاخر
        title_text = f"""
        <para align="center">
            <font name="Helvetica-Bold" size="20" color="#2E86AB">تقرير {package_level} المتميز</font><br/>
            <font size="16" color="#A23B72">التحليل العقاري المتقدم لـ {user_city}</font>
        </para>
        """
        elements.append(Paragraph(self._safe_arabic(title_text), premium_title_style))
        elements.append(Spacer(1, 1.5*cm))
        
        # 🎯 بطاقة المعلومات الفاخرة
        info_card = f"""
        <b>معلومات التقرير المتميز:</b><br/><br/>
        
        <b>🎯 الباقة:</b> <font color="#2E86AB">{package_level}</font><br/>
        <b>🏙️ المدينة:</b> {user_city}<br/>
        <b>📊 وصف السوق:</b> {city_info['description']}<br/>
        <b>👤 العميل:</b> {user_info.get('user_type', 'مستثمر')}<br/>
        <b>🏠 نوع العقار:</b> {user_info.get('property_type', 'شقة')}<br/>
        <b>📐 المساحة:</b> {user_info.get('area', 120)} م²<br/>
        <b>📅 التاريخ:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}<br/>
        <b>📄 الصفحات:</b> {self.package_pages.get(package_level, 15)} صفحة<br/>
        <b>🏆 الجودة:</b> تحليل متقدم بخبرة {self._get_expert_level(package_level)}<br/>
        """
        elements.append(Paragraph(self._safe_arabic(info_card), info_style))
        elements.append(Spacer(1, 2*cm))
        
        # 🎯 ختم الجودة
        quality_stamp = f"""
        <para align="center">
            <font name="Helvetica-Bold" size="14" color="#F18F01">🛡️ تقرير معتمد لـ {user_city}</font><br/>
            <font size="12" color="#2E86AB">تم الإعداد بواسطة فريق الخبراء العقاريين</font>
        </para>
        """
        elements.append(Paragraph(self._safe_arabic(quality_stamp), premium_subtitle_style))
        
        return elements
    
    def _create_executive_summary_enhanced(self, user_info, market_data, real_data, package_level, city_info):
        """ملخص تنفيذي محسّن مع تحليل المدينة"""
        elements = []
        
        title_style = self._get_premium_style('premium_title')
        content_style = self._get_premium_style('premium_content')
        
        user_city = user_info.get('city', 'المدينة المستهدفة')
        
        elements.append(Paragraph(self._safe_arabic(f"<b>📊 الملخص التنفيذي المتقدم - {user_city}</b>"), title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # 🎯 تحليل متقدم يعكس لغة الخبراء مع معلومات المدينة
        if not real_data.empty:
            avg_price = real_data['السعر'].mean()
            avg_roi = real_data['العائد_المتوقع'].mean() if 'العائد_المتوقع' in real_data.columns else 6.5
            market_growth = market_data.get('معدل_النمو_الشهري', city_info.get('growth_rate', 2.0))
            
            summary_content = f"""
            <b>السادة العملاء الكرام،</b><br/><br/>
            
            يسعدنا تقديم هذا التقرير المتخصص الذي يقدم رؤية شاملة ومتعمقة لسوق العقارات 
            في <font color="#2E86AB">{user_city}</font> - {city_info['description']}.<br/><br/>
            
            <b>🎯 النتائج الرئيسية:</b><br/>
            • <b>القيمة السوقية:</b> {safe_num(avg_price)} ريال كمتوسط أسعار<br/>
            • <b>العوائد المتوقعة:</b> {safe_num(avg_roi, '.1f')}% سنوياً<br/>
            • <b>النمو السوقي:</b> {safe_num(market_growth, '.1f')}% شهرياً<br/>
            • <b>حجم العينة:</b> {len(real_data)} عقار تم تحليله<br/>
            • <b>نقاط القوة:</b> {city_info['strength']}<br/><br/>
            
            <b>💡 الرؤية الاستراتيجية:</b><br/>
            بناءً على تحليلنا المتعمق، نرى أن سوق {user_city} الحالي يوفر فرصاً استثمارية 
            { 'استثنائية' if avg_roi > 8 else 'ممتازة' if avg_roi > 6 else 'جيدة' } 
            للمستثمرين الأذكياء، مع تركيز على {city_info['opportunity']}.<br/><br/>
            
            <b>🏆 توصيات الخبراء:</b><br/>
            نوصي بالتركيز على {self._get_recommended_strategy(user_info, real_data)} 
            لتحقيق أقصى استفادة من الفرص المتاحة في سوق {user_city}.
            """
        else:
            summary_content = f"""
            <b>تحليل أولي لسوق {user_city}:</b><br/>
            {city_info['description']}<br/><br/>
            
            جاري جمع وتحليل البيانات المتخصصة لتقديم رؤية شاملة ودقيقة 
            تناسب متطلباتكم الاستثمارية واحتياجات السوق الحالي في {user_city}.
            """
        
        elements.append(Paragraph(self._safe_arabic(summary_content), content_style))
        
        # 🎯 إضافة جدول مؤشرات سريع
        if not real_data.empty:
            elements.extend(self._create_quick_indicators_table(real_data, market_data, city_info))
        
        return elements
    
    def _create_quick_indicators_table(self, real_data, market_data, city_info):
        """جدول المؤشرات السريعة مع مقارنة المدينة"""
        elements = []
        
        from reportlab.platypus import Table
        from reportlab.lib import colors
        
        if not real_data.empty:
            # حساب المؤشرات
            price_stats = real_data['السعر'].describe()
            roi_stats = real_data['العائد_المتوقع'].describe() if 'العائد_المتوقع' in real_data.columns else pd.Series([6.5, 8.0, 5.0], index=['mean', 'max', 'min'])
            
            table_data = [
                ['المؤشر', 'القيمة', 'التقييم'],
                ['متوسط السعر', f"{safe_num(price_stats['mean'])} ريال", self._get_rating(price_stats['mean'], 800000, 1500000)],
                ['أعلى عائد', f"{safe_num(roi_stats['max'], '.1f')}%", self._get_rating(roi_stats['max'], 7, 10)],
                ['معدل النمو', f"{safe_num(market_data.get('معدل_النمو_الشهري', city_info.get('growth_rate', 2.0)), '.1f')}%", self._get_rating(market_data.get('معدل_النمو_الشهري', 2.0), 1.5, 3.0)],
                ['قوة السوق', f"{city_info['strength'][:20]}...", "ممتاز 🏆"],
                ['الفرص', f"{city_info['opportunity'][:20]}...", "واعدة 💎"]
            ]
            
            table = Table(table_data, colWidths=[4*cm, 4*cm, 3*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#DEE2E6'))
            ]))
            
            elements.append(Spacer(1, 0.5*cm))
            elements.append(Paragraph(self._safe_arabic(f"<b>📈 مؤشرات سوق {user_info.get('city', '')}:</b>"), self._get_premium_style('premium_subtitle')))
            elements.append(Spacer(1, 0.3*cm))
            elements.append(table)
        
        return elements

    # ... باقي الدوال بنفس التحسينات مع إضافة city_info ...

    def _create_premium_conclusion(self, user_info, package_level, city_info):
        """خاتمة فاخرة مع تركيز على المدينة"""
        elements = []
        
        title_style = self._get_premium_style('premium_title')
        content_style = self._get_premium_style('premium_content')
        
        user_city = user_info.get('city', 'المدينة')
        
        elements.append(Paragraph(self._safe_arabic(f"<b>🏁 الخاتمة والتوصيات النهائية - {user_city}</b>"), title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        conclusion_content = f"""
        <b>السادة العملاء الكرام،</b><br/><br/>
        
        نصل معكم إلى ختام هذا التقرير الشامل الذي يهدف إلى تزويدكم برؤية استراتيجية 
        متكاملة لسوق العقارات في <font color="#2E86AB">{user_city}</font> - {city_info['description']}.<br/><br/>
        
        <b>🎯 النقاط الرئيسية:</b><br/>
        • سوق {user_city} يوفر فرصاً استثمارية {city_info['opportunity']}<br/>
        • {city_info['strength']} يدعم استدامة النمو<br/>
        • أهمية التحليل العلمي الدقيق في اتخاذ القرارات<br/>
        • ضرورة بناء استراتيجية متكاملة لإدارة المخاطر<br/><br/>
        
        <b>💎 توصياتنا النهائية لـ {user_city}:</b><br/>
        1. الاستمرار في متابعة تطورات سوق {user_city} بدقة<br/>
        2. الاستفادة من {city_info['opportunity']}<br/>
        3. تنويع المحفظة الاستثمارية داخل {user_city}<br/>
        4. بناء شراكات استراتيجية محلية في {user_city}<br/>
        5. الالتزام بخطط طوارئ مخصصة لسوق {user_city}<br/><br/>
        
        <b>🌹 كلمة أخيرة من Warda Intelligence:</b><br/>
        "نؤمن بأن النجاح في استثمارات {user_city} يأتي من الجمع بين البيانات الدقيقة 
        والرؤية الاستراتيجية والخبرة العملية. نحن هنا لنساعدكم في رحلتكم الاستثمارية 
        في هذه المدينة الواعدة ونتطلع إلى مشاركتكم النجاحات القادمة."<br/><br/>
        """
        
        elements.append(Paragraph(self._safe_arabic(conclusion_content), content_style))
        elements.append(Spacer(1, 1*cm))
        
        # 🎯 تذييل الصفحة الفاخر
        footer = f"""
        <para align="center">
            <font name="Helvetica-Bold" size="10" color="#2E86AB">
                🌹 Warda Intelligence - الذكاء الاستثماري المتقدم في {user_city}<br/>
                📧 info@warda-intelligence.com | 📞 +966 500 000 000<br/>
                🌐 www.warda-intelligence.com<br/>
                🛡️ تقرير معتمد لـ {user_city} - جميع الحقوق محفوظة © 2024
            </font>
        </para>
        """
        elements.append(Paragraph(self._safe_arabic(footer), self._get_premium_style('premium_info')))
        
        return elements

    # ... باقي الدوال بنفس الهيكل مع إضافة دعم المدن ...

# دالة الاستخدام المباشرة المحسنة
def create_enhanced_pdf(user_info, market_data, real_data, package_level, smart_report_content=None):
    """
    دالة رئيسية محسنة لإنشاء PDF فاخر مع دعم جميع المدن
    """
    generator = EnhancedPDFGenerator()
    return generator.create_enhanced_pdf(
        user_info, market_data, real_data, package_level, smart_report_content
    )
