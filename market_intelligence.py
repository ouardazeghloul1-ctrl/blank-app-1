# market_intelligence.py - ذكاء السوق المتقدم والتحليلات المعقدة
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

class MarketIntelligence:
    def __init__(self):
        self.models = {}
        self.market_insights = {}
    
    def advanced_market_analysis(self, real_data, user_info):
        """تحليل سوق متقدم باستخدام الذكاء الاصطناعي"""
        if real_data.empty:
            return self._get_basic_insights(user_info)
        
        insights = {
            "market_trends": self._analyze_market_trends(real_data),
            "investment_opportunities": self._find_advanced_opportunities(real_data),
            "risk_assessment": self._assess_market_risks(real_data),
            "future_predictions": self._predict_future_market(real_data),
            "competitive_analysis": self._analyze_competition(real_data)
        }
        
        return insights
    
    def _analyze_market_trends(self, real_data):
        """تحيل اتجاهات السوق المتقدمة"""
        trends = {}
        
        # تحليل الاتجاهات السعرية
        price_trend = self._calculate_price_trend(real_data)
        trends["price_trend"] = price_trend
        
        # تحليل توزيع العوائد
        roi_distribution = self._analyze_roi_distribution(real_data)
        trends["roi_distribution"] = roi_distribution
        
        # تحليل حركة السوق
        market_movement = self._analyze_market_movement(real_data)
        trends["market_movement"] = market_movement
        
        return trends
    
    def _find_advanced_opportunities(self, real_data):
        """اكتشاف فرص متقدمة باستخدام خوارزميات متطورة"""
        opportunities = []
        
        # الفرص ذات العوائد العالية والمخاطر المنخفضة
        high_roi_low_risk = real_data[
            (real_data['العائد_المتوقع'] > real_data['العائد_المتوقع'].quantile(0.7)) &
            (real_data['مستوى_الخطورة'] == 'منخفض')
        ]
        
        if not high_roi_low_risk.empty:
            for _, opp in high_roi_low_risk.iterrows():
                opportunities.append({
                    "property": opp['العقار'],
                    "area": opp['المنطقة'],
                    "price": opp['السعر'],
                    "roi": opp['العائد_المتوقع'],
                    "risk": opp['مستوى_الخطورة'],
                    "score": self._calculate_opportunity_score(opp)
                })
        
        return sorted(opportunities, key=lambda x: x['score'], reverse=True)[:10]
    
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
        
        # السعر (20%)
        price_score = max(0, 20 - (property_data['السعر'] / 5000000) * 10)
        score += price_score
        
        # الموقع (10%)
        score += 10  # تقدير مبدئي
        
        return min(100, score)
    
    def _predict_future_market(self, real_data, periods=12):
        """توقع مستقبل السوق باستخدام النمذجة"""
        if len(real_data) < 10:
            return {"message": "لا توجد بيانات كافية للتنبؤ"}
        
        try:
            # تحضير البيانات للتنبؤ
            X = np.array(range(len(real_data))).reshape(-1, 1)
            y = real_data['السعر'].values
            
            # تدريب نموذج الانحدار
            model = LinearRegression()
            model.fit(X, y)
            
            # التنبؤ بالفترات القادمة
            future_X = np.array(range(len(real_data), len(real_data) + periods)).reshape(-1, 1)
            future_prices = model.predict(future_X)
            
            predictions = []
            for i, price in enumerate(future_prices, 1):
                current_avg = real_data['السعر'].mean()
                change = ((price / current_avg) - 1) * 100
                predictions.append({
                    "month": i,
                    "predicted_price": int(price),
                    "change_percent": round(change, 1)
                })
            
            return predictions
            
        except Exception as e:
            return {"error": f"خطأ في التنبؤ: {e}"}
    
    def _get_basic_insights(self, user_info):
        """رؤى أساسية عندما لا توجد بيانات"""
        return {
            "market_trends": {
                "price_trend": "غير متوفر - تحتاج بيانات",
                "roi_distribution": "غير متوفر - تحتاج بيانات",
                "market_movement": "غير متوفر - تحتاج بيانات"
            },
            "investment_opportunities": [],
            "risk_assessment": "غير متوفر - تحتاج بيانات",
            "future_predictions": {"message": "جمع المزيد من البيانات لتفعيل التنبؤات"},
            "competitive_analysis": "غير متوفر - تحتاج بيانات"
        }

# اختبار النظام
if __name__ == "__main__":
    intelligence = MarketIntelligence()
    
    # بيانات تجريبية
    sample_data = pd.DataFrame({
        'العقار': [f'عقار {i}' for i in range(1, 21)],
        'المنطقة': ['النخيل', 'الربوة', 'العليا'] * 7,
        'السعر': np.random.normal(1000000, 300000, 20),
        'العائد_المتوقع': np.random.uniform(4, 12, 20),
        'مستوى_الخطورة': np.random.choice(['منخفض', 'متوسط', 'مرتفع'], 20, p=[0.6, 0.3, 0.1])
    })
    
    insights = intelligence.advanced_market_analysis(sample_data, {})
    print("✅ ذكاء السوق المتقدم جاهز!")
    print(f"تم اكتشاف {len(insights['investment_opportunities'])} فرصة استثمارية")
