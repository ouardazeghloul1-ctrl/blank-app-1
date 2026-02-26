# =========================================
# Government Data Provider
# تحميل بيانات وزارة العدل وتحضيرها للنظام
# =========================================

import pandas as pd
from pathlib import Path

# ضع هنا اسم ملف الوزارة بالضبط
DATA_PATH = Path("data/market_transactions.csv")

def load_government_data(selected_city=None, selected_property_type=None):
    """
    تحميل بيانات وزارة العدل
    - فلترة حسب المدينة فقط
    - تجاهل نوع العقار (لأن الوزارة تكتب 'سكني')
    - تجهيز الأعمدة للنظام
    """

    try:
        if not DATA_PATH.exists():
            print("❌ ملف البيانات غير موجود في المسار:", DATA_PATH)
            return pd.DataFrame()

        # قراءة الملف
        df = pd.read_csv(DATA_PATH)

        if df.empty:
            print("⚠️ ملف البيانات فارغ")
            return df

        # تنظيف أسماء الأعمدة
        df.columns = df.columns.str.strip()

        # ==============================
        # فلترة المدينة فقط
        # ==============================
        if selected_city and "المدينة" in df.columns:
            df = df[df["المدينة"].astype(str).str.contains(selected_city, na=False)]

        if df.empty:
            print(f"⚠️ لا توجد بيانات لمدينة {selected_city}")
            return df

        # ==============================
        # تنظيف وتحويل السعر
        # ==============================
        if "السعر" in df.columns:
            df["السعر"] = (
                df["السعر"]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace('"', "", regex=False)
                .astype(float)
            )

        # ==============================
        # تنظيف وتحويل المساحة
        # ==============================
        if "المساحة" in df.columns:
            df["المساحة"] = (
                df["المساحة"]
                .astype(str)
                .str.replace(",", "", regex=False)
                .astype(float)
            )

        # ==============================
        # حساب سعر المتر
        # ==============================
        if "السعر" in df.columns and "المساحة" in df.columns:
            df["سعر_المتر"] = df["السعر"] / df["المساحة"]

        # ==============================
        # توحيد اسم الحي إذا وجد
        # ==============================
        if "الحي / المدينة" in df.columns:
            df["الحي"] = df["الحي / المدينة"]

        # ==============================
        # إضافة عمود نوع العقار (افتراضي)
        # لأن الوزارة لا تفصل بين شقة/فيلا
        # ==============================
        df["نوع_العقار"] = "سكني"

        print(f"✅ تم تحميل {len(df)} صفقة من {selected_city}")

        return df

    except Exception as e:
        print(f"❌ خطأ في تحميل البيانات الحكومية: {e}")
        return pd.DataFrame()
