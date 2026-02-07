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

# =========================================
# سقف الذكاء حسب الباقة
# =========================================

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
            "note": "التحليل مبني على عينة بيانات محدودة"
        }

    if count < 150:
        return {
            "level": "متوسط",
            "tone": "تحليلي",
            "confidence": "جيدة",
            "note": "التحليل يعكس اتجاهات مستقرة نسبيًا"
        }

    return {
        "level": "مرتفع",
        "tone": "استشاري",
        "confidence": "عالية",
        "note": "التحليل يستند إلى قاعدة بيانات قوية"
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
# استخراج إشارات السوق الذكية
# =========================================

def extract_market_signals(real_data: pd.DataFrame) -> dict:
    signals = {}

    if real_data is None or real_data.empty:
        return {}

    # مستوى الطلب
    days_col = None
    for col in ["days_on_market", "مدة_السوق", "أيام_السوق"]:
        if col in real_data.columns:
            days_col = col
            break

    if days_col:
        avg_days = real_data[days_col].mean()
        if pd.notna(avg_days):
            if avg_days < 30:
                signals["مستوى_الطلب"] = "مرتفع"
            elif avg_days < 60:
                signals["مستوى_الطلب"] = "متوسط"
            else:
                signals["مستوى_الطلب"] = "ضعيف"
    else:
        signals["مستوى_الطلب"] = "غير محدد"

    # حالة السوق
    price_col = None
    for col in ["price", "السعر", "سعر", "سعر_المتر"]:
        if col in real_data.columns:
            price_col = col
            break

    if price_col:
        price_std = real_data[price_col].std()
        price_mean = real_data[price_col].mean()

        if pd.notna(price_std) and pd.notna(price_mean) and price_mean > 0:
            ratio = price_std / price_mean
            if ratio < 0.1:
                signals["حالة_السوق"] = "توازن"
            elif ratio < 0.2:
                signals["حالة_السوق"] = "توازن حذر"
            else:
                signals["حالة_السوق"] = "تذبذب مرتفع"
        else:
            signals["حالة_السوق"] = "بيانات غير كافية"
    else:
        signals["حالة_السوق"] = "بيانات غير مكتملة"

    # مزاج السوق
    if signals.get("مستوى_الطلب") == "مرتفع" and signals.get("حالة_السوق") == "توازن":
        signals["مزاج_السوق"] = "إيجابي غير اندفاعي"
    elif signals.get("مستوى_الطلب") == "ضعيف":
        signals["مزاج_السوق"] = "حذر وانتقائي"
    else:
        signals["مزاج_السوق"] = "انتقائي"

    # ✅ ضمان المتغيرات المطلوبة للقوالب
    signals.setdefault("مستوى_العرض", "غير محدد")

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
        package = (
            user_info.get("package")
            or user_info.get("chosen_pkg")
            or "مجانية"
        )

        policy = AI_PACKAGE_POLICY.get(package, AI_PACKAGE_POLICY["مجانية"])

        raw_depth = get_analysis_depth(real_data)
        analysis_depth = apply_intelligence_cap(raw_depth, package)

        # إشارات السوق
        market_signals = extract_market_signals(real_data)

        # البيانات الحية
        self.live_system.update_live_data(real_data)
        live_summary = self.live_system.get_live_data_summary(city)
        live_indicators = live_summary.get("مؤشرات_حية", {})

        # ذكاء السوق
        market_insights = self.market_intel.advanced_market_analysis(
            real_data, user_info
        )

        values = {
            "المدينة": city,
            "سرعة_البيع": live_indicators.get("سرعة_البيع", "غير متوفر"),
            "التغير_اليومي": live_indicators.get("التغير_اليومي", "غير متوفر"),
            "اتجاه_الأسعار": market_data.get("اتجاه_الاسعار", "مستقر"),
            "مستوى_المخاطر_العام": market_insights
                .get("risk_assessment", {})
                .get("overall_risk", "متوسط"),
            "عمق_التحليل": analysis_depth["level"],
            "نبرة_التحليل": analysis_depth["tone"],
            "مستوى_الثقة": analysis_depth["confidence"],
            "ملاحظة_البيانات": analysis_depth["note"],
        }

        def apply_policy(key, text):
            mode = policy.get(key, "hidden")
            if mode == "full":
                return text
            if mode == "summary":
                return text.split("\n\n")[0] + "\n\n(ملخص تنفيذي مختصر)"
            return ""

        # القرار التنبؤي النهائي
        final_decision_text = generate_executive_summary(
            user_info=user_info,
            market_data=market_data,
            real_data=real_data
        )

        all_values = {**values, **market_signals}

        live_market_text = apply_policy(
            "live_market",
            LIVE_MARKET_SNAPSHOT.format(**all_values)
        )

        opportunities_text = apply_policy(
            "opportunities",
            OPPORTUNITY_INSIGHT.format(**all_values)
        )

        risk_text = apply_policy(
            "risk",
            RISK_INSIGHT.format(**all_values)
        )

        return {
            "ai_live_market": fill_ai_template(live_market_text, market_signals),
            "ai_opportunities": fill_ai_template(opportunities_text, market_signals),
            "ai_risk": fill_ai_template(risk_text, market_signals),
            "ai_final_decision": apply_policy(
                "final_decision",
                final_decision_text
            ),
        }
