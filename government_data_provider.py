import pandas as pd

FILE_PATH = "market_transactions.csv"

def load_government_data():
    df = pd.read_csv(
        FILE_PATH,
        sep=None,
        engine="python",
        encoding="utf-8-sig"
    )

    # 🔹 إعادة تسمية الأعمدة حسب ما يظهر في ملفك
    column_map = {
        "المنطقة": "region",
        "المدينة": "city",
        "الحي": "district",
        "قيمة الصفقة": "price",
        "المساحة": "area",
        "تاريخ الصفقة": "date"
    }

    df = df.rename(columns=column_map)

    # 🔹 حساب سعر المتر
    if "price" in df.columns and "area" in df.columns:
        df["price_per_sqm"] = df["price"] / df["area"]

    return df
