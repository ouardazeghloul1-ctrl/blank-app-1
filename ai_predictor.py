# ai_predictor.py
# ================================
# نموذج استقرائي داخلي (In-sample Price Estimation)
# لا يمثل تنبؤًا سوقيًا زمنيًا
# مستقل عن الواجهة (Streamlit / PDF)
# ================================

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


REQUIRED_COLUMNS = ["price", "area", "date"]


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
    تحليل استقرائي داخلي يوضح العلاقة بين المساحة والسعر داخل العينة الحالية
    لا يمثل تنبؤًا زمنيًا ولا توصية استثمارية
    
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

    # تحويل التاريخ
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    if df.empty:
        return None, {
            "status": "invalid_date_data",
            "message": "التواريخ غير صالحة للتحليل"
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

    # التأكد من وجود عدد كافٍ من البيانات
    if len(df) < 20:
        return None, {
            "status": "insufficient_data",
            "message": "عدد البيانات غير كافٍ لبناء نموذج استقرائي موثوق (يجب أن يكون 20 على الأقل)"
        }

    # حساب سعر المتر
    df["price_per_sqm"] = df["price"] / df["area"]

    # تدريب النموذج
    X = df[["area"]].values
    y = df["price"].values

    model = LinearRegression()
    model.fit(X, y)

    # نطاق الاستقراء
    future_areas = np.linspace(
        df["area"].min(),
        df["area"].max(),
        10
    ).reshape(-1, 1)

    future_prices = model.predict(future_areas)

    predictions_df = pd.DataFrame({
        "area": future_areas.flatten(),
        "estimated_price": future_prices.round(0).astype(int)
    })

    meta = {
        "status": "ok",
        "rows_used": len(df),
        "min_area": float(df["area"].min()),
        "max_area": float(df["area"].max()),
        "model": "LinearRegression (in-sample)",
        "scope": "price_vs_area",
        "confidence_note": (
            "هذا النموذج استقرائي داخلي مبني على بيانات العينة الحالية فقط، "
            "ولا يمثل توقعًا زمنيًا أو توصية استثمارية."
        )
    }

    return predictions_df, meta


# للاختبار المستقل
if __name__ == "__main__":
    # بيانات تجريبية للاختبار
    test_data = pd.DataFrame({
        "price": [500000, 750000, 1000000, 1250000, 1500000] * 5,
        "area": [80, 100, 120, 150, 180] * 5,
        "date": pd.date_range(start="2023-01-01", periods=25, freq="M")
    })
    
    pred, meta = analyze_results(test_data)
    if pred is not None:
        print("✅ تم تحليل البيانات بنجاح")
        print(f"📊 عدد النقاط المستخدمة: {meta['rows_used']}")
        print(f"📈 نطاق المساحات: {meta['min_area']} - {meta['max_area']}")
        print("\n🔮 الاستقراء السعري:")
        print(pred.head())
    else:
        print(f"❌ فشل التحليل: {meta['message']}")
