import pandas as pd

FILE_PATH = "market_transactions.csv"

def load_government_data():
    df = pd.read_csv(
        FILE_PATH,
        sep=",",                # مهم جداً
        encoding="utf-8-sig",
        low_memory=False       # مع المحرك الافتراضي فقط
    )

    return df
