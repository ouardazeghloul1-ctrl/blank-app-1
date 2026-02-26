import pandas as pd

FILE_PATH = "market_transactions.csv"

def load_government_data():
    df = pd.read_csv(FILE_PATH, sep=",", encoding="utf-8-sig")

    df = df.rename(columns={
        "المدينة": "city",
        "تصنيف العقار": "property_type",
        "السعر": "price",
        "المساحة": "area",
        "تاريخ الصفقة ميلادي": "date",
        "المدينة / الحي": "district"
    })

    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df["area"] = pd.to_numeric(df["area"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.dropna(subset=["price", "area", "date"])

    df["transaction_type"] = "بيع"
    df["price_per_sqm"] = df["price"] / df["area"]

    return df
