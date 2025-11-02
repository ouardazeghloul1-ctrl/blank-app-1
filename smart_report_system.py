# smart_report_system.py - النظام الذكي للتقارير حسب الفئة والباقة
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from io import BytesIO
import arabic_reshaper
from bidi.algorithm import get_display
class SmartReportSystem:
    def __init__(self):
        self.user_profiles = {
            "مستثمر": self._investor_report,
            "وسيط عقاري": self._broker_report, 
            "شركة تطوير": self._developer_report,
            "فرد": self._individual_report,
            "باحث عن فرصة": self._opportunity_seeker_report,
            "مالك عقار": self._property_owner_report
        }
        
        self.package_features = {
            "مجانية": {"pages": 15, "analysis_depth": "basic", "charts": 3},
            "فضية": {"pages": 35, "analysis_depth": "advanced", "charts": 8},
            "ذهبية": {"pages": 60, "analysis_depth": "premium", "charts": 15},
            "ماسية": {"pages": 90, "analysis_depth": "vip", "charts": 25}
        }
    
    # 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽
    # 🔽 اضع الدوال الجديدة هنا - بعد __init__ وقبل دوال التقرير 🔽
    # 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽 🔽
    
    def _analyze_risks(self, real_data, market_data):
        """تحليل المخاطر"""
        if real_data.empty:
            return "لا توجد بيانات كافية لتحليل المخاطر"
        
        risk_counts = real_data['مستوى_الخطورة'].value_counts()
        return f"""
        • المخاطر المنخفضة: {risk_counts.get('منخفض', 0)} عقار
        • المخاطر المتوسطة: {risk_counts.get('متوسط', 0)} عقار
        • المخاطر المرتفعة: {risk_counts.get('مرتفع', 0)} عقار
        """

    def _find_investment_opportunities(self, real_data):
        """اكتشاف فرص الاستثمار"""
        if real_data.empty:
            return "لا توجد فرص استثمارية متاحة"
        
        best_opportunities = real_data.nlargest(3, 'العائد_المتوقع')
        result = ""
        for _, opp in best_opportunities.iterrows():
            result += f"• {opp['العقار']} - عائد {opp['العائد_المتوقع']}%\n"
        return result

    def _analyze_roi(self, real_data, market_data):
        """تحليل العوائد"""
        if real_data.empty:
            return "لا توجد بيانات لتحليل العوائد"
        
        avg_roi = real_data['العائد_المتوقع'].mean()
        return f"متوسط العوائد: {avg_roi:.1f}%"

    def _property_valuation(self, real_data, user_info):
        """تقييم العقار"""
        return "تحليل تقييم العقار المتقدم"

    def _optimal_selling_timing(self, market_data):
        """التوقيت الأمثل للبيع"""
        return "تحليل التوقيت الأمثل للبيع"

    def _value_improvement_tips(self, user_info, real_data):
        """نصائح تحسين القيمة"""
        return "نصائح متقدمة لتحسين قيمة العقار"

    def _find_suitable_living_areas(self, real_data, user_info):
        """البحث عن مناطق سكن مناسبة"""
        return "تحليل المناطق السكنية المناسبة"

    def _financing_analysis(self, user_info, market_data):
        """تحليل التمويل"""
        return "تحليل خيارات التمويل المتاحة"

    def _compare_housing_options(self, real_data):
        """مقارنة خيارات السكن"""
        return "مقارنة متقدمة بين خيارات السكن"
    
    # 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼
    # 🔼 انتهت الدوال الجديدة - هنا تبدأ دوال التقرير الأصلية 🔼
    # 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼 🔼
    
    def generate_smart_report(self, user_info, market_data, real_data, package_level):
        """إنشاء التقرير الذكي حسب الفئة والباقة"""
        user_type = user_info.get('user_type', 'مستثمر')
        report_generator = self.user_profiles.get(user_type, self._investor_report)
        
        return report_generator(user_info, market_data, real_data, package_level)
    
    def _investor_report(self, user_info, market_data, real_data, package_level):
        """تقرير المستثمر - يركز على العوائد والمخاطر"""
        # ... الكود الحالي يبقى كما هو ...
    def arabic_text(self, text):
        """تحويل النص العربي للعرض الصحيح"""
        return get_display(arabic_reshaper.reshape(str(text)))
    
    def generate_smart_report(self, user_info, market_data, real_data, package_level):
        """إنشاء التقرير الذكي حسب الفئة والباقة"""
        user_type = user_info.get('user_type', 'مستثمر')
        report_generator = self.user_profiles.get(user_type, self._investor_report)
        
        return report_generator(user_info, market_data, real_data, package_level)
    
    def generate_extended_report(self, user_info, market_data, real_data, package_level):
        """🆕 إنشاء تقرير موسع يملأ عدد الصفحات المطلوب"""
        user_type = user_info.get('user_type', 'مستثمر')
        target_pages = self.package_features.get(package_level, {}).get('pages', 15)
        
        # الحصول على المحتوى الأساسي
        basic_report = self.generate_smart_report(user_info, market_data, real_data, package_level)
        
        # الحصول على المحتوى الموسع
        extended_generator = self.extended_content.get(user_type, self._extended_investor_content)
        extended_content = extended_generator(user_info, market_data, real_data, package_level, target_pages)
        
        # دمج المحتوى
        full_report = basic_report + "\n\n" + extended_content
        return full_report
    
    def _investor_report(self, user_info, market_data, real_data, package_level):
        """تقرير المستثمر - يركز على العوائد والمخاطر"""
        report_content = {
            "title": "تقرير المستثمر الذكي - تحليل العوائد والمخاطر",
            "sections": []
        }
        
        # 📈 تحليل العوائد
        roi_analysis = self._analyze_roi(real_data, market_data)
        report_content["sections"].append({
            "title": "📊 تحليل العوائد الاستثمارية",
            "content": roi_analysis
        })
        
        # 🎯 فرص الاستثمار
        opportunities = self._find_investment_opportunities(real_data)
        report_content["sections"].append({
            "title": "🎯 أفضل فرص الاستثمار",
            "content": opportunities
        })
        
        # 📉 تحليل المخاطر
        risk_analysis = self._analyze_risks(real_data, market_data)
        report_content["sections"].append({
            "title": "🛡️ تحليل المخاطر",
            "content": risk_analysis
        })
        
        return self._format_report(report_content, package_level, "مستثمر")
    
    # 🆕 المحتوى الموسع للمستثمر
    def _extended_investor_content(self, user_info, market_data, real_data, package_level, target_pages):
        """محتوى موسع للمستثمر لملء الصفحات"""
        extended_sections = []
        
        # إضافة أقسام إضافية حسب الباقة
        if package_level in ["فضية", "ذهبية", "ماسية"]:
            extended_sections.extend([
                self._create_advanced_roi_analysis(real_data),
                self._create_market_trends_analysis(market_data),
                self._create_portfolio_strategy(user_info, real_data),
                self._create_financing_comparison()
            ])
        
        if package_level in ["ذهبية", "ماسية"]:
            extended_sections.extend([
                self._create_risk_management_plan(real_data),
                self._create_18month_forecast(market_data),
                self._create_competitor_analysis(real_data)
            ])
        
        if package_level == "ماسية":
            extended_sections.extend([
                self._create_international_comparison(),
                self._create_7year_investment_plan(user_info, market_data),
                self._create_advanced_analytics(real_data)
            ])
        
        # تنسيق المحتوى الموسع
        extended_content = "\n\n" + "="*60 + "\n"
        extended_content += "📚 المحتوى الموسع الإضافي\n"
        extended_content += "="*60 + "\n\n"
        
        for section in extended_sections:
            extended_content += section + "\n\n" + "-"*40 + "\n\n"
        
        return extended_content
    
    def _create_advanced_roi_analysis(self, real_data):
        """تحليل العوائد المتقدم"""
        if real_data.empty:
            return "📊 **تحليل العوائد المتقدم:**\nلا توجد بيانات كافية"
        
        # تحليل متقدم للعوائد
        roi_stats = real_data['العائد_المتوقع'].describe()
        high_roi_properties = real_data[real_data['العائد_المتوقع'] > real_data['العائد_المتوقع'].quantile(0.8)]
        
        analysis = f"""
        📊 **تحليل العوائد المتقدم:**
        
        📈 **الإحصائيات التفصيلية:**
        • المتوسط: {roi_stats['mean']:.1f}%
        • الوسيط: {roi_stats['50%']:.1f}%
        • أعلى 20%: {roi_stats['80%']:.1f}%
        • الانحراف المعياري: {roi_stats['std']:.1f}%
        
        🎯 **العقارات ذات أعلى عوائد ({len(high_roi_properties)} عقار):**
        """
        
        for _, prop in high_roi_properties.head(5).iterrows():
            analysis += f"• {prop['العقار']} - {prop['المنطقة']}: {prop['العائد_المتوقع']}%\n"
        
        return analysis
    
    def _create_market_trends_analysis(self, market_data):
        """تحليل اتجاهات السوق"""
        growth = market_data.get('معدل_النمو_الشهري', 2.5)
        liquidity = market_data.get('مؤشر_السيولة', 85)
        
        analysis = f"""
        📈 **تحليل اتجاهات السوق:**
        
        📊 **مؤشرات النمو:**
        • معدل النمو الشهري: {growth:.1f}%
        • النمو السنوي المتوقع: {(1 + growth/100)**12 - 1:.1%}
        • مؤشر السيولة: {liquidity:.0f}%
        
        🎯 **التوقعات:**
        • المدى القصير (3 أشهر): {'إيجابي' if growth > 2 else 'مستقر'}
        • المدى المتوسط (12 شهر): {'نمو قوي' if growth > 3 else 'نمو معتدل'}
        • السيولة: {'عالية' if liquidity > 80 else 'متوسطة'}
        """
        
        return analysis
    
    def _create_portfolio_strategy(self, user_info, real_data):
        """استراتيجية المحفظة الاستثمارية"""
        if real_data.empty:
            return "💼 **استراتيجية المحفظة:**\nلا توجد بيانات كافية"
        
        # تحليل التوزيع الأمثل
        area_diversity = real_data['المنطقة'].nunique()
        type_diversity = real_data['نوع_العقار'].nunique()
        
        strategy = f"""
        💼 **استراتيجية المحفظة الاستثمارية:**
        
        🎯 **التنويع الموصى به:**
        • التنويع الجغرافي: {min(area_diversity, 5)} مناطق مختلفة
        • التنويع النوعي: {min(type_diversity, 3)} أنواع عقارية
        • توزيع المخاطر: 60% منخفضة، 30% متوسطة، 10% مرتفعة
        
        📊 **التوزيع الأمثل:**
        • المناطق الرائدة: 40% من المحفظة
        • المناطق الناشئة: 30% من المحفظة  
        • المناطق المستقرة: 30% من المحفظة
        
        💡 **نصائح إدارة المحفظة:**
        • إعادة التوازن ربع سنوي
        • متابعة مؤشرات السوق شهرياً
        • الاحتفاظ بسيولة لفرص جديدة
        """
        
        return strategy
    
    # 🆕 أقسام إضافية للباقات الأعلى
    def _create_18month_forecast(self, market_data):
        """توقعات 18 شهراً"""
        current_growth = market_data.get('معدل_النمو_الشهري', 2.5)
        
        forecast = """
        🔮 **توقعات 18 شهراً القادمة:**
        
        📅 **الجداول الزمنية المتوقعة:**
        """
        
        months = [3, 6, 12, 18]
        for months_ahead in months:
            growth_factor = (1 + current_growth/100) ** months_ahead
            forecast += f"• بعد {months_ahead} شهر: +{(growth_factor-1)*100:.1f}%\n"
        
        forecast += """
        🎯 **الاستراتيجية المقترحة:**
        • الأشهر 1-6: التركيز على الصفقات سريعة التنفيذ
        • الأشهر 7-12: التوسع في المناطق الناشئة
        • الأشهر 13-18: تحسين وتنويع المحفظة
        """
        
        return forecast
    
    def _create_7year_investment_plan(self, user_info, market_data):
        """خطة استثمارية 7 سنوات"""
        plan = """
        🗓️ **خطة الاستثمار الاستراتيجية 7 سنوات:**
        
        📊 **مراحل الخطة:**
        
        **السنة 1-2: التأسيس**
        • بناء محفظة أساسية
        • التعلم من تجارب السوق
        • بناء شبكة العلاقات
        
        **السنة 3-4: التوسع**
        • تنويع المحفظة
        • الدخول في مشاريع تطوير
        • الاستفادة من الرافعة المالية
        
        **السنة 5-7: النضوج**
        • تحسين توزيع المحفظة
        • الاستعداد لدورات السوق
        • التخطيط للخروج الاستراتيجي
        
        💡 **أهداف الأداء:**
        • العوائد المستهدفة: 8-12% سنوياً
        • معدل النمو: 15-20% سنوياً
        • تحقيق التوزيع الجغرافي المستهدف
        """
        
        return plan

    # باقي الدوال الحالية تبقى كما هي...
    def _property_owner_report(self, user_info, market_data, real_data, package_level):
        """تقرير مالك العقار - يركز على تقييم القيمة والبيع"""
        report_content = {
            "title": "تقرير مالك العقار - تقييم القيمة والاستراتيجية",
            "sections": []
        }
        
        # 🏠 تقييم القيمة الحالية
        valuation = self._property_valuation(real_data, user_info)
        report_content["sections"].append({
            "title": "💰 تقييم قيمة العقار",
            "content": valuation
        })
        
        # ⏰ توقيت البيع الأمثل
        timing_analysis = self._optimal_selling_timing(market_data)
        report_content["sections"].append({
            "title": "⏰ التوقيت الأمثل للبيع",
            "content": timing_analysis
        })
        
        # 📈 تحسين القيمة
        value_improvement = self._value_improvement_tips(user_info, real_data)
        report_content["sections"].append({
            "title": "🔧 نصائح لتحسين القيمة",
            "content": value_improvement
        })
        
        return self._format_report(report_content, package_level, "مالك عقار")
    
    # 🆕 المحتوى الموسع لمالك العقار
    def _extended_owner_content(self, user_info, market_data, real_data, package_level, target_pages):
        """محتوى موسع لمالك العقار"""
        extended_sections = []
        
        extended_sections.extend([
            self._create_property_comparison(real_data, user_info),
            self._create_market_timing_analysis(market_data),
            self._create_value_enhancement_plan(user_info)
        ])
        
        if package_level in ["فضية", "ذهبية", "ماسية"]:
            extended_sections.extend([
                self._create_sales_strategy(),
                self._create_tax_optimization()
            ])
        
        # تنسيق المحتوى الموسع
        extended_content = "\n\n" + "="*60 + "\n"
        extended_content += "📚 المحتوى الموسع الإضافي\n"
        extended_content += "="*60 + "\n\n"
        
        for section in extended_sections:
            extended_content += section + "\n\n" + "-"*40 + "\n\n"
        
        return extended_content
    
    def _create_property_comparison(self, real_data, user_info):
        """مقارنة العقار مع المنافسين"""
        if real_data.empty:
            return "📊 **مقارنة العقار:**\nلا توجد بيانات كافية"
        
        user_city = user_info.get('city', 'الرياض')
        user_type = user_info.get('property_type', 'شقة')
        
        comparable = real_data[
            (real_data['المدينة'] == user_city) & 
            (real_data['نوع_العقار'] == user_type)
        ]
        
        if not comparable.empty:
            avg_price = comparable['السعر'].mean()
            avg_psm = comparable['سعر_المتر'].mean()
            
            comparison = f"""
            📊 **مقارنة العقار مع المنافسين:**
            
            🏘️ **السوق المحلي ({user_city} - {user_type}):**
            • متوسط أسعار السوق: {avg_price:,.0f} ريال
            • متوسط سعر المتر: {avg_psm:,.0f} ريال
            • عدد العقارات المنافسة: {len(comparable)} عقار
            
            📈 **مؤشرات التنافسية:**
            • نطاق الأسعار: {comparable['السعر'].min():,.0f} - {comparable['السعر'].max():,.0f} ريال
            • توزيع المناطق: {comparable['المنطقة'].nunique()} منطقة
            """
        else:
            comparison = "📊 **مقارنة العقار:**\nلا توجد عقارات مشابهة للمقارنة"
        
        return comparison

    # دوال الفئات الأخرى مع المحتوى الموسع...
    def _individual_report(self, user_info, market_data, real_data, package_level):
        """تقرير الفرد - يركز على السكن والتمويل"""
        report_content = {
            "title": "تقرير الباحث عن سكن - الخيارات والتمويل",
            "sections": []
        }
        
        # 🏡 مناطق مناسبة للسكن
        suitable_areas = self._find_suitable_living_areas(real_data, user_info)
        report_content["sections"].append({
            "title": "🏡 أفضل المناطق للسكن",
            "content": suitable_areas
        })
        
        # 💰 تحليل التمويل
        financing_analysis = self._financing_analysis(user_info, market_data)
        report_content["sections"].append({
            "title": "💰 تحليل خيارات التمويل",
            "content": financing_analysis
        })
        
        # 📊 مقارنة الخيارات
        options_comparison = self._compare_housing_options(real_data)
        report_content["sections"].append({
            "title": "📊 مقارنة الخيارات المتاحة",
            "content": options_comparison
        })
        
        return self._format_report(report_content, package_level, "فرد")
    
    def _extended_individual_content(self, user_info, market_data, real_data, package_level, target_pages):
        """محتوى موسع للفرد"""
        extended_sections = [
            self._create_neighborhood_analysis(real_data, user_info),
            self._create_lifestyle_comparison(),
            self._create_future_planning_guide()
        ]
        
        # تنسيق المحتوى الموسع
        extended_content = "\n\n" + "="*60 + "\n"
        extended_content += "📚 المحتوى الموسع الإضافي\n"
        extended_content += "="*60 + "\n\n"
        
        for section in extended_sections:
            extended_content += section + "\n\n" + "-"*40 + "\n\n"
        
        return extended_content

    # دوال الفئات الأخرى تبقى كما هي...
    def _broker_report(self, user_info, market_data, real_data, package_level):
        # الكود الحالي...
        pass
    
    def _developer_report(self, user_info, market_data, real_data, package_level):
        # الكود الحالي...
        pass
    
    def _opportunity_seeker_report(self, user_info, market_data, real_data, package_level):
        # الكود الحالي...
        pass
    
    # دوال المحتوى الموسع للفئات الأخرى...
    def _extended_broker_content(self, user_info, market_data, real_data, package_level, target_pages):
        pass
    
    def _extended_developer_content(self, user_info, market_data, real_data, package_level, target_pages):
        pass
    
    def _extended_opportunity_content(self, user_info, market_data, real_data, package_level, target_pages):
        pass

    # باقي الدوال المساعدة تبقى كما هي...
    def _analyze_roi(self, real_data, market_data):
        # الكود الحالي...
        pass
    
    def _find_investment_opportunities(self, real_data):
        # الكود الحالي...
        pass
    
    # ... جميع الدوال الأخرى تبقى كما هي

    def _format_report(self, report_content, package_level, user_type):
        """تنسيق التقرير النهائي"""
        package_info = self.package_features.get(package_level, self.package_features["مجانية"])
        
        formatted_report = f"""
        🎯 **تقرير {report_content['title']}**
        👤 **الفئة:** {user_type}
        💎 **الباقة:** {package_level}
        📄 **عدد الصفحات:** {package_info['pages']}
        📊 **عدد الرسوم البيانية:** {package_info['charts']}
        
        {'='*50}
        """
        
        for section in report_content['sections']:
            formatted_report += f"""
            {section['title']}
            {'-'*30}
            {section['content']}
            """
        
        formatted_report += f"""
        {'='*50}
        📅 **تم إنشاء التقرير في:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
        🏢 **Warda Intelligence** - شريكك في القرارات العقارية الذكية
        """
        
        return formatted_report

