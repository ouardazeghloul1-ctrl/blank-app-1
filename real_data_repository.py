# real_data_repository.py
# =========================================
# مستودع البيانات الحقيقية – Warda Intelligence
# المصدر الوحيد للبيانات في النظام
# =========================================

import os
import pandas as pd
from datetime import datetime


DATA_FOLDER = "data"


REQUIRED_COLUMNS = {
    "السعر": "price",
    "المساحة": "area",
    "المدينة": "city",
    "المنطقة": "district",
    "نوع_العقار": "property_type",
    "المصدر": "source",
    "تاريخ_الجلب": "date",
}


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    توحيد أسماء الأعمدة العربية إلى شكل قياسي
    """
    df = df.copy()

    for ar, en in REQUIRED_COLUMNS.items():
        if ar in df.columns and en not in df.columns:
            df[en] = df[ar]

    return df


def _clean_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    تنظيف الأنواع والقيم
    """
    df = df.copy()

    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

    if "area" in df.columns:
        df["area"] = (
            df["area"]
            .astype(str)
            .str.extract(r"(\d+\.?\d*)")[0]
            .astype(float)
        )

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.dropna(subset=["price", "area", "city"])

    return df


def load_real_data(city: str = None, property_type: str = None) -> pd.DataFrame:
    """
    تحميل ودمج كل البيانات الحقيقية من مجلد data/
    مع إمكانية التصفية حسب المدينة ونوع العقار
    """

    if not os.path.exists(DATA_FOLDER):
        return pd.DataFrame()

    frames = []

    for file in os.listdir(DATA_FOLDER):
        if not file.endswith(".csv"):
            continue

        path = os.path.join(DATA_FOLDER, file)

        try:
            df = pd.read_csv(path)
            df = _normalize_columns(df)
            df = _clean_types(df)

            frames.append(df)
        except Exception:
            continue

    if not frames:
        return pd.DataFrame()

    data = pd.concat(frames, ignore_index=True)

    if city:
        data = data[data["city"] == city]

    if property_type:
        data = data[data["property_type"] == property_type]

    return data.reset_index(drop=True)


# اختبار سريع
if __name__ == "__main__":
    df = load_real_data("الرياض", "شقة")
    print(df.head())
    print(f"عدد العقارات: {len(df)}")
