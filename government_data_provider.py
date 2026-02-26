import pandas as pd
import csv

FILE_PATH = "market_transactions.csv"

def load_government_data(selected_city=None, selected_property_type=None):

    rows = []

    # قراءة الملف بطريقة تدعم الأرقام التي تحتوي فاصلة مثل "100,000"
    with open(FILE_PATH, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    df = pd.DataFrame(rows)

    # حذف الهيدر إذا كان موجود
    if df.iloc[0].astype(str).str.contains("المنطقة").any():
        df = df.iloc[1:].reset_index(drop=True)

    # أخذ أول 10 أعمدة فقط
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
    text_cols = ["region", "city", "district", "property_type"]
    for col in text_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace(",", "", regex=False)
        )

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

    # حذف الصفوف الفارغة رقمياً
    df = df.dropna(subset=["price", "area"])

    # حساب سعر المتر
    df["price_per_sqm"] = df["price"] / df["area"]

    # =========================
    # فلترة المدينة (بحث مرن جداً)
    # =========================
    if selected_city:
        selected_city = selected_city.strip()

        df = df[
            df["region"].str.contains(selected_city, na=False) |
            df["city"].str.contains(selected_city, na=False) |
            df["district"].str.contains(selected_city, na=False)
        ]

    # =========================
    # فلترة نوع العقار (مؤقتاً مبسطة)
    # وزارة العدل تستخدم فقط: سكني / تجاري / زراعي
    # =========================
    if selected_property_type:

        if selected_property_type in ["شقة", "فيلا"]:
            df = df[df["property_type"].str.contains("سكني", na=False)]

        elif selected_property_type == "أرض":
            df = df[df["property_type"].str.contains("زراعي|أرض", na=False)]

    return df
