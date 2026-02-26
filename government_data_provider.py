import pandas as pd
import os

FILE_PATH = "market_transactions.csv"

def load_government_data():
    print("هل الملف موجود؟", os.path.exists(FILE_PATH))

    try:
        df = pd.read_csv(
            FILE_PATH,
            sep=",",
            encoding="utf-8-sig",
            engine="python",
            low_memory=False
        )
    except Exception as e:
        raise Exception(f"خطأ أثناء قراءة الملف: {e}")

    print("الأعمدة الموجودة:", df.columns.tolist())

    return df
