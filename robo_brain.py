# robo_chat/robo_brain.py

class RoboAdvisor:
    def __init__(self, user_profile, knowledge, guard):
        self.user = user_profile
        self.knowledge = knowledge
        self.guard = guard

    def answer(self, question: str) -> str:
        city = self.user.get("city")

        if "السوق" in question or "الوضع" in question:
            return self._market_answer(city)

        if "فرصة" in question or "استثمار" in question:
            return self._opportunity_answer(city)

        return "سؤالك مهم، هل تقصـدين السوق أم الفرص الاستثمارية؟"

    def _market_answer(self, city):
        summary = self.knowledge.market_summary(city)

        if not self.guard.allow("فضية"):
            return summary + "\n🔒 التحليل التفصيلي متاح في الباقة الفضية."

        return summary + "\n📊 التحليل العميق متوفر حسب باقتك."

    def _opportunity_answer(self, city):
        if not self.guard.allow("ذهبية"):
            return (
                f"أرصد فرصًا في {city}، لكن التفاصيل الدقيقة "
                "تتطلب الباقة الذهبية أو أعلى."
            )

        ops = self.knowledge.today_opportunities(city)
        if not ops:
            return f"اليوم لا توجد فرص قوية في {city}، وهذا بحد ذاته إشارة ذكية."

        return f"""
📌 تم رصد فرصة ذكية اليوم في {city}.

عدد الفرص الظاهرة: {len(ops)}
التحليل الكامل + التوقيت متاح للماسية.
"""
