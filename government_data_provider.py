# =========================================
# Government Data Provider - Stable Version
# =========================================

import pandas as pd
from pathlib import Path

DATA_PATH = Path("market_transactions.csv")

def load_government_data(selected_city=None, selected_property_type=None):
    """
    تحميل بيانات حكومية حقيقية مع فلترة ذكية
    المصدر الوحيد للحقيقة في النظام
    """
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

        # تنظيف أسماء الأعمدة
        df.columns = df.columns.str.strip()
        print("📊 الأعمدة المتوفرة:", df.columns.tolist())

        # ======================
        # توحيد الأعمدة الأساسية (موسع)
        # ======================

        column_map = {
            "السعر": "price",
            "قيمة الصفقة": "price",
            "سعر البيع": "price",
            "تاريخ الصفقة": "date",
            "التاريخ": "date",
            "الحي": "district",
            "الحي / المدينة": "district",
            "المنطقة": "city",           # ✅ الأهم: المنطقة = city
            "المدينة": "city",
            "المساحة": "area",
            "نوع العقار": "property_type",
            "نوع_العقار": "property_type"
        }

        for ar_col, en_col in column_map.items():
            if ar_col in df.columns:
                df[en_col] = df[ar_col]

        # ======================
        # تنظيف السعر (إلزامي)
        # ======================

        if "price" in df.columns:
            df["price"] = pd.to_numeric(df["price"], errors="coerce")
        else:
            print("⚠️ لا يوجد عمود سعر - لا يمكن المتابعة")
            return pd.DataFrame()

        df = df.dropna(subset=["price"])

        # ======================
        # تنظيف المساحة (إن وجدت)
        # ======================

        if "area" in df.columns:
            df["area"] = pd.to_numeric(df["area"], errors="coerce")
            # بعض الصفقات قد لا تحتوي مساحة → نعطي قيمة افتراضية 100
            df["area"] = df["area"].fillna(100)
        else:
            # إذا ما في مساحة أبداً → نضيف عمود بقيمة افتراضية
            df["area"] = 100

        # ======================
        # فلترة المدينة الذكية (الأهم)
        # ======================

        if selected_city:
            city_mask = pd.Series([False] * len(df))

            # البحث في عمود city (إن وجد)
            if "city" in df.columns:
                city_mask = city_mask | df["city"].astype(str).str.contains(selected_city, na=False)

            # البحث في عمود district (إن وجد)
            if "district" in df.columns:
                city_mask = city_mask | df["district"].astype(str).str.contains(selected_city, na=False)

            # إذا لم نجد أي تطابق، نحاول البحث في النص الكامل للصف (حل أخير)
            if not city_mask.any():
                # دمج جميع الأعمدة النصية والبحث فيها
                text_columns = df.select_dtypes(include=['object']).columns
                for col in text_columns:
                    city_mask = city_mask | df[col].astype(str).str.contains(selected_city, na=False)

            df = df[city_mask]

        # ======================
        # فلترة نوع العقار
        # ======================

        if selected_property_type and selected_property_type != "الكل":
            property_mask = pd.Series([False] * len(df))
            
            possible_cols = ["property_type", "نوع العقار", "نوع_العقار"]
            for col in possible_cols:
                if col in df.columns:
                    property_mask = property_mask | df[col].astype(str).str.contains(selected_property_type, na=False)
            
            # إذا وجدنا تطابق، نطبق الفلترة
            if property_mask.any():
                df = df[property_mask]

        # ======================
        # أعمدة افتراضية لحماية النظام
        # ======================

        if "district" not in df.columns:
            df["district"] = "غير محدد"

        if "date" not in df.columns:
            df["date"] = pd.NA

        if "property_type" not in df.columns:
            df["property_type"] = selected_property_type or "غير محدد"

        # ======================
        # إحصائيات للتصحيح
        # ======================

        print(f"✅ تم تحميل {len(df)} صفقة")
        if selected_city:
            print(f"🏙️ بعد فلترة المدينة '{selected_city}': {len(df)} صفقة")
        if selected_property_type:
            print(f"🏠 بعد فلترة النوع '{selected_property_type}': {len(df)} صفقة")

        return df.reset_index(drop=True)

    except Exception as e:
        print("❌ خطأ في تحميل البيانات:", str(e))
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


# ======================
# دالة اختبار سريعة (تشغيل يدوي)
# ======================
if __name__ == "__main__":
    print("🔍 اختبار تحميل البيانات:")
    
    # اختبار بدون فلترة
    df_all = load_government_data()
    print(f"كل البيانات: {len(df_all)} صفقة")
    
    # اختبار مع فلترة الرياض
    df_riyadh = load_government_data(selected_city="الرياض")
    print(f"الرياض: {len(df_riyadh)} صفقة")
    
    # اختبار مع فلترة شقق في الرياض
    df_riyadh_apart = load_government_data(selected_city="الرياض", selected_property_type="شقة")
    print(f"شقق الرياض: {len(df_riyadh_apart)} صفقة")
    
    # عرض أول 5 صفوف للتحقق
    if not df_riyadh.empty:
        print("\n📋 عينة من بيانات الرياض:")
        print(df_riyadh[["price", "area", "district", "city"] if "city" in df_riyadh.columns else ["price", "area"]].head())
