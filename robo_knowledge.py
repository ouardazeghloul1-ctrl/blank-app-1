# robo_chat/robo_knowledge.py

class RoboKnowledge:
    def __init__(self, real_data, opportunities, alerts, market_data):
        self.real_data = real_data
        self.opportunities = opportunities
        self.alerts = alerts
        self.market = market_data

    def market_summary(self, city):
        return f"""
السوق في {city} حاليًا يتميز بـ:
• سيولة: {self.market.get('مؤشر_السيولة', 'غير متوفر')}
• نمو شهري: {self.market.get('معدل_النمو_الشهري', 'غير متوفر')}%
• عدد العقارات المحللة: {self.market.get('عدد_العقارات_الحقيقية', 0)}
"""

    def today_opportunities(self, city):
        city_ops = [
            o for o in self.opportunities.get("عقارات_مخفضة", [])
            if o.get("المنطقة") == city
        ]
        return city_ops[:2]  # نُظهر فقط 1–2
