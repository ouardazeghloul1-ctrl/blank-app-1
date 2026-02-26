import pandas as pd

FILE_PATH = "market_transactions.csv"

def load_government_data():
    df = pd.read_csv(
        FILE_PATH,
        sep=";",                 # ✅ غالباً هذا هو الصحيح
        encoding="utf-8-sig",
        engine="python"          # مهم لتفادي أخطاء parsing
    )
    return df
