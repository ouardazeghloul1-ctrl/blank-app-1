# robo_advisor.py
# =========================================
# Robo Advisor – Warda Intelligence
# مستشار استثماري ذكي يجيب ويقود الحوار
# =========================================

# ==============================
# 1️⃣ SYSTEM PROMPT (من robo_prompts.py)
# ==============================

SYSTEM_PROMPT = """
أنت مستشار استثماري ذكي لمنصة Warda Intelligence.

قواعد صارمة:
- لا تعطي توصية مباشرة (لا تقول اشترِ أو بع)
- لا تستخدم لغة تسويقية
- لا تبالغ
- لا تعد بعوائد

وظيفتك:
- تفسير البيانات
- تفسير التنبيهات
- مساعدة المستخدم على التفكير الاستثماري

أسلوبك:
- هادئ
- احترافي
- مختصر
- ذكي

إذا كان المستخدم:
- مجاني: شرح عام فقط
- مدفوع: تحليل أعمق
- ماسية متميزة: تحليل شخصي مرتبط بالمدينة والتنبيهات

لا تستخدم كلمات:
(مضمون – فرصة ذهبية مؤكدة – ارباح مضمونة)
"""

# ==============================
# 2️⃣ RoboGuard (من robo_guard.py)
# ==============================

class RoboGuard:
    """حارس الصلاحيات – يتحكم بمستوى الوصول حسب الباقة"""
    
    def __init__(self, package):
        self.package = package

    def allow(self, level):
        hierarchy = {
            "مجانية": 1,
            "فضية": 2,
            "ذهبية": 3,
            "ماسية": 4,
            "ماسية متميزة": 5
        }
        return hierarchy.get(self.package, 1) >= hierarchy[level]

# ==============================
# 3️⃣ RoboKnowledge (من robo_knowledge.py)
# ==============================

class RoboKnowledge:
    """قاعدة معرفة الروبو – يربط البيانات والتنبيهات والفرص"""
    
    def __init__(self, real_data, opportunities, alerts, market_data):
        self.real_data = real_data
        self.opportunities = opportunities
        self.alerts = alerts
        self.market = market_data  # ✅ الاسم الصحيح هو market وليس market_data

    def market_summary(self, city):
        """ملخص سريع لمدينة محددة"""
        return f"""
السوق في {city} حاليًا يتميز بـ:
• سيولة: {self.market.get('مؤشر_السيولة', 'غير متوفر')}
• نمو شهري: {self.market.get('معدل_النمو_الشهري', 'غير متوفر')}%
• عدد العقارات المحللة: {self.market.get('عدد_العقارات_الحقيقية', 0)}
"""

    def today_opportunities(self, city):
        """البحث عن فرص بناءً على المدينة أو المنطقة"""
        city_ops = [
            o for o in self.opportunities.get("عقارات_مخفضة", [])
            if o.get("المدينة") == city or o.get("المنطقة") == city
        ]
        return city_ops[:2]  # نُظهر فقط 1–2

    def decision_signal(self, city):
        """إشارة قرار استثماري بناءً على البيانات الحقيقية"""
        liquidity = self.market.get("مؤشر_السيولة", 0)
        growth = self.market.get("معدل_النمو_الشهري", 0)
        opportunities = self.today_opportunities(city)

        # إشارة مواتية (بدلاً من ENTER)
        if liquidity > 80 and growth > 3 and opportunities:
            return {
                "signal": "FAVORABLE",
                "confidence": "HIGH",
                "reason": "سيولة عالية + نمو قوي + فرص فعلية"
            }

        # مراقبة مع تفاؤل (بدلاً من WATCH)
        if liquidity > 65 and growth > 1.5:
            return {
                "signal": "NEUTRAL",
                "confidence": "MEDIUM",
                "reason": "سوق مستقر مع فرص انتقائية"
            }

        # انتظار حذر (بدلاً من WAIT)
        return {
            "signal": "CAUTIOUS",
            "confidence": "LOW",
            "reason": "سيولة ضعيفة أو غياب فرص واضحة"
        }

# ==============================
# 4️⃣ RoboAdvisor (من robo_brain.py) – مع إضافة الأسئلة الذكية
# ==============================

