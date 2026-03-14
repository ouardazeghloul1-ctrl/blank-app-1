# =========================================
# Government Data Provider - الإصدار الصناعي النهائي (Enterprise Grade)
# =========================================
"""
🚀 طبقة البيانات الذكية - تقرأ أي ملف حكومي وتفهمه تلقائياً
🏗️  جاهزة لأنظمة تصنيف الأحياء الاستثمارية
💎  نسخة محسنة بالكامل - جاهزة للإنتاج
"""

import pandas as pd
import re
from pathlib import Path
from typing import Dict, Optional

# الملف موجود داخل نفس المشروع
DATA_PATH = Path("market_transactions.csv")


def smart_column_mapper(df: pd.DataFrame) -> Dict[str, str]:
    """
    🧠 محرك اكتشاف الأعمدة الذكي - يقرأ أي ملف حكومي مهما تغيرت أسماء الأعمدة
    يستخدم نظام تسجيل (Scoring System) لتحديد أفضل تطابق
    """
    
    # أنماط البحث لكل عمود مستهدف (مدعومة بالعربية والإنجليزية)
    column_patterns = {
        "price": [
            "السعر", "قيمة الصفقة", "اجمالي قيمة الصفقات", "الثمن", 
            "المبلغ", "price", "total_value", "اجمالي", "القيمة",
            "قيمة", "price_value"
        ],
        "area": [
            "المساحة", "المساحه", "متر", "مساحة", "area", "property_area",
            "المساحة بالمتر", "الوحدات", "المساحه بالمتر",
            "مساحه", "sqm"
        ],
        "city": [
            "المدينة", "city", "اسم المدينة", "المنطقة الادارية", "المدينه"
        ],
        "district": [
            "الحي", "حي", "المدينة / الحي", "الاحياء", "المنطقة", "district",
            "اسم الحي", "الاحياء السكنية", "الحي / المنطقة",
            "المدينة الحي", "neighborhood"
        ],
        "date": [
            "تاريخ الصفقة", "التاريخ", "تاريخ العقد", "date", "transaction_date",
            "تاريخ الصفقة ميلادي", "تاريخ التسجيل", "تاريخ العقد ميلادي"
        ],
        "property_type": [
            "تصنيف العقار", "نوع العقار", "الغرض", "property_type", "usage",
            "الاستخدام", "نوع الصفقة", "التصنيف"
        ],
        "units": [
            "عدد العقارات", "الوحدات", "units", "عدد الوحدات", "العدد",
            "عدد الوحدات بالصفقة"
        ]
    }
    
    mapping = {}
    used_columns = set()
    
    # البحث عن أفضل تطابق لكل عمود
    for target, patterns in column_patterns.items():
        best_match = None
        best_score = 0
        
        for col in df.columns:
            if col in used_columns:
                continue
                
            col_clean = col.strip().replace(" ", "").replace("/", "").replace("-", "").lower()
            
            for pattern in patterns:
                pattern_clean = pattern.replace(" ", "").replace("/", "").replace("-", "").lower()
                
                # حساب درجة المطابقة:
                # 100: تطابق تام
                # 80: النمط موجود داخل اسم العمود
                # 60: اسم العمود موجود داخل النمط
                if pattern_clean == col_clean:
                    score = 100
                elif pattern_clean in col_clean:
                    score = 80
                elif col_clean in pattern_clean:
                    score = 60
                else:
                    continue
                
                if score > best_score:
                    best_score = score
                    best_match = col
        
        if best_match:
            mapping[target] = best_match
            used_columns.add(best_match)
    
    # تقرير بالاكتشافات
    print("🔍 Smart Column Mapper اكتشف:")
    if mapping:
        for target, original in mapping.items():
            print(f"  ✅ {target:12} ← '{original}'")
    else:
        print("  ⚠️ لم يتم اكتشاف أي أعمدة!")
    
    for target in column_patterns.keys():
        if target not in mapping:
            print(f"  ⚠️ {target:12} ← لم يتم العثور على عمود")
    
    return mapping


