# market_intelligence.py - ذكاء السوق المتقدم والتحليلات المعقدة
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class MarketIntelligence:
    def __init__(self):
        self.market_insights = {}
    
    def advanced_market_analysis(self, real_data, user_info):
        """تحليل سوق متقدم"""
        if real_data.empty:
            return self._get_basic_insights(user_info)
        
        insights = {
            "market_trends": self._analyze_market_trends(real_data),
            "investment_opportunities": self._find_advanced_opportunities(real_data),
            "risk_assessment": self._assess_market_risks(real_data),
            "future_predictions": self._predict_future_market(real_data)
        }
        
        return insights
    
    def _analyze_market_trends(self, real_data):
        """تحليل اتجاهات السوق"""
        trends = {}
        
        if not real_data.empty:
            # استخدام أسماء أعمدة مرنة
            price_column = 'السعر' if 'السعر' in real_data.columns else 'price'
            roi_column = 'العائد_المتوقع' if 'العائد_المتوقع' in real_data.columns else 'roi'
            risk_column = 'مستوى_الخطورة' if 'مستوى_الخطورة' in real_data.columns else 'risk_level'
            
            trends["avg_price"] = real_data[price_column].mean() if price_column in real_data.columns else "غير متوفر"
            trends["avg_roi"] = real_data[roi_column].mean() if roi_column in real_data.columns else "غير متوفر"
            trends["property_count"] = len(real_data)
            
            if risk_column in real_data.columns:
                trends["risk_distribution"] = real_data[risk_column].value_counts().to_dict()
            else:
                trends["risk_distribution"] = {}
        
        return trends
    
    def _find_advanced_opportunities(self, real_data):
        """اكتشاف فرص متقدمة"""
        opportunities = []
        
        if not real_data.empty:
            # تحديد أسماء الأعمدة المرنة
            price_column = 'السعر' if 'السعر' in real_data.columns else 'price'
            roi_column = 'العائد_المتوقع' if 'العائد_المتوقع' in real_data.columns else 'roi'
            risk_column = 'مستوى_الخطورة' if 'مستوى_الخطورة' in real_data.columns else 'risk_level'
            property_column = 'العقار' if 'العقار' in real_data.columns else 'property'
            
            # التحقق من وجود الأعمدة الضرورية
            has_required_columns = all(col in real_data.columns for col in [price_column, roi_column, risk_column, property_column])
            
            if has_required_columns:
                # الفرص ذات العوائد العالية والمخاطر المنخفضة
                high_roi_low_risk = real_data[
                    (real_data[roi_column] > real_data[roi_column].quantile(0.7)) &
                    (real_data[risk_column] == 'منخفض')
                ]
                
                for _, opp in high_roi_low_risk.iterrows():
                    area_name = (
                        opp.get("المنطقة")
                        or opp.get("الحي")
                        or opp.get("district")
                        or opp.get("city")
                        or "غير محدد"
                    )
                    
                    opportunities.append({
                        "property": opp[property_column],
                        "area": area_name,
                        "price": opp[price_column],
                        "roi": opp[roi_column],
                        "risk": opp[risk_column],
                        "score": self._calculate_opportunity_score(opp)
                    })
        
        return sorted(opportunities, key=lambda x: x['score'], reverse=True)[:5]
    
    def _calculate_opportunity_score(self, property_data):
        """حساب درجة الفرصة الاستثمارية"""
        score = 0
        
        # تحديد أسماء الأعمدة المرنة
        roi_column = 'العائد_المتوقع' if 'العائد_المتوقع' in property_data.index else 'roi'
        risk_column = 'مستوى_الخطورة' if 'مستوى_الخطورة' in property_data.index else 'risk_level'
        
        # العائد (40%)
        if roi_column in property_data:
            score += (property_data[roi_column] / 15) * 40
        
        # المخاطرة (30%)
        risk_multiplier = {
            'منخفض': 30,
            'متوسط': 15, 
            'مرتفع': 5,
            'low': 30,
            'medium': 15,
            'high': 5
        }
        
        if risk_column in property_data:
            risk_level = property_data[risk_column]
            score += risk_multiplier.get(risk_level, 10)
        
        return min(100, score)
    
    def _predict_future_market(self, real_data, periods=12):
        """توقع مستقبل السوق"""
        if len(real_data) < 10:
            return {"message": "لا توجد بيانات كافية للتنبؤ"}
        
        try:
            predictions = []
            price_column = 'السعر' if 'السعر' in real_data.columns else 'price'
            
            if price_column not in real_data.columns:
                return {"message": "لا توجد بيانات أسعار للتنبؤ"}
            
            current_avg = real_data[price_column].mean()
            
            for i in range(1, periods + 1):
                # نمو تقديري بسيط
                growth = np.random.normal(0.02, 0.01)  # نمو 2% ± 1%
                future_price = current_avg * (1 + growth) ** i
                change = ((future_price / current_avg) - 1) * 100
                
                predictions.append({
                    "month": i,
                    "predicted_price": int(future_price),
                    "change_percent": round(change, 1)
                })
            
            return predictions
            
        except Exception as e:
            return {"error": f"خطأ في التنبؤ: {e}"}
    
    def _assess_market_risks(self, real_data):
        """تقييم مخاطر السوق"""
        if real_data.empty:
            return "لا توجد بيانات كافية لتقييم المخاطر"
        
        risk_column = 'مستوى_الخطورة' if 'مستوى_الخطورة' in real_data.columns else 'risk_level'
        
        if risk_column not in real_data.columns:
            return "لا توجد بيانات عن مستويات الخطورة"
        
        risk_levels = real_data[risk_column].value_counts()
        total_properties = len(real_data)
        
        risk_assessment = {
            "low_risk_percentage": round((risk_levels.get('منخفض', risk_levels.get('low', 0)) / total_properties) * 100, 1),
            "medium_risk_percentage": round((risk_levels.get('متوسط', risk_levels.get('medium', 0)) / total_properties) * 100, 1),
            "high_risk_percentage": round((risk_levels.get('مرتفع', risk_levels.get('high', 0)) / total_properties) * 100, 1),
            "overall_risk": "منخفض" if risk_levels.get('منخفض', risk_levels.get('low', 0)) > risk_levels.get('مرتفع', risk_levels.get('high', 0)) else "متوسط"
        }
        
        return risk_assessment
    
    def _get_basic_insights(self, user_info):
        """رؤى أساسية عندما لا توجد بيانات"""
        return {
            "market_trends": {
                "avg_price": "غير متوفر",
                "avg_roi": "غير متوفر", 
                "property_count": 0
            },
            "investment_opportunities": [],
            "risk_assessment": "غير متوفر",
            "future_predictions": {"message": "جمع المزيد من البيانات لتفعيل التنبؤات"}
        }

# اختبار النظام
if __name__ == "__main__":
    intelligence = MarketIntelligence()
    print("✅ ذكاء السوق المتقدم جاهز!")