class RoboAdvisor:
    """عقل الروبو – يجيب على الأسئلة ويقود الحوار بذكاء"""
    
    def __init__(self, user_profile, knowledge, guard):
        self.user = user_profile
        self.knowledge = knowledge
        self.guard = guard

    def _follow_up(self, city, package):
        """سؤال ذكي يقود الحوار مع أمثلة جاهزة"""
        if package == "مجانية":
            return "\n💬 مثال: قل (وش وضع السوق في جدة؟) أو (تحليل الرياض)"
        if package == "فضية":
            return "\n💬 مثال: قل (راقب شمال الرياض) أو (حلل شقق جدة)"
        if package == "ذهبية":
            return "\n💬 مثال: قل (حلل فرص النرجس) أو (قارن شمال الرياض وجنوبها)"
        if package in ["ماسية", "ماسية متميزة"]:
            return "\n💬 مثال: قل (قيّم وضعي في الرياض) أو (أفضل خيار استثماري لي)"
        return "\n💬 مثال: هل تريد استفسارًا آخر؟"

    def answer(self, question: str) -> str:
        city = self.user.get("city")
        package = self.user.get("package", "مجانية")

        # 🔒 تفعيل RoboGuard: التحقق من الصلاحية الأساسية
        if not self.guard.allow("مجانية"):
            return "⚠️ لا يمكنني تقديم إجابة حاليًا. تحقق من باقتك." + self._follow_up(city, package)

        # أسئلة السوق
        if "السوق" in question or "الوضع" in question:
            return self._market_answer(city, package) + self._follow_up(city, package)

        # فرص واستثمار
        if "فرصة" in question or "استثمار" in question:
            return self._opportunity_answer(city, package) + self._follow_up(city, package)

        # أسئلة عامة - نمرر الباقة لـ _basic_answer
        return self._basic_answer(question, package) + self._follow_up(city, package)

    def _basic_answer(self, question, package="مجانية"):
        """إجابة ذكية تفرق بين المجاني والمدفوع"""
        market = self.knowledge.market  # ✅ تم التصحيح: market وليس market_data

        if not market:
            return "يتم حاليًا تحليل السوق. أعد المحاولة بعد ثوانٍ."

        # ✅ المجاني: لمحة عامة فقط
        if package == "مجانية":
            return f"""
📊 **لمحة سريعة عن السوق:**

• السيولة: {market.get('مؤشر_السيولة', 'غير محدد')}%
• النمو الشهري: {market.get('معدل_النمو_الشهري', 'غير محدد')}%
• عدد العقارات المحللة: {market.get('عدد_العقارات_الحقيقية', '—')}

🔒 التحليل الاستثماري الكامل والتوصيات متاحة في الباقات المدفوعة.
"""

        # ✅ الباقات المدفوعة (فضية فأعلى): تحليل أعمق + توصية ذكية
        liquidity = market.get('مؤشر_السيولة', 0)
        growth = market.get('معدل_النمو_الشهري', 0)
        
        # توليد توصية ذكية بناءً على البيانات
        if liquidity > 80 and growth > 3:
            recommendation = "🔥 السوق في حالة نمو قوي مع سيولة عالية. هذا توقيت ممتاز للدخول إذا كان هدفك متوسط المدى."
        elif liquidity > 60 and growth > 1.5:
            recommendation = "📈 السوق مستقر مع مؤشرات إيجابية. يُفضل الاستثمار التدريجي مع تنويع المحفظة."
        elif liquidity < 50 or growth < 0.5:
            recommendation = "⚠️ السوق يعاني من بعض التباطؤ. ننصح بدراسة متأنية والتركيز على المناطق الواعدة فقط."
        else:
            recommendation = "📊 السوق في حالة طبيعية. الفرص موجودة لكنها تحتاج بحثًا أعمق."

        return f"""
📊 **تحليل السوق المتقدم:**

• السيولة: {liquidity}% {'(مرتفعة)' if liquidity > 80 else '(متوسطة)' if liquidity > 60 else '(منخفضة)'}
• النمو الشهري: {growth}% {'(قوي)' if growth > 3 else '(إيجابي)' if growth > 1.5 else '(ضعيف)'}
• عدد العقارات المحللة: {market.get('عدد_العقارات_الحقيقية', '—')}

📈 **توصية المستشار:**
{recommendation}
"""

    def _market_answer(self, city, package):
        summary = self.knowledge.market_summary(city)

        # المجاني: ملخص فقط
        if package == "مجانية":
            return summary + "\n🔒 التحليل التفصيلي متاح في الباقات المدفوعة."

        # المدفوع: ملخص + تحليل
        return summary + "\n📊 التحليل العميق متوفر حسب باقتك."

    def _opportunity_answer(self, city, package):
        """إجابة الفرص مع إشارة قرار ذكية"""
        
        # 🔒 تفعيل RoboGuard للفرص: الباقة الفضية كحد أدنى
        if not self.guard.allow("فضية"):
            return "🔒 تفاصيل الفرص وإشارات القرار متاحة من الباقة الفضية فأعلى."

        ops = self.knowledge.today_opportunities(city)
        signal = self.knowledge.decision_signal(city)

        # ✅ الباقة الفضية: ترى إشارة القرار + السبب
        if package == "فضية":
            return f"""
📌 **إشارة القرار اليوم في {city}:**

🔹 القرار: **{signal['signal']}**
🔹 مستوى الثقة: **{signal['confidence']}**
🔹 السبب: {signal['reason']}

📊 هذا القرار مبني على تحليل السوق والبيانات المتاحة.

🔒 تفاصيل الفرص متاحة في الباقة الذهبية.
"""

        # ✅ الباقة الذهبية: ترى إشارة القرار + الفرص
        if package == "ذهبية":
            if not ops:
                return f"""
📌 **إشارة القرار اليوم في {city}:**
🔹 القرار: **{signal['signal']}**
🔹 السبب: {signal['reason']}

⚠️ لا توجد فرص قوية اليوم، لكن إشارة القرار تساعدك في التوقيت المناسب.
"""
            
            return f"""
📌 **إشارة القرار اليوم في {city}:**

🔹 القرار: **{signal['signal']}**
🔹 مستوى الثقة: **{signal['confidence']}**
🔹 السبب: {signal['reason']}

📌 تم رصد {len(ops)} فرصة ذكية اليوم.

🔍 هل تريد تفاصيل هذه الفرص؟
"""

        # ✅ الباقة الماسية والماسية المتميزة: إشارة + فرص + تفاصيل متقدمة
        if package in ["ماسية", "ماسية متميزة"]:
            return f"""
📌 **إشارة القرار اليوم في {city}:**

🔹 القرار: **{signal['signal']}**
🔹 مستوى الثقة: **{signal['confidence']}**
🔹 السبب: {signal['reason']}

عدد الفرص المكتشفة: {len(ops)}

💡 هذا القرار مبني على:
• بيانات سوق حقيقية
• تحليل فرص فعلية
• توقيت السوق الحالي

🔍 هل تريد تفاصيل الفرص المتاحة؟
"""

        # افتراضي
        return f"""
📌 تم رصد فرص في {city}.
للاطلاع على إشارات القرار والفرص، اختر باقتك المناسبة.
"""

