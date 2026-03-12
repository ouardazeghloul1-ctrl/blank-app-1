import pandas as pd

def repair_market_data(df):

    if df is None or df.empty:
        return df

    data = df.copy()

    # إصلاح المساحة
    if "area" in data.columns:
        median_area = data["area"].median()

        if pd.isna(median_area):
            median_area = 120

        data["area"] = data["area"].fillna(median_area)
        data.loc[data["area"] <= 0, "area"] = median_area

    # إصلاح السعر
    if "price" in data.columns:
        median_price = data["price"].median()

        if pd.isna(median_price):
            median_price = 500000

        data["price"] = data["price"].fillna(median_price)

    # إصلاح التاريخ
    if "date" in data.columns:
        data["date"] = pd.to_datetime(data["date"], errors="coerce")
        data["date"] = data["date"].ffill()

    return data
