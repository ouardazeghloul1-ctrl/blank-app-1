# =========================================
# District Ranking Engine
# Warda Intelligence
# =========================================

import pandas as pd
import numpy as np


# -----------------------------------------
# دالة تصنيف DPI (للتحسين الاختياري)
# -----------------------------------------
def classify_dpi(dpi):
    """تصنيف مؤشر قوة الحي"""
    if dpi >= 80:
        return "ممتاز"
    elif dpi >= 70:
        return "جيد جداً"
    elif dpi >= 60:
        return "جيد"
    elif dpi >= 50:
        return "متوسط"
    else:
        return "ضعيف"


# -----------------------------------------
# حساب مؤشرات الحي
# -----------------------------------------
def compute_district_metrics(df: pd.DataFrame):
    """
    يحسب المؤشرات الأساسية لكل حي
    """
    if df is None or df.empty:
        return pd.DataFrame()

    # ✅ التعديل 1: دعم كلا العمودين district_clean و district
    district_col = "district_clean" if "district_clean" in df.columns else "district"
    
    # ✅ التعديل 2: إزالة الصفقات بدون حي مع مراعاة NaN
    mask = df[district_col].notna() & (df[district_col] != "غير محدد")
    df_filtered = df[mask].copy()
    
    if df_filtered.empty:
        return pd.DataFrame()

    # ✅ التعديل 3: استخدام observed=True لتحسين الأداء
    grouped = df_filtered.groupby(district_col, observed=True)

    metrics = grouped.agg(
        transactions=("price", "count"),
        avg_price=("price", "mean"),
        median_price=("price", "median"),
        avg_price_sqm=("price_per_sqm", "mean"),
        median_price_sqm=("price_per_sqm", "median"),
    ).reset_index()
    
    # توحيد اسم العمود
    metrics = metrics.rename(columns={district_col: "district_clean"})

    return metrics


