# =========================================
# Government Data Provider - الإصدار النهائي بعد تعديل المدينة الذكي
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
        # ✅ توحيد الأعمدة الأساسية - المعدل حسب ملف منصتك
        # ======================

        column_map = {
            "السعر": "price",
            "قيمة الصفقة": "price",
            "سعر البيع": "price",

            "تاريخ الصفقة": "date",
            "تاريخ الصفقة ميلادي": "date",

            "المنطقة": "city",
            "المدينة": "city",

            "المدينة / الحي": "district",

            "المساحة": "area",

            "تصنيف العقار": "property_type",   # 🔥 هذا أهم سطر

            "عدد العقارات": "units"
        }

        for ar_col, en_col in column_map.items():
            if ar_col in df.columns:
                df[en_col] = df[ar_col]

        # ======================
        # تنظيف النصوص من المسافات والرموز المخفية (الأهم)
        # ======================

        text_columns = df.select_dtypes(include=['object']).columns
        for col in text_columns:
            df[col] = df[col].astype(str).str.strip()

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
        # 🔍 طباعة القيم الفريدة للتصحيح
        # ======================

        print("\n🔎 القيم الفريدة قبل الفلترة:")
        if "property_type" in df.columns:
            unique_types = df["property_type"].unique()
            print(f"نوع العقار: {unique_types[:10]}")
        if "city" in df.columns:
            unique_cities = df["city"].unique()
            print(f"المدينة: {unique_cities[:10]}")
        if "district" in df.columns:
            unique_districts = df["district"].unique()
            print(f"الحي: {unique_districts[:5]}")

        # ======================
        # فلترة المدينة الذكية جدًا (مع إزالة "ال")
        # ======================

        if selected_city:
            city_mask = pd.Series(False, index=df.index)

            # إزالة "ال" من بداية الاسم للمقارنة المرنة
            clean_selected = selected_city.replace("ال", "").strip()
            print(f"🔍 البحث عن: '{selected_city}' (بعد التنظيف: '{clean_selected}')")

            if "city" in df.columns:
                # تنظيف عمود المدينة من "ال" أيضًا
                df_city_clean = df["city"].astype(str).str.replace("ال", "", regex=False).str.strip()
                city_mask = city_mask | df_city_clean.str.contains(clean_selected, na=False, regex=False)

            if "district" in df.columns:
                # تنظيف عمود الحي من "ال" أيضًا
                df_district_clean = df["district"].astype(str).str.replace("ال", "", regex=False).str.strip()
                city_mask = city_mask | df_district_clean.str.contains(clean_selected, na=False, regex=False)

            df = df[city_mask]
            
            # إحصائيات بعد الفلترة
            print(f"🏙️ بعد فلترة المدينة '{selected_city}': {len(df)} صفقة")

        # ======================
        # فلترة نوع العقار الذكية (الحل الصحيح)
        # ======================

        if selected_property_type and selected_property_type != "الكل":
            
            # خريطة التحويل بين اختيار المستخدم والبيانات الحكومية
            property_mapping = {
                "شقة": "سكني",
                "فيلا": "سكني",
                "أرض": "سكني",
                "محل تجاري": "تجاري",
                "سكني": "سكني",      # للحالات المباشرة
                "تجاري": "تجاري"      # للحالات المباشرة
            }

            mapped_type = property_mapping.get(selected_property_type)
            
            if mapped_type and "property_type" in df.columns:
                # فلترة حسب النوع المحول
                df = df[df["property_type"].str.contains(mapped_type, na=False, regex=False)]
                print(f"🏠 تم تحويل '{selected_property_type}' → '{mapped_type}'")
            
            # إذا لم نجد property_type، نحاول البحث في الوصف
            elif "description" in df.columns and mapped_type:
                df = df[df["description"].str.contains(mapped_type, na=False, regex=False)]
            
            # إذا ما زلنا لم نجد، نستخدم البحث النصي العام (محسن)
            else:
                print("⚠️ لم نجد property_type، نبحث في النص العام...")
                # البحث في كل الأعمدة النصية
                text_columns = df.select_dtypes(include=['object']).columns
                type_mask = pd.Series(False, index=df.index)
                
                # استخدام الكلمة الكاملة للبحث (وليس [:3])
                search_terms = [selected_property_type]
                if selected_property_type == "محل تجاري":
                    search_terms = ["تجاري", "محل"]
                
                for col in text_columns:
                    for term in search_terms:
                        type_mask = type_mask | df[col].str.contains(term, na=False, regex=False)
                
                if type_mask.any():
                    df = df[type_mask]

            # إحصائيات بعد فلترة النوع
            if selected_property_type:
                print(f"🏠 بعد فلترة النوع '{selected_property_type}': {len(df)} صفقة")

        # ======================
        # أعمدة افتراضية لحماية النظام
        # ======================

        if "district" not in df.columns:
            df["district"] = "غير محدد"

        if "date" not in df.columns:
            df["date"] = pd.NA

        if "property_type" not in df.columns:
            df["property_type"] = "سكني"  # قيمة افتراضية

        # ======================
        # إحصائيات نهائية
        # ======================

        print(f"\n✅ تم تحميل {len(df)} صفقة في النتيجة النهائية")

        return df.reset_index(drop=True)

    except Exception as e:
        print("❌ خطأ في تحميل البيانات:", str(e))
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


