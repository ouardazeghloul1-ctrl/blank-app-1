# robo_chat/robo_knowledge.py

class RoboKnowledge:
    def __init__(self, real_data, opportunities, alerts, market_data):
        self.real_data = real_data
        self.opportunities = opportunities
        self.alerts = alerts
        self.market = market_data  # ✅ الاسم الصحيح هو market وليس market_data

    def market_summary(self, city):
        return f"""
السوق في {city} حاليًا يتميز بـ:
• سيولة: {self.market.get('مؤشر_السيولة', 'غير متوفر')}
• نمو شهري: {self.market.get('معدل_النمو_الشهري', 'غير متوفر')}%
• عدد العقارات المحللة: {self.market.get('عدد_العقارات_الحقيقية', 0)}
"""

    def today_opportunities(self, city):
        """البحث عن فرص بناءً على المدينة أو المنطقة"""
        city_ops = [
            o for o in self.opportunities.get("عقارات_مخفضة", [])
            if o.get("المدينة") == city or o.get("المنطقة") == city
        ]
        return city_ops[:2]  # نُظهر فقط 1–2

    def decision_signal(self, city):
        """إشارة قرار استثماري بناءً على البيانات الحقيقية"""
        liquidity = self.market.get("مؤشر_السيولة", 0)
        growth = self.market.get("معدل_النمو_الشهري", 0)
        opportunities = self.today_opportunities(city)

        # إشارة دخول قوية
        if liquidity > 80 and growth > 3 and opportunities:
            return {
                "signal": "ENTER",
                "confidence": "HIGH",
                "reason": "سيولة عالية + نمو قوي + فرص فعلية"
            }

        # مراقبة مع تفاؤل
        if liquidity > 65 and growth > 1.5:
            return {
                "signal": "WATCH",
                "confidence": "MEDIUM",
                "reason": "سوق مستقر مع فرص انتقائية"
            }

        # انتظار حذر
        return {
            "signal": "WAIT",
            "confidence": "LOW",
            "reason": "سيولة ضعيفة أو غياب فرص واضحة"
        }
