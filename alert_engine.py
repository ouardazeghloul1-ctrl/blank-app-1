# =========================================
# Alert Engine – Warda Intelligence
# Generates ALL golden opportunity alerts (NO discarding)
# =========================================

from datetime import datetime
from live_real_data_provider import get_live_real_data
from smart_opportunities import SmartOpportunityFinder

MIN_DISCOUNT_PERCENT = 15  # الحد الأدنى للفرصة الذهبية

class AlertEngine:
    def __init__(self):
        self.opportunity_finder = SmartOpportunityFinder()

    def generate_daily_alerts(self, city, property_type):
        """
        يولد ALL الفرص الذهبية لمدينة واحدة (بدون رمي أي فرصة)
        """
        real_data = get_live_real_data(
            city=city,
            property_type=property_type
        )

        if real_data.empty:
            return []

        # 1️⃣ البحث عن جميع الفرص المخفضة
        undervalued = self.opportunity_finder.find_undervalued_properties(
            real_data, city
        )

        if not undervalued:
            return []

        alerts = []

        # 2️⃣ تحويل كل فرصة إلى تنبيه (بدون استثناء)
        for prop in undervalued:
            # تحويل الخصم من نص إلى رقم
            discount_raw = prop.get("الخصم", "0").replace("%", "")
            try:
                discount = float(discount_raw)
            except:
                continue  # تخطي إذا كان التنسيق خاطئًا

            # تصفية فقط: الخصم القوي (لا رمي عشوائي)
            if discount < MIN_DISCOUNT_PERCENT:
                continue

            # ✅ أمان إضافي لأسماء الحقول - نحاول أكثر من مفتاح
            current_price = prop.get("السعر_الحالي") or prop.get("السعر") or 0
            avg_price = prop.get("متوسط_المنطقة") or prop.get("متوسط_السعر") or 0
            district = prop.get("المنطقة") or prop.get("الحي") or "غير محدد"
            
            # إنشاء تنبيه لكل فرصة ذهبية
            alert = {
                "type": "GOLDEN_OPPORTUNITY",
                "city": city,
                "district": district,
                "title": "💰 فرصة ذهبية بخصم قوي عن السوق",
                "description": f"عقار في {district} بخصم {discount:.1f}% أقل من متوسط المنطقة",
                "signal": {
                    "discount_percent": discount,
                    "current_price": current_price,
                    "avg_area_price": avg_price,
                    "expected_return": prop.get("العائد_المتوقع", "غير متاح"),
                    "window_hours": 48,
                    "property_type": property_type
                },
                "confidence": "HIGH",
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "source": [
                    "live_real_data_provider",
                    "smart_opportunities.find_undervalued_properties"
                ]
            }
            
            alerts.append(alert)

        return alerts  # كل الفرص، كلها، بدون استثناء
