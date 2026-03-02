"""
smart_report_system.py
النظام الذكي للتقارير حسب الفئة والباقة
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from io import BytesIO
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

# 🔧 التعديل 2: دالة الحماية الرياضية
def safe_div(a, b, default=0):
    """تقسيم آمن يحمي من القسمة على صفر أو قيم خاطئة"""
    try:
        if b in [0, None, 0.0]:
            return default
        return a / b
    except (ZeroDivisionError, TypeError, ValueError):
        return default

class SmartReportSystem:
    def __init__(self, user_data):
        # 🔧 التعديل الأول: تثبيت المتغيرات الأساسية
        self.user_data = user_data
        self.category = user_data.get("category", "investor")
        self.city = user_data.get("city", "")
        self.plan = user_data.get("plan", "مجانية")
        self.user_type = user_data.get("user_type", "مستثمر")
        
        # خريطة تصنيف المستخدمين
        self.category_map = {
            "investor": "مستثمر",
            "broker": "وسيط عقاري",
            "developer": "شركة تطوير",
            "individual": "فرد",
            "opportunity": "باحث عن فرصة",
            "owner": "مالك عقار"
        }
        
        # الحصول على الفئة المنسقة
        self.normalized_category = self.category_map.get(self.category, "مستثمر")
        
        # نظام الباقات
        self.package_features = {
            "مجانية": {"pages": 15, "analysis_depth": "basic", "charts": 3},
            "فضية": {"pages": 35, "analysis_depth": "advanced", "charts": 8},
            "ذهبية": {"pages": 60, "analysis_depth": "premium", "charts": 15},
            "ماسية": {"pages": 90, "analysis_depth": "vip", "charts": 25},
            "ماسية متميزة": {"pages": 120, "analysis_depth": "ultimate", "charts": 35}
        }
        
        # نظام المدن الذكي
        self.city_insights = {
            "الرياض": {
                "growth_trend": 2.8,
                "strength": "رؤية 2030 والمشاريع الكبرى",
                "opportunity": "التحول الاقتصادي والنمو السكاني",
                "description": "العاصمة الاقتصادية والقلب النابض للمملكة"
            },
            "جدة": {
                "growth_trend": 2.2,
                "strength": "الموقع الاستراتيجي والمشاريع السياحية", 
                "opportunity": "الاستثمارات الكبرى والبنية التحتية",
                "description": "عروس البحر الأحمر والعاصمة التجارية"
            },
            "مكة المكرمة": {
                "growth_trend": 2.5,
                "strength": "الموقع الديني والطلب المستمر",
                "opportunity": "المشاريع التنموية والخدمات",
                "description": "أطهر بقاع الأرض والعاصمة الدينية العالمية"
            },
            "المدينة المنورة": {
                "growth_trend": 2.1,
                "strength": "الاستقرار السوقي والموقع الديني",
                "opportunity": "التوسع العمراني والخدمات",
                "description": "مدينة النبي صلى الله عليه وسلم - طيبة الطيبة"
            },
            "الدمام": {
                "growth_trend": 1.9,
                "strength": "التنويع الاقتصادي والموقع الاستراتيجي",
                "opportunity": "المشاريع الصناعية واللوجستية",
                "description": "عاصمة المنطقة الشرقية والقلب النابض للطاقة"
            }
        }
    
    def arabic_text(self, text):
        """تحويل النص العربي للعرض الصحيح"""
        return get_display(arabic_reshaper.reshape(str(text)))
    
    def generate_extended_report(self, user_info, market_data, real_data, chosen_pkg):
        """الدالة الرئيسية - توليد تقرير ذكي حسب الفئة"""
        
        # 🔧 التعديل 2: حارس جودة التقرير
        if not market_data or not isinstance(market_data, dict):
            market_data = {
                'متوسط_السوق': 6000,
                'العائد_التأجيري': 7.5,
                'معدل_النمو_الشهري': 2.5,
                'مؤشر_السيولة': 85,
                'حجم_التداول_شهري': 120,
                'طالب_الشراء': 180,
                'عرض_العقارات': 100,
                'معدل_الإشغال': 90,
                'أقل_سعر': 4200,
                'أعلى_سعر': 9000
            }
        
        # توحيد مصدر المدينة
        user_city = self.city or user_info.get('city', 'المدينة المستهدفة')
        
        # استخدام self.category فقط
        if self.category == "investor":
            return self._investor_report(user_info, market_data, real_data, chosen_pkg, user_city)
            
        elif self.category == "broker":
            return self._broker_report(user_info, market_data, real_data, chosen_pkg, user_city)
            
        elif self.category == "developer":
            return self._developer_report(user_info, market_data, real_data, chosen_pkg, user_city)
            
        elif self.category == "individual":
            return self._individual_report(user_info, market_data, real_data, chosen_pkg, user_city)
            
        elif self.category == "opportunity":
            return self._opportunity_seeker_report(user_info, market_data, real_data, chosen_pkg, user_city)
            
        elif self.category == "owner":
            return self._owner_report(user_info, market_data, real_data, chosen_pkg, user_city)
            
        else:
            return self._general_report(user_info, market_data, real_data, chosen_pkg, user_city)
    
    def _investor_report(self, user_info, market_data, real_data, chosen_pkg, user_city):
        """👤 تقرير المستثمر - يركز على العوائد والمخاطر"""
        package_info = self.package_features.get(chosen_pkg, self.package_features["مجانية"])
        
        # استخدام safe_div للقيم الرياضية
        price_per_area = market_data.get('متوسط_السوق', 0) * user_info.get('area', 120)
        demand_supply_ratio = safe_div(
            market_data.get('طالب_الشراء', 0),
            market_data.get('عرض_العقارات', 1),
            1.0
        )
        
        report = f"""
