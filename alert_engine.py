# =========================================
# Alert Engine – Warda Intelligence
# Generates raw alert signals (NOT messages)
# =========================================

from datetime import datetime
from live_real_data_provider import get_live_real_data
from smart_opportunities import SmartOpportunityFinder

class AlertEngine:
    def __init__(self):
        self.opportunity_finder = SmartOpportunityFinder()

    def generate_daily_alert(self, city, property_type):
        """
        يولد تنبيهًا واحدًا عالي الجودة في اليوم
        """
        real_data = get_live_real_data(
            city=city,
            property_type=property_type
        )

        if real_data.empty:
            return None

        # 1️⃣ البحث عن فرص مخفضة
        undervalued = self.opportunity_finder.find_undervalued_properties(
            real_data, city
        )

        if undervalued:
            best = undervalued[0]
            return {
                "type": "GOLDEN_OPPORTUNITY",
                "city": city,
                "district": best["المنطقة"],
                "signal": {
                    "discount_percent": best["الخصم"],
                    "current_price": best["السعر_الحالي"],
                    "avg_area_price": best["متوسط_المنطقة"],
                    "expected_return": best.get("العائد_المتوقع", "N/A"),
                    "window_hours": 48
                },
                "source": [
                    "live_real_data_provider",
                    "smart_opportunities.find_undervalued_properties"
                ],
                "confidence": "HIGH",
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

        return None
