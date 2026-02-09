# =========================================
# Gold Decision Engine
# Warda Intelligence
# =========================================
# هذه الطبقة هي العقل الرقمي للقرار التنفيذي
# لا تحتوي نصوصًا – أرقام فقط + منطق فقط
# =========================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from real_data_repository import load_real_data


# -----------------------------------------
# أدوات مساعدة
# -----------------------------------------

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def safe_div(a, b, default=0):
    try:
        return a / b if b != 0 else default
    except Exception:
        return default


# -----------------------------------------
# (1) Decision Confidence Index – DCI
# -----------------------------------------

def calculate_dci(real_data: pd.DataFrame) -> int:
    """
    مؤشر موثوقية القرار (0 – 100)
    يعتمد على:
    - اكتمال البيانات
    - حداثة البيانات
    - حجم العينة
    - استقرار الأسعار
    """

    if real_data is None or real_data.empty:
        return 0

    score = 0

    # اكتمال البيانات
    completeness = real_data[["price", "area"]].notnull().mean().mean()
    score += completeness * 30  # 30%

    # حجم العينة
    sample_size = len(real_data)
    sample_score = clamp(sample_size / 500, 0, 1)  # 500 عقار = مثالي
    score += sample_score * 25  # 25%

    # حداثة البيانات
    if "date" in real_data.columns:
        latest_date = real_data["date"].max()
        if pd.notnull(latest_date):
            days_diff = (datetime.now() - latest_date).days
            freshness = clamp(1 - (days_diff / 180), 0, 1)  # 6 أشهر
            score += freshness * 25  # 25%

    # استقرار الأسعار (تذبذب)
    if "price" in real_data.columns and len(real_data) > 5:
        volatility = real_data["price"].pct_change().std()
        stability = clamp(1 - safe_div(volatility, 0.1), 0, 1)  # 10% تذبذب = خطر
        score += stability * 20  # 20%

    return int(round(clamp(score, 0, 100)))


# -----------------------------------------
# (2) Value Gap Score – VGS
# -----------------------------------------

def calculate_vgs(real_data: pd.DataFrame) -> float:
    """
    فجوة القيمة (%)
    الفرق بين متوسط سعر المتر وسعر السوق الفعلي
    """

    if real_data is None or real_data.empty:
        return 0.0

    if "price" not in real_data.columns or "area" not in real_data.columns:
        return 0.0

    real_data = real_data.copy()
    real_data["price_per_m2"] = real_data["price"] / real_data["area"]

    market_avg = real_data["price_per_m2"].mean()
    current_avg = real_data["price_per_m2"].median()

    gap = safe_div((current_avg - market_avg), market_avg) * 100

    return round(gap, 2)


# -----------------------------------------
# (3) Risk-Adjusted Opportunity Score – RAOS
# -----------------------------------------

def calculate_raos(real_data: pd.DataFrame, vgs: float) -> int:
    """
    الفرصة المعدلة بالمخاطر (0 – 100)
    تعتمد على:
    - فجوة القيمة
    - التذبذب
    - كثافة السوق (سيولة تقريبية)
    """

    if real_data is None or real_data.empty:
        return 0

    score = 50  # نقطة تعادل

    # فجوة القيمة
    score += clamp(abs(vgs), 0, 20)  # حتى +20

    # التذبذب
    if "price" in real_data.columns and len(real_data) > 5:
        volatility = real_data["price"].pct_change().std()
        volatility_penalty = clamp(volatility * 200, 0, 25)
        score -= volatility_penalty

    # السيولة التقريبية (كثافة البيانات)
    liquidity_score = clamp(len(real_data) / 300, 0, 1) * 15
    score += liquidity_score

    return int(round(clamp(score, 0, 100)))


# -----------------------------------------
# (4) Scenario Convergence Metric – SCM
# -----------------------------------------

def calculate_scm(real_data: pd.DataFrame) -> dict:
    """
    تقاطع السيناريوهات
    نحاكي 20 سيناريو مبسط اعتمادًا على توزيع الأسعار
    """

    TOTAL_SCENARIOS = 20

    if real_data is None or real_data.empty or "price" not in real_data.columns:
        return {"matched": 0, "total": TOTAL_SCENARIOS, "percentage": 0}

    prices = real_data["price"].dropna()
    mean_price = prices.mean()
    std_price = prices.std()

    matched = 0

    for i in range(TOTAL_SCENARIOS):
        simulated_price = np.random.normal(mean_price, std_price)

        # منطق القرار المبسط:
        # هل السعر ضمن نطاق أمان (±15%)؟
        if abs(simulated_price - mean_price) / mean_price <= 0.15:
            matched += 1

    percentage = int(round((matched / TOTAL_SCENARIOS) * 100))

    return {
        "matched": matched,
        "total": TOTAL_SCENARIOS,
        "percentage": percentage
    }


# -----------------------------------------
# الدالة الذهبية – واجهة واحدة فقط
# -----------------------------------------

def generate_gold_decision_metrics(city: str, property_type: str) -> dict:
    """
    الدالة الوحيدة التي يجب استدعاؤها من الخارج
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


# -----------------------------------------
# اختبار محلي
# -----------------------------------------

if __name__ == "__main__":
    metrics = generate_gold_decision_metrics("الرياض", "شقة")
    print(metrics)
