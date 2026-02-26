import pandas as pd
import csv

FILE_PATH = "market_transactions.csv"

def load_government_data(selected_city=None, selected_property_type=None):

    rows = []

    # قراءة الملف بطريقة آمنة تدعم "100,000"
    with open(FILE_PATH, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    # تحويل إلى DataFrame
    df = pd.DataFrame(rows)

    # حذف الهيدر إذا كان موجودًا
    if df.iloc[0].astype(str).str.contains("المنطقة").any():
        df = df.iloc[1:].reset_index(drop=True)

    # التأكد أن لدينا 10 أعمدة فقط
    df = df.iloc[:, :10]

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

    # تنظيف وتحويل الأرقام
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

    # =========================
    # الفلترة الذكية حسب اختيار المستخدم
    # =========================

    if selected_city:
        df = df[df["city"].str.contains(selected_city, na=False)]

    if selected_property_type:

        # وزارة العدل تصنف شقة + فيلا = سكني
        if selected_property_type in ["شقة", "فيلا"]:
            df = df[df["property_type"].str.contains("سكني", na=False)]

        elif selected_property_type == "أرض":
            df = df[df["property_type"].str.contains("زراعي|أرض", na=False)]

    return df
