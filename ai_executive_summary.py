# ai_executive_summary.py
# =========================================
# Executive Decision Engine – Warda Intelligence (Diamond Tier)
# =========================================

from smart_opportunities import SmartOpportunityFinder


class FinalDecision:
    def __init__(
        self,
        stance: str,                 # موقف الحركة العام
        confidence: float,           # 0.00 – 1.00
        horizon: str,                # أفق زمني
        rationale: list,             # لماذا هذا القرار
        risks: list,                 # المخاطر
        decision_cost: list,         # كلفة تجاهل القرار
        boundaries: list,            # حدود صلاحية القرار
        best_mistake: list,          # أفضل خطأ مقبول
        change_triggers: list,       # متى نعيد التقييم
        execution_guidance: list,    # كيف يتصرف عمليًا
        regret_index: list           # مؤشر الندم المستقبلي
    ):
        self.stance = stance
        self.confidence = confidence
        self.horizon = horizon
        self.rationale = rationale
        self.risks = risks
        self.decision_cost = decision_cost
        self.boundaries = boundaries
        self.best_mistake = best_mistake
        self.change_triggers = change_triggers
        self.execution_guidance = execution_guidance
        self.regret_index = regret_index

    def to_text(self) -> str:
        lines = []

        lines.append("🏁 القرار الاستشاري التنفيذي النهائي")
        lines.append("")

        lines.append(f"• موقف الحركة الحالي: {self.stance}")
        lines.append(f"• درجة الثقة في هذا القرار: {int(self.confidence * 100)}%")
        lines.append(f"• الأفق الزمني المرجعي: {self.horizon}")
        lines.append("")

        lines.append("🔎 لماذا هذا هو الموقف الأنسب الآن؟")
        for r in self.rationale:
            lines.append(f"- {r}")

        lines.append("")
        lines.append("⚠️ المخاطر التي يجب مراقبتها:")
        for r in self.risks:
            lines.append(f"- {r}")

        lines.append("")
        lines.append("💰 كلفة تجاهل هذا القرار:")
        for c in self.decision_cost:
            lines.append(f"- {c}")

        lines.append("")
        lines.append("🚧 حدود صلاحية هذا القرار:")
        for b in self.boundaries:
            lines.append(f"- {b}")

        lines.append("")
        lines.append("🎯 في حال حدوث خطأ، هذا هو الخطأ الأقل ضررًا:")
        for m in self.best_mistake:
            lines.append(f"- {m}")

        lines.append("")
        lines.append("⏳ متى يجب إعادة تقييم هذا الموقف؟")
        for t in self.change_triggers:
            lines.append(f"- {t}")

        lines.append("")
        lines.append("🧭 كيف تتصرف عمليًا بعد إغلاق هذا التقرير:")
        for g in self.execution_guidance:
            lines.append(f"- {g}")

        lines.append("")
        lines.append("📉 مؤشر الندم المستقبلي:")
        for r in self.regret_index:
            lines.append(f"- {r}")

        return "\n".join(lines)


def generate_executive_summary(user_info, market_data, real_data):
    if real_data is None or real_data.empty:
        return (
            "❌ لا يمكن إصدار قرار استشاري موثوق لغياب بيانات سوقية فعلية.\n"
            "يوصى بالاكتفاء بالمراقبة الذكية إلى حين توفر بيانات قابلة للتحليل."
        )

    city = user_info.get("city", "المدينة")

    finder = SmartOpportunityFinder()
    undervalued = finder.find_undervalued_properties(real_data, city)

    liquidity = market_data.get("مؤشر_السيولة", 55)
    growth = market_data.get("معدل_النمو_الشهري", 1.0)

    # =========================
    # منطق اتخاذ موقف الحركة
    # =========================

    if liquidity >= 60 and growth >= 1.2 and len(undervalued) >= 3:
        decision = FinalDecision(
            stance="التحرك المدروس",
            confidence=0.86,
            horizon="5–7 سنوات",
            rationale=[
                "الطلب الحالي يعكس استخدامًا فعليًا لا اندفاعًا مؤقتًا",
                "وجود فجوات سعرية مقارنة بالقيمة التشغيلية",
                "السيولة تسمح بالحركة دون ضغط تخارج"
            ],
            risks=[
                "زيادة غير متوقعة في المعروض",
                "تغيرات تنظيمية محتملة"
            ],
            decision_cost=[
                "تفويت فجوات سعرية قد لا تتكرر",
                "الانتظار قد يؤدي لارتفاع تكلفة الدخول"
            ],
            boundaries=[
                "ارتفاع الأسعار أكثر من 12% خلال 6 أشهر",
                "تراجع السيولة دون مستوى 50"
            ],
            best_mistake=[
                "التأخر في الدخول أفضل من الدخول في أصل ضعيف",
                "تقليل حجم الحركة أفضل من التوسع المفرط"
            ],
            change_triggers=[
                "تراجع مؤشر السيولة",
                "اختفاء الفجوات السعرية"
            ],
            execution_guidance=[
                "التحرك بهدف واضح (استقرار / تشغيل / تخارج)",
                "عدم ربط القرار بالمقارنة مع الآخرين",
                "مراجعة الموقف كل 6 أشهر"
            ],
            regret_index=[
                "مرتفع عند تجاهل الإطار التحليلي",
                "منخفض عند الالتزام بخطة منضبطة"
            ]
        )

    elif liquidity < 45 or growth < 0.8:
        decision = FinalDecision(
            stance="تجنب التنفيذ حاليًا",
            confidence=0.79,
            horizon="3–5 سنوات",
            rationale=[
                "ضعف السيولة يقلل مرونة القرار",
                "اتجاه النمو غير مستقر"
            ],
            risks=[
                "تجميد القرار لفترة أطول من المتوقع"
            ],
            decision_cost=[
                "الدخول في هذا التوقيت قد يؤدي لخروج غير مرن"
            ],
            boundaries=[
                "تحسن السيولة فوق مستوى 60",
                "استقرار النمو الشهري"
            ],
            best_mistake=[
                "تفويت فرصة أفضل من دخول سيئ"
            ],
            change_triggers=[
                "تحسن مؤشرات الطلب الحقيقي"
            ],
            execution_guidance=[
                "الاكتفاء بالمراقبة دون التزام",
                "تحديث القراءة دوريًا"
            ],
            regret_index=[
                "مرتفع عند الدخول بدافع الضغط",
                "منخفض عند الصبر التحليلي"
            ]
        )

    else:
        decision = FinalDecision(
            stance="الترقب الذكي",
            confidence=0.82,
            horizon="2–4 سنوات",
            rationale=[
                "السوق في مرحلة انتقائية",
                "الإشارات لم تكتمل بعد"
            ],
            risks=[
                "الدخول المبكر",
                "تفويت فرص أوضح لاحقًا"
            ],
            decision_cost=[
                "التحرك العشوائي قد يربك المسار"
            ],
            boundaries=[
                "ظهور خصومات تشغيلية حقيقية",
                "تحسن مؤشرات الطلب"
            ],
            best_mistake=[
                "الانتظار أفضل من قرار غير مكتمل"
            ],
            change_triggers=[
                "تغير سلوك السوق بشكل واضح"
            ],
            execution_guidance=[
                "الاستعداد المالي دون التزام",
                "إعادة التقييم كل 3 أشهر"
            ],
            regret_index=[
                "مرتفع عند التسرع",
                "منخفض عند الانضباط"
            ]
        )

    return decision.to_text()
