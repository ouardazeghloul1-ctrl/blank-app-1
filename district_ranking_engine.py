# =========================================
# District Ranking Engine
# Warda Intelligence
# =========================================

import pandas as pd


# -----------------------------------------
# حساب مؤشرات الحي
# -----------------------------------------
def compute_district_metrics(df: pd.DataFrame):

    """
    يحسب المؤشرات الأساسية لكل حي
    """

    if df is None or df.empty:
        return pd.DataFrame()

    # إزالة الصفقات بدون حي
    df = df[df["district_clean"] != "غير محدد"]

    # تجميع حسب الحي
    grouped = df.groupby("district_clean")

    metrics = grouped.agg(
        transactions=("price", "count"),
        avg_price=("price", "mean"),
        median_price=("price", "median"),
        avg_price_sqm=("price_per_sqm", "mean"),
        median_price_sqm=("price_per_sqm", "median"),
    ).reset_index()

    return metrics


# -----------------------------------------
# حساب الاستقرار السعري
# -----------------------------------------
def compute_price_stability(df: pd.DataFrame):

    """
    يقيس استقرار الأسعار داخل الحي
    """

    grouped = df.groupby("district_clean")

    volatility = grouped["price_per_sqm"].std().reset_index()
    volatility.columns = ["district_clean", "price_volatility"]

    return volatility


# -----------------------------------------
# حساب السيولة
# -----------------------------------------
def compute_liquidity_score(metrics_df):

    """
    تحويل عدد الصفقات إلى مؤشر سيولة من 0 إلى 100
    """

    max_tx = metrics_df["transactions"].max()

    if max_tx == 0:
        metrics_df["liquidity_score"] = 0
    else:
        metrics_df["liquidity_score"] = (
            metrics_df["transactions"] / max_tx
        ) * 100

    return metrics_df


# -----------------------------------------
# حساب استقرار السعر
# -----------------------------------------
def compute_stability_score(metrics_df):

    """
    كلما كان الانحراف أقل كان الاستقرار أعلى
    """

    max_vol = metrics_df["price_volatility"].max()

    if max_vol == 0:
        metrics_df["stability_score"] = 100
    else:
        metrics_df["stability_score"] = (
            1 - metrics_df["price_volatility"] / max_vol
        ) * 100

    metrics_df["stability_score"] = metrics_df["stability_score"].clip(0, 100)

    return metrics_df


# -----------------------------------------
# حساب قوة السعر
# -----------------------------------------
def compute_price_strength(metrics_df):

    """
    يقارن سعر الحي بمتوسط المدينة
    """

    city_avg = metrics_df["avg_price_sqm"].mean()

    metrics_df["price_strength"] = (
        metrics_df["avg_price_sqm"] / city_avg
    ) * 100

    return metrics_df


# -----------------------------------------
# مؤشر قوة الحي DPI
# -----------------------------------------
def compute_dpi(metrics_df):

    """
    District Power Index
    """

    metrics_df["dpi"] = (
        metrics_df["liquidity_score"] * 0.40 +
        metrics_df["stability_score"] * 0.30 +
        metrics_df["price_strength"] * 0.30
    )

    return metrics_df


# -----------------------------------------
# ترتيب الأحياء
# -----------------------------------------
def rank_districts(df: pd.DataFrame):

    """
    يعيد جدول ترتيب الأحياء
    """

    if df is None or df.empty:
        return pd.DataFrame()

    # المؤشرات الأساسية
    metrics = compute_district_metrics(df)

    # الاستقرار
    volatility = compute_price_stability(df)

    metrics = metrics.merge(
        volatility,
        on="district_clean",
        how="left"
    )

    # السيولة
    metrics = compute_liquidity_score(metrics)

    # الاستقرار
    metrics = compute_stability_score(metrics)

    # قوة السعر
    metrics = compute_price_strength(metrics)

    # DPI
    metrics = compute_dpi(metrics)

    # ترتيب
    metrics = metrics.sort_values(
        by="dpi",
        ascending=False
    )

    metrics["rank"] = range(1, len(metrics) + 1)
    
    # عدد الأحياء الكلي في المدينة
    metrics["total_districts"] = len(metrics)

    return metrics


# -----------------------------------------
# استخراج أفضل الأحياء
# -----------------------------------------
def get_top_districts(df: pd.DataFrame, top_n=5):

    ranked = rank_districts(df)

    if ranked.empty:
        return ranked

    return ranked.head(top_n)


# -----------------------------------------
# نص تحليل الحي
# -----------------------------------------
def build_district_summary(row):

    name = row["district_clean"]
    dpi = row["dpi"]
    tx = row["transactions"]
    price = row["avg_price_sqm"]

    text = f"""
حي {name} سجل مؤشر قوة استثمارية يبلغ {dpi:.1f} نقطة،
مع متوسط سعر متر يقارب {price:,.0f} ريال
وعدد صفقات بلغ {tx} صفقة.

تشير هذه المؤشرات إلى مستوى جيد من السيولة والاستقرار
مما يجعله من الأحياء الجاذبة للاستثمار العقاري.
"""

    return text


# -----------------------------------------
# اختبار سريع
# -----------------------------------------
if __name__ == "__main__":

    print("Testing District Ranking Engine")

    # مثال وهمي
    data = {
        "district_clean": ["النرجس", "النرجس", "الملقا", "الملقا", "الياسمين"],
        "price": [900000, 850000, 1200000, 1100000, 800000],
        "price_per_sqm": [5000, 5200, 7000, 6800, 4500],
    }

    df = pd.DataFrame(data)

    ranking = rank_districts(df)

    print(ranking)