# اختبار النظام المحدث
if __name__ == "__main__":
    smart_system = SmartReportSystem()
    
    # بيانات تجريبية
    sample_user = {
        "user_type": "مستثمر",
        "city": "الرياض", 
        "property_type": "شقة",
        "area": 120
    }
    
    sample_market = {
        "معدل_النمو_الشهري": 2.5,
        "العائد_التأجيري": 7.8,
        "مؤشر_السيولة": 85
    }
    
    sample_data = pd.DataFrame({
        'العقار': ['شقة النخيل', 'فيلا الربوة', 'شقة العليا'],
        'المدينة': ['الرياض', 'الرياض', 'الرياض'],
        'المنطقة': ['النخيل', 'الربوة', 'العليا'],
        'نوع_العقار': ['شقة', 'فيلا', 'شقة'],
        'السعر': [850000, 2500000, 920000],
        'المساحة': [120, 350, 110],
        'سعر_المتر': [7083, 7142, 8363],
        'العائد_المتوقع': [8.5, 6.2, 9.1],
        'مستوى_الخطورة': ['منخفض', 'متوسط', 'منخفض']
    })
    
    # اختبار التقرير الموسع
    extended_report = smart_system.generate_extended_report(sample_user, sample_market, sample_data, "ذهبية")
    print("✅ تم إنشاء التقرير الذكي الموسع بنجاح!")
    print(f"📄 طول التقرير: {len(extended_report)} حرف")
    print(extended_report[:1000] + "...")  # عرض جزء من التقرير
