import pandas as pd

FILE_PATH = "market_transactions.csv"

def load_government_data(selected_city=None, selected_property_type=None):

    # نقرأ الملف كسطر واحد
    df_raw = pd.read_csv(
        FILE_PATH,
        header=None,
        encoding="utf-8-sig"
    )

    # نفصل العمود الواحد إلى أعمدة متعددة
    df = df_raw[0].str.split(",", expand=True)

    # تسمية الأعمدة حسب ترتيبها في ملف الوزارة
    df.columns = [
        "region",            # المنطقة
        "city",              # المدينة
        "district",          # الحي
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
    df["price"] = pd.to_numeric(df["price"].str.replace('"', ''), errors="coerce")
    df["area"] = pd.to_numeric(df["area"].str.replace('"', ''), errors="coerce")

    # حساب سعر المتر
    df["price_per_sqm"] = df["price"] / df["area"]

    df = df.dropna(subset=["price", "area"])

    # فلترة مرنة
    if selected_city:
        df = df[df["city"].str.contains(selected_city, na=False)]

    if selected_property_type:
        df = df[df["property_type"].str.contains(selected_property_type, na=False)]

    return df