# -----------------------------------------
# حساب الاستقرار السعري
# -----------------------------------------
def compute_price_stability(df: pd.DataFrame):
    """
    يقيس استقرار الأسعار داخل الحي
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # ✅ التعديل 1: دعم كلا العمودين
    district_col = "district_clean" if "district_clean" in df.columns else "district"
    
    # التأكد من وجود price_per_sqm
    if "price_per_sqm" not in df.columns:
        if "price" in df.columns and "area" in df.columns:
            df = df.copy()
            df["price_per_sqm"] = df["price"] / df["area"].replace(0, 1)
        else:
            return pd.DataFrame()

    # ✅ التعديل 3: استخدام observed=True
    grouped = df.groupby(district_col, observed=True)
    
    # حساب الانحراف المعياري
    volatility = grouped["price_per_sqm"].std().reset_index()
    volatility.columns = [district_col, "price_volatility"]
    
    # ✅ التعديل 4: معالجة NaN (يحدث عندما يكون الحي به صفقة واحدة فقط)
    volatility["price_volatility"] = volatility["price_volatility"].fillna(0)
    
    # توحيد اسم العمود
    volatility = volatility.rename(columns={district_col: "district_clean"})

    return volatility


# -----------------------------------------
# حساب السيولة
# -----------------------------------------
def compute_liquidity_score(metrics_df):
    """
    تحويل عدد الصفقات إلى مؤشر سيولة من 0 إلى 100
    """
    if metrics_df is None or metrics_df.empty:
        return metrics_df
    
    metrics_df = metrics_df.copy()
    
    max_tx = metrics_df["transactions"].max()

    if max_tx == 0 or pd.isna(max_tx):
        metrics_df["liquidity_score"] = 0
    else:
        metrics_df["liquidity_score"] = (metrics_df["transactions"] / max_tx) * 100
    
    # التأكد من أن القيم بين 0 و 100
    metrics_df["liquidity_score"] = metrics_df["liquidity_score"].clip(0, 100)

    return metrics_df


# -----------------------------------------
# حساب استقرار السعر
# -----------------------------------------
def compute_stability_score(metrics_df):
    """
    كلما كان الانحراف أقل كان الاستقرار أعلى
    """
    if metrics_df is None or metrics_df.empty:
        return metrics_df
    
    metrics_df = metrics_df.copy()
    
    max_vol = metrics_df["price_volatility"].max()

    if max_vol == 0 or pd.isna(max_vol):
        metrics_df["stability_score"] = 100
    else:
        metrics_df["stability_score"] = (1 - metrics_df["price_volatility"] / max_vol) * 100

    metrics_df["stability_score"] = metrics_df["stability_score"].clip(0, 100)

    return metrics_df


# -----------------------------------------
# حساب قوة السعر
# -----------------------------------------
def compute_price_strength(metrics_df):
    """
    يقارن سعر الحي بمتوسط المدينة
    """
    if metrics_df is None or metrics_df.empty:
        return metrics_df
    
    metrics_df = metrics_df.copy()
    
    # ✅ التعديل 3: منع division by zero
    city_avg = metrics_df["avg_price_sqm"].mean()
    
    if city_avg == 0 or pd.isna(city_avg):
        metrics_df["price_strength"] = 50
        return metrics_df

    metrics_df["price_strength"] = (metrics_df["avg_price_sqm"] / city_avg) * 100
    metrics_df["price_strength"] = metrics_df["price_strength"].clip(0, 200)  # حد أقصى 200% من متوسط المدينة

    return metrics_df


# -----------------------------------------
# مؤشر قوة الحي DPI
# -----------------------------------------
def compute_dpi(metrics_df):
    """
    District Power Index
    يجمع عدة مؤشرات في مؤشر واحد
    """
    if metrics_df is None or metrics_df.empty:
        return metrics_df
    
    metrics_df = metrics_df.copy()
    
    # التأكد من وجود جميع المؤشرات المطلوبة
    required_cols = ["liquidity_score", "stability_score", "price_strength"]
    for col in required_cols:
        if col not in metrics_df.columns:
            metrics_df[col] = 50
    
    # حساب DPI مع الأوزان
    metrics_df["dpi"] = (
        metrics_df["liquidity_score"] * 0.40 +
        metrics_df["stability_score"] * 0.30 +
        metrics_df["price_strength"] * 0.30
    )
    
    # التأكد من أن القيم بين 0 و 100
    metrics_df["dpi"] = metrics_df["dpi"].clip(0, 100)

    return metrics_df


# -----------------------------------------
# ترتيب الأحياء
# -----------------------------------------
def rank_districts(df: pd.DataFrame):
    """
    يعيد جدول ترتيب الأحياء كاملاً مع جميع المؤشرات
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # ✅ التعديل 5: منع SettingWithCopyWarning
    df = df.copy()
    
    # التأكد من وجود الأعمدة المطلوبة
    required_cols = ["price", "price_per_sqm"]
    for col in required_cols:
        if col not in df.columns:
            if col == "price_per_sqm" and "price" in df.columns and "area" in df.columns:
                df["price_per_sqm"] = df["price"] / df["area"].replace(0, 1)
            else:
                print(f"⚠️ العمود {col} غير موجود في البيانات")
                return pd.DataFrame()

    # المؤشرات الأساسية
    metrics = compute_district_metrics(df)
    
    if metrics.empty:
        return pd.DataFrame()

    # الاستقرار السعري
    volatility = compute_price_stability(df)
    
    if not volatility.empty:
        metrics = metrics.merge(volatility, on="district_clean", how="left")
    else:
        metrics["price_volatility"] = 0

    # السيولة
    metrics = compute_liquidity_score(metrics)

    # الاستقرار
    metrics = compute_stability_score(metrics)

    # قوة السعر
    metrics = compute_price_strength(metrics)

    # DPI
    metrics = compute_dpi(metrics)

    # ✅ التعديل 4: ترتيب محسّن باستخدام mergesort للاستقرار مع البيانات الكبيرة
    metrics = metrics.sort_values(
        by="dpi", 
        ascending=False,
        kind="mergesort"
    ).reset_index(drop=True)

    # إضافة عمود الترتيب
    metrics["rank"] = range(1, len(metrics) + 1)
    
    # عدد الأحياء الكلي في المدينة
    metrics["total_districts"] = len(metrics)
    
    # ✅ إضافة تقييم نصي لكل حي (باستخدام الدالة المنفصلة)
    metrics["rating"] = metrics["dpi"].apply(classify_dpi)

    return metrics