# ==============================
# 5️⃣ Router بسيط (من robo_router.py)
# ==============================

def handle_robo_question(user_profile, knowledge, guard, question):
    """
    الدالة الرئيسية للاستخدام من الواجهة
    user_profile: dict يحتوي على city, package
    knowledge: كائن RoboKnowledge
    guard: كائن RoboGuard
    question: نص السؤال
    """
    robo = RoboAdvisor(user_profile, knowledge, guard)
    return robo.answer(question)

# ==============================
# 6️⃣ اختبار سريع (يشتغل فقط إذا شغلت الملف مباشرة)
# ==============================

if __name__ == "__main__":
    print("\n🧪 تشغيل اختبار Robo Advisor...")
    
    # بيانات تجريبية
    user = {"city": "الرياض", "package": "ذهبية"}
    
    market_data = {
        "مؤشر_السيولة": 85,
        "معدل_النمو_الشهري": 3.2,
        "عدد_العقارات_الحقيقية": 1243
    }
    
    opportunities = {
        "عقارات_مخفضة": [
            {"المدينة": "الرياض", "المنطقة": "الملقا", "الخصم": "15%"},
            {"المدينة": "الرياض", "المنطقة": "النرجس", "الخصم": "12%"}
        ]
    }
    
    guard = RoboGuard("ذهبية")
    knowledge = RoboKnowledge(None, opportunities, None, market_data)
    
    # اختبار الأسئلة
    print("\n📝 سؤال: وش وضع السوق في الرياض؟")
    print(handle_robo_question(user, knowledge, guard, "السوق في الرياض"))
    
    print("\n📝 سؤال: فيه فرص استثمارية؟")
    print(handle_robo_question(user, knowledge, guard, "فرصة"))
    
    print("\n✅ انتهى الاختبار")
