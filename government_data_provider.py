# =========================================
# Government Data Provider - النسخة النهائية المستقرة
# =========================================

import pandas as pd
from pathlib import Path

# الملف موجود داخل نفس المشروع
DATA_PATH = Path("market_transactions.csv")


def load_government_data(selected_city=None, selected_property_type=None):
    """
    تحميل بيانات السوق من ملف CSV داخل المشروع
    المصدر الرسمي الوحيد للبيانات
    """

    try:
        # ======================
        # 1️⃣ قراءة الملف المحلي
        # ======================
        if not DATA_PATH.exists():
            print("❌ ملف market_transactions.csv غير موجود داخل المشروع")
            return pd.DataFrame()

        df = pd.read_csv(DATA_PATH, encoding="utf-8-sig", low_memory=False)

        if df.empty:
            print("⚠️ الملف موجود لكنه فارغ")
            return df

        # تنظيف أسماء الأعمدة
        df.columns = df.columns.str.strip()

        # ======================
        # 2️⃣ توحيد أسماء الأعمدة
        # ======================

        column_map = {
            "السعر": "price",
            "قيمة الصفقة": "price",

            "تاريخ الصفقة ميلادي": "date",
            "تاريخ الصفقة": "date",

            "المنطقة": "region",
            "المدينة": "city",

            "المدينة / الحي": "district",

            "المساحة": "area",

            "تصنيف العقار": "property_type",

            "عدد العقارات": "units"
        }

        for ar_col, en_col in column_map.items():
            if ar_col in df.columns:
                df[en_col] = df[ar_col]

        # ======================
        # 3️⃣ تنظيف البيانات الأساسية
        # ======================

        # السعر
        if "price" not in df.columns:
            print("❌ لا يوجد عمود سعر")
            return pd.DataFrame()

        # تنظيف السعر من الفواصل والرموز
        df["price"] = (
            df["price"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace(" ", "", regex=False)
        )

        df["price"] = pd.to_numeric(df["price"], errors="coerce")

        # لا نحذف كل الصفوف مباشرة
        df = df[df["price"] > 0]

        # المساحة
        if "area" in df.columns:
            df["area"] = pd.to_numeric(df["area"], errors="coerce")
        else:
            df["area"] = None

        # تنظيف النصوص
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()

        # ======================
        # 4️⃣ فلترة المدينة
        # ======================

        if selected_city and "city" in df.columns:
            df = df[df["city"].str.contains(selected_city, na=False)]

        # ======================
        # 5️⃣ فلترة نوع العقار - نسخة ذكية
        # ======================

        if selected_property_type and selected_property_type != "الكل":
            if "property_type" in df.columns:

                # تحويل اختيار المستخدم إلى التصنيف الحكومي
                property_map = {
                    "شقة": "سكني",
                    "فيلا": "سكني",
                    "أرض": "سكني",
                    "محل تجاري": "تجاري",
                    "سكني": "سكني",
                    "تجاري": "تجاري"
                }

                mapped_value = property_map.get(selected_property_type)

                if mapped_value:
                    df = df[df["property_type"].str.contains(mapped_value, na=False)]
                else:
                    # إذا لم يكن هناك تطابق في الخريطة، استخدم النص الأصلي
                    df = df[df["property_type"].str.contains(selected_property_type, na=False)]

        # ======================
        # 6️⃣ حماية أعمدة أساسية
        # ======================

        if "district" not in df.columns:
            df["district"] = "غير محدد"

        if "property_type" not in df.columns:
            df["property_type"] = "غير محدد"

        if "date" not in df.columns:
            df["date"] = None

        print(f"✅ تم تحميل {len(df)} صفقة")

        return df.reset_index(drop=True)

    except Exception as e:
        print("❌ خطأ أثناء تحميل البيانات:", e)
        return pd.DataFrame()