# -----------------------------------------
# استخراج أفضل الأحياء
# -----------------------------------------
def get_top_districts(df: pd.DataFrame, top_n=5):
    """
    إرجاع أفضل N حي
    """
    ranked = rank_districts(df)

    if ranked.empty:
        return ranked

    return ranked.head(top_n)


# -----------------------------------------
# نص تحليل الحي
# -----------------------------------------
def build_district_summary(row):
    """
    بناء نص وصفي مختصر لتحليل الحي
    """
    name = row.get("district_clean", "غير محدد")
    dpi = row.get("dpi", 0)
    tx = row.get("transactions", 0)
    price = row.get("avg_price_sqm", 0)
    rating = row.get("rating", "متوسط")
    
    text = f"""
📍 حي {name} 
📊 التقييم: {rating}
📈 مؤشر قوة الحي (DPI): {dpi:.1f} نقطة
💰 متوسط سعر المتر: {price:,.0f} ريال
📊 عدد الصفقات: {tx} صفقة

{_get_dpi_interpretation(dpi, tx)}
"""
    return text


def _get_dpi_interpretation(dpi, transactions):
    """تفسير مبسط لمؤشر DPI"""
    if dpi >= 80:
        return "يتمتع الحي بجاذبية استثمارية عالية جداً، مع سيولة ممتازة واستقرار في الأسعار."
    elif dpi >= 70:
        return "الحي قوي استثمارياً مع مؤشرات إيجابية في السيولة والاستقرار."
    elif dpi >= 60:
        return "الحي يتمتع بمؤشرات جيدة، مع فرص استثمارية معقولة."
    elif dpi >= 50:
        return "الحي متوسط الجاذبية، قد يتطلب دراسة أعمق للفرص المتاحة."
    else:
        return "الحي ضعيف نسبياً من ناحية المؤشرات الاستثمارية."


# -----------------------------------------
# اختبار سريع
# -----------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("🔍 اختبار District Ranking Engine")
    print("=" * 50)

    # بيانات اختبار مع حالات متنوعة
    data = {
        "district_clean": ["النرجس", "النرجس", "الملقا", "الملقا", "الياسمين", "الوادي", None, "غير محدد"],
        "price": [900000, 850000, 1200000, 1100000, 800000, 750000, 600000, 500000],
        "price_per_sqm": [5000, 5200, 7000, 6800, 4500, 4200, 3800, 3500],
    }

    df = pd.DataFrame(data)
    print(f"\n📊 بيانات الاختبار: {len(df)} صفقة")
    print("ملاحظة: يوجد صفقة بـ None وأخرى بـ 'غير محدد' (سيتم تجاهلها)")
    print(df)

    # حساب الترتيب
    ranking = rank_districts(df)
    
    if not ranking.empty:
        print("\n📈 ترتيب الأحياء حسب DPI:")
        print(ranking[["rank", "district_clean", "dpi", "transactions", "rating"]])
        
        # أفضل الأحياء
        top = get_top_districts(df, top_n=3)
        print("\n🏆 أفضل 3 أحياء:")
        for _, row in top.iterrows():
            print(build_district_summary(row))
    else:
        print("⚠️ لم يتم العثور على أحياء صالحة للتحليل")
