"""
Gold Decision Engine
--------------------
محرك القرار الرقمي التنفيذي – Warda Intelligence

• يدعم جميع المدن
• يدعم جميع أنواع العقار (شقة – فيلا – محل – أرض ...)
• يعتمد فقط على البيانات الحية بعد الفلترة
• لا يحتوي أي افتراضات سوقية مسبقة
• يُستخدم حصريًا في الخلاصة التنفيذية
• مصدر البيانات الوحيد: orchestrator (لا يتم جلب بيانات من الداخل)
"""

# =========================================
# Gold Decision Engine
# =========================================

import pandas as pd
import numpy as np
from datetime import datetime


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


def ensure_time_order(df):
    """ضمان الترتيب الزمني للبيانات قبل حساب التغييرات"""
    if df is None or df.empty:
        return df
    if "date" in df.columns:
        return df.sort_values("date")
    return df


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
        # ضمان الترتيب الزمني قبل حساب التغييرات
        tmp = ensure_time_order(real_data.copy())
        
        # تحسين: استخدام price_per_m2 بدلاً من price المطلق
        if "area" in tmp.columns:
            tmp["price_per_m2"] = tmp["price"] / tmp["area"]
            volatility = tmp["price_per_m2"].pct_change().std()
        else:
            volatility = tmp["price"].pct_change().std()
        
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
    • فجوة القيمة (نعطي نقاط فقط للانحراف السلبي)
    • التذبذب
    • السيولة التقريبية
    """

    if real_data is None or real_data.empty:
        return 0

    score = 50  # نقطة تعادل

    # ✅ تأثير فجوة القيمة - نعطي نقاط فقط إذا كان هناك خصم سعري (vgs سلبي)
    if vgs < 0:
        score += clamp(abs(vgs), 0, 20)
    # إذا كانت الفجوة إيجابية (سوق مبالغ فيه)، لا نضيف نقاط

    # التذبذب (خصم حتى 25)
    if "price" in real_data.columns and len(real_data) > 5:
        # ضمان الترتيب الزمني قبل حساب التغييرات
        tmp = ensure_time_order(real_data.copy())
        
        # تحسين: استخدام price_per_m2 للتذبذب
        if "area" in tmp.columns:
            tmp["price_per_m2"] = tmp["price"] / tmp["area"]
            volatility = tmp["price_per_m2"].pct_change().std()
        else:
            volatility = tmp["price"].pct_change().std()
        
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
    
    ملاحظة: تم تثبيت seed لضمان استقرار النتائج
    """

    TOTAL_SCENARIOS = 20

    if real_data is None or real_data.empty or "price" not in real_data.columns:
        return {"matched": 0, "total": TOTAL_SCENARIOS, "percentage": 0}

    # ✅ تحسين: استخدام price_per_m2 بدلاً من price المطلق لمحاكاة أكثر دقة
    if "area" in real_data.columns:
        tmp = real_data.copy()
        tmp["price_per_m2"] = tmp["price"] / tmp["area"]
        values = tmp["price_per_m2"].dropna()
    else:
        values = real_data["price"].dropna()
    
    mean_val = values.mean()
    # ✅ تحسين إضافي: حد أدنى 1% انحراف لمنع أمان مفرط في الأسواق المستقرة جداً
    std_val = max(values.std(), mean_val * 0.01)

    matched = 0

    # ✅ تثبيت random seed لضمان نتائج مستقرة بين التشغيلات المختلفة
    np.random.seed(42)

    for _ in range(TOTAL_SCENARIOS):
        simulated_val = np.random.normal(mean_val, std_val)

        # منطق الأمان السعري (±15%)
        if abs(simulated_val - mean_val) / mean_val <= 0.15:
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

def generate_gold_decision_metrics(
    city: str,
    property_type: str,
    real_data=None,
    market_data=None
) -> dict:
    """
    Gold Decision Metrics Engine
    ----------------------------
    يحسب مؤشرات القرار الذهبي اعتمادًا على البيانات الحية.
    
    ملاحظة معمارية مهمة:
    - مصدر البيانات الوحيد هو orchestrator
    - لا يتم جلب بيانات من الداخل (real_data_repository)
    - إذا كانت البيانات غير صالحة، نعيد قيماً صفرية آمنة
    
    المدخلات:
        city: المدينة (للتوثيق فقط - لا يستخدم في الجلب)
        property_type: نوع العقار (للتوثيق فقط - لا يستخدم في الجلب)
        real_data: DataFrame بالبيانات الحقيقية (من orchestrator)
        market_data: dict بمؤشرات السوق (اختياري)
    
    المخرجات:
        dict: المؤشرات الأربعة (DCI, VGS, RAOS, SCM)
    """

    # 🔒 حماية من البيانات غير الصالحة - بدون جلب من الداخل
    if real_data is None or not isinstance(real_data, pd.DataFrame) or real_data.empty:
        # إرجاع قيم صفرية آمنة - orchestrator مسؤول عن تمرير البيانات
        return {
            "DCI": 0,
            "VGS": 0.0,
            "RAOS": 0,
            "SCM": {"matched": 0, "total": 20, "percentage": 0}
        }
    
    if market_data is None or not isinstance(market_data, dict):
        market_data = {}

    # ضمان الترتيب الزمني للبيانات بالكامل مرة واحدة
    real_data = ensure_time_order(real_data)

    # احتساب المؤشرات الذهبية
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


# للاختبار المستقل (اختياري)
if __name__ == "__main__":
    # بيانات تجريبية للاختبار
    test_data = pd.DataFrame({
        "price": [500000, 750000, 1000000, 1250000, 1500000] * 20,
        "area": [80, 100, 120, 150, 180] * 20,
        "date": pd.date_range(start="2023-01-01", periods=100, freq="W")
    })
    
    metrics = generate_gold_decision_metrics(
        city="الرياض",
        property_type="شقة",
        real_data=test_data
    )
    
    print("📊 Gold Decision Metrics:")
    print(f"DCI: {metrics['DCI']}/100")
    print(f"VGS: {metrics['VGS']}%")
    print(f"RAOS: {metrics['RAOS']}/100")
    print(f"SCM: {metrics['SCM']['percentage']}%")
