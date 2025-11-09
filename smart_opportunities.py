# smart_opportunities.py - نظام اكتشاف الفرص الذكية
import pandas as pd
import numpy as np
from datetime import datetime

class SmartOpportunityFinder:
    def __init__(self):
        self.opportunity_cache = {}
    
    def find_undervalued_properties(self, real_data, city):
        """اكتشاف العقارات تحت السوق"""
        try:
            if real_data.empty:
                return []
            
            # حساب متوسط السعر للمنطقة
            area_avg_prices = real_data.groupby('المنطقة')['سعر_المتر'].mean()
            
            undervalued = []
            for _, property in real_data.iterrows():
                area_avg = area_avg_prices.get(property['المنطقة'], property['سعر_المتر'])
                
                # إذا السعر أقل من المتوسط بـ 15%
                if property['سعر_المتر'] < area_avg * 0.85:
                    discount = ((area_avg - property['سعر_المتر']) / area_avg) * 100
                    undervalued.append({
                        'العقار': property['العقار'],
                        'المنطقة': property['المنطقة'], 
                        'السعر_الحالي': property['السعر'],
                        'سعر_المتر': property['سعر_المتر'],
                        'متوسط_المنطقة': area_avg,
                        'الخصم': f"{discount:.1f}%",
                        'العائد_المتوقع': property.get('العائد_المتوقع', 'N/A'),
                        'مستوى_الخطورة': property.get('مستوى_الخطورة', 'غير محدد')
                    })
            
            return sorted(undervalued, key=lambda x: float(x['الخصم'][:-1]), reverse=True)[:10]
            
        except Exception as e:
            print(f"خطأ في اكتشاف العقارات المخفضة: {e}")
            return []
    
    def predict_rising_areas(self, real_data, city):
        """تحليل المناطق الصاعدة"""
        try:
            if real_data.empty:
                return []
            
            # تحليل النمو بالمناطق
            area_growth = real_data.groupby('المنطقة').agg({
                'سعر_المتر': ['mean', 'count'],
                'العائد_المتوقع': 'mean'
            }).round(2)
            
            rising_areas = []
            for area in area_growth.index:
                avg_price = area_growth.loc[area, ('سعر_المتر', 'mean')]
                property_count = area_growth.loc[area, ('سعر_المتر', 'count')]
                avg_return = area_growth.loc[area, ('العائد_المتوقع', 'mean')]
                
                # منطق تحديد المناطق الصاعدة
                growth_score = (
                    (avg_return / 10) +  # العائد
                    (min(property_count / 50, 1)) +  # كثافة العقارات
                    (1 if avg_return > 8 else 0.5)  # عوائد عالية
                )
                
                if growth_score > 1.5:
                    rising_areas.append({
                        'المنطقة': area,
                        'متوسط_السعر': avg_price,
                        'عدد_العقارات': property_count,
                        'متوسط_العائد': avg_return,
                        'درجة_النمو': f"{growth_score:.1f}",
                        'التوصية': "منطقة صاعدة - فرصة مبكرة"
                    })
            
            return sorted(rising_areas, key=lambda x: float(x['درجة_النمو']), reverse=True)
            
        except Exception as e:
            print(f"خطأ في تحليل المناطق الصاعدة: {e}")
            return []
    
    def get_golden_timing(self, market_data):
        """تحديد التوقيت الذهبي للاستثمار"""
        growth = market_data.get('معدل_النمو_الشهري', 0)
        liquidity = market_data.get('مؤشر_السيولة', 0)
        
        if growth > 3 and liquidity > 85:
            return "🟢 التوقيت ممتاز - السوق في ذروة النمو والسيولة"
        elif growth > 2 and liquidity > 75:
            return "🟡 التوقيت جيد - استثمر مع مراقبة المؤشرات"
        elif growth > 1:
            return "🟠 التوقيت مقبول - ابحث عن الصفقات الذكية"
        else:
            return "🔴 الانتظار أفضل - السوق يحتاج استقرار"
    
    def analyze_all_opportunities(self, user_info, market_data, real_data):
        """تحليل شامل لكل الفرص"""
        city = user_info.get('city', 'المدينة')
        
        return {
            'عقارات_مخفضة': self.find_undervalued_properties(real_data, city),
            'مناطق_صاعدة': self.predict_rising_areas(real_data, city),
            'توقيت_الاستثمار': self.get_golden_timing(market_data),
            'ملخص_الفرص': f"تم اكتشاف {len(self.find_undervalued_properties(real_data, city))} فرصة استثمارية في {city}"
        }
