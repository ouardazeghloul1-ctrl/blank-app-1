# alert_engine.py
from datetime import datetime
from alert_rules import *
from alert_storage import save_alert, get_today_alerts
from live_real_data_provider import get_live_real_data
from smart_opportunities import SmartOpportunityFinder

finder = SmartOpportunityFinder()

def score_opportunity(discount_percent, confidence):
    score = 50
    if discount_percent >= 30: score += 30
    elif discount_percent >= 20: score += 20
    elif discount_percent >= 15: score += 10

    if confidence == "HIGH": score += 15
    return min(score, 100)

def generate_city_alert(city: str, property_type: str):
    # حد يومي
    if len(get_today_alerts(city)) >= MAX_ALERTS_PER_CITY_PER_DAY:
        return None

    real_data = get_live_real_data(city, property_type)
    if real_data.empty:
        return None

    undervalued = finder.find_undervalued_properties(real_data, city)
    if not undervalued:
        return None

    top = undervalued[0]
    discount = float(top["الخصم"].replace("%", ""))

    score = score_opportunity(discount, "HIGH")

    if score < SCORE_THRESHOLD:
        return None

    alert = {
        "type": "GOLDEN_OPPORTUNITY",
        "city": city,
        "district": top["المنطقة"],
        "property_type": property_type,
        "facts": {
            "current_price": top["السعر_الحالي"],
            "avg_price": top["متوسط_المنطقة"],
            "discount_percent": discount,
        },
        "confidence": "HIGH",
        "score": score,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source": ["live_real_data_provider", "smart_opportunities"]
    }

    save_alert(alert)
    return alert
