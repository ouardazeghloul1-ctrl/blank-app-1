import pandas as pd

FILE_PATH = "market_transactions.csv"

def load_government_data(selected_city=None, selected_property_type=None):

    # القراءة الصحيحة مع دعم الأرقام التي تحتوي على فاصلة
    df = pd.read_csv(
        FILE_PATH,
        sep=",",
        quotechar='"',
        encoding="utf-8-sig",
        engine="python"
    )

    # تنظيف أسماء الأعمدة
    df.columns = df.columns.str.strip()

    # إعادة تسمية حسب ترتيب ملف الوزارة الفعلي
    df.columns = [
        "region",
        "city",
        "district",
        "hijri_date",
        "gregorian_date",
        "reference_number",
        "property_type",
        "transaction_count",
        "price",
        "area"
    ]

    # تنظيف النصوص
    for col in ["region", "city", "district", "property_type"]:
        df[col] = df[col].astype(str).str.strip()

    # تحويل الأرقام
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace('"', "", regex=False)
    )

    df["area"] = (
        df["area"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace('"', "", regex=False)
    )

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["area"] = pd.to_numeric(df["area"], errors="coerce")

    df["price_per_sqm"] = df["price"] / df["area"]

    df = df.dropna(subset=["price", "area"])

    # فلترة مرنة
    if selected_city:
        df = df[df["city"].str.contains(selected_city, na=False)]

    if selected_property_type:
        df = df[df["property_type"].str.contains(selected_property_type, na=False)]

    return df
