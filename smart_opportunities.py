# smart_opportunities.py - نظام اكتشاف الفرص الذكية
# =================================================
# ملاحظة معمارية مهمة:
# هذا الملف محصور فقط داخل AlertEngine
# لا يُستخدم في التقرير أو الخلاصة التنفيذية أو ai_report_reasoner
# =================================================

import pandas as pd
import numpy as np
from datetime import datetime

class SmartOpportunityFinder:
    def __init__(self):
        # reserved for future use
        self.opportunity_cache = {}
    
    def _safe_col(self, row, *names):
        """
        طبقة أمان للوصول إلى الأعمدة - تدعم الأسماء العربية والإنجليزية
        """
        for name in names:
            if name in row and pd.notna(row[name]):
                return row[name]
        return None
    
    def _has_required_columns(self, df, required_cols):
        """
        التحقق من وجود الأعمدة المطلوبة
        """
        if df is None or df.empty:
            return False
        return all(col in df.columns for col in required_cols)
    
    def find_undervalued_properties(self, real_data, city):
        """اكتشاف العقارات تحت السوق"""
        try:
            if real_data.empty:
                return []
            
            # التحقق من وجود الأعمدة المطلوبة
            required = ['price_per_sqm', 'district']
            if not self._has_required_columns(real_data, required):
                print("⚠️ الأعمدة المطلوبة غير موجودة: price_per_sqm, district")
                return []
            
            # حساب متوسط السعر للمنطقة
            area_avg_prices = real_data.groupby('district')['price_per_sqm'].mean()
            
            undervalued = []
            for _, property in real_data.iterrows():
                district = self._safe_col(property, 'district', 'المنطقة')
                if district is None:
                    continue
                
                price_per_sqm = self._safe_col(property, 'price_per_sqm', 'سعر_المتر')
                if price_per_sqm is None:
                    continue
                
                area_avg = area_avg_prices.get(district, price_per_sqm)
                
                # إذا السعر أقل من المتوسط بـ 15%
                if price_per_sqm < area_avg * 0.85:
                    discount = ((area_avg - price_per_sqm) / area_avg) * 100
                    
                    # استخراج باقي الحقول بأمان
                    property_name = self._safe_col(property, 'العقار', 'property_name', 'name') or f"عقار في {district}"
                    current_price = self._safe_col(property, 'price', 'السعر')
                    expected_return = self._safe_col(property, 'العائد_المتوقع', 'expected_return', 'return')
                    risk_level = self._safe_col(property, 'مستوى_الخطورة', 'risk_level', 'risk')
                    
                    undervalued.append({
                        'العقار': property_name,
                        'المنطقة': district, 
                        'السعر_الحالي': current_price,
                        'سعر_المتر': price_per_sqm,
                        'متوسط_المنطقة': area_avg,
                        'الخصم': f"{discount:.1f}%",
                        'العائد_المتوقع': expected_return if expected_return is not None else 'N/A',
                        'مستوى_الخطورة': risk_level if risk_level is not None else 'غير محدد'
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
            
            # التحقق من وجود الأعمدة المطلوبة
            required = ['price_per_sqm', 'district']
            if not self._has_required_columns(real_data, required):
                print("⚠️ الأعمدة المطلوبة غير موجودة: price_per_sqm, district")
                return []
            
            # تحليل النمو بالمناطق
            area_growth = real_data.groupby('district').agg({
                'price_per_sqm': ['mean', 'count'],
            }).round(2)
            
            # إضافة العائد المتوقع إذا كان موجوداً
            if 'expected_return' in real_data.columns:
                area_growth['expected_return'] = real_data.groupby('district')['expected_return'].mean()
            else:
                area_growth['expected_return'] = 5.0  # قيمة افتراضية
            
            rising_areas = []
            for area in area_growth.index:
                avg_price = area_growth.loc[area, ('price_per_sqm', 'mean')]
                property_count = area_growth.loc[area, ('price_per_sqm', 'count')]
                avg_return = area_growth.loc[area, 'expected_return'] if isinstance(area_growth.loc[area, 'expected_return'], (int, float)) else 5.0
                
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
        """تحديد التوقيت الذهبي للاستثمار (نصي إرشادي فقط)"""
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
