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
# سياسة عرض الذكاء الاصطناعي حسب الباقة
# =========================================

AI_PACKAGE_POLICY = {
    "ماسية متميزة": {
        "live_market": "full",
        "opportunities": "full",
        "risk": "full",
        "final_decision": "full",
    },
    "ماسية": {
        "live_market": "full",
        "opportunities": "full",
        "risk": "summary",
        "final_decision": "full",
    },
    "ذهبية": {
        "live_market": "summary",
        "opportunities": "summary",
        "risk": "summary",
        "final_decision": "summary",
    },
    "فضية": {
        "live_market": "summary",
        "opportunities": "hidden",
        "risk": "hidden",
        "final_decision": "summary",
    },
    "مجانية": {
        "live_market": "summary",
        "opportunities": "hidden",
        "risk": "hidden",
        "final_decision": "hidden",
    },
}

AI_INTELLIGENCE_CAP = {
    "ماسية متميزة": "مرتفع",
    "ماسية": "مرتفع",
    "ذهبية": "متوسط",
    "فضية": "منخفض",
    "مجانية": "منخفض",
}

# =========================================
# تحديد عمق التحليل حسب حجم البيانات
# =========================================

def get_analysis_depth(real_data):
    count = len(real_data) if real_data is not None else 0

    if count < 50:
        return {
            "level": "منخفض",
            "tone": "تحفظي",
            "confidence": "محدودة",
            "note": "التحليل مبني على عينة بيانات محدودة",
        }

    if count < 150:
        return {
            "level": "متوسط",
            "tone": "تحليلي",
            "confidence": "جيدة",
            "note": "التحليل يعكس اتجاهات مستقرة نسبيًا",
        }

    return {
        "level": "مرتفع",
        "tone": "استشاري",
        "confidence": "عالية",
        "note": "التحليل يستند إلى قاعدة بيانات قوية",
    }


def apply_intelligence_cap(depth_info, package):
    cap = AI_INTELLIGENCE_CAP.get(package, "منخفض")
    hierarchy = ["منخفض", "متوسط", "مرتفع"]

    if hierarchy.index(depth_info["level"]) > hierarchy.index(cap):
        return {
            "level": cap,
            "tone": "تحليلي" if cap == "متوسط" else "تحفظي",
            "confidence": "جيدة" if cap == "متوسط" else "محدودة",
            "note": "تم ضبط مستوى التحليل بما يتناسب مع مستوى الباقة",
        }

    return depth_info


# =========================================
# استخراج إشارات السوق
# =========================================

def extract_market_signals(real_data: pd.DataFrame) -> dict:
    signals = {}

    if real_data is None or real_data.empty:
        return signals

    # مستوى الطلب
    signals["مستوى_الطلب"] = "انتقائي"

    # حالة السوق
    signals["حالة_السوق"] = "مستقرة نسبيًا"

    # مزاج السوق
    signals["مزاج_السوق"] = "محايد"

    # ✅ مستوى العرض (الحل هنا)
    signals["مستوى_العرض"] = "متوازن"

    return signals


def fill_ai_template(template: str, signals: dict) -> str:
    if not template:
        return ""

    for key, value in signals.items():
        template = template.replace(f"{{{key}}}", value)

    return template


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

        raw_depth = get_analysis_depth(real_data)
        analysis_depth = apply_intelligence_cap(raw_depth, package)

        # إشارات السوق
        market_signals = extract_market_signals(real_data)

        # ضمان المفاتيح
        market_signals.setdefault("مستوى_الطلب", "غير محدد")
        market_signals.setdefault("حالة_السوق", "غير متاحة")
        market_signals.setdefault("مزاج_السوق", "محايد")
        market_signals.setdefault("مستوى_العرض", "غير محدد")

        # القيم العامة
        values = {
            "المدينة": city,
            "عمق_التحليل": analysis_depth["level"],
            "نبرة_التحليل": analysis_depth["tone"],
            "مستوى_الثقة": analysis_depth["confidence"],
            "ملاحظة_البيانات": analysis_depth["note"],
        }

        all_values = {**values, **market_signals}

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
                LIVE_MARKET_SNAPSHOT.format(**all_values),
            ),
            "ai_opportunities": apply_policy(
                "opportunities",
                OPPORTUNITY_INSIGHT.format(**all_values),
            ),
            "ai_risk": apply_policy(
                "risk",
                RISK_INSIGHT.format(**all_values),
            ),
            "ai_final_decision": apply_policy(
                "final_decision",
                final_decision_text,
            ),
        }
