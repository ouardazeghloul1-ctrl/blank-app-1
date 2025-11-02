# ultimate_report_system.py
class UltimateReportSystem:
    def __init__(self):
        self.all_categories = {
            "مستثمر": self._create_investor_report,
            "وسيط عقاري": self._create_broker_report, 
            "شركة تطوير": self._create_developer_report,
            "فرد": self._create_individual_report,
            "باحث عن فرصة": self._create_opportunity_report,
            "مالك عقار": self._create_owner_report
        }
    
    def create_ultimate_report(self, user_info, market_data, real_data, package_level):
        user_type = user_info.get('user_type', 'مستثمر')
        return self.all_categories[user_type](user_info, market_data, real_data, package_level)
    
    def _create_investor_report(self, user_info, market_data, real_data, package_level):
        return f"""
        📈 **تقرير المستثمر المتقدم - {user_info['city']}**
        
        💰 **التحليل المالي:**
        • العوائد المتوقعة: {real_data['العائد_المتوقع'].mean():.1f}%
        • أفضل 3 مناطق: {', '.join(real_data['المنطقة'].value_counts().head(3).index.tolist())}
        • حجم السوق: {len(real_data)} عقار
        
        🎯 **الفرص الذهبية:**
        1. الاستثمار في المناطق الناشئة
        2. الشراء في أوقات الذروة
        3. التنويع بين العقارات
        
        📊 **مؤشرات الأداء:**
        • النمو الشهري: {market_data.get('معدل_النمو_الشهري', 2.5)}%
        • السيولة: {market_data.get('مؤشر_السيولة', 85)}%
        """
    
    def _create_broker_report(self, user_info, market_data, real_data, package_level):
        return f"""
        🤝 **تقرير الوسيط العقاري - {user_info['city']}**
        
        🏘️ **قاعدة البيانات:**
        • إجمالي العقارات: {len(real_data)} عقار
        • التوزيع الجغرافي: {real_data['المنطقة'].nunique()} منطقة
        
        💰 **استراتيجيات التسعير:**
        • متوسط السوق: {real_data['السعر'].mean():,.0f} ريال
        • نطاق الأسعار: {real_data['السعر'].min():,.0f} - {real_data['السعر'].max():,.0f}
        
        📈 **نصائح البيع:**
        1. التركيز على {real_data['المنطقة'].mode()[0]}
        2. تسعير تنافسي
        3. عرض الصور والمقاطع
        """
    
    # وسأضيف نفس الشيء للفئات الأربع الأخرى...
