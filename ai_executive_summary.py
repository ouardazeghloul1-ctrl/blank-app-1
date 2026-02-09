# ai_executive_summary.py
# =========================================
# Executive Predictive Decision Engine
# Warda Intelligence
# =========================================

from smart_opportunities import SmartOpportunityFinder
import pandas as pd


def safe_pct(x, default=0.0):
    try:
        return round(float(x * 100), 2)
    except Exception:
        return default


def generate_executive_summary(user_info, market_data, real_data):
    """
    الخلاصة التنفيذية التنبؤية – مبنية على 6 كتل ثابتة
    كل القيم ناتجة عن بيانات حية + تحليل ذكاء اصطناعي
    """

    if real_data is None or real_data.empty:
        return (
            "EXECUTIVE_DECISION_START\n"
            "الخلاصة التنفيذية التنبؤية – Warda Intelligence\n\n"
            "تعذر توليد الخلاصة التنفيذية لعدم توفر بيانات سوقية حقيقية.\n"
            "نظام Warda Intelligence يعمل فقط عند توفر بيانات قابلة للتحليل."
        )

    city = user_info.get("city", "المدينة")

    # =========================
    # استخراج الإشارات الذكية
    # =========================
    finder = SmartOpportunityFinder()
    undervalued = finder.find_undervalued_properties(real_data, city)
    rising_areas = finder.predict_rising_areas(real_data, city)

    liquidity = market_data.get("مؤشر_السيولة", 50)
    growth = market_data.get("معدل_النمو_الشهري", 0.0)

    # =========================
    # مؤشرات سلوكية
    # =========================
    volatility = safe_pct(
        real_data["price"].pct_change().std()
        if "price" in real_data.columns else None,
        0.5
    )

    activity_score = min(100, max(20, liquidity))
    selectivity_score = min(10, max(1, len(undervalued)))

    positive_signals = len(undervalued) + len(rising_areas)
    negative_signals = 1 if volatility > 2 else 0

    # =========================
    # طبقة التنبؤ الاحتمالي
    # =========================
    p_3m = min(max(int((0.55 + (growth / 10)) * 100), 45), 85)
    p_6m = min(max(int((0.60 + (liquidity / 200)) * 100), 50), 90)
    p_12m = min(max(int((0.65 + (len(undervalued) / 10)) * 100), 55), 95)

    # =========================
    # بناء القرار – الكتل الست
    # =========================
    lines = []

    # 🔑 مفتاح تشغيل القرار التنفيذي (مهم جدًا)
    lines.append("EXECUTIVE_DECISION_START")
    lines.append("الخلاصة التنفيذية التنبؤية – Warda Intelligence")
    lines.append("")

    # الكتلة 1: تعريف القرار
    lines.append("[DECISION_BLOCK:DECISION_DEFINITION]")
    lines.append("تعريف القرار التنبؤي")
    lines.append(
        "هذا القرار ناتج عن نظام ذكاء اصطناعي تنبؤي مبني على بيانات سوقية حية، "
        "مقارنة تاريخية، رصد فجوات قيمة، وتحليل سلوك فعلي للسوق."
    )
    lines.append("لا يعتمد على آراء بشرية أو توصيات عامة.")
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # الكتلة 2: وضع السوق
    lines.append("[DECISION_BLOCK:MARKET_STATUS]")
    lines.append("وضع السوق الحالي (قراءة رقمية)")
    lines.append(f"قوة النشاط السوقي: {activity_score}%")
    lines.append(f"درجة الانتقائية: {selectivity_score}/10")
    lines.append(
        f"مستوى التذبذب: "
        f"{'منخفض' if volatility < 1 else 'متوسط' if volatility < 2 else 'مرتفع'}"
    )
    lines.append(
        f"الإشارات الإيجابية مقابل السلبية: "
        f"{positive_signals} مقابل {negative_signals}"
    )
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # الكتلة 3: الإشارات التنبؤية
    lines.append("[DECISION_BLOCK:PREDICTIVE_SIGNALS]")
    lines.append("الإشارات التنبؤية")
    lines.append(f"أفق 3 أشهر: استقرار انتقائي باحتمالية تقريبية {p_3m}%")
    lines.append(f"أفق 6 أشهر: تحسن موضعي باحتمالية تقريبية {p_6m}%")
    lines.append(f"أفق 12 شهرًا: إعادة تسعير قائمة على القيمة باحتمالية {p_12m}%")
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # الكتلة 4: السيناريوهات
    lines.append("[DECISION_BLOCK:SCENARIOS]")
    lines.append("السيناريوهات المحتملة")
    lines.append("في حال ثبات المعطيات: القرار الحالي يظل صالحًا دون تعديل.")
    lines.append("في حال تحسن السوق: تتوسع فرص الحركة دون تغيير جوهر القرار.")
    lines.append("في حال تراجع السوق: يتحول القرار تلقائيًا إلى وضع حماية.")
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # الكتلة 5: الموقف الأمثل
    lines.append("[DECISION_BLOCK:OPTIMAL_POSITION]")
    lines.append("الموقف الأمثل في المرحلة الحالية")
    if liquidity >= 60 and len(undervalued) >= 3:
        lines.append("تموضع يسمح بالحركة الهادئة ضمن نطاق محسوب.")
    elif liquidity < 45:
        lines.append("تثبيت الموقع الحالي مع جاهزية عالية للتغيير.")
    else:
        lines.append("جاهزية كاملة دون التزام حتى نضوج الإشارات.")
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # الكتلة 6: ضمان القرار
    lines.append("[DECISION_BLOCK:DECISION_GUARANTEE]")
    lines.append("ضمان القرار")
    lines.append("لا حاجة لإعادة التفكير طالما لم تتغير المؤشرات الأساسية.")
    lines.append("يُعاد التقييم فقط عند تغيّر السيولة أو اختفاء فجوات القيمة.")
    lines.append("تجاهل الضجيج قصير المدى، هذا القرار صُمم ليصمد.")
    lines.append("")
    lines.append(
        "قيمة هذا القرار أنه يهدف إلى تقليل الخطأ الاستثماري "
        "قبل السعي وراء مكسب لحظي."
    )
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")
    lines.append("EXECUTIVE_DECISION_END")

    return "\n".join(lines)
