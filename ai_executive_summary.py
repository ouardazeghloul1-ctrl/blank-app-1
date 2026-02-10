# =========================================
# Executive Predictive Decision Engine
# Warda Intelligence – Diamond Version
# =========================================

from smart_opportunities import SmartOpportunityFinder
from gold_decision_engine import generate_gold_decision_metrics
import numpy as np
import pandas as pd


def safe_pct(x, default=0.0):
    try:
        return round(float(x * 100), 2)
    except Exception:
        return default


def compute_long_term_forecast(real_data: pd.DataFrame):
    """
    حساب تنبؤ زمني 10 سنوات مبني فقط على البيانات الحية
    """
    if real_data is None or real_data.empty or "price" not in real_data.columns:
        return {
            "y1_3": 0.0,
            "y4_6": 0.0,
            "y7_10": 0.0,
            "cumulative_min": 0.0,
            "cumulative_max": 0.0,
        }

    prices = real_data["price"].dropna()

    annual_growth = prices.pct_change().median()
    annual_growth = annual_growth if pd.notna(annual_growth) else 0.01

    y1_3 = safe_pct(annual_growth * 0.7)
    y4_6 = safe_pct(annual_growth * 1.2)
    y7_10 = safe_pct(annual_growth * 1.7)

    cumulative_min = safe_pct((1 + annual_growth * 0.6) ** 10 - 1)
    cumulative_max = safe_pct((1 + annual_growth * 1.1) ** 10 - 1)

    return {
        "y1_3": y1_3,
        "y4_6": y4_6,
        "y7_10": y7_10,
        "cumulative_min": cumulative_min,
        "cumulative_max": cumulative_max,
    }


def generate_executive_summary(user_info, market_data, real_data):
    """
    الخلاصة التنفيذية التنبؤية – Diamond
    """

    if real_data is None or real_data.empty:
        return (
            "EXECUTIVE_DECISION_START\n"
            "الخلاصة التنفيذية التنبؤية – Warda Intelligence\n\n"
            "تعذر توليد الخلاصة التنفيذية لعدم توفر بيانات سوقية حقيقية.\n"
            "EXECUTIVE_DECISION_END"
        )

    city = user_info.get("city", "غير محددة")
    property_type = user_info.get("property_type", "غير محدد")

    # =========================
    # Gold Metrics (LIVE)
    # =========================
    gold = generate_gold_decision_metrics(
        city=city,
        property_type=property_type,
        real_data=real_data,
        market_data=market_data
    )

    dci = gold.get("DCI", 0)
    vgs = gold.get("VGS", 0.0)
    raos = gold.get("RAOS", 0)
    scm = gold.get("SCM", {}).get("percentage", 0)

    # =========================
    # Forecast 10 Years
    # =========================
    forecast = compute_long_term_forecast(real_data)

    # =========================
    # Opportunity Signals
    # =========================
    finder = SmartOpportunityFinder()
    undervalued = finder.find_undervalued_properties(real_data, city)
    rising_areas = finder.predict_rising_areas(real_data, city)

    volatility = safe_pct(
        real_data["price"].pct_change().std()
        if "price" in real_data.columns else 0.0
    )

    # =========================
    # BUILD SUMMARY
    # =========================
    lines = []

    lines.append("EXECUTIVE_DECISION_START")
    lines.append("الخلاصة التنفيذية التنبؤية – Warda Intelligence")
    lines.append("")
    lines.append("تمت معايرة هذه المؤشرات مقابل نطاقات تاريخية مماثلة لدورات سوقية سابقة.")
    lines.append("")

    # 🧱 1 — تعريف القرار
    lines.append("[DECISION_BLOCK:DECISION_DEFINITION]")
    lines.append(f"مؤشر موثوقية القرار: {dci} من 100")
    lines.append("يشير هذا المستوى إلى أن البيانات الحالية صالحة لاتخاذ قرار استثماري طويل المدى.")
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # 🧱 2 — وضع السوق
    lines.append("[DECISION_BLOCK:MARKET_STATUS]")
    lines.append(f"فجوة القيمة الحالية: {vgs} بالمئة")
    lines.append(f"مستوى التذبذب السعري: {volatility} بالمئة")
    lines.append(f"مؤشر الفرصة المعدلة بالمخاطر: {raos} من 100")
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # 🧱 3 — الإشارات التنبؤية
    lines.append("[DECISION_BLOCK:PREDICTIVE_SIGNALS]")
    lines.append(f"تقاطع السيناريوهات التنبؤية: {scm} بالمئة")
    lines.append(f"عدد الفرص منخفضة القيمة المكتشفة: {len(undervalued)}")
    lines.append(f"عدد المناطق الصاعدة المحتملة: {len(rising_areas)}")
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # 🧱 4 — التنبؤ الزمني 10 سنوات
    lines.append("[DECISION_BLOCK:SCENARIOS]")
    lines.append(f"السنوات 1 إلى 3: نمو سنوي متوقع {forecast['y1_3']} بالمئة")
    lines.append(f"السنوات 4 إلى 6: نمو سنوي متوقع {forecast['y4_6']} بالمئة")
    lines.append(f"السنوات 7 إلى 10: نمو سنوي متوقع {forecast['y7_10']} بالمئة")
    lines.append(
        f"العائد التراكمي المتوقع لعشر سنوات بين "
        f"{forecast['cumulative_min']} و {forecast['cumulative_max']} بالمئة"
    )
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # 🧱 5 — الوضع التنفيذي الحالي (القرار اللغوي الذكي)
    lines.append("[DECISION_BLOCK:OPTIMAL_POSITION]")
    lines.append("الوضع التنفيذي الحالي")

    if dci >= 65 and raos >= 45 and scm >= 65:
        lines.append(
            "المرحلة الحالية تسمح بالتحرك الانتقائي الهادئ، "
            "مع التركيز على الأصول التي تُظهر فجوة قيمة واضحة، "
            "دون الحاجة إلى تسريع القرار أو توسيع نطاق التعرض."
        )
    elif dci >= 55 and scm >= 60:
        lines.append(
            "المرحلة الحالية مناسبة للتموضع المرحلي والمراقبة المستمرة، "
            "مع الجاهزية للتحرك عند تحسن جودة الإشارات."
        )
    else:
        lines.append(
            "المرحلة الحالية تتطلب التريث والمراقبة النشطة، "
            "مع الحفاظ على الجاهزية دون التزام حتى تتضح الصورة بشكل أفضل."
        )

    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # 🧱 6 — ضمان القرار
    lines.append("[DECISION_BLOCK:DECISION_GUARANTEE]")
    lines.append(
        "يبقى هذا التوجه صالحًا طالما ظل مؤشر الموثوقية فوق 55 "
        "ولم ينخفض تقاطع السيناريوهات تحت 60 بالمئة."
    )
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    lines.append(
        "هذا التقرير موجه لقرارات استثمارية لا تقل عن 36 شهرًا، "
        "ولا يُعد مناسبًا للمضاربة أو القرارات قصيرة الأجل."
    )

    lines.append("EXECUTIVE_DECISION_END")

    return "\n".join(lines)
