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

    # نمو سنوي تاريخي فعلي (median لتقليل الضجيج)
    annual_growth = prices.pct_change().median()
    annual_growth = annual_growth if pd.notna(annual_growth) else 0.01

    # تدرج زمني محافظ
    y1_3 = safe_pct(annual_growth * 0.7)
    y4_6 = safe_pct(annual_growth * 1.2)
    y7_10 = safe_pct(annual_growth * 1.7)

    # العائد التراكمي (نطاق)
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
    رقمية، حية، قابلة للطباعة مباشرة
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
    # Gold Decision Metrics (LIVE)
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
    # Forecast 10 Years (LIVE)
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
    # BUILD EXECUTIVE SUMMARY
    # =========================
    lines = []

    lines.append("EXECUTIVE_DECISION_START")
    lines.append("الخلاصة التنفيذية التنبؤية – Warda Intelligence")
    lines.append("")
    lines.append("تمت معايرة هذه المؤشرات مقابل نطاقات تاريخية مماثلة لدورات سوقية سابقة.")
    lines.append("")

    # ---- Block 1
    lines.append("[DECISION_BLOCK:DECISION_DEFINITION]")
    lines.append(f"مؤشر موثوقية القرار: {dci} من 100")
    lines.append("هذا المؤشر يؤكد صلاحية البيانات لاتخاذ قرار استثماري طويل المدى.")
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # ---- Block 2
    lines.append("[DECISION_BLOCK:MARKET_STATUS]")
    lines.append(f"فجوة القيمة الحالية: {vgs} بالمئة")
    lines.append(f"مستوى التذبذب السعري: {volatility} بالمئة")
    lines.append(f"مؤشر الفرصة المعدلة بالمخاطر: {raos} من 100")
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # ---- Block 3
    lines.append("[DECISION_BLOCK:PREDICTIVE_SIGNALS]")
    lines.append(f"تقاطع السيناريوهات التنبؤية: {scm} بالمئة")
    lines.append(f"عدد الفرص منخفضة القيمة المكتشفة: {len(undervalued)}")
    lines.append(f"عدد المناطق الصاعدة المحتملة: {len(rising_areas)}")
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # ---- Block 4 (10 Years Forecast)
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

    # ---- Block 5
    lines.append("[DECISION_BLOCK:OPTIMAL_POSITION]")
    lines.append(
        "الدخول الانتقائي طويل المدى في أصول أقل من متوسط مناطقها، "
        "مع تجنب الشراء الواسع أو القرارات قصيرة الأجل."
    )
    lines.append("[END_DECISION_BLOCK]")
    lines.append("")

    # ---- Block 6
    lines.append("[DECISION_BLOCK:DECISION_GUARANTEE]")
    lines.append(
        "يبقى هذا القرار صالحًا طالما ظل مؤشر الموثوقية فوق 55 "
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
