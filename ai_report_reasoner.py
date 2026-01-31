# ai_report_reasoner.py
# =========================================
# عقل التقرير الاستشاري – Warda Intelligence
# =========================================

from live_data_system import LiveDataSystem
from market_intelligence import MarketIntelligence
from smart_opportunities import SmartOpportunityFinder
from ai_text_templates import (
    LIVE_MARKET_SNAPSHOT,
    OPPORTUNITY_INSIGHT,
    RISK_INSIGHT,
    FINAL_DECISION,
)


class AIReportReasoner:
    def __init__(self):
        self.live_system = LiveDataSystem()
        self.market_intel = MarketIntelligence()
        self.opportunity_finder = SmartOpportunityFinder()

    def generate_all_insights(self, user_info, market_data, real_data):
        city = user_info.get("city", "المدينة")

        # =========================
        # البيانات الحية
        # =========================
        self.live_system.update_live_data(real_data)
        live_summary = self.live_system.get_live_data_summary(city)
        live_indicators = live_summary.get("مؤشرات_حية", {})

        # =========================
        # ذكاء السوق
        # =========================
        market_insights = self.market_intel.advanced_market_analysis(
            real_data, user_info
        )

        # =========================
        # الفرص الذكية
        # =========================
        opportunities = self.opportunity_finder.analyze_all_opportunities(
            user_info, market_data, real_data
        )

        # =========================
        # تعبئة القيم
        # =========================
        values = {
            "المدينة": city,
            "حالة_السوق": live_summary.get("حالة_السوق", "غير محددة"),
            "مستوى_الطلب": live_indicators.get("مؤشر_الطلب", "غير متوفر"),
            "مستوى_العرض": live_indicators.get("مؤشر_العرض", "غير متوفر"),
            "سرعة_البيع": live_indicators.get("سرعة_البيع", "غير متوفر"),
            "التغير_اليومي": live_indicators.get("التغير_اليومي", "غير متوفر"),
            "اتجاه_الأسعار": market_data.get("اتجاه_الاسعار", "مستقر"),
            "مزاج_السوق": live_summary.get("حالة_السوق", "متوازن"),
            "مستوى_المخاطر_العام": market_insights
            .get("risk_assessment", {})
            .get("overall_risk", "متوسط"),
        }

        return {
            "ai_live_market": self._fill_template(
                LIVE_MARKET_SNAPSHOT, values
            ),
            "ai_opportunities": self._fill_template(
                OPPORTUNITY_INSIGHT, values
            ),
            "ai_risk": self._fill_template(
                RISK_INSIGHT, values
            ),
            "ai_final_decision": self._fill_template(
                FINAL_DECISION, values
            ),
        }

    def _fill_template(self, text: str, values: dict) -> str:
        """
        استبدال {{المفاتيح}} بالقيم الفعلية
        """
        for key, val in values.items():
            text = text.replace(f"{{{{{key}}}}}", str(val))
        return text
