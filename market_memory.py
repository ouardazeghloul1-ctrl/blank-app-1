# market_memory.py
# =========================================
# Market Memory Layer – Warda Intelligence
# تخزين السوق ومقارنته زمنيًا
# =========================================

import os
import pandas as pd
from datetime import datetime

MEMORY_FOLDER = "market_memory"
os.makedirs(MEMORY_FOLDER, exist_ok=True)


def _build_filename(city, property_type):
    date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
    return f"{city}_{property_type}_{date_str}.csv"


def store_snapshot(df: pd.DataFrame, city: str, property_type: str):
    """
    تخزين لقطة السوق كما هي (بدون تعديل)
    """
    if df is None or df.empty:
        return None

    filename = _build_filename(city, property_type)
    path = os.path.join(MEMORY_FOLDER, filename)

    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def load_last_snapshots(city: str, property_type: str, limit=2):
    """
    تحميل آخر لقطتين للسوق
    """
    files = [
        f for f in os.listdir(MEMORY_FOLDER)
        if f.startswith(f"{city}_{property_type}")
    ]

    files = sorted(files, reverse=True)[:limit]

    snapshots = []
    for f in files:
        try:
            df = pd.read_csv(os.path.join(MEMORY_FOLDER, f))
            snapshots.append(df)
        except Exception:
            continue

    return snapshots