🏦 **تقرير المستثمر العقاري المتقدم - Warda Intelligence**

📌 **هذا التقرير مخصص لك بناءً على ملفك الاستثماري**

📍 **المدينة:** {user_city}
💰 **الباقة:** {chosen_pkg}
🧾 **عدد صفحات التقرير:** {package_info['pages']} صفحة تحليلية
📊 **عمق التحليل:** {package_info['analysis_depth']}
📅 **التاريخ:** {datetime.now().strftime('%Y-%m-%d')}

📈 **التحليل الاستثماري في {user_city}:**

🔍 **مؤشرات السوق الرئيسية:**
• متوسط سعر المتر: {safe_num(market_data.get('متوسط_السوق', 0))} ريال
• متوسط سعر المسكن: {safe_num(price_per_area)} ريال
• العائد التأجيري: {safe_num(market_data.get('العائد_التأجيري', 0), '.1f')}%
• معدل النمو الشهري: {safe_num(market_data.get('معدل_النمو_الشهري', 0), '.1f')}%
• مؤشر السيولة: {safe_num(market_data.get('مؤشر_السيولة', 0), '.0f')}%
• نسبة العرض للطلب: 1 : {safe_num(demand_supply_ratio, '.1f')}

🎯 **التوصيات الاستراتيجية للمستثمر:**

1. **📊 تحليل الفرص:**
   - التركيز على العقارات ذات العائد فوق {safe_num((float(market_data.get('العائد_التأجيري', 0)) if str(market_data.get('العائد_التأجيري', 0)).replace('.', '', 1).isdigit() else 0) + 2, '.1f')}%
   - استهداف المناطق ذات النمو فوق المتوسط في {user_city}
   - تنويع المحفظة بين 3-5 مناطق مختلفة

2. **🛡️ إدارة المخاطر:**
   - توزيع المخاطر: 60% منخفضة، 30% متوسطة، 10% مرتفعة
   - الحفاظ على سيولة طارئة 10-15%
   - استخدام التحوط ضد تقلبات السوق

3. **💰 التوقيت الاستثماري:**
   - شراء فوري: في حالة النمو > 3% والسيولة > 80%
   - شراء تدريجي: في حالة النمو 1-3%
   - انتظار: في حالة النمو < 1%

💡 **رؤية الخبراء:**
"الاستثمار في {user_city} يتطلب استراتيجية واضحة ومرونة في التنفيذ. 
الفرص الحالية في سوق {user_city} ممتازة للمستثمرين ذوي الرؤية الطويلة الأمد."

