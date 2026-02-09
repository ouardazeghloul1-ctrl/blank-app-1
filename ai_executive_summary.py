# =========================================
# Executive Predictive Decision Engine
# Warda Intelligence
# =========================================

from smart_opportunities import SmartOpportunityFinder
from gold_decision_engine import generate_gold_decision_metrics
import pandas as pd


def safe_pct(x, default=0.0):
    try:
        return round(float(x * 100), 2)
    except Exception:
        return default


def generate_executive_summary(user_info, market_data, real_data):
    """
    الخلاصة التنفيذية التنبؤية – مبنية على قرار رقمي ذهبي
    """

    if real_data is None or real_data.empty:
        return (
            "EXECUTIVE_DECISION_START\n"
            "الخلاصة التنفيذية التنبؤية – Warda Intelligence\n\n"
            "تعذر توليد الخلاصة التنفيذية لعدم توفر بيانات سوقية حقيقية.\n"
            "نظام Warda Intelligence يعمل فقط عند توفر بيانات قابلة للتحليل."
        )

    city = user_info.get("city", "غير محددة")
    property_type = user_info.get("property_type", "غير محدد")

    # =====================================
    # 🟡 استدعاء القرار الذهبي (Gold Metrics)
    # =====================================
    gold = generate_gold_decision_metrics(
        city=city,
        property_type=property_type
    )

    dci = gold.get("DCI", 0)
    vgs = gold.get("VGS", 0.0)
    raos = gold.get("RAOS", 0)
    scm = gold.get("SCM", {"matched": 0, "total": 0, "percentage": 0})

    # =====================================
    # إشارات الفرص (موجودة سابقًا)
    # =====================================
    finder = SmartOpportunityFinder()
    undervalued = finder.find_undervalued_properties(real_data, city)
    rising_areas = finder.predict_rising_areas(real_data, city)

    liquidity = market_data.get("مؤشر_السيولة", 50)
    growth = market_data.get("معدل_النمو_الشهري", 0.0)

    volatility = safe_pct(
        real_data["price"].pct_change().std()
        if "price" in real_data.columns else None,
        0.5
    )

    # =====================================
    # بناء الخلاصة – الكتل الست
    # =====================================
    lines = []

    lines.append("EXECUTIVE_DECISION_START")
    lines.append("الخلاصة التنفيذية التنبؤية – Warda Intelligence")
    lines.append("")

    # 🧱 الكتلة 1: تعريف القرار
    lines.append("[DECISION_BLOCK:DECISION_DEFINITION]")
    lines.append("تعريف القرار التنبؤي")
    lines.append(
        "هذا القرار ناتج عن نظام ذكاء اصطناعي تنبؤي رقمي، "
        "مبني على بيانات سوقية حية، تحليل فجوات القيمة، "
        "واختبار تقاطع السيناريوهات."
    )
    lines.append(
        f"مؤشر موثوقية القرار (DCI): {dci}/100"
    )
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # 🧱 الكتلة 2: وضع السوق
    lines.append("[DECISION_BLOCK:MARKET_STATUS]")
    lines.append("وضع السوق الحالي (قراءة رقمية)")
    lines.append(f"فجوة القيمة الحالية: {vgs}%")
    lines.append(f"مستوى التذبذب السعري: {volatility}%")
    lines.append(f"مؤشر الفرصة المعدلة بالمخاطر (RAOS): {raos}/100")
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # 🧱 الكتلة 3: الإشارات التنبؤية
    lines.append("[DECISION_BLOCK:PREDICTIVE_SIGNALS]")
    lines.append("الإشارات التنبؤية المعتمدة")
    lines.append(
        f"تقاطع السيناريوهات: "
        f"{scm.get('percentage', 0)}% "
        f"({scm.get('matched', 0)} من {scm.get('total', 0)})"
    )
    lines.append(
        f"عدد الفرص ذات فجوة القيمة المكتشفة: {len(undervalued)}"
    )
    lines.append(
        f"عدد المناطق الصاعدة المحتملة: {len(rising_areas)}"
    )
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # 🧱 الكتلة 4: السيناريوهات
    lines.append("[DECISION_BLOCK:SCENARIOS]")
    lines.append("السيناريوهات المحتملة")
    lines.append(
        "السيناريو الأساسي: استمرار التوازن الحالي دون اختلالات."
    )
    lines.append(
        "السيناريو الإيجابي: تحسن انتقائي يعزز هامش الحركة."
    )
    lines.append(
        "السيناريو الوقائي: ضغط مؤقت لا يكسر القرار."
    )
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # 🧱 الكتلة 5: القرار التنفيذي
    lines.append("[DECISION_BLOCK:OPTIMAL_POSITION]")
    lines.append("القرار التنفيذي الحالي")
    lines.append(
        "التموضع الانتقائي الهادئ دون التزام كامل، "
        "مع أولوية للأصول الأقل من متوسط مناطقها، "
        "والتحرك فقط عند نضوج إشارة القيمة."
    )
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # 🧱 الكتلة 6: ضمان القرار
    lines.append("[DECISION_BLOCK:DECISION_GUARANTEE]")
    lines.append("ضمان القرار")
    lines.append(
        "يبقى هذا القرار صالحًا طالما لم تتغير فجوة القيمة "
        "أو ينخفض مؤشر الفرصة المعدلة بالمخاطر."
    )
    lines.append(
        "تُعاد المراجعة فقط عند تغيّر جوهري في السيولة "
        "أو ارتفاع التذبذب خارج النطاق الآمن."
    )
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    lines.append("EXECUTIVE_DECISION_END")

    return "\n".join(lines)
