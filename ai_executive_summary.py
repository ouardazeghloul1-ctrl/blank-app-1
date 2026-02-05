# ai_executive_summary.py
# =========================================
# Executive Decision Engine – Warda Intelligence
# =========================================

import pandas as pd
from smart_opportunities import SmartOpportunityFinder


# =========================================
# 🧠 الكيان التنفيذي الحاكم للقرار
# =========================================
class FinalDecision:
    def __init__(
        self,
        action: str,
        confidence: float,
        horizon: str,
        rationale: list,
        risks: list,
        change_triggers: list,
        execution_guidance: list
    ):
        self.action = action              # BUY / WAIT / AVOID
        self.confidence = confidence      # 0.00 – 1.00
        self.horizon = horizon            # "3–5 years"
        self.rationale = rationale
        self.risks = risks
        self.change_triggers = change_triggers
        self.execution_guidance = execution_guidance

    def to_text(self) -> str:
        """
        يحول القرار إلى نص تنفيذي فاخر (10,000$ decision style)
        """
        lines = []

        lines.append("القرار التنفيذي الاستثماري")
        lines.append("")

        lines.append(f"• التوصية: {self.action}")
        lines.append(f"• درجة الثقة: {int(self.confidence * 100)}%")
        lines.append(f"• الأفق الزمني: {self.horizon}")
        lines.append("")

        lines.append("لماذا هذا القرار؟")
        for r in self.rationale:
            lines.append(f"- {r}")

        lines.append("")
        lines.append("المخاطر التي نراقبها:")
        for r in self.risks:
            lines.append(f"- {r}")

        lines.append("")
        lines.append("متى نعيد النظر؟")
        for t in self.change_triggers:
            lines.append(f"- {t}")

        lines.append("")
        lines.append("كيف تتصرف عمليًا الآن:")
        for g in self.execution_guidance:
            lines.append(f"- {g}")

        return "\n".join(lines)


# =========================================
# 🧠 مولد الخلاصة التنفيذية
# =========================================
def generate_executive_summary(user_info, market_data, real_data):
    if real_data is None or real_data.empty:
        return (
            "❌ تعذر إصدار قرار استثماري موثوق بسبب غياب البيانات الفعلية.\n"
            "يوصى بعدم اتخاذ أي إجراء حتى توفر بيانات حقيقية قابلة للتحليل."
        )

    city = user_info.get("city", "المدينة")
    property_type = user_info.get("property_type", "العقار")

    finder = SmartOpportunityFinder()

    undervalued = finder.find_undervalued_properties(real_data, city)
    liquidity = market_data.get("مؤشر_السيولة", 0)
    growth = market_data.get("معدل_النمو_الشهري", 0)

    # =========================
    # 🚦 منطق القرار
    # =========================
    if liquidity >= 60 and growth >= 1.2 and len(undervalued) >= 3:
        decision = FinalDecision(
            action="BUY",
            confidence=0.87,
            horizon="5–7 سنوات",
            rationale=[
                "الطلب حقيقي وليس مضاربيًا",
                "وجود فجوات سعرية أقل من القيمة التشغيلية",
                "السيولة تسمح بالخروج الآمن"
            ],
            risks=[
                "زيادة مفاجئة في المعروض",
                "تغير تنظيمي غير متوقع"
            ],
            change_triggers=[
                "انخفاض مؤشر السيولة دون 50",
                "اتساع مدة بقاء العقار في السوق"
            ],
            execution_guidance=[
                "التركيز على أصول ذات طلب تشغيلي فعلي",
                "عدم التوسع بأكثر من 20% من رأس المال",
                "مراجعة القرار كل 6 أشهر"
            ]
        )

    elif liquidity < 45 or growth < 0.8:
        decision = FinalDecision(
            action="AVOID",
            confidence=0.78,
            horizon="3–5 سنوات",
            rationale=[
                "ضعف السيولة الحالية",
                "عدم استقرار اتجاه النمو"
            ],
            risks=[
                "تجمّد رأس المال",
                "خروج صعب في السوق الثانوي"
            ],
            change_triggers=[
                "تحسن السيولة فوق 60",
                "عودة النمو فوق 1.2%"
            ],
            execution_guidance=[
                "وضع السوق تحت المراقبة فقط",
                "عدم الشراء أو الالتزام حاليًا",
                "الاستعداد السريع عند تحسن المؤشرات"
            ]
        )

    else:
        decision = FinalDecision(
            action="WAIT",
            confidence=0.81,
            horizon="2–4 سنوات",
            rationale=[
                "السوق انتقائي والفرص غير مكتملة",
                "التوازن لم يصل بعد لنقطة حسم"
            ],
            risks=[
                "الدخول المبكر",
                "فوات فرص أفضل لاحقًا"
            ],
            change_triggers=[
                "ظهور خصومات حقيقية",
                "تحسن مؤشرات الطلب"
            ],
            execution_guidance=[
                "المراقبة النشطة لا السلبية",
                "تجهيز التمويل دون التزام",
                "تحديث القرار كل 3 أشهر"
            ]
        )

    return decision.to_text()