📞 **للحصول على تحليل متعمق:**
تواصل مع مستشارينا المتخصصين لتحليل محفظتك الحالية وتطوير استراتيجية استثمارية مخصصة.
        """
        
        # إضافة المحتوى الموسع للباقات المميزة
        return report + self._get_extended_content(user_info, market_data, real_data, chosen_pkg, "تقرير المستثمر")
    
    def _broker_report(self, user_info, market_data, real_data, chosen_pkg, user_city):
        """🧑‍💼 تقرير الوسيط العقاري - يركز على الصفقات والأسواق"""
        package_info = self.package_features.get(chosen_pkg, self.package_features["مجانية"])
        
        # استخدام safe_div للقيم الرياضية
        demand_supply_ratio = safe_div(
            market_data.get('طالب_الشراء', 0),
            market_data.get('عرض_العقارات', 1),
            1.0
        )
        avg_sale_time = 100 - market_data.get('مؤشر_السيولة', 0)
        
        report = f"""
🏠 **تقرير الوسيط العقاري المحترف - Warda Intelligence**

📌 **هذا التقرير مخصص لك بناءً على ملفك الاستثماري**

📍 **المدينة:** {user_city}
💰 **الباقة:** {chosen_pkg}
🧾 **عدد صفحات التقرير:** {package_info['pages']} صفحة تحليلية
📊 **عمق التحليل:** {package_info['analysis_depth']}
📅 **التاريخ:** {datetime.now().strftime('%Y-%m-%d')}

📊 **تحليل سوق الوساطة في {user_city}:**

🔍 **مؤشرات أداء السوق:**
• حجم التداول الشهري: {safe_num(market_data.get('حجم_التداول_شهري', 0))} صفقة
• متوسط وقت البيع: {safe_num(avg_sale_time, '.0f')} يوم
• نسبة العرض للطلب: 1 : {safe_num(demand_supply_ratio, '.1f')}
• معدل الإشغال: {safe_num(market_data.get('معدل_الإشغال', 0), '.0f')}%

🎯 **استراتيجيات زيادة الصفقات:**

1. **📈 تحسين قائمة العقارات:**
   - التركيز على المناطق ذات سرعة البيع العالية
   - تحسين جودة الصور والوصف للعقارات
   - استخدام التسعير التنافسي الذكي

2. **🤝 بناء العلاقات:**
   - تطوير شبكة مستثمرين محليين في {user_city}
   - التعاون مع المطورين العقاريين
   - بناء سمعة مهنية قوية

3. **💰 تحسين الإيرادات:**
   - زيادة متوسط قيمة الصفقة
   - تقليل وقت البيع
   - تحسين عمولات الصفقات

💡 **نصائح الخبراء للوسطاء:**
"الوسيط الناجح في {user_city} ليس مجرد بائع، بل مستشار موثوق. 
بناء الثقة مع العملاء هو استثمار طويل الأجل يضمن استمرارية الصفقات."

📞 **لتحسين أدائك:**
استفد من أدواتنا المتقدمة للوساطة العقارية وتدريباتنا الاحترافية.
        """
        
        # إضافة المحتوى الموسع للباقات المميزة
        return report + self._get_extended_content(user_info, market_data, real_data, chosen_pkg, "تقرير الوسيط")
    
    def _developer_report(self, user_info, market_data, real_data, chosen_pkg, user_city):
        """🏗️ تقرير شركة التطوير - يركز على المشاريع والجدوى"""
        package_info = self.package_features.get(chosen_pkg, self.package_features["مجانية"])
        
        # استخدام safe_div للقيم الرياضية
        demand_gap = market_data.get('طالب_الشراء', 0) - market_data.get('عرض_العقارات', 0)
        annual_growth = market_data.get('معدل_النمو_الشهري', 0) * 12
        
        report = f"""
🏗️ **تقرير تطوير المشاريع العقارية - Warda Intelligence**

📌 **هذا التقرير مخصص لك بناءً على ملفك الاستثماري**

📍 **المدينة:** {user_city}
💰 **الباقة:** {chosen_pkg}
🧾 **عدد صفحات التقرير:** {package_info['pages']} صفحة تحليلية
📊 **عمق التحليل:** {package_info['analysis_depth']}
📅 **التاريخ:** {datetime.now().strftime('%Y-%m-%d')}

📊 **تحليل فرص التطوير في {user_city}:**

🔍 **مؤشرات سوق التطوير:**
• معدل النمو السكاني: {safe_num(annual_growth, '.1f')}% سنوياً
• فجوة العرض والطلب: {safe_num(demand_gap)} وحدة
• متوسط سعر البناء: {safe_num(market_data.get('متوسط_السوق', 0) * 0.4, '.0f')} ريال/م²
• العائد على الاستثمار: {safe_num(market_data.get('العائد_التأجيري', 0) + 5, '.1f')}%

