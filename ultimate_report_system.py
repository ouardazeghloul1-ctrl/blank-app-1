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
        report_generator = self.all_categories.get(user_type, self._create_investor_report)
        return report_generator(user_info, market_data, real_data, package_level)
    
    def _create_investor_report(self, user_info, market_data, real_data, package_level):
        return f"""
        📈 **تقرير المستثمر المتقدم - {user_info['city']}**
        
        💰 **التحليل المالي:**
        • العوائد المتوقعة: {safe_num(real_data['العائد_المتوقع'].mean(), '.1f')}%
        • أفضل المناطق: {', '.join(real_data['المنطقة'].value_counts().head(3).index.tolist())}
        • حجم السوق: {len(real_data)} عقار
        
        🎯 **الفرص الذهبية:**
        1. الاستثمار في المناطق الناشئة
        2. الشراء في أوقات الذروة  
        3. التنويع بين العقارات
        """
    
    def _create_broker_report(self, user_info, market_data, real_data, package_level):
        return f"""
        🤝 **تقرير الوسيط العقاري - {user_info['city']}**
        
        🏘️ **قاعدة البيانات:**
        • إجمالي العقارات: {len(real_data)} عقار
        • التوزيع الجغرافي: {real_data['المنطقة'].nunique()} منطقة
        
        💰 **استراتيجيات التسعير:**
       • متوسط السوق: {safe_num(real_data['السعر'].mean())} ريال
       • نطاق الأسعار: {safe_num(real_data['السعر'].min())} - {safe_num(real_data['السعر'].max())}
        """
    
    def _create_developer_report(self, user_info, market_data, real_data, package_level):
        return f"""
        🏗️ **تقرير شركة التطوير - {user_info['city']}**
        
        📊 **تحليل السوق للتطوير:**
        • الطلب على {user_info['property_type']}: {len(real_data)} عقار
        • متوسط الأسعار: {safe_num(real_data['السعر'].mean())} ريال
        • المناطق الواعدة: {', '.join(real_data['المنطقة'].value_counts().head(3).index.tolist())}
        """
    
    def _create_individual_report(self, user_info, market_data, real_data, package_level):
        return f"""
        🏠 **تقرير الباحث عن سكن - {user_info['city']}**
        
        🏡 **المناطق المناسبة:**
        • المناطق المتوسطة السعر: {real_data['المنطقة'].mode()[0]}
        • متوسط الأسعار: {safe_num(real_data['السعر'].mean())} ريال
        • المساحات المتاحة: 80-200 م²
        """
    
    def _create_opportunity_report(self, user_info, market_data, real_data, package_level):
        return f"""
        💎 **تقرير الباحث عن فرص - {user_info['city']}**
        
        🎯 **الفرص المميزة:**
        • العقارات ذات العوائد العالية: {safe_num(real_data['العائد_المتوقع'].max(), '.1f')}%
        • المناطق الصاعدة: {real_data['المنطقة'].value_counts().index[1]}
        • أسعار منافسة: {safe_num(real_data['السعر'].min())} ريال      
        """
    
    def _create_owner_report(self, user_info, market_data, real_data, package_level):
        return f"""
        🏡 **تقرير مالك العقار - {user_info['city']}**
        
        💰 **تقييم القيمة:**
        • القيمة السوقية: {safe_num(real_data['السعر'].mean())} ريال          • أفضل وقت للبيع: خلال 3-6 أشهر    
        • نصائح لزيادة القيمة: تجديد الواجهة، تحسين الخدمات
        """
