# ai_executive_summary.py
# =========================================
# Executive Decision Engine – Warda Intelligence
# =========================================

import pandas as pd
from smart_opportunities import SmartOpportunityFinder


def generate_executive_summary(user_info, market_data, real_data):
    if real_data is None or real_data.empty:
        return {
            "decision_text": (
                "❌ تعذر إصدار قرار استثماري موثوق بسبب غياب بيانات فعلية كافية.\n"
                "يوصى بعدم اتخاذ أي قرار قبل توفر بيانات سوقية حقيقية."
            ),
            "decision_type": "WAIT",
            "confidence_level": "حذرة",
        }

    city = user_info.get("city", "المدينة")
    property_type = user_info.get("property_type", "العقار")

    finder = SmartOpportunityFinder()
    undervalued = finder.find_undervalued_properties(real_data, city)
    timing = finder.get_golden_timing(market_data)

    liquidity = market_data.get("مؤشر_السيولة", 0)
    growth = market_data.get("معدل_النمو_الشهري", 0)

    decision_type = "WAIT"
    confidence = "متوسطة"

    if len(undervalued) >= 3 and liquidity >= 60 and growth >= 1:
        decision_type = "BUY"
        confidence = "عالية"
    elif liquidity < 45 or growth < 0:
        decision_type = "AVOID"
        confidence = "حذرة"

    decision_text = f"""
المدينة: {city}
نوع العقار: {property_type}

القرار التنفيذي:
{ "الشراء مدعوم بالمعطيات الحالية." if decision_type == "BUY"
else "التريث مطلوب حاليًا." if decision_type == "WAIT"
else "تجنّب التنفيذ في الوضع الحالي." }

مستوى الثقة في القرار: {confidence}

هذا القرار مبني على:
• بيانات سوقية فعلية
• تحليل سيولة حقيقي
• رصد فرص وتسعير دون القيمة
• قراءة توقيت السوق
"""

    return {
        "decision_text": decision_text.strip(),
        "decision_type": decision_type,
        "confidence_level": confidence,
    }
