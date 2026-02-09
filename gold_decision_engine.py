"""
Gold Decision Engine
--------------------
محرك القرار الرقمي التنفيذي – Warda Intelligence

• يدعم جميع المدن
• يدعم جميع أنواع العقار (شقة – فيلا – محل – أرض ...)
• يعتمد فقط على البيانات الحية بعد الفلترة
• لا يحتوي أي افتراضات سوقية مسبقة
• يُستخدم حصريًا في الخلاصة التنفيذية
"""

# =========================================
# Gold Decision Engine
# =========================================

import pandas as pd
import numpy as np
from datetime import datetime

from real_data_repository import load_real_data


# -----------------------------------------
# أدوات مساعدة عامة
# -----------------------------------------

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def safe_div(a, b, default=0.0):
    try:
        return a / b if b else default
    except Exception:
        return default


# -----------------------------------------
# (1) Decision Confidence Index – DCI
# -----------------------------------------

def calculate_dci(real_data: pd.DataFrame) -> int:
    """
    مؤشر موثوقية القرار (0 – 100)

    يعتمد على:
    • اكتمال البيانات
    • حجم العينة
    • حداثة البيانات
    • استقرار الأسعار
    """

    if real_data is None or real_data.empty:
        return 0

    score = 0.0

    # اكتمال البيانات (30%)
    completeness = real_data[["price", "area"]].notnull().mean().mean()
    score += completeness * 30

    # حجم العينة (25%)
    sample_size = len(real_data)
    sample_score = clamp(sample_size / 500, 0, 1)  # 500 عقار = ممتاز
    score += sample_score * 25

    # حداثة البيانات (25%)
    if "date" in real_data.columns:
        latest_date = real_data["date"].max()
        if pd.notnull(latest_date):
            days_diff = (datetime.now() - latest_date).days
            freshness = clamp(1 - (days_diff / 180), 0, 1)  # 6 أشهر
            score += freshness * 25

    # استقرار الأسعار (20%)
    if "price" in real_data.columns and len(real_data) > 5:
        volatility = real_data["price"].pct_change().std()
        stability = clamp(1 - safe_div(volatility, 0.10), 0, 1)
        score += stability * 20

    return int(round(clamp(score, 0, 100)))


# -----------------------------------------
# (2) Value Gap Score – VGS
# -----------------------------------------

def calculate_vgs(real_data: pd.DataFrame) -> float:
    """
    فجوة القيمة (%)
    الفرق بين السعر الحالي ومتوسط السوق
    """

    if real_data is None or real_data.empty:
        return 0.0

    if "price" not in real_data.columns or "area" not in real_data.columns:
        return 0.0

    df = real_data.copy()
    df["price_per_m2"] = df["price"] / df["area"]

    market_avg = df["price_per_m2"].mean()
    current_median = df["price_per_m2"].median()

    gap = safe_div((current_median - market_avg), market_avg) * 100
    return round(gap, 2)


# -----------------------------------------
# (3) Risk-Adjusted Opportunity Score – RAOS
# -----------------------------------------

def calculate_raos(real_data: pd.DataFrame, vgs: float) -> int:
    """
    مؤشر الفرصة بعد خصم المخاطر (0 – 100)

    يعتمد على:
    • فجوة القيمة
    • التذبذب
    • السيولة التقريبية
    """

    if real_data is None or real_data.empty:
        return 0

    score = 50  # نقطة تعادل

    # تأثير فجوة القيمة (+20)
    score += clamp(abs(vgs), 0, 20)

    # التذبذب (خصم حتى 25)
    if "price" in real_data.columns and len(real_data) > 5:
        volatility = real_data["price"].pct_change().std()
        penalty = clamp(volatility * 200, 0, 25)
        score -= penalty

    # السيولة التقريبية (+15)
    liquidity_score = clamp(len(real_data) / 300, 0, 1) * 15
    score += liquidity_score

    return int(round(clamp(score, 0, 100)))


# -----------------------------------------
# (4) Scenario Convergence Metric – SCM
# -----------------------------------------

def calculate_scm(real_data: pd.DataFrame) -> dict:
    """
    تقاطع السيناريوهات (%)

    نحاكي 20 سيناريو سعري مبسط
    ونقيس كم منها يؤدي لنفس القرار
    """

    TOTAL_SCENARIOS = 20

    if real_data is None or real_data.empty or "price" not in real_data.columns:
        return {"matched": 0, "total": TOTAL_SCENARIOS, "percentage": 0}

    prices = real_data["price"].dropna()
    mean_price = prices.mean()
    std_price = prices.std()

    matched = 0

    for _ in range(TOTAL_SCENARIOS):
        simulated_price = np.random.normal(mean_price, std_price)

        # منطق الأمان السعري (±15%)
        if abs(simulated_price - mean_price) / mean_price <= 0.15:
            matched += 1

    percentage = int(round((matched / TOTAL_SCENARIOS) * 100))

    return {
        "matched": matched,
        "total": TOTAL_SCENARIOS,
        "percentage": percentage
    }


# -----------------------------------------
# الواجهة الذهبية – دالة واحدة فقط
# -----------------------------------------

def generate_gold_decision_metrics(city: str, property_type: str) -> dict:
    """
    الواجهة الوحيدة المسموح باستدعائها من بقية النظام
    """

    real_data = load_real_data(city=city, property_type=property_type)

    dci = calculate_dci(real_data)
    vgs = calculate_vgs(real_data)
    raos = calculate_raos(real_data, vgs)
    scm = calculate_scm(real_data)

    return {
        "DCI": dci,
        "VGS": vgs,
        "RAOS": raos,
        "SCM": scm
    }
