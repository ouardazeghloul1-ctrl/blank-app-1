# =========================================
# عقل التقرير الاستشاري – Warda Intelligence
# =========================================

# ملاحظة معمارية:
# هذا العقل لا يجلب بيانات بنفسه
# يعتمد فقط على market_data و real_data القادمة من orchestrator

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
        """
        عقل استشاري نصي بحت - لا يعتمد على أي أنظمة خارجية
        كل البيانات تأتي من orchestrator عبر market_data و real_data
        """
        pass

    def generate_all_insights(self, user_info, market_data, real_data):
        """
        توليد الرؤى النصية حسب الباقة
        يعتمد فقط على market_data و real_data القادمة من orchestrator
        
        ملاحظة: real_data غير مستخدم حاليًا
        مخصص للتوسعة المستقبلية دون كسر التوقيع
        """
        city = user_info.get("city", "المدينة")
        package = user_info.get("package") or user_info.get("chosen_pkg") or "مجانية"
        policy = AI_PACKAGE_POLICY.get(package, AI_PACKAGE_POLICY["مجانية"])

        # =========================================
        # اشتقاق إشارات السوق من market_data
        # =========================================
        growth = market_data.get("معدل_النمو_الشهري", 0)
        liquidity = market_data.get("مؤشر_السيولة", 50)

        # تحديد اتجاه الأسعار
        if growth > 2:
            price_trend = "صاعد"
        elif growth < -2:
            price_trend = "هابط"
        else:
            price_trend = "مستقر"

        # تحديد مستوى الطلب من السيولة
        if liquidity >= 75:
            demand_level = "مرتفع"
        elif liquidity <= 40:
            demand_level = "ضعيف"
        else:
            demand_level = "انتقائي"

        # تحديد مستوى المخاطر
        if growth < -3:
            risk_level = "مرتفع"
        elif abs(growth) <= 1:
            risk_level = "منخفض"
        else:
            risk_level = "متوسط"

        # إشارات السوق (إن وُجدت)
        market_signals = {
            "سرعة_البيع": market_data.get("سرعة_البيع", "متوسطة"),
            "التغير_اليومي": market_data.get("التغير_اليومي", "0%"),
        }

        # إشارات مشتقة من البيانات الحقيقية
        derived_signals = {
            "اتجاه_الأسعار": price_trend,
            "مستوى_الطلب": demand_level,
            "مستوى_المخاطر_العام": risk_level,
        }

        base_values = {
            "المدينة": city,
        }

        # دمج شامل وآمن - مع إضافة الإشارات المشتقة
        all_values = {
            **DEFAULT_AI_VALUES,
            **base_values,
            **market_signals,
            **derived_signals,
        }

        def apply_policy(key, text):
            mode = policy.get(key, "hidden")
            if mode == "full":
                return text
            if mode == "summary":
                return text.split("\n")[0] + "\n(ملخص تنفيذي)"
            return ""

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
        }
