# live_data_system.py - نظام البيانات الحية
import pandas as pd
from datetime import datetime, timedelta
import random

class LiveDataSystem:
    def __init__(self):
        self.last_update = None
        self.data_cache = {}
    
    def get_live_market_indicators(self, city):
        """مؤشرات السوق الحية (محاكاة)"""
        # في الواقع، هذه ستأتي من مصادر حية مثل APIs
        indicators = {
            'الرياض': {
                'مؤشر_الطلب': random.randint(75, 95),
                'مؤشر_العرض': random.randint(65, 85),
                'سرعة_البيع': f"{random.randint(15, 45)} يوم",
                'التغير_اليومي': f"{random.uniform(-0.5, 1.2):.1f}%",
                'حجم_المعاملات': random.randint(200, 500)
            },
            'جدة': {
                'مؤشر_الطلب': random.randint(70, 90),
                'مؤشر_العرض': random.randint(60, 80),
                'سرعة_البيع': f"{random.randint(20, 50)} يوم", 
                'التغير_اليومي': f"{random.uniform(-0.3, 0.9):.1f}%",
                'حجم_المعاملات': random.randint(150, 400)
            },
            'الدمام': {
                'مؤشر_الطلب': random.randint(65, 85),
                'مؤشر_العرض': random.randint(70, 90),
                'سرعة_البيع': f"{random.randint(25, 60)} يوم",
                'التغير_اليومي': f"{random.uniform(-0.2, 0.6):.1f}%",
                'حجم_المعاملات': random.randint(100, 300)
            }
        }
        
        return indicators.get(city, indicators['الرياض'])
    
    def get_price_trends(self, city, property_type):
        """اتجاهات الأسعار الحية"""
        trends = {
            'اتجاه_الاسعار': 'صاعد' if random.random() > 0.3 else 'مستقر',
            'التغير_الشهري': f"{random.uniform(0.5, 2.5):.1f}%",
            'التغير_السنوي': f"{random.uniform(3.0, 8.5):.1f}%",
            'مستوى_النشاط': 'عالي' if random.random() > 0.4 else 'متوسط'
        }
        return trends
    
    def update_live_data(self, real_data):
        """تحديث البيانات الحية"""
        self.last_update = datetime.now()
        self.data_cache['last_update'] = self.last_update
        self.data_cache['data_count'] = len(real_data)
        return True
    
    def get_live_data_summary(self, city):
        """ملخص البيانات الحية"""
        return {
            'آخر_تحديث': self.last_update.strftime('%Y-%m-%d %H:%M') if self.last_update else 'لم يتم التحديث',
            'مؤشرات_حية': self.get_live_market_indicators(city),
            'حالة_السوق': self._get_market_status(city),
            'توصية_فورية': self._get_instant_recommendation(city)
        }
    
    def _get_market_status(self, city):
        """حالة السوق الحية"""
        indicators = self.get_live_market_indicators(city)
        demand = indicators['مؤشر_الطلب']
        
        if demand > 85:
            return "🟢 سوق نشط - فرص ممتازة"
        elif demand > 70:
            return "🟡 سوق معتدل - فرص جيدة"
        else:
            return "🔴 سوق هادئ - انتقائية في الشراء"
    
    def _get_instant_recommendation(self, city):
        """توصية فورية بناءً على البيانات الحية"""
        indicators = self.get_live_market_indicators(city)
        
        if float(indicators['التغير_اليومي'][:-1]) > 0.5:
            return "📈 اتجاه صاعد - فرصة للاستثمار الفوري"
        else:
            return "⚖️ استقرار في السوق - ابحث عن الصفقات الذكية"
