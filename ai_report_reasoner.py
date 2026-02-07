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
# استخراج إشارات السوق الذكية
# =========================================

def extract_market_signals(real_data: pd.DataFrame) -> dict:
    signals = {}

    if real_data is None or real_data.empty:
        return signals

    # الطلب
    days_col = next(
        (c for c in ["days_on_market", "مدة_السوق", "أيام_السوق"] if c in real_data.columns),
        None,
    )

    if days_col:
        avg_days = real_data[days_col].mean()
        if pd.notna(avg_days):
            signals["مستوى_الطلب"] = (
                "مرتفع" if avg_days < 30 else "متوسط" if avg_days < 60 else "ضعيف"
            )
    else:
        signals["مستوى_الطلب"] = "غير محدد"

    # حالة السوق
    price_col = next(
        (c for c in ["price", "السعر", "سعر", "سعر_المتر"] if c in real_data.columns),
        None,
    )

    if price_col:
        std = real_data[price_col].std()
        mean = real_data[price_col].mean()
        if pd.notna(std) and pd.notna(mean) and mean > 0:
            ratio = std / mean
            signals["حالة_السوق"] = (
                "حالة توازن"
                if ratio < 0.1
                else "توازن حذر"
                if ratio < 0.2
                else "تذبذب مرتفع"
            )
        else:
            signals["حالة_السوق"] = "بيانات غير كافية"
    else:
        signals["حالة_السوق"] = "غير متاحة"

    # مزاج السوق
    if signals.get("مستوى_الطلب") == "مرتفع" and signals.get("حالة_السوق") == "حالة توازن":
        signals["مزاج_السوق"] = "إيجابي غير اندفاعي"
    elif signals.get("مستوى_الطلب") == "ضعيف":
        signals["مزاج_السوق"] = "حذر وانتقائي"
    else:
        signals["مزاج_السوق"] = "انتقائي"

    return signals


def fill_ai_template(template: str, signals: dict) -> str:
    if not template:
        return ""
    for k, v in signals.items():
        template = template.replace(f"{{{k}}}", str(v))
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

        market_signals = extract_market_signals(real_data)

        # ضمان market_data (عدم السماح بالأصفار)
        liquidity = market_data.get("مؤشر_السيولة", 50) or 50
        growth = market_data.get("معدل_النمو_الشهري", 1.0) or 1.0

        safe_market_data = {
            "مؤشر_السيولة": liquidity,
            "معدل_النمو_الشهري": growth,
        }

        # البيانات الحية
        self.live_system.update_live_data(real_data)
        live_summary = self.live_system.get_live_data_summary(city)
        live_indicators = live_summary.get("مؤشرات_حية", {})

        market_insights = self.market_intel.advanced_market_analysis(real_data, user_info)

        values = {
            "المدينة": city,
            "سرعة_البيع": live_indicators.get("سرعة_البيع", "غير متوفر"),
            "التغير_اليومي": live_indicators.get("التغير_اليومي", "غير متوفر"),
            "اتجاه_الأسعار": market_data.get("اتجاه_الاسعار", "مستقر"),
            "مستوى_المخاطر_العام": market_insights.get("risk_assessment", {}).get(
                "overall_risk", "متوسط"
            ),
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

        # ✅ الخلاصة التنفيذية – الكتل الست
        final_decision_text = generate_executive_summary(
            user_info=user_info,
            market_data=safe_market_data,
            real_data=real_data,
        )

        all_values = {**values, **market_signals}

        return {
            "ai_live_market": fill_ai_template(
                apply_policy("live_market", LIVE_MARKET_SNAPSHOT.format(**all_values)),
                market_signals,
            ),
            "ai_opportunities": fill_ai_template(
                apply_policy("opportunities", OPPORTUNITY_INSIGHT.format(**all_values)),
                market_signals,
            ),
            "ai_risk": fill_ai_template(
                apply_policy("risk", RISK_INSIGHT.format(**all_values)),
                market_signals,
            ),
            "ai_final_decision": apply_policy("final_decision", final_decision_text),
        }
