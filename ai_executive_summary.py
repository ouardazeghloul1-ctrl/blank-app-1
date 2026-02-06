# ai_executive_summary.py
# =========================================
# Executive Decision Engine – Warda Intelligence (Diamond Tier)
# =========================================

from smart_opportunities import SmartOpportunityFinder


class ExecutiveDecision:
    """
    كيان قرار استشاري محايد
    لا يفترض نوع الحركة
    بل يحدد الموقف الصحيح داخل دورة السوق
    """

    def __init__(
        self,
        market_phase: str,
        stance: str,
        confidence: float,
        horizon: str,
        value_signals: list,
        risk_watchlist: list,
        invalidation_triggers: list,
        execution_principles: list,
    ):
        self.market_phase = market_phase
        self.stance = stance
        self.confidence = confidence
        self.horizon = horizon
        self.value_signals = value_signals
        self.risk_watchlist = risk_watchlist
        self.invalidation_triggers = invalidation_triggers
        self.execution_principles = execution_principles

    def to_text(self) -> str:
        lines = []

        lines.append("القرار الاستشاري النهائي: موقعك الصحيح الآن")
        lines.append("")

        lines.append(f"• موقعك ضمن دورة السوق: {self.market_phase}")
        lines.append(f"• الموقف الاستثماري الأمثل: {self.stance}")
        lines.append(f"• درجة الثقة في هذا الموقف: {int(self.confidence * 100)}%")
        lines.append(f"• الأفق الزمني المرجعي: {self.horizon}")
        lines.append("")

        lines.append("لماذا هذا هو الموقف المنطقي حاليًا؟")
        for v in self.value_signals:
            lines.append(f"- {v}")

        lines.append("")
        lines.append("ما الذي يجب مراقبته دون استعجال؟")
        for r in self.risk_watchlist:
            lines.append(f"- {r}")

        lines.append("")
        lines.append("متى يصبح هذا القرار غير صالح؟")
        for t in self.invalidation_triggers:
            lines.append(f"- {t}")

        lines.append("")
        lines.append("كيف تتصرف بعد إغلاق هذا التقرير؟")
        for p in self.execution_principles:
            lines.append(f"- {p}")

        return "\n".join(lines)


def generate_executive_summary(user_info, market_data, real_data):
    if real_data is None or real_data.empty:
        return (
            "تعذر إصدار قرار استشاري موثوق لغياب بيانات سوقية فعلية.\n"
            "يوصى بالاكتفاء بالمراقبة إلى حين توفر بيانات قابلة للتحليل."
        )

    city = user_info.get("city", "المدينة")

    finder = SmartOpportunityFinder()
    undervalued = finder.find_undervalued_properties(real_data, city)
    rising_areas = finder.predict_rising_areas(real_data, city)
    timing = finder.get_golden_timing(market_data)

    liquidity = market_data.get("مؤشر_السيولة", 0)
    growth = market_data.get("معدل_النمو_الشهري", 0)

    # =========================
    # تحديد مرحلة السوق
    # =========================
    if len(undervalued) >= 3 and growth >= 1.2:
        market_phase = "مرحلة انتقائية مدعومة بالقيمة"
    elif growth < 1:
        market_phase = "مرحلة حذر وإعادة تموضع"
    else:
        market_phase = "مرحلة انتقالية تتطلب انضباطًا"

    # =========================
    # تحديد الموقف العام
    # =========================
    if liquidity >= 60 and len(undervalued) >= 3:
        stance = "التحرك المدروس"
        confidence = 0.86
    elif liquidity < 45 or growth < 0.8:
        stance = "تجنب التنفيذ في الوضع الحالي"
        confidence = 0.79
    else:
        stance = "الترقب الذكي"
        confidence = 0.82

    decision = ExecutiveDecision(
        market_phase=market_phase,
        stance=stance,
        confidence=confidence,
        horizon="3–5 سنوات",
        value_signals=[
            f"رصد {len(undervalued)} فجوة قيمة حقيقية مقارنة بمتوسطات السوق",
            f"وجود {len(rising_areas)} مناطق تُظهر إشارات صعود مبكرة" if rising_areas else
            "غياب إشارات صعود جماعي، ما يعزز الانتقائية",
            f"قراءة التوقيت الحالية: {timing}",
        ],
        risk_watchlist=[
            "اتساع الفجوة بين الأسعار المعروضة والمنفذة",
            "زيادة مفاجئة في المعروض دون نمو موازٍ في الطلب",
            "تغيرات تنظيمية قد تؤثر على بعض الفئات",
        ],
        invalidation_triggers=[
            "تراجع السيولة دون المستويات الصحية",
            "اختفاء الفجوات السعرية القائمة حاليًا",
            "تحول سلوك السوق من انتقائي إلى اندفاعي أو ركودي",
        ],
        execution_principles=[
            "التعامل مع هذا القرار كإطار، لا كأمر فوري",
            "عدم تعديل المسار بسبب الضجيج قصير المدى",
            "إعادة التقييم فقط عند تحقق إحدى إشارات التغيير أعلاه",
            "استخدام هذا القرار كمرجع ثابت خلال الأشهر القادمة",
        ],
    )

    return decision.to_text()