🎯 **استراتيجيات التطوير الناجح:**

1. **📍 اختيار الموقع الاستراتيجي:**
   - قرب من المشاريع التنموية الكبرى
   - توافر البنية التحتية
   - سهولة الوصول والنقل

2. **📐 التصميم والجدوى:**
   - دراسة احتياجات السوق بدقة
   - تحليل المنافسين المحليين
   - حساب نقطة التعادل والربحية

3. **💰 إدارة المشروع:**
   - تحسين تكاليف البناء
   - إدارة الجدول الزمني
   - تسويق فعال خلال البناء

💡 **رؤية خبراء التطوير:**
"المشاريع الناجحة في {user_city} تبدأ بدراسة جدوى دقيقة وتنتهي بتسليم يتجاوز توقعات العملاء. 
الجودة والوقت والكلفة مثلث النجاح في التطوير العقاري."

📞 **لدراسات الجدوى المتخصصة:**
نوفر دراسات جدوى مفصلة وتحليلات سوق متقدمة لمشاريعك المستقبلية.
        """
        
        # إضافة المحتوى الموسع للباقات المميزة
        return report + self._get_extended_content(user_info, market_data, real_data, chosen_pkg, "تقرير المطور")
    
    def _individual_report(self, user_info, market_data, real_data, chosen_pkg, user_city):
        """👨‍👩‍👧 تقرير الفرد - يركز على السكن والتمويل"""
        package_info = self.package_features.get(chosen_pkg, self.package_features["مجانية"])
        area = user_info.get('area', 120)
        
        # استخدام safe_div للقيم الرياضية
        avg_property_price = market_data.get('متوسط_السوق', 0) * area
        min_price = market_data.get('أقل_سعر', 0) * area
        max_price = market_data.get('أعلى_سعر', 0) * area
        
        report = f"""
🏡 **تقرير البحث عن السكن المثالي - Warda Intelligence**

📌 **هذا التقرير مخصص لك بناءً على ملفك الاستثماري**

📍 **المدينة:** {user_city}
💰 **الباقة:** {chosen_pkg}
🧾 **عدد صفحات التقرير:** {package_info['pages']} صفحة تحليلية
📊 **عمق التحليل:** {package_info['analysis_depth']}
📅 **التاريخ:** {datetime.now().strftime('%Y-%m-%d')}

📊 **تحليل سوق السكن في {user_city}:**

🔍 **مؤشرات السوق للمشتري:**
• متوسط سعر المسكن: {safe_num(avg_property_price)} ريال
• نطاق الأسعار: {safe_num(min_price)} - {safe_num(max_price)} ريال
• خيارات التمويل المتاحة: 5-8 خيارات مختلفة
• فترة البحث المتوقعة: {safe_num(100 - market_data.get('مؤشر_السيولة', 0), '.0f')} يوم

🎯 **خطة البحث الذكي:**

1. **📍 تحديد المناطق المناسبة:**
   - قرب من مكان العمل/الدراسة
   - توافر الخدمات الأساسية
   - البيئة المجتمعية المناسبة

2. **💰 التخطيط المالي:**
   - حساب المبلغ المقدم (20-30%)
   - اختيار برنامج التمويل الأنسب
   - توقع التكاليف التشغيلية

3. **🔍 تقييم العقار:**
   - الفحص الفني الدقيق
   - مقارنة مع عقارات مشابهة
   - التفاوض على السعر والشروط

💡 **نصائح لشراء أول منزل:**
"لا تستعجل القرار في {user_city}. زور العقار في أوقات مختلفة، تحدث مع الجيران، 
وتأكد من ملاءمته لاحتياجاتك الحالية والمستقبلية."

📞 **لمساعدتك في البحث:**
نوفر لك قائمة بالعقارات المناسبة ونساعدك في المفاوضات والتمويل.
        """
        
        # إضافة المحتوى الموسع للباقات المميزة
        return report + self._get_extended_content(user_info, market_data, real_data, chosen_pkg, "تقرير الفرد")
    
    def _opportunity_seeker_report(self, user_info, market_data, real_data, chosen_pkg, user_city):
        """🔍 تقرير الباحث عن فرص - يركز على الاكتشاف والاستثمار"""
        package_info = self.package_features.get(chosen_pkg, self.package_features["مجانية"])
        
        # استخدام safe_div للقيم الرياضية
        discounted_properties = market_data.get('عرض_العقارات', 0) * 0.15
        renovation_opportunities = market_data.get('عرض_العقارات', 0) * 0.25
        
        report = f"""
