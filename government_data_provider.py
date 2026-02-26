import pandas as pd

FILE_PATH = "market_transactions.csv"

def load_government_data():
    # قراءة الملف مهما كان الفاصل
    df = pd.read_csv(
        FILE_PATH,
        sep=None,
        engine="python",
        encoding="utf-8-sig"
    )

    # تنظيف أسماء الأعمدة من المسافات
    df.columns = df.columns.str.strip()

    # ==============================
    # 🔹 إعادة تسمية الأعمدة
    # عدلي الأسماء هنا إذا اختلفت عندك
    # ==============================
    column_map = {
        "المنطقة": "region",
        "المدينة": "city",
        "الحي": "district",
        "قيمة الصفقة": "price",
        "المساحة": "area",
        "تاريخ الصفقة": "date",
        "نوع العقار": "property_type",
        "تصنيف العقار": "property_type"
    }

    df = df.rename(columns=column_map)

    # ==============================
    # 🔹 تأمين الأعمدة الأساسية
    # ==============================
    required_columns = ["city", "district", "price", "area", "date"]

    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    # إذا لم يوجد نوع عقار ننشئه
    if "property_type" not in df.columns:
        df["property_type"] = "غير محدد"

    # ==============================
    # 🔹 تنظيف القيم النصية
    # ==============================
    df["city"] = df["city"].astype(str).str.strip()
    df["property_type"] = df["property_type"].astype(str).str.strip()

    # ==============================
    # 🔹 توحيد أسماء المدن
    # ==============================
    df["city"] = df["city"].replace({
        "منطقة الرياض": "الرياض",
        "منطقة مكة المكرمة": "مكة المكرمة",
        "منطقة المدينة المنورة": "المدينة المنورة",
        "منطقة الشرقية": "الدمام"
    })

    # ==============================
    # 🔹 توحيد أنواع العقارات
    # ==============================
    df["property_type"] = df["property_type"].replace({
        "شقق": "شقة",
        "شقة سكنية": "شقة",
        "وحدة سكنية": "شقة",
        "فلل": "فيلا",
        "فيلا سكنية": "فيلا",
        "أراضي": "أرض",
        "قطعة أرض": "أرض"
    })

    # ==============================
    # 🔹 تحويل أرقام
    # ==============================
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["area"] = pd.to_numeric(df["area"], errors="coerce")

    # حساب سعر المتر
    df["price_per_sqm"] = df["price"] / df["area"]

    # إزالة الصفوف غير الصالحة
    df = df.dropna(subset=["price", "area"])

    return df
