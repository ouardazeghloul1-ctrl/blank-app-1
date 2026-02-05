# ai_executive_summary.py
# =========================================
# Executive Decision Engine – Warda Intelligence
# Decision Authority Layer (MASIA DIAMOND+)
# =========================================

import pandas as pd
from smart_opportunities import SmartOpportunityFinder


# =========================
# 🧠 Decision Object
# =========================
class FinalDecision:
    def __init__(
        self,
        action,
        confidence,
        horizon,
        summary_text,
        rationale,
        risks,
        change_triggers
    ):
        self.action = action              # BUY / WAIT / AVOID
        self.confidence = confidence      # 0.0 – 1.0
        self.horizon = horizon            # "3–5 years"
        self.summary_text = summary_text  # النص الاستشاري الكامل
        self.rationale = rationale        # list[str]
        self.risks = risks                # list[str]
        self.change_triggers = change_triggers


# =========================
# 🎯 Decision Builder (العقل الحاكم)
# =========================
def build_final_decision(user_info, market_data, real_data):
    """
    يبني القرار الاستثماري النهائي كنظام
    (وليس كنص فقط)
    """

    if real_data is None or real_data.empty:
        return FinalDecision(
            action="AVOID",
            confidence=0.90,
            horizon="غير محدد",
            summary_text=(
                "تعذر إصدار قرار استثماري موثوق بسبب غياب بيانات سوقية فعلية. "
                "أي قرار في هذه الحالة يُعد مخاطرة غير محسوبة."
            ),
            rationale=["غياب البيانات الفعلية"],
            risks=["اتخاذ قرار دون أساس رقمي"],
            change_triggers=["توفر بيانات سوقية حقيقية قابلة للتحليل"]
        )

    city = user_info.get("city", "المدينة")
    property_type = user_info.get("property_type", "العقار")

    # =========================
    # 📊 الأساس الرقمي
    # =========================
    total_properties = len(real_data)
    avg_price_m2 = real_data["سعر_المتر"].mean()
    min_price_m2 = real_data["سعر_المتر"].min()
    max_price_m2 = real_data["سعر_المتر"].max()

    avg_return = (
        real_data["العائد_المتوقع"].mean()
        if "العائد_المتوقع" in real_data.columns
        else None
    )

    # =========================
    # 🧠 Smart Opportunities
    # =========================
    finder = SmartOpportunityFinder()
    undervalued = finder.find_undervalued_properties(real_data, city)
    rising_areas = finder.predict_rising_areas(real_data, city)
    timing = finder.get_golden_timing(market_data)

    undervalued_count = len(undervalued)
    best_discount = (
        max(float(o["الخصم"].replace("%", "")) for o in undervalued)
        if undervalued else 0
    )
    top_areas = [a["المنطقة"] for a in rising_areas[:3]]

    # =========================
    # 📈 مؤشرات السوق
    # =========================
    growth = market_data.get("معدل_النمو_الشهري", 0)
    liquidity = market_data.get("مؤشر_السيولة", 0)

    # =========================
    # 🚦 منطق القرار
    # =========================
    action = "WAIT"
    confidence = 0.55
    rationale = []
    risks = []
    change_triggers = []

    if undervalued_count >= 3 and best_discount >= 15 and liquidity >= 60:
        action = "BUY"
        confidence = 0.82
        rationale = [
            "وجود فجوات سعرية حقيقية تتجاوز 15%",
            "تحسن تشغيلي واضح في مناطق محددة",
            "سيولة سوقية تسمح بالخروج عند الحاجة"
        ]
        risks = [
            "تغير مفاجئ في السيولة",
            "زيادة غير متوقعة في المعروض"
        ]
        change_triggers = [
            "اتساع الفجوة بين السعر المعروض والمنفذ",
            "ارتفاع مدة بقاء العقار في السوق"
        ]

    elif liquidity < 50 or growth < 1:
        action = "AVOID"
        confidence = 0.78
        rationale = [
            "ضعف السيولة الحالية",
            "تباطؤ النمو دون مؤشرات انعكاس"
        ]
        risks = [
            "تآكل العائد",
            "تجميد رأس المال"
        ]
        change_triggers = [
            "تحسن السيولة فوق 60",
            "عودة النمو الشهري فوق 1.5%"
        ]

    else:
        action = "WAIT"
        confidence = 0.60
        rationale = [
            "السوق انتقائي والفرص الواضحة محدودة",
            "عدم اكتمال إشارات الدخول الآمن"
        ]
        risks = [
            "تفويت فرصة أفضل لاحقًا"
        ]
        change_triggers = [
            "ظهور خصومات حقيقية جديدة",
            "تحسن مؤشرات الطلب الفعلي"
        ]

    # =========================
    # 🏁 النص الاستشاري (كما تحبينه)
    # =========================
    summary_text = f"""
🏁 الخلاصة الاستشارية التنفيذية
{city} – {property_type}

• القرار: {action}
• درجة الثقة: {int(confidence * 100)}%
• الأفق الزمني: 3–5 سنوات

• تم تحليل {total_properties} عقارًا فعليًا
• متوسط سعر المتر: {avg_price_m2:,.0f} ريال
• النطاق السعري: {min_price_m2:,.0f} – {max_price_m2:,.0f} ريال/م²
{f"• متوسط العائد المتوقع: {avg_return:.1f}%" if avg_return else ""}

• أعلى خصم مكتشف: {best_discount:.1f}%
• المناطق الأكثر جاذبية: {", ".join(top_areas) if top_areas else "غير مكتملة حاليًا"}

هذا القرار مبني على بيانات فعلية وتحليل سلوكي،
ولا يعتمد على سيناريو متفائل واحد.
"""

    return FinalDecision(
        action=action,
        confidence=confidence,
        horizon="3–5 years",
        summary_text=summary_text.strip(),
        rationale=rationale,
        risks=risks,
        change_triggers=change_triggers
    )


# =========================
# واجهة قديمة (نحافظ عليها)
# =========================
def generate_executive_summary(user_info, market_data, real_data):
    """
    للحفاظ على التوافق مع بقية النظام
    """
    decision = build_final_decision(user_info, market_data, real_data)
    return decision.summary_text