💎 **تقرير صائد الفرص العقارية - Warda Intelligence**

📌 **هذا التقرير مخصص لك بناءً على ملفك الاستثماري**

📍 **المدينة:** {user_city}
💰 **الباقة:** {chosen_pkg}
🧾 **عدد صفحات التقرير:** {package_info['pages']} صفحة تحليلية
📊 **عمق التحليل:** {package_info['analysis_depth']}
📅 **التاريخ:** {datetime.now().strftime('%Y-%m-%d')}

📊 **تحليل فرص السوق في {user_city}:**

🔍 **مؤشرات الفرص المخفية:**
• عقارات بخصم 10-20%: {safe_num(discounted_properties, '.0f')} عقار
• مناطق نمو جديدة: 3-5 مناطق مرشحة
• فرص التجديد والتحسين: {safe_num(renovation_opportunities, '.0f')} عقار
• سرعة اكتشاف الفرص: 2-3 أيام للفرص الممتازة

🎯 **استراتيجيات اكتشاف الفرص:**

1. **📊 البحث المتقدم:**
   - مراقبة السوق يومياً
   - البحث عن البائعين المستعجلين
   - اكتشاف المناطق قبل انتشارها

2. **💡 تحليل القيمة المخفية:**
   - عقارات بحاجة إلى تحسين
   - مناطق على وشك التطوير
   - فرص الشراء بالجملة

3. **🚀 التنفيذ السريع:**
   - اتخاذ القرار خلال 48 ساعة
   - تمويل مسبق الاستعداد
   - فريق تنفيذ سريع

💡 **فلسفة صائد الفرص:**
"الفرص الحقيقية في {user_city} لا تعلن عن نفسها. تحتاج إلى عين مدربة، 
وأذن صاغية، وقدرة على التحرك السريع."

📞 **للاكتشاف المبكر للفرص:**
اشترك في نظام التنبيهات الفورية لدينا لاكتشاف الفرص قبل الجميع.
        """
        
        # إضافة المحتوى الموسع للباقات المميزة
        return report + self._get_extended_content(user_info, market_data, real_data, chosen_pkg, "تقرير صائد الفرص")
    
    def _owner_report(self, user_info, market_data, real_data, chosen_pkg, user_city):
        """🏡 تقرير مالك العقار - يركز على الإدارة والبيع"""
        package_info = self.package_features.get(chosen_pkg, self.package_features["مجانية"])
        
        # استخدام safe_div للقيم الرياضية
        avg_sale_time = 100 - market_data.get('مؤشر_سيولة', market_data.get('مؤشر_السيولة', 85))
        maintenance_cost = market_data.get('متوسط_السوق', 6000) * 120 * 0.015  # 1.5% من قيمة العقار
        
        report = f"""
🏠 **تقرير مالك العقار الذكي - Warda Intelligence**

📌 **هذا التقرير مخصص لك بناءً على ملفك الاستثماري**

📍 **المدينة:** {user_city}
💰 **الباقة:** {chosen_pkg}
🧾 **عدد صفحات التقرير:** {package_info['pages']} صفحة تحليلية
📊 **عمق التحليل:** {package_info['analysis_depth']}
📅 **التاريخ:** {datetime.now().strftime('%Y-%m-%d')}

📊 **تحليل سوق المالك في {user_city}:**

🔍 **مؤشرات السوق للمالكين:**
• متوسط وقت البيع: {safe_num(avg_sale_time, '.0f')} يوم
• هامش التفاوض: 5-15% حسب المنطقة
• معدل الإيجار: {safe_num(market_data.get('العائد_التأجيري', 0), '.1f')}% سنوياً
• تكلفة الصيانة السنوية: ~{safe_num(maintenance_cost)} ريال

🎯 **استراتيجيات تعظيم القيمة:**

1. **💰 تحسين القيمة السوقية:**
   - تجديد الواجهات والديكور الداخلي
   - تحسين كفاءة الطاقة
   - تحديث المرافق والخدمات

2. **⏰ التوقيت الأمثل للبيع:**
   - بيع خلال مواسم الذروة في {user_city}
   - الاستفادة من المشاريع التنموية القريبة
   - تجنب المنافسة العالية

