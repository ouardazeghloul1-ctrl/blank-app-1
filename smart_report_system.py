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
            "مالك عقار": self._property_owner_report, 
            "فرد": self._individual_report,
            "وسيط عقاري": self._broker_report,
            "شركة تطوير": self._developer_report,
            "باحث عن فرصة": self._opportunity_seeker_report
        }
        
        self.package_features = {
            "مجانية": {"pages": 15, "analysis_depth": "basic", "charts": 3},
            "فضية": {"pages": 35, "analysis_depth": "advanced", "charts": 8},
            "ذهبية": {"pages": 60, "analysis_depth": "premium", "charts": 15},
            "ماسية": {"pages": 90, "analysis_depth": "vip", "charts": 25}
        }
    
    def arabic_text(self, text):
        """تحويل النص العربي للعرض الصحيح"""
        return get_display(arabic_reshaper.reshape(str(text)))
    
    def generate_smart_report(self, user_info, market_data, real_data, package_level):
        """إنشاء التقرير الذكي حسب الفئة والباقة"""
        user_type = user_info.get('user_type', 'مستثمر')
        report_generator = self.user_profiles.get(user_type, self._investor_report)
        
        return report_generator(user_info, market_data, real_data, package_level)
    
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
    
    def _broker_report(self, user_info, market_data, real_data, package_level):
        """تقرير الوسيط العقاري"""
        report_content = {
            "title": "تقرير الوسيط العقاري - فرص السوق والمنافسة",
            "sections": []
        }
        
        # 🏢 تحليل المنافسين
        competition = self._analyze_competition(real_data)
        report_content["sections"].append({
            "title": "🏢 تحليل المنافسة في السوق",
            "content": competition
        })
        
        # 💼 فرص الوساطة
        brokerage_opportunities = self._find_brokerage_opportunities(real_data)
        report_content["sections"].append({
            "title": "💼 أفضل فرص الوساطة",
            "content": brokerage_opportunities
        })
        
        return self._format_report(report_content, package_level, "وسيط عقاري")
    
    def _developer_report(self, user_info, market_data, real_data, package_level):
        """تقرير شركة التطوير"""
        report_content = {
            "title": "تقرير شركة التطوير - دراسات الجدوى والفرص",
            "sections": []
        }
        
        # 📊 دراسة الجدوى
        feasibility = self._feasibility_analysis(real_data, user_info)
        report_content["sections"].append({
            "title": "📊 دراسة الجدوى الأولية",
            "content": feasibility
        })
        
        return self._format_report(report_content, package_level, "شركة تطوير")
    
    def _opportunity_seeker_report(self, user_info, market_data, real_data, package_level):
        """تقرير الباحث عن فرصة"""
        report_content = {
            "title": "تقرير الباحث عن فرصة - اكتشاف الفرص الاستثنائية",
            "sections": []
        }
        
        # 💎 فرص استثنائية
        exceptional_opportunities = self._find_exceptional_opportunities(real_data)
        report_content["sections"].append({
            "title": "💎 الفرص الاستثنائية",
            "content": exceptional_opportunities
        })
        
        return self._format_report(report_content, package_level, "باحث عن فرصة")
    
    def _analyze_roi(self, real_data, market_data):
        """تحليل العائد على الاستثمار"""
        if real_data.empty:
            return "لا توجد بيانات كافية لتحليل العوائد"
        
        avg_roi = real_data['العائد_المتوقع'].mean()
        max_roi = real_data['العائد_المتوقع'].max()
        min_roi = real_data['العائد_المتوقع'].min()
        
        analysis = f"""
        📈 **تحليل العوائد الاستثمارية:**
        
        • **متوسط العائد السنوي:** {avg_roi:.1f}%
        • **أعلى عائد متوقع:** {max_roi:.1f}%
        • **أقل عائد متوقع:** {min_roi:.1f}%
        
        💡 **التوصيات:**
        - العوائد بين {min_roi:.1f}% و {max_roi:.1f}% تعتبر تنافسية في السوق الحالي
        - التركيز على العقارات ذات عوائد فوق {avg_roi:.1f}% لتحقيق أرباح أعلى من المتوسط
        """
        
        return analysis
    
    def _find_investment_opportunities(self, real_data):
        """اكتشاف أفضل فرص الاستثمار"""
        if real_data.empty:
            return "لا توجد بيانات كافية لتحديد الفرص"
        
        # العثور على عقارات ذات عوائد عالية وأسعار معقولة
        high_return_properties = real_data[
            real_data['العائد_المتوقع'] > real_data['العائد_المتوقع'].mean()
        ].nlargest(5, 'العائد_المتوقع')
        
        opportunities = "🏆 **أفضل 5 فرص استثمارية:**\n\n"
        
        for idx, property in high_return_properties.iterrows():
            opportunities += f"""
            **{property['العقار']}**
            • المنطقة: {property['المنطقة']}
            • السعر: {property['السعر']:,.0f} ريال
            • العائد المتوقع: {property['العائد_المتوقع']}%
            • مستوى الخطورة: {property['مستوى_الخطورة']}
            """
        
        return opportunities
    
    def _property_valuation(self, real_data, user_info):
        """تقييم قيمة العقار"""
        user_area = user_info.get('area', 120)
        user_city = user_info.get('city', 'الرياض')
        property_type = user_info.get('property_type', 'شقة')
        
        # حساب متوسط سعر المتر في المنطقة
        city_data = real_data[real_data['المدينة'] == user_city]
        if not city_data.empty:
            avg_psm = city_data['سعر_المتر'].mean()
            estimated_value = avg_psm * user_area
            
            valuation = f"""
            🏠 **تقييم قيمة العقار:**
            
            • **المدينة:** {user_city}
            • **نوع العقار:** {property_type}
            • **المساحة:** {user_area} م²
            • **متوسط سعر المتر في المنطقة:** {avg_psm:,.0f} ريال/م²
            
            💰 **القيمة السوقية المقدرة:** {estimated_value:,.0f} ريال
            
            📊 **نطاق السعر العادل:** {estimated_value*0.9:,.0f} - {estimated_value*1.1:,.0f} ريال
            """
        else:
            valuation = "لا توجد بيانات كافية لتقييم العقار في هذه المدينة"
        
        return valuation
    
    def _find_suitable_living_areas(self, real_data, user_info):
        """العثور على مناطق مناسبة للسكن"""
        user_budget = user_info.get('area', 120) * 5000  # تقدير مبدئي
        
        suitable_areas = real_data[
            real_data['السعر'] <= user_budget * 1.2
        ].groupby('المنطقة').agg({
            'السعر': 'mean',
            'العائد_المتوقع': 'mean'
        }).round(2)
        
        if not suitable_areas.empty:
            analysis = "🏡 **المناطق المناسبة لميزانيتك:**\n\n"
            for area, data in suitable_areas.nlargest(5, 'العائد_المتوقع').iterrows():
                analysis += f"""
                **{area}**
                • متوسط السعر: {data['السعر']:,.0f} ريال
                • جودة الاستثمار: {'ممتازة' if data['العائد_المتوقع'] > 8 else 'جيدة'}
                """
        else:
            analysis = "🔍 نوصي بتعديل معايير البحث أو زيادة الميزانية قليلاً"
        
        return analysis
    
    def _analyze_competition(self, real_data):
        """تحليل المنافسة للوسيط العقاري"""
        if real_data.empty:
            return "لا توجد بيانات كافية لتحليل المنافسة"
        
        area_competition = real_data['المنطقة'].value_counts()
        analysis = "🏢 **تحليل المنافسة في المناطق:**\n\n"
        
        for area, count in area_competition.head(5).items():
            analysis += f"• **{area}**: {count} عقار متاح\n"
        
        analysis += f"\n💡 **إجمالي العقارات في السوق:** {len(real_data)} عقار"
        return analysis
    
    def _find_brokerage_opportunities(self, real_data):
        """اكتشاف فرص الوساطة"""
        if real_data.empty:
            return "لا توجد بيانات كافية لتحديد فرص الوساطة"
        
        # عقارات ذات أسعار تنافسية
        competitive_prices = real_data[
            real_data['سعر_المتر'] < real_data['سعر_المتر'].mean()
        ]
        
        opportunities = "💼 **أفضل فرص الوساطة:**\n\n"
        
        if not competitive_prices.empty:
            for _, prop in competitive_prices.head(3).iterrows():
                opportunities += f"""
                **{prop['العقار']}**
                • السعر: {prop['السعر']:,.0f} ريال
                • سعر المتر: {prop['سعر_المتر']:,.0f} ريال
                • ميزة تنافسية في التسعير
                """
        else:
            opportunities = "🔍 التركيز على التسويق الذكي والعروض المميزة"
        
        return opportunities
    
    def _feasibility_analysis(self, real_data, user_info):
        """دراسة الجدوى لشركات التطوير"""
        user_city = user_info.get('city', 'الرياض')
        property_type = user_info.get('property_type', 'شقة')
        
        city_data = real_data[real_data['المدينة'] == user_city]
        
        if not city_data.empty:
            avg_price = city_data['السعر'].mean()
            avg_roi = city_data['العائد_المتوقع'].mean()
            
            analysis = f"""
            📊 **دراسة الجدوى الأولية - {user_city}**
            
            • **متوسط أسعار السوق:** {avg_price:,.0f} ريال
            • **متوسط العوائد:** {avg_roi:.1f}%
            • **حجم السوق:** {len(city_data)} عقار
            • **نوع العقار:** {property_type}
            
            💡 **التوصية:** {'السوق واعد للاستثمار' if avg_roi > 7 else 'يحتاج دراسة متعمقة'}
            """
        else:
            analysis = "لا توجد بيانات كافية لدراسة الجدوى في هذه المدينة"
        
        return analysis
    
    def _find_exceptional_opportunities(self, real_data):
        """اكتشاف فرص استثنائية"""
        if real_data.empty:
            return "لا توجد بيانات كافية لاكتشاف الفرص"
        
        # عقارات ذات عوائد عالية جداً
        high_return = real_data[real_data['العائد_المتوقع'] > real_data['العائد_المتوقع'].quantile(0.8)]
        
        opportunities = "💎 **الفرص الاستثنائية:**\n\n"
        
        if not high_return.empty:
            for _, prop in high_return.head(3).iterrows():
                opportunities += f"""
                ⭐ **{prop['العقار']}**
                • العائد: {prop['العائد_المتوقع']}% 
                • المنطقة: {prop['المنطقة']}
                • فرصة نادرة بعائد مرتفع
                """
        else:
            opportunities = "🔍 ركز على العقارات ذات القيمة المضافة والتحسينات"
        
        return opportunities
    
    def _analyze_risks(self, real_data, market_data):
        """تحليل المخاطر"""
        if real_data.empty:
            return "لا توجد بيانات كافية لتحليل المخاطر"
        
        risk_distribution = real_data['مستوى_الخطورة'].value_counts()
        analysis = "🛡️ **تحليل توزيع المخاطر:**\n\n"
        
        for risk, count in risk_distribution.items():
            analysis += f"• **{risk}**: {count} عقار\n"
        
        return analysis
    
    def _optimal_selling_timing(self, market_data):
        """توقيت البيع الأمثل"""
        growth = market_data.get('معدل_النمو_الشهري', 0)
        
        if growth > 3:
            return "⏰ **التوقيت ممتاز للبيع** - السوق في ذروة النمو والأسعار مرتفعة"
        elif growth > 1.5:
            return "⏰ **التوقيت جيد للبيع** - استفد من استقرار السوق"
        else:
            return "⏰ **انتظر 3-6 أشهر** - السوق في مرحلة تصحيح"
    
    def _value_improvement_tips(self, user_info, real_data):
        """نصائح لتحسين قيمة العقار"""
        return """
        🔧 **نصائح لتحسين قيمة العقار:**
        
        • تجديد الواجهة الخارجية والداخلية
        • تحسين كفاءة الطاقة (عزل، نوافذ مزدوجة)
        • إضافة مرافق ترفيهية (جيم، مسابح)
        • تحسين الإضاءة والتهوية
        • الصيانة الدورية للأنظمة
        """
    
    def _financing_analysis(self, user_info, market_data):
        """تحليل خيارات التمويل"""
        return """
        💰 **خيارات التمويل المتاحة:**
        
        • **التمويل العقاري:** حتى 90% من قيمة العقار
        • **القروض الشخصية:** لتمويل التحسينات
        • **الشراكة الاستثمارية:** تقليل المخاطر
        • **التأجير التمويلي:** خيار مرن للشركات
        """
    
    def _compare_housing_options(self, real_data):
        """مقارنة خيارات السكن"""
        if real_data.empty:
            return "لا توجد بيانات للمقارنة"
        
        options = "📊 **مقارنة خيارات السكن:**\n\n"
        
        # تحليل حسب نوع العقار
        property_analysis = real_data.groupby('نوع_العقار').agg({
            'السعر': 'mean',
            'العائد_المتوقع': 'mean'
        }).round(2)
        
        for prop_type, data in property_analysis.iterrows():
            options += f"• **{prop_type}**: {data['السعر']:,.0f} ريال - عائد {data['العائد_المتوقع']}%\n"
        
        return options
    
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

# اختبار النظام
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
        "العائد_التأجيري": 7.8
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
    
    report = smart_system.generate_smart_report(sample_user, sample_market, sample_data, "فضية")
    print("✅ تم إنشاء التقرير الذكي بنجاح!")
    print(report)
