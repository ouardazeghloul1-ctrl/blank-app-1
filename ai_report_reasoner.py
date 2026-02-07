# ai_report_reasoner.py
# =========================================
# عقل التقرير الاستشاري – Warda Intelligence
# =========================================

from live_data_system import LiveDataSystem
from market_intelligence import MarketIntelligence
from smart_opportunities import SmartOpportunityFinder
from ai_executive_summary import generate_executive_summary
import pandas as pd

from ai_text_templates import (
    LIVE_MARKET_SNAPSHOT,
    OPPORTUNITY_INSIGHT,
    RISK_INSIGHT,
)

# =========================================
# قيم افتراضية شاملة (تمنع أي KeyError)
# =========================================

DEFAULT_AI_VALUES = {
    "المدينة": "غير محددة",
    "سرعة_البيع": "متوسطة",
    "التغير_اليومي": "0%",
    "اتجاه_الأسعار": "مستقر",
    "مستوى_الطلب": "انتقائي",
    "مستوى_العرض": "متوازن",
    "حالة_السوق": "مستقرة نسبيًا",
    "مزاج_السوق": "محايد",
    "مستوى_المخاطر_العام": "متوسط",
    "عمق_التحليل": "مرتفع",
    "نبرة_التحليل": "استشاري",
    "مستوى_الثقة": "عالية",
    "ملاحظة_البيانات": "التحليل مبني على بيانات سوقية حية",
}

# =========================================
# سياسات الباقات
# =========================================

AI_PACKAGE_POLICY = {
    "ماسية متميزة": {"live_market": "full", "opportunities": "full", "risk": "full", "final_decision": "full"},
    "ماسية": {"live_market": "full", "opportunities": "full", "risk": "summary", "final_decision": "full"},
    "ذهبية": {"live_market": "summary", "opportunities": "summary", "risk": "summary", "final_decision": "summary"},
    "فضية": {"live_market": "summary", "opportunities": "hidden", "risk": "hidden", "final_decision": "summary"},
    "مجانية": {"live_market": "summary", "opportunities": "hidden", "risk": "hidden", "final_decision": "hidden"},
}

# =========================================
# أدوات مساعدة
# =========================================

def fill_ai_template(template: str, values: dict) -> str:
    if not template:
        return ""
    return template.format(**values)

# =========================================
# AI Report Reasoner
# =========================================

class AIReportReasoner:
    def __init__(self):
        self.live_system = LiveDataSystem()
        self.market_intel = MarketIntelligence()
        self.opportunity_finder = SmartOpportunityFinder()

    def generate_all_insights(self, user_info, market_data, real_data):
        city = user_info.get("city", "المدينة")
        package = user_info.get("package") or user_info.get("chosen_pkg") or "مجانية"
        policy = AI_PACKAGE_POLICY.get(package, AI_PACKAGE_POLICY["مجانية"])

        # إشارات السوق (إن وُجدت)
        market_signals = {
            "سرعة_البيع": market_data.get("سرعة_البيع", "متوسطة"),
            "التغير_اليومي": market_data.get("التغير_اليومي", "0%"),
        }

        base_values = {
            "المدينة": city,
            "اتجاه_الأسعار": market_data.get("اتجاه_الاسعار", "مستقر"),
        }

        # دمج شامل وآمن
        all_values = {
            **DEFAULT_AI_VALUES,
            **base_values,
            **market_signals,
        }

        def apply_policy(key, text):
            mode = policy.get(key, "hidden")
            if mode == "full":
                return text
            if mode == "summary":
                return text.split("\n")[0] + "\n(ملخص تنفيذي)"
            return ""

        final_decision_text = generate_executive_summary(
            user_info=user_info,
            market_data=market_data,
            real_data=real_data,
        )

        return {
            "ai_live_market": apply_policy(
                "live_market",
                fill_ai_template(LIVE_MARKET_SNAPSHOT, all_values),
            ),
            "ai_opportunities": apply_policy(
                "opportunities",
                fill_ai_template(OPPORTUNITY_INSIGHT, all_values),
            ),
            "ai_risk": apply_policy(
                "risk",
                fill_ai_template(RISK_INSIGHT, all_values),
            ),
            "ai_final_decision": apply_policy(
                "final_decision",
                final_decision_text,
            ),
        }
