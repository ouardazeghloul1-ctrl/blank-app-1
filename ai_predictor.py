# ai_predictor.py
# ================================
# محرك التنبؤ والتحليل الذكي
# مستقل عن الواجهة (Streamlit / PDF)
# ================================

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


REQUIRED_COLUMNS = ["price", "area"]


def _normalize_dataframe(df):
    """
    توحيد شكل البيانات:
    - يقبل dict أو DataFrame
    - يعيد DataFrame نظيف أو None
    """
    if df is None:
        return None

    # إذا كان dict نحوله إلى DataFrame
    if isinstance(df, dict):
        try:
            df = pd.DataFrame(df)
        except Exception:
            return None

    if not isinstance(df, pd.DataFrame):
        return None

    if df.empty:
        return None

    return df.copy()


def analyze_results(df):
    """
    تحليل تنبؤي بسيط قائم على المساحة والسعر
    يعيد:
    - predictions_df (DataFrame)
    - meta (dict معلومات تشخيصية)
    """

    df = _normalize_dataframe(df)

    if df is None:
        return None, {
            "status": "no_data",
            "message": "لا توجد بيانات صالحة للتحليل"
        }

    # 🔎 التحقق من الأعمدة المطلوبة
    if not all(col in df.columns for col in REQUIRED_COLUMNS):
        return None, {
            "status": "missing_columns",
            "message": f"الأعمدة المطلوبة غير موجودة: {REQUIRED_COLUMNS}"
        }

    # تنظيف البيانات
    df = df.dropna(subset=REQUIRED_COLUMNS)
    if df.empty:
        return None, {
            "status": "empty_after_cleaning",
            "message": "البيانات غير كافية بعد التنظيف"
        }

    # تحويل المساحة إلى أرقام
    df["area"] = (
        df["area"]
        .astype(str)
        .str.extract(r"(\d+\.?\d*)")[0]
        .astype(float)
    )

    df = df.dropna(subset=["area", "price"])
    if df.empty:
        return None, {
            "status": "invalid_numeric_data",
            "message": "المساحة أو السعر غير صالحين للتحليل"
        }

    # حساب سعر المتر
    df["price_per_sqm"] = df["price"] / df["area"]

    # تدريب النموذج
    X = df[["area"]].values
    y = df["price"].values

    model = LinearRegression()
    model.fit(X, y)

    # نطاق التنبؤ
    future_areas = np.linspace(
        df["area"].min(),
        df["area"].max(),
        10
    ).reshape(-1, 1)

    future_prices = model.predict(future_areas)

    predictions_df = pd.DataFrame({
        "area": future_areas.flatten(),
        "predicted_price": future_prices.round(0).astype(int)
    })

    meta = {
        "status": "ok",
        "rows_used": len(df),
        "min_area": float(df["area"].min()),
        "max_area": float(df["area"].max()),
        "model": "LinearRegression",
        "confidence_note": "تنبؤ استرشادي وليس توصية استثمارية مباشرة"
    }

    return predictions_df, meta