# ======================
# دالة اختبار شاملة (تشغيل يدوي)
# ======================
if __name__ == "__main__":
    print("=" * 60)
    print("🔍 اختبار تحميل البيانات - الإصدار النهائي بعد تعديل المدينة الذكي")
    print("=" * 60)
    
    # اختبار 1: كل البيانات
    print("\n📊 1. كل البيانات:")
    df_all = load_government_data()
    print(f"→ الإجمالي: {len(df_all)} صفقة")
    
    # اختبار 2: الرياض فقط
    print("\n" + "=" * 60)
    print("📊 2. الرياض:")
    df_riyadh = load_government_data(selected_city="الرياض")
    print(f"→ الرياض: {len(df_riyadh)} صفقة")
    
    # اختبار 3: شقق الرياض (الأهم)
    print("\n" + "=" * 60)
    print("📊 3. شقق الرياض:")
    df_riyadh_apart = load_government_data(selected_city="الرياض", selected_property_type="شقة")
    print(f"→ شقق الرياض: {len(df_riyadh_apart)} صفقة")
    
    # اختبار 4: فلل الرياض
    print("\n" + "=" * 60)
    print("📊 4. فلل الرياض:")
    df_riyadh_villa = load_government_data(selected_city="الرياض", selected_property_type="فيلا")
    print(f"→ فلل الرياض: {len(df_riyadh_villa)} صفقة")
    
    # اختبار 5: محال تجارية الرياض
    print("\n" + "=" * 60)
    print("📊 5. محال تجارية الرياض:")
    df_riyadh_commercial = load_government_data(selected_city="الرياض", selected_property_type="محل تجاري")
    print(f"→ محال تجارية الرياض: {len(df_riyadh_commercial)} صفقة")
    
    # اختبار 6: جدة
    print("\n" + "=" * 60)
    print("📊 6. جدة:")
    df_jeddah = load_government_data(selected_city="جدة")
    print(f"→ جدة: {len(df_jeddah)} صفقة")
    
    # اختبار 7: شقق جدة
    print("\n" + "=" * 60)
    print("📊 7. شقق جدة:")
    df_jeddah_apart = load_government_data(selected_city="جدة", selected_property_type="شقة")
    print(f"→ شقق جدة: {len(df_jeddah_apart)} صفقة")
    
    # اختبار 8: الرياض بدون "ال" (للتأكد من المرونة)
    print("\n" + "=" * 60)
    print("📊 8. الرياض (بدون ال):")
    df_riyadh_no_al = load_government_data(selected_city="رياض")
    print(f"→ الرياض: {len(df_riyadh_no_al)} صفقة")
    
    # عرض عينة من البيانات إذا وجدت
    if not df_riyadh_apart.empty:
        print("\n" + "=" * 60)
        print("📋 عينة من شقق الرياض (أول 5 صفقات):")
        display_cols = []
        if "price" in df_riyadh_apart.columns:
            display_cols.append("price")
        if "area" in df_riyadh_apart.columns:
            display_cols.append("area")
        if "district" in df_riyadh_apart.columns:
            display_cols.append("district")
        if "property_type" in df_riyadh_apart.columns:
            display_cols.append("property_type")
        
        if display_cols:
            print(df_riyadh_apart[display_cols].head())
        else:
            print("✅ توجد بيانات ولكن لا توجد أعمدة للعرض")
    
    print("\n" + "=" * 60)
    print("✅ انتهى الاختبار")
    print("=" * 60)