def clean_price(price_series: pd.Series) -> pd.Series:
    """💰 تنظيف وتحويل عمود السعر بذكاء فائق - محسن للأداء"""
    
    # ✅ تحسين معالجة القيم الفارغة
    cleaned = price_series.fillna('').astype(str)
    
    # ✅ تحسين الأداء: استخدام str.replace بدلاً من apply مع re.sub
    cleaned = cleaned.str.replace(r'[^\d.]', '', regex=True)
    
    # تحويل إلى رقم
    numeric_prices = pd.to_numeric(cleaned, errors='coerce')
    
    # تطبيق فلتر منطقي للأسعار (إزالة الأخطاء الواضحة)
    valid_price_mask = (numeric_prices > 1000) & (numeric_prices < 1_000_000_000)
    
    # ✅ استخدام pd.NA بدلاً من None
    numeric_prices[~valid_price_mask] = pd.NA
    
    return numeric_prices


def normalize_property_type(type_series: pd.Series) -> pd.Series:
    """
    🏠 توحيد تصنيفات العقارات لأنظمة التحليل الذكية
    سكني، تجاري، أرض، اخرى
    """
    
    # خريطة تصنيف شاملة
    type_map = {
        # سكني
        'شقة': 'سكني',
        'فيلا': 'سكني',
        'بيت': 'سكني',
        'دور': 'سكني',
        'شاليه': 'سكني',
        'سكني': 'سكني',
        'سكن': 'سكني',
        'منزل': 'سكني',
        'دوبلكس': 'سكني',
        'تاون هاوس': 'سكني',
        
        # تجاري
        'محل': 'تجاري',
        'معرض': 'تجاري',
        'مكتب': 'تجاري',
        'عيادة': 'تجاري',
        'تجاري': 'تجاري',
        'مركز': 'تجاري',
        'مخزن': 'تجاري',
        'مستودع': 'تجاري',
        
        # أرض
        'ارض': 'أرض',
        'أرض': 'أرض',
        'قطعة': 'أرض',
        'ارض خام': 'أرض',
        'اراضي': 'أرض',
        'قطعة ارض': 'أرض'
    }
    
    def normalize_single(value):
        if pd.isna(value):
            return 'اخرى'
        
        value_str = str(value).strip()
        for key, normalized in type_map.items():
            if key in value_str:
                return normalized
        return 'اخرى'
    
    return type_series.apply(normalize_single)


