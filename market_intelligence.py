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
            trends["avg_price"] = real_data['السعر'].mean()
            trends["avg_roi"] = real_data['العائد_المتوقع'].mean()
            trends["property_count"] = len(real_data)
            trends["risk_distribution"] = real_data['مستوى_الخطورة'].value_counts().to_dict()
        
        return trends
    
    def _find_advanced_opportunities(self, real_data):
        """اكتشاف فرص متقدمة"""
        opportunities = []
        
        if not real_data.empty:
            # الفرص ذات العوائد العالية والمخاطر المنخفضة
            high_roi_low_risk = real_data[
                (real_data['العائد_المتوقع'] > real_data['العائد_المتوقع'].quantile(0.7)) &
                (real_data['مستوى_الخطورة'] == 'منخفض')
            ]
            
            for _, opp in high_roi_low_risk.iterrows():
                opportunities.append({
                    "property": opp['العقار'],
                    "area": opp['المنطقة'],
                    "price": opp['السعر'],
                    "roi": opp['العائد_المتوقع'],
                    "risk": opp['مستوى_الخطورة'],
                    "score": self._calculate_opportunity_score(opp)
                })
        
        return sorted(opportunities, key=lambda x: x['score'], reverse=True)[:5]
    
    def _calculate_opportunity_score(self, property_data):
        """حساب درجة الفرصة الاستثمارية"""
        score = 0
        
        # العائد (40%)
        score += (property_data['العائد_المتوقع'] / 15) * 40
        
        # المخاطرة (30%)
        risk_multiplier = {
            'منخفض': 30,
            'متوسط': 15, 
            'مرتفع': 5
        }
        score += risk_multiplier.get(property_data['مستوى_الخطورة'], 10)
        
        return min(100, score)
    
    def _predict_future_market(self, real_data, periods=12):
        """توقع مستقبل السوق"""
        if len(real_data) < 10:
            return {"message": "لا توجد بيانات كافية للتنبؤ"}
        
        try:
            predictions = []
            current_avg = real_data['السعر'].mean()
            
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
        
        risk_levels = real_data['مستوى_الخطورة'].value_counts()
        total_properties = len(real_data)
        
        risk_assessment = {
            "low_risk_percentage": (risk_levels.get('منخفض', 0) / total_properties) * 100,
            "medium_risk_percentage": (risk_levels.get('متوسط', 0) / total_properties) * 100,
            "high_risk_percentage": (risk_levels.get('مرتفع', 0) / total_properties) * 100,
            "overall_risk": "منخفض" if risk_levels.get('منخفض', 0) > risk_levels.get('مرتفع', 0) else "متوسط"
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