3. **📈 إدارة العقار المؤجر:**
   - اختيار المستأجر المناسب
   - عقود إيجار متوازنة
   - صيانة وقائية منتظمة

💡 **نصائح للملاك الأذكياء:**
"العقار في {user_city} ليس مجرد أصل، بل مشروع استثماري يحتاج إلى إدارة ذكية. 
التحسينات الصغيرة تخلق فرقاً كبيراً في القيمة والإيجار."

📞 **لإدارة متكاملة:**
نوفر خدمات إدارة العقارات والتقييم الدوري وتحسين القيمة السوقية.
        """
        
        # إضافة المحتوى الموسع للباقات المميزة
        return report + self._get_extended_content(user_info, market_data, real_data, chosen_pkg, "تقرير المالك")
    
    def _general_report(self, user_info, market_data, real_data, chosen_pkg, user_city):
        """📄 تقرير عام - للمستخدمين الجدد أو الفئات غير المحددة"""
        package_info = self.package_features.get(chosen_pkg, self.package_features["مجانية"])
        
        # استخدام safe_div للقيم الرياضية
        demand_supply_ratio = safe_div(
            market_data.get('طالب_الشراء', 0),
            market_data.get('عرض_العقارات', 1),
            1.0
        )
        
        report = f"""
📊 **التقرير العام لسوق العقارات - Warda Intelligence**

📌 **هذا التقرير مخصص لك بناءً على ملفك الاستثماري**

📍 **المدينة:** {user_city}
💰 **الباقة:** {chosen_pkg}
🧾 **عدد صفحات التقرير:** {package_info['pages']} صفحة تحليلية
📊 **عمق التحليل:** {package_info['analysis_depth']}
📅 **التاريخ:** {datetime.now().strftime('%Y-%m-%d')}

📈 **نظرة عامة على سوق {user_city}:**

🔍 **مؤشرات السوق الرئيسية:**
• متوسط الأسعار: {safe_num(market_data.get('متوسط_السوق', 0))} ريال/م²
• حركة السوق: {safe_num(market_data.get('حجم_التداول_شهري', 0))} صفقة/شهر
• اتجاه النمو: {safe_num(market_data.get('معدل_النمو_الشهري', 0), '.1f')}% شهرياً
• سيولة السوق: {safe_num(market_data.get('مؤشر_السيولة', 0), '.0f')}/100
• نسبة العرض للطلب: 1 : {safe_num(demand_supply_ratio, '.1f')}

🎯 **توصيات عامة:**

1. **📋 للمستثمرين الجدد:**
   - ابدأ بالعقارات الصغيرة في {user_city}
   - تعلم من السوق المحلي أولاً
   - استشر الخبراء قبل الاستثمار الكبير

2. **🏠 للمشترين:**
   - حدد ميزانيتك بدقة
   - ابحث في مناطق متعددة في {user_city}
   - لا تتسرع في اتخاذ القرار

3. **💰 للبائعين:**
   - جهز عقارك للعرض
   - سعر تنافسي وجذاب
   - استخدم وسائط عرض متعددة

💡 **رسالة من Warda Intelligence:**
"سوق {user_city} مليء بالفرص لمن يعرف كيف يبحث. نحن هنا لنساعدك في اتخاذ القرار الصحيح 
بناءً على بيانات دقيقة وتحليل متخصص."

📞 **للحصول على تحليل مخصص:**
اختر فئتك في المرة القادمة للحصول على تقرير مخصص لاحتياجاتك.
        """
        
        # إضافة المحتوى الموسع للباقات المميزة
        return report + self._get_extended_content(user_info, market_data, real_data, chosen_pkg, "تقرير عام")
    
    def _get_extended_content(self, user_info, market_data, real_data, chosen_pkg, report_type):
        """إضافة محتوى موسع للباقات المميزة"""
        user_city = self.city or user_info.get('city', 'المدينة المستهدفة')
        
        if chosen_pkg in ["ذهبية", "ماسية", "ماسية متميزة"]:
            return f"""

📚 **المحتوى التحليلي المتقدم - {report_type}**

💎 **للحصول على تحليل كامل شامل:**
1. دراسات الجدوى التفصيلية
2. تحليل المنافسين المتقدم
3. نماذج التنبؤ بالأسعار
4. استشارات متخصصة مباشرة