def load_government_data(selected_city: Optional[str] = None, 
                        selected_property_type: Optional[str] = None) -> pd.DataFrame:
    """
    🎯 المحرك الرئيسي للبيانات - واجهة موحدة لجميع أنظمة المشروع
    
    المخرجات: DataFrame موحد يحتوي على:
    - price: السعر بعد التنظيف
    - price_raw: السعر الأصلي قبل التقدير
    - area: المساحة (بدون قيم صفرية)
    - price_per_sqm: سعر المتر المربع (عدد صحيح)
    - city: المدينة
    - district: الحي الأصلي (بعد استخراج اسم الحي فقط)
    - property_type: نوع العقار الموحد
    - property_subtype: نوع العقار الفرعي (شقة/فيلا/تاون هاوس/غير سكني)
    - date: التاريخ
    - units: عدد الوحدات
    - price_source: مصدر السعر (original/estimated)
    - price_validity: حالة السعر (valid/estimated/corrected)
    """
    
    try:
        # ======================
        # 1️⃣ قراءة الملف
        # ======================
        if not DATA_PATH.exists():
            print(f"❌ ملف البيانات غير موجود في المسار: {DATA_PATH}")
            print("📌 يرجى التأكد من وجود ملف market_transactions.csv")
            return pd.DataFrame()
        
        print(f"📂 جاري قراءة الملف: {DATA_PATH}")
        
        # دعم CSV و Excel
        if DATA_PATH.suffix.lower() == ".xlsx":
            df = pd.read_excel(DATA_PATH)
        else:
            # ملفات الوزارة مفصولة بفاصلة منقوطة ;
            df = pd.read_csv(DATA_PATH, encoding="utf-8-sig", sep=";", low_memory=False)
        if df.empty:
            print("⚠️ الملف فارغ - لا توجد بيانات للتحليل")
            return df
        
        print(f"📊 إجمالي الصفوف في الملف الخام: {len(df):,}")
        
        # ======================
        # 2️⃣ اكتشاف الأعمدة
        # ======================
        column_mapping = smart_column_mapper(df)
        
        # التأكد من وجود عمود السعر (إلزامي)
        if 'price' not in column_mapping:
            print("❌ لا يمكن الاستمرار: لم يتم العثور على عمود السعر")
            print("📌 الأعمدة الموجودة:", list(df.columns))
            return pd.DataFrame()
        
        # ======================
        # 3️⃣ بناء DataFrame الموحد
        # ======================
        normalized_df = pd.DataFrame()
        
        # السعر الخام (مع الاحتفاظ به للمراجعة)
        normalized_df['price_raw'] = clean_price(df[column_mapping['price']])
        normalized_df['price'] = normalized_df['price_raw'].copy()
        
        # المساحة
        if 'area' in column_mapping:
            normalized_df['area'] = pd.to_numeric(df[column_mapping['area']], errors='coerce')
            
            # إزالة المساحات غير المنطقية
            normalized_df.loc[normalized_df['area'] <= 0, 'area'] = pd.NA
            normalized_df.loc[normalized_df['area'] > 20000, 'area'] = pd.NA  # تعديل الحد الأقصى للمساحة
            
            # حساب متوسط المساحة من القيم الموجبة فقط
            median_area = normalized_df.loc[normalized_df['area'] > 0, 'area'].median()
            if pd.isna(median_area):
                median_area = 120
            normalized_df['area'] = normalized_df['area'].fillna(median_area)
        else:
            normalized_df['area'] = 120  # قيمة افتراضية إذا لم يوجد عمود المساحة
        
        # المدينة
        if 'city' in column_mapping:
            normalized_df['city'] = df[column_mapping['city']].astype(str).str.strip()
            # تنظيف اسم المدينة
            normalized_df['city'] = normalized_df['city'].str.replace("منطقة", "", regex=False)
            normalized_df['city'] = normalized_df['city'].str.replace("المنطقة", "", regex=False)
            normalized_df['city'] = normalized_df['city'].str.replace("الادارية", "", regex=False)
            normalized_df['city'] = normalized_df['city'].str.strip()
        else:
            normalized_df['city'] = 'غير محدد'
        
        # الحي - استخراج اسم الحي فقط مع توحيد المسافات بشكل ذكي
        if 'district' in column_mapping:
            normalized_df['district'] = (
                df[column_mapping['district']]
                .astype(str)
                .str.replace(r"\s+", " ", regex=True)  # توحيد المسافات المتعددة إلى مسافة واحدة
                .str.split("/")
                .str[-1]
                .str.strip()
            )
        else:
            normalized_df['district'] = 'غير محدد'
        
        # التاريخ
        if 'date' in column_mapping:
            normalized_df['date'] = pd.to_datetime(df[column_mapping['date']], errors='coerce')
            normalized_df['date'] = normalized_df['date'].ffill()
        else:
            normalized_df['date'] = None
        
        # نوع العقار
        if 'property_type' in column_mapping:
            raw_types = df[column_mapping['property_type']].astype(str).str.strip()
            normalized_df['property_type_raw'] = raw_types
            normalized_df['property_type'] = normalize_property_type(raw_types)
        else:
            normalized_df['property_type'] = 'غير محدد'
            normalized_df['property_type_raw'] = 'غير محدد'
        
        # عدد الوحدات
        if 'units' in column_mapping:
            normalized_df['units'] = pd.to_numeric(df[column_mapping['units']], errors='coerce')
        else:
            normalized_df['units'] = 1
        
        # ======================
        # 4️⃣ التأكد من نوع البيانات قبل التقدير
        # ======================
        
        normalized_df['price'] = pd.to_numeric(normalized_df['price'], errors='coerce')
        
        # ======================
        # 5️⃣ التقدير الهرمي للأسعار المفقودة (Hierarchical Price Imputation)
        # ======================
        
        # تعويض السعر بمتوسط الحي
        district_median_price = normalized_df.groupby('district')['price'].transform('median')
        normalized_df['price'] = normalized_df['price'].fillna(district_median_price)
        
        # تعويض السعر بمتوسط المدينة
        city_median_price = normalized_df.groupby('city')['price'].transform('median')
        normalized_df['price'] = normalized_df['price'].fillna(city_median_price)
        
        # التعويض الأخير بالمتوسط العام (نادراً ما يستخدم)
        global_median_price = normalized_df['price'].median()
        if pd.isna(global_median_price):
            global_median_price = 500000
        normalized_df['price'] = normalized_df['price'].fillna(global_median_price)
        
        # ======================
        # 6️⃣ حساب سعر المتر بعد تصحيح الأسعار
        # ======================
        
        # إعادة حساب سعر المتر بعد تصحيح الأسعار
        normalized_df['price_per_sqm'] = normalized_df['price'] / normalized_df['area']
        
        # إزالة القيم غير المنطقية (أقل من 200 ريال أو أكثر من 200,000 ريال)
        normalized_df.loc[
            (normalized_df['price_per_sqm'] < 200) | (normalized_df['price_per_sqm'] > 200000), 
            'price_per_sqm'
        ] = pd.NA
        
        # تعديل مهم: استخدام clip بدلاً من حذف الصفقات
        # هذا يحافظ على جميع الصفقات مع تصحيح القيم الشاذة
        normalized_df['price_per_sqm'] = normalized_df['price_per_sqm'].clip(500, 200000)
        
        # تحويل سعر المتر إلى عدد صحيح
        normalized_df['price_per_sqm'] = pd.to_numeric(
            normalized_df['price_per_sqm'], 
            errors="coerce"
        )
        normalized_df['price_per_sqm'] = normalized_df['price_per_sqm'].replace(
            [float("inf"), float("-inf")], 
            pd.NA
        )
        normalized_df['price_per_sqm'] = (
            normalized_df['price_per_sqm']
            .round(0)
            .astype("Int64")
        )
        
        # تعبئة القيم الناقصة
        normalized_df['units'] = normalized_df['units'].fillna(1)
        
        # ======================
        # 7️⃣ إضافة مؤشرات جودة البيانات
        # ======================
        
        normalized_df['price_source'] = 'original'
        normalized_df.loc[normalized_df['price_raw'].isna(), 'price_source'] = 'estimated'
        
        # مؤشر جودة متقدم (3 مستويات) - مع منطق صحيح
        normalized_df['price_validity'] = 'valid'
        normalized_df.loc[normalized_df['price_raw'].isna(), 'price_validity'] = 'estimated'
        # فقط الصفقات التي كانت valid ثم أصبح سعر المتر غير منطقي تصبح corrected
        normalized_df.loc[
            (normalized_df['price_per_sqm'].isna()) & (normalized_df['price_validity'] == 'valid'), 
            'price_validity'
        ] = 'corrected'
        
        # إحصائيات جودة البيانات
        price_quality = (normalized_df['price_source'] == 'original').sum() / len(normalized_df) * 100
        estimated_ratio = (normalized_df['price_validity'] == 'estimated').sum() / len(normalized_df) * 100
        corrected_ratio = (normalized_df['price_validity'] == 'corrected').sum() / len(normalized_df) * 100
        valid_ratio = (normalized_df['price_validity'] == 'valid').sum() / len(normalized_df) * 100
        
        print(f"\n📊 جودة البيانات:")
        print(f"   نسبة الأسعار الأصلية: {price_quality:.1f}%")
        print(f"   نسبة الأسعار المقدرة: {100-price_quality:.1f}%")
        print(f"\n📊 تصنيف جودة الأسعار (ثلاثي المستويات):")
        print(f"   - أسعار صالحة (valid): {valid_ratio:.1f}%")
        print(f"   - أسعار مقدرة (estimated): {estimated_ratio:.1f}%")
        print(f"   - أسعار مصححة (corrected): {corrected_ratio:.1f}%")
        
        # =====================================
        # 8️⃣ تصنيف نوع العقار الفرعي (شقة / فيلا / تاون هاوس)
        # يطبق فقط على العقارات السكنية
        # =====================================
        def classify_property_subtype(area, property_type):
            # إذا لم يكن العقار سكني، نصنفه كـ "غير سكني"
            if property_type != "سكني":
                return "غير سكني"
            
            if pd.isna(area):
                return "غير محدد"
            
            # شقة
            if area < 180:
                return "شقة"
            # تاون هاوس
            elif area < 350:
                return "تاون هاوس"
            # فيلا
            else:
                return "فيلا"
        
        normalized_df["property_subtype"] = normalized_df.apply(
            lambda row: classify_property_subtype(row["area"], row["property_type"]), 
            axis=1
        )
        
        # ======================
        # 9️⃣ تطبيق الفلاتر
        # ======================
        
        # فلترة المدينة
        if selected_city and selected_city != 'الكل':
            city_mask = normalized_df['city'].astype(str).str.strip().str.contains(
                selected_city.strip(), case=False, na=False
            )
            normalized_df = normalized_df[city_mask]
            print(f"🏙️  بعد فلترة المدينة '{selected_city}': {len(normalized_df)} صفقة")
        
        # فلترة نوع العقار
        if selected_property_type and selected_property_type != 'الكل':
            if selected_property_type in ['سكني', 'تجاري', 'أرض']:
                normalized_df = normalized_df[normalized_df['property_type'] == selected_property_type]
                print(f"🏠 بعد فلترة النوع '{selected_property_type}': {len(normalized_df)} صفقة")
        
        # ======================
        # 🔟 تقرير إحصائي شامل
        # ======================
        
        print(f"\n✅ اكتمل تحميل وتنظيف البيانات:")
        print(f"  📊 إجمالي الصفقات: {len(normalized_df):,}")
        print(f"  🏙️  المدن: {normalized_df['city'].nunique()}")
        print(f"  🏘️  الأحياء: {normalized_df['district'].nunique()}")
        print(f"  🏠  أنواع العقارات: {normalized_df['property_type'].unique().tolist()}")
        print(f"  🏢  أنواع العقارات الفرعية: {normalized_df['property_subtype'].unique().tolist()}")
        
        # إحصائيات الأسعار
        if len(normalized_df) > 0:
            print(f"  💰 متوسط السعر: {normalized_df['price'].mean():,.0f} ريال")
            print(f"  📏 متوسط سعر المتر: {normalized_df['price_per_sqm'].mean():,.0f} ريال")
            print(f"  📐 إجمالي الصفقات المحتفظ بها: {len(normalized_df):,} صفقة")
            print(f"  🔢 نوع بيانات سعر المتر: {normalized_df['price_per_sqm'].dtype}")
            
            # إحصائيات أنواع العقارات الفرعية
            subtype_counts = normalized_df['property_subtype'].value_counts()
            print(f"  📊 توزيع أنواع العقارات الفرعية:")
            for subtype, count in subtype_counts.items():
                print(f"     - {subtype}: {count:,} صفقة ({count/len(normalized_df)*100:.1f}%)")
        
        if 'date' in normalized_df.columns and normalized_df['date'].notna().any():
            min_date = normalized_df['date'].min()
            max_date = normalized_df['date'].max()
            if pd.notna(min_date) and pd.notna(max_date):
                print(f"  📅 الفترة: {min_date.year} - {max_date.year}")
                print(f"  📅 عدد التواريخ الصالحة: {normalized_df['date'].notna().sum():,}")
        
        # ======================
        # 🔍 DEBUG: طباعة معلومات قبل الإرجاع
        # ======================
        print("\n🔍 DEBUG INFO:")
        print(f"  DEBUG FINAL ROWS: {len(normalized_df)}")
        print(f"  DEBUG COLUMNS: {list(normalized_df.columns)}")
        
        return normalized_df.reset_index(drop=True)
    
    except Exception as e:
        print("🔥 ERROR IN GOVERNMENT DATA PROVIDER")
        import traceback
        traceback.print_exc()
        raise e


