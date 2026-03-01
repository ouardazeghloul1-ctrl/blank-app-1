# =========================================
# Government Data Provider - Stable Version
# =========================================

import pandas as pd
from pathlib import Path

DATA_PATH = Path("market_transactions.csv")

def load_government_data(selected_city=None, selected_property_type=None):

    try:
        if not DATA_PATH.exists():
            print("❌ ملف البيانات غير موجود:", DATA_PATH.absolute())
            return pd.DataFrame()

        df = pd.read_csv(
            DATA_PATH,
            encoding="cp1256",
            engine="python",
            on_bad_lines="skip"
        )

        if df.empty:
            print("⚠️ ملف البيانات فارغ")
            return df

        df.columns = df.columns.str.strip()

        print("📊 الأعمدة:", df.columns.tolist())

        # ======================
        # توحيد الأعمدة الأساسية
        # ======================

        column_map = {
            "السعر": "price",
            "قيمة الصفقة": "price",
            "تاريخ الصفقة": "date",
            "التاريخ": "date",
            "الحي": "district",
            "الحي / المدينة": "district",
            "المدينة": "city"
        }

        for ar_col, en_col in column_map.items():
            if ar_col in df.columns:
                df[en_col] = df[ar_col]

        # ======================
        # تنظيف السعر
        # ======================

        if "price" in df.columns:
            df["price"] = pd.to_numeric(df["price"], errors="coerce")
        else:
            print("⚠️ لا يوجد عمود سعر")
            return pd.DataFrame()

        df = df.dropna(subset=["price"])

        # ======================
        # فلترة المدينة (إن وجدت)
        # ======================

        if selected_city and "district" in df.columns:
            df = df[df["district"].astype(str).str.contains(selected_city, na=False)]

        if df.empty:
            print("⚠️ لا توجد بيانات بعد الفلترة")
            return df

        # ======================
        # أعمدة افتراضية لحماية النظام
        # ======================

        if "area" not in df.columns:
            df["area"] = 1  # مؤقتاً لمنع الانهيار

        if "district" not in df.columns:
            df["district"] = "غير محدد"

        if "date" not in df.columns:
            df["date"] = pd.NA

        print(f"✅ تم تحميل {len(df)} صفقة")

        return df.reset_index(drop=True)

    except Exception as e:
        print("❌ خطأ:", e)
        return pd.DataFrame()
