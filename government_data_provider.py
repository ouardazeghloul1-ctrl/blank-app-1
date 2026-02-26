import pandas as pd

FILE_PATH = "market_transactions.csv"

def load_government_data():
    df = pd.read_csv(
    FILE_PATH,
    sep=None,
    engine="python",
    encoding="utf-8-sig"

    )
    return df
