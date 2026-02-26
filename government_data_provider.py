import pandas as pd

FILE_PATH = "market_transactions.csv"

def load_government_data():
    df = pd.read_csv(
        FILE_PATH,
        sep=None,
        engine="python",
        encoding="utf-8-sig"
    )

    # 🔹 تنظيف أسماء الأعمدة من المسافات
    df.columns = df.columns.str.strip()

    # 🔹 إعادة تسمية الأعمدة
    column_map = {
        "المنطقة": "region",
        "المدينة": "city",
        "الحي": "district",
        "قيمة الصفقة": "price",
        "المساحة": "area",
        "تاريخ الصفقة": "date",
        "نوع العقار": "property_type",   # 🔥 هذا السطر الجديد المهم
        "تصنيف العقار": "property_type"
    }

    df = df.rename(columns=column_map)

    # 🔹 إذا لم يوجد نوع عقار ننشئه بقيمة افتراضية
    if "property_type" not in df.columns:
        df["property_type"] = "غير محدد"

    # 🔹 حساب سعر المتر
    if "price" in df.columns and "area" in df.columns:
        df["price_per_sqm"] = df["price"] / df["area"]

    return df
