import pandas as pd
import csv

FILE_PATH = "market_transactions.csv"

def load_government_data(selected_city=None, selected_property_type=None):

    rows = []

    # قراءة الملف بطريقة تدعم القيم مثل "100,000"
    with open(FILE_PATH, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    df = pd.DataFrame(rows)

    # حذف الهيدر إن وجد
    if df.iloc[0].astype(str).str.contains("المنطقة").any():
        df = df.iloc[1:].reset_index(drop=True)

    # نأخذ أول 10 أعمدة فقط
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

    # تنظيف الأرقام
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
    # فلترة المدينة (بحث مرن في 3 أعمدة)
    # =========================
    if selected_city:
        df = df[
            df["region"].str.contains(selected_city, na=False) |
            df["city"].str.contains(selected_city, na=False) |
            df["district"].str.contains(selected_city, na=False)
        ]

    # =========================
    # فلترة نوع العقار حسب تصنيف الوزارة
    # =========================
    if selected_property_type:

        # الوزارة تصنف شقة + فيلا = سكني
        if selected_property_type in ["شقة", "فيلا"]:
            df = df[df["property_type"].str.contains("سكني", na=False)]

        elif selected_property_type == "أرض":
            df = df[df["property_type"].str.contains("زراعي|أرض", na=False)]

    return df