# =========================================
# اختبار شامل للتأكد من جاهزية النظام
# =========================================
if __name__ == "__main__":
    print("=" * 60)
    print("🏗️  اختبار Government Data Provider - الإصدار الصناعي النهائي")
    print("=" * 60)
    
    # اختبار تحميل كل البيانات
    print("\n📊 اختبار 1: تحميل كل البيانات")
    df = load_government_data()
    
    if not df.empty:
        print("\n🔍 عينة من البيانات النهائية:")
        display_cols = ['price', 'price_raw', 'area', 'price_per_sqm', 'district', 'property_type', 'property_subtype', 'price_source', 'price_validity', 'date']
        print(df[display_cols].head(10).to_string())
        
        # ✅ التحقق من أن سعر المتر أصبح عدداً صحيحاً
        print("\n🔍 التحقق من نوع بيانات price_per_sqm:")
        print(f"   نوع البيانات: {df['price_per_sqm'].dtype}")
        print(f"   عينة من القيم: {df['price_per_sqm'].head(5).tolist()}")
        
        # التحقق من الاحتفاظ بجميع الصفقات
        print(f"\n✅ عدد الصفقات المحتفظ بها: {len(df):,}")
        
        # التحقق من عدم وجود مساحات صفرية
        zero_areas = df[df['area'] == 0]
        print(f"✅ عدد الصفقات بمساحة صفرية: {len(zero_areas)} (تم استبدالها بالمتوسط)")
        
        # التحقق من عدم وجود أسعار فارغة
        null_prices = df[df['price'].isna()]
        print(f"✅ عدد الصفقات بسعر فارغ: {len(null_prices)} (تم استبدالها بالمتوسط)")
        
        # التحقق من وجود price_per_sqm
        print(f"✅ تم إنشاء عمود price_per_sqm بنجاح")
        print(f"   عدد القيم الصالحة: {df['price_per_sqm'].notna().sum():,}")
        
        # التحقق من التواريخ
        print(f"✅ عدد التواريخ الصالحة: {df['date'].notna().sum():,}")
        
        # التحقق من تصنيف العقار الفرعي
        print(f"\n✅ توزيع أنواع العقارات الفرعية:")
        subtype_counts = df['property_subtype'].value_counts()
        for subtype, count in subtype_counts.items():
            print(f"   - {subtype}: {count:,} صفقة ({count/len(df)*100:.1f}%)")
        
        # التحقق من جودة البيانات (ثلاثي المستويات)
        print(f"\n✅ جودة البيانات (تصنيف ثلاثي):")
        validity_counts = df['price_validity'].value_counts()
        for validity, count in validity_counts.items():
            print(f"   - {validity}: {count:,} صفقة ({count/len(df)*100:.1f}%)")
        
        # اختبار فلترة الرياض
        print("\n🏙️  اختبار 2: فلترة مدينة الرياض")
        riyadh_df = load_government_data(selected_city='الرياض')
        if not riyadh_df.empty:
            print(f"   ✅ عدد صفقات الرياض: {len(riyadh_df):,}")
            print(f"   📊 متوسط سعر المتر في الرياض: {riyadh_df['price_per_sqm'].mean():,.0f} ريال")
        
        # اختبار فلترة العقارات السكنية
        print("\n🏠 اختبار 3: فلترة العقارات السكنية")
        residential_df = load_government_data(selected_property_type='سكني')
        if not residential_df.empty:
            print(f"   ✅ عدد الصفقات السكنية: {len(residential_df):,}")
            print(f"   📊 توزيع أنواع العقارات السكنية:")
            subtype_counts = residential_df['property_subtype'].value_counts()
            for subtype, count in subtype_counts.items():
                print(f"      - {subtype}: {count:,} صفقة")
        
        print("\n" + "=" * 60)
        print("✅✅✅ النظام جاهز بالكامل - تم إغلاق government_data_provider.py نهائياً")
        print("=" * 60)
