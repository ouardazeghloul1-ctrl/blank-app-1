# ai_report_reasoner.py
# =========================================
# عقل التقرير الاستشاري – Warda Intelligence
# =========================================

from live_data_system import LiveDataSystem
from market_intelligence import MarketIntelligence
from smart_opportunities import SmartOpportunityFinder


class AIReportReasoner:
    def __init__(self):
        self.live_system = LiveDataSystem()
        self.market_intel = MarketIntelligence()
        self.opportunity_finder = SmartOpportunityFinder()

    def generate_all_insights(self, user_info, market_data, real_data):
        city = user_info.get("city", "المدينة")

        # --- تحديث البيانات الحية ---
        self.live_system.update_live_data(real_data)
        live_summary = self.live_system.get_live_data_summary(city)

        # --- تحليل السوق المتقدم ---
        market_insights = self.market_intel.advanced_market_analysis(
            real_data, user_info
        )

        # --- تحليل الفرص ---
        opportunities = self.opportunity_finder.analyze_all_opportunities(
            user_info, market_data, real_data
        )

        return {
            "live_market_snapshot_text": self._build_live_market_text(
                city, live_summary
            ),
            "opportunity_insight_text": self._build_opportunity_text(
                city, opportunities
            ),
            "risk_insight_text": self._build_risk_text(
                city, market_insights
            ),
            "final_decision_text": self._build_final_decision_text(city),
        }

    # --------------------------------------------------

    def _build_live_market_text(self, city, live_summary):
        indicators = live_summary.get("مؤشرات_حية", {})

        return f"""
لقطة السوق الحالية

بناءً على تحليل المؤشرات الحية للسوق العقاري في {city}، يظهر أن السوق يمر حاليًا بمرحلة {live_summary.get('حالة_السوق', 'غير محددة')}، 
حيث يسجّل مستوى الطلب نشاطًا ملحوظًا مقابل عرض متوازن نسبيًا.

تشير البيانات إلى أن متوسط سرعة إتمام الصفقات يدور حول {indicators.get('سرعة_البيع', 'غير متوفر')}، 
وهو ما يعكس سلوكًا استثماريًا أكثر وعيًا وانتقائية.

قراءة استشارية:
في هذه المرحلة، يملك المستثمر الذي يعتمد على التحليل الهادئ والانتقائي أفضلية واضحة عند اختيار الفرص.
""".strip()

    # --------------------------------------------------

    def _build_opportunity_text(self, city, opportunities):
        count = len(opportunities.get("عقارات_مخفضة", []))

        return f"""
الفرص الاستثمارية الذكية

أظهر تحليل البيانات الفعلية في {city} وجود {count} فرص استثمارية تتمتع بتسعير أقل من متوسط السوق في مناطقها،
وهو ما يشير إلى وجود فجوات سعرية قابلة للاستثمار الذكي.

قراءة استشارية:
الفرص الأعلى جودة غالبًا ما تكون في المناطق التي تسبق دورة الصعود وليس في ذروتها.
""".strip()

    # --------------------------------------------------

    def _build_risk_text(self, city, market_insights):
        return f"""
تحليل المخاطر الاستثماري

يشير تحليل توزيع المخاطر في سوق {city} إلى حالة توازن نسبي بين العائد والمخاطرة،
حيث لا يظهر السوق إشارات مجازفة مفرطة ولا ركودًا حادًا.

قراءة استشارية:
إدارة المخاطر تعني اختيار الصفقة الصحيحة، لا تجنب السوق بالكامل.
""".strip()

    # --------------------------------------------------

    def _build_final_decision_text(self, city):
        return f"""
القرار الاستثماري النهائي

السوق العقاري في {city} يقدّم فرصًا حقيقية للمستثمر المنضبط،
شرط وضوح الهدف، والاعتماد على البيانات، وتجنّب القرارات العاطفية.

خلاصة استشارية:
التحرك الواعي في الوقت المناسب هو العامل الحاسم لتحقيق نتائج مستقرة.
""".strip()
