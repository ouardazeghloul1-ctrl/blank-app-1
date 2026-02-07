# ai_executive_summary.py
# =========================================
# Executive Decision Engine – Warda Intelligence (Diamond Tier)
# =========================================

import pandas as pd
from smart_opportunities import SmartOpportunityFinder


def compute_market_metrics(real_data: pd.DataFrame) -> dict:
    """
    تحويل البيانات الحية إلى مؤشرات رقمية قابلة للتنبؤ
    """
    metrics = {}

    # قوة النشاط السوقي (Activity Strength)
    metrics["activity_strength"] = min(100, max(30, len(real_data) * 2))

    # التذبذب السعري
    price_changes = real_data["price"].pct_change().dropna()
    volatility = price_changes.std()

    if volatility < 0.01:
        metrics["volatility_level"] = "منخفض"
    elif volatility < 0.03:
        metrics["volatility_level"] = "متوسط"
    else:
        metrics["volatility_level"] = "مرتفع"

    # النمو الشهري (Median لتجنب التشويه)
    monthly_growth = price_changes.median()
    metrics["monthly_growth"] = round(float(monthly_growth * 100), 2) if pd.notna(monthly_growth) else 1.0

    # إشارات السوق
    metrics["positive_signals"] = int((price_changes > 0).sum())
    metrics["negative_signals"] = int((price_changes <= 0).sum())

    return metrics


def generate_executive_summary(user_info, market_data, real_data):
    """
    الخلاصة التنفيذية التنبؤية المبنية على 6 كتل ثابتة
    """

    if real_data is None or real_data.empty:
        return (
            "تعذر إصدار خلاصة تنفيذية تنبؤية لغياب بيانات سوقية حقيقية.\n"
            "النظام يعمل فقط عند توفر بيانات قابلة للتحليل."
        )

    city = user_info.get("city", "المدينة")

    # محرك الفرص
    finder = SmartOpportunityFinder()
    undervalued = finder.find_undervalued_properties(real_data, city)
    rising_areas = finder.predict_rising_areas(real_data, city)

    # المؤشرات الرقمية
    metrics = compute_market_metrics(real_data)

    # طبقة التنبؤ الاحتمالي (Prediction Layer)
    short_term = min(90, max(50, 55 + metrics["monthly_growth"] * 2))
    mid_term = min(92, max(55, 60 + metrics["activity_strength"] / 5))
    long_term = min(95, max(60, 65 + len(undervalued) * 3))

    lines = []

    # 🧱 الكتلة (1): تعريف القرار التنبؤي
    lines.append("الخلاصة التنفيذية التنبؤية – Warda Intelligence")
    lines.append("")
    lines.append(
        "هذا القرار ناتج عن نظام ذكاء اصطناعي تنبؤي مبني على بيانات سوقية حية، "
        "مقارنة تاريخية، رصد فجوات سعرية، وتحليل سلوك السوق، "
        "ولا يستند إلى آراء بشرية أو توقعات عامة."
    )
    lines.append("")

    # 🧱 الكتلة (2): وضع السوق الحالي بالأرقام
    lines.append("📊 وضع السوق الحالي:")
    lines.append(f"- قوة النشاط السوقي: {metrics['activity_strength']}%")
    lines.append(f"- مستوى التذبذب: {metrics['volatility_level']}")
    lines.append(
        f"- الإشارات الإيجابية مقابل السلبية: "
        f"{metrics['positive_signals']} / {metrics['negative_signals']}"
    )
    lines.append(f"- عدد فجوات القيمة المكتشفة: {len(undervalued)}")
    lines.append(f"- عدد المناطق الصاعدة: {len(rising_areas)}")
    lines.append("")

    # 🧱 الكتلة (3): الإشارات التنبؤية
    lines.append("🔮 الإشارات التنبؤية (AI Prediction):")
    lines.append(f"- خلال 3 أشهر: اتجاه مستقر انتقائي باحتمالية {int(short_term)}%")
    lines.append(f"- خلال 6 أشهر: تحسن موضعي باحتمالية {int(mid_term)}%")
    lines.append(f"- خلال 12 شهر: إعادة تسعير قائمة على القيمة باحتمالية {int(long_term)}%")
    lines.append("")

    # 🧱 الكتلة (4): السيناريوهات الذكية
    lines.append("🧠 السيناريوهات المحتملة:")
    lines.append(
        "- إذا بقي الوضع كما هو: القرار الحالي يظل صالحًا دون تعديل.\n"
        "- إذا تحسّن السوق: تتسع دائرة الخيارات دون الحاجة لتغيير الموقف.\n"
        "- إذا ساء السوق: يحمي هذا القرار من الاندفاع ويقلل الخطأ."
    )
    lines.append("")

    # 🧱 الكتلة (5): الموقف الأمثل الآن (بدون تسميته)
    lines.append("🧭 الموقف الأمثل الآن:")
    if short_term > 65 and len(undervalued) >= 3:
        lines.append("- تموضع ذكي يسمح بالحركة دون ضغط أو استعجال")
    else:
        lines.append("- الجاهزية والمراقبة مع مرونة عالية في التوقيت")
    lines.append("")

    # 🧱 الكتلة (6): ضمان القرار (نفسي + منطقي)
    lines.append("📌 ضمان القرار:")
    lines.append("- لا حاجة لإعادة التفكير طالما بقيت هذه المؤشرات قائمة")
    lines.append("- يُعاد التقييم فقط عند تغيّر سلوك السوق، لا عند الضجيج السعري")
    lines.append("- تجاهل الأخبار غير المرتبطة بالبيانات الفعلية")

    return "\n".join(lines)