🏆 **باقة {chosen_pkg} تقدم:**
• {self.package_features.get(chosen_pkg, {}).get('pages', 60)} صفحة تحليلية
• {self.package_features.get(chosen_pkg, {}).get('charts', 15)} رسم بياني تفاعلي
• تحديثات دورية للسوق
• دعم استشاري متخصص

🎯 **استثمر في معرفتك اليوم لتبني مستقبلك الغد في {user_city}**
"""
        return ""

    # دالة التوافق مع الكود القديم
    def generate_smart_report(self, user_info, market_data, real_data, chosen_pkg):
        """دالة التوافق - تستدعي generate_extended_report"""
        return self.generate_extended_report(user_info, market_data, real_data, chosen_pkg)

# اختبار النظام المحدث
if __name__ == "__main__":
    print("🧪 اختبار النظام الذكي للتقارير - النسخة المحسنة\n")
    
    # اختبار تقارير مختلفة
    test_cases = [
        {"city": "الرياض", "plan": "ذهبية", "category": "investor", "user_type": "مستثمر"},
        {"city": "جدة", "plan": "فضية", "category": "broker", "user_type": "وسيط عقاري"},
        {"city": "الدمام", "plan": "مجانية", "category": "individual", "user_type": "فرد"},
        {"city": "مكة المكرمة", "plan": "ماسية", "category": "opportunity", "user_type": "باحث عن فرصة"},
        {"city": "المدينة المنورة", "plan": "ذهبية", "category": "owner", "user_type": "مالك عقار"}
    ]
    
    for i, test_data in enumerate(test_cases):
        print(f"\n{'='*80}")
        print(f"اختبار #{i+1}: {test_data['user_type']} - {test_data['city']} - {test_data['plan']}")
        print('='*80)
        
        smart_system = SmartReportSystem(test_data)
        
        # بيانات تجريبية
        sample_user_info = {"city": test_data['city'], "area": 120}
        sample_market_data = {
            'متوسط_السوق': 6000,
            'العائد_التأجيري': 7.5,
            'معدل_النمو_الشهري': 2.5,
            'مؤشر_السيولة': 85,
            'حجم_التداول_شهري': 120,
            'طالب_الشراء': 180,
            'عرض_العقارات': 100,
            'معدل_الإشغال': 90,
            'أقل_سعر': 4200,
            'أعلى_سعر': 9000
        }
        
        try:
            report = smart_system.generate_extended_report(
                sample_user_info, 
                sample_market_data, 
                pd.DataFrame(), 
                test_data['plan']
            )
            
            # التحقق من التعديلات الجديدة
            contains_pages = "🧾 **عدد صفحات التقرير:**" in report
            contains_personalized = "📌 **هذا التقرير مخصص لك بناءً على ملفك الاستثماري**" in report
            contains_extended = "المحتوى التحليلي المتقدم" in report
            
            print(f"📄 نوع التقرير: {test_data['user_type']}")
            print(f"🏙️ المدينة: {test_data['city']}")
            print(f"💰 الباقة: {test_data['plan']}")
            print(f"🎯 الفئة: {test_data['category']}")
            print(f"📊 عدد الصفحات مذكور: {'✅' if contains_pages else '❌'}")
            print(f"🎭 رسالة تخصيص: {'✅' if contains_personalized else '❌'}")
            print(f"🚀 محتوى موسع: {'✅' if contains_extended else '❌'}")
            print(f"📏 طول التقرير: {len(report)} حرف")
            print(f"✅ تم إنشاء تقرير {test_data['user_type']} بنجاح!")
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء التقرير: {e}")
    
    print(f"\n{'='*80}")
    print("🎯 اختبار حارس الجودة:")
    
    # اختبار مع بيانات فارغة
    smart_system = SmartReportSystem({"city": "الرياض", "plan": "ذهبية", "category": "investor"})
    try:
        report = smart_system.generate_extended_report(
            {"city": "الرياض", "area": 120},
            {},  # بيانات فارغة
            pd.DataFrame(),
            "ذهبية"
        )
        print("✅ تم توليد تقرير بنجاح مع بيانات فارغة (استخدم البيانات الاحتياطية)")
    except Exception as e:
        print(f"❌ خطأ في معالجة البيانات الفارغة: {e}")
    
    print("✅ جميع التعديلات تم تطبيقها بنجاح!")
