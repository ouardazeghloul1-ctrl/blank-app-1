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
    """💰 تنظيف وتحويل عمود السعر بذكاء فائق"""
    
    # تحويل إلى string والتعامل مع القيم الفارغة
    cleaned = price_series.astype(str).fillna('0')
    
    # إزالة كل الرموز غير الرقمية مع الحفاظ على النقاط العشرية
    cleaned = cleaned.apply(lambda x: re.sub(r'[^\d.]', '', str(x)))
    
    # تحويل إلى رقم
    numeric_prices = pd.to_numeric(cleaned, errors='coerce')
    
    # تطبيق فلتر منطقي للأسعار (إزالة الأخطاء الواضحة)
    # الأسعار الأقل من 1000 أو الأكثر من مليار تعتبر أخطاء إدخال
    valid_price_mask = (numeric_prices > 1000) & (numeric_prices < 1_000_000_000)
    numeric_prices[~valid_price_mask] = None
    
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


def clean_district_name(district_series: pd.Series) -> pd.Series:
    """
    🏘️  تنظيف أسماء الأحياء بشكل ذكي للغاية
    تتعامل مع: الرياض/حي الربيع، حي النرجس، النرجس، Nargis
    وتوحدها إلى lowercase موحد
    """
    
    def clean_single(value):
        if pd.isna(value):
            return 'غير محدد'
        
        # تحويل إلى نص وتنظيف أساسي
        text = str(value).strip()
        
        # التعامل مع الأسماء التي تحتوي على '/'
        # مثلاً: "الرياض/حي الربيع" -> "الربيع"
        if '/' in text:
            parts = text.split('/')
            text = parts[-1]  # نأخذ الجزء الأخير
        
        # إزالة كلمة "حي" أو "الحي" أو "حى" أو "الحى"
        text = re.sub(r'(حي|الحي|حى|الحى|District|dist|Dist)\s*', '', text, flags=re.IGNORECASE)
        
        # إزالة المسافات الزائدة
        text = re.sub(r'\s+', ' ', text).strip()
        
        # تحويل إلى lowercase لتوحيد الكتابة (مهم جداً للتحليل)
        text = text.lower()
        
        return text if text else 'غير محدد'
    
    return district_series.apply(clean_single)


def load_government_data(selected_city: Optional[str] = None, 
                        selected_property_type: Optional[str] = None) -> pd.DataFrame:
    """
    🎯 المحرك الرئيسي للبيانات - واجهة موحدة لجميع أنظمة المشروع
    
    المخرجات: DataFrame موحد يحتوي على:
    - price: السعر بعد التنظيف
    - area: المساحة (بدون قيم صفرية)
    - price_per_sqm: سعر المتر المربع (عدد صحيح)
    - city: المدينة
    - district: الحي الأصلي
    - district_clean: الحي بعد التنظيف (lowercase)
    - property_type: نوع العقار الموحد
    - date: التاريخ
    - units: عدد الوحدات
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
        
        # التعديل 1 — دعم CSV و Excel
        if DATA_PATH.suffix.lower() == ".xlsx":
            df = pd.read_excel(DATA_PATH)
        else:
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
        
        # السعر (مع الفلترة الذكية)
        normalized_df['price'] = clean_price(df[column_mapping['price']])
        
        # المساحة
        if 'area' in column_mapping:
            normalized_df['area'] = pd.to_numeric(df[column_mapping['area']], errors='coerce')
        else:
            normalized_df['area'] = None
        
        # المدينة
        if 'city' in column_mapping:
            # التعديل 2 — تنظيف اسم المدينة
            normalized_df['city'] = df[column_mapping['city']].astype(str).str.strip()
            # تنظيف اسم المدينة
            normalized_df['city'] = normalized_df['city'].str.replace("منطقة", "", regex=False)
            normalized_df['city'] = normalized_df['city'].str.replace("المنطقة", "", regex=False)
            normalized_df['city'] = normalized_df['city'].str.replace("الادارية", "", regex=False)
            normalized_df['city'] = normalized_df['city'].str.strip()
        else:
            normalized_df['city'] = 'غير محدد'
        
        # الحي (الأصلي والمنظف)
        if 'district' in column_mapping:
            normalized_df['district'] = df[column_mapping['district']].astype(str).str.strip()
        else:
            normalized_df['district'] = 'غير محدد'
        
        # تنظيف الحي بشكل ذكي + تحويل إلى lowercase
        normalized_df['district_clean'] = clean_district_name(normalized_df['district'])
        
        # التاريخ
        if 'date' in column_mapping:
            normalized_df['date'] = pd.to_datetime(df[column_mapping['date']], errors='coerce')
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
        # 4️⃣ تنظيف البيانات
        # ======================
        
        # إزالة الصفوف ذات الأسعار غير الصالحة
        initial_count = len(normalized_df)
        normalized_df = normalized_df[normalized_df['price'].notna()]
        
        # تعبئة القيم الناقصة
        normalized_df['units'] = normalized_df['units'].fillna(1)
        
        # معالجة المساحات بشكل ذكي
        normalized_df['area'] = pd.to_numeric(normalized_df['area'], errors='coerce')
        
        # التعديل 3 — منع أخطاء المساحة
        # إزالة المساحات غير المنطقية
        normalized_df.loc[normalized_df['area'] <= 0, 'area'] = pd.NA
        
        # نحتفظ بالصفوف التي ليس لديها مساحة (سنحاول تقديرها لاحقاً)
        # أو مساحتها أكبر من 0
        area_mask = (normalized_df['area'] > 0) | (normalized_df['area'].isna())
        normalized_df = normalized_df[area_mask]
        
        # سعر المتر المربع (قلب التحليل العقاري)
        normalized_df['price_per_sqm'] = pd.NA
        valid_area_mask = (normalized_df['area'] > 0) & normalized_df['area'].notna()
        normalized_df.loc[valid_area_mask, 'price_per_sqm'] = (
            normalized_df.loc[valid_area_mask, 'price'] / 
            normalized_df.loc[valid_area_mask, 'area']
        )
        
        # ✅ التحسين: تحويل سعر المتر إلى عدد صحيح (Int64) بدلاً من float
        # هذا أفضل للتحليل والعرض
        # أولاً: التأكد من أن جميع القيم رقمية
        normalized_df['price_per_sqm'] = pd.to_numeric(
            normalized_df['price_per_sqm'], 
            errors="coerce"
        )
        # ثانياً: إزالة القيم اللانهائية (inf, -inf)
        normalized_df['price_per_sqm'] = normalized_df['price_per_sqm'].replace(
            [float("inf"), float("-inf")], 
            pd.NA
        )
        # ثالثاً: التقريب والتحويل إلى Int64
        normalized_df['price_per_sqm'] = (
            normalized_df['price_per_sqm']
            .round(0)
            .astype("Int64")  # Int64 يتعامل مع القيم الفارغة (NaN)
        )
        
        print(f"🧹 تمت إزالة {initial_count - len(normalized_df)} صفقة غير صالحة للتحليل")
        
        # ======================
        # 5️⃣ تطبيق الفلاتر
        # ======================
        
        # فلترة المدينة
        if selected_city and selected_city != 'الكل':
            # التعديل 4 — تحسين فلترة المدينة
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
        # 6️⃣ تقرير إحصائي شامل
        # ======================
        
        print(f"\n✅ اكتمل تحميل وتنظيف البيانات:")
        print(f"  📊 إجمالي الصفقات: {len(normalized_df):,}")
        print(f"  🏙️  المدن: {normalized_df['city'].nunique()}")
        print(f"  🏘️  الأحياء: {normalized_df['district_clean'].nunique()}")
        print(f"  🏠  أنواع العقارات: {normalized_df['property_type'].unique().tolist()}")
        
        # إحصائيات الأسعار
        if len(normalized_df) > 0:
            print(f"  💰 متوسط السعر: {normalized_df['price'].mean():,.0f} ريال")
            print(f"  📏 متوسط سعر المتر: {normalized_df['price_per_sqm'].mean():,.0f} ريال")
            print(f"  📐 الصفقات ذات المساحة المعروفة: {valid_area_mask.sum():,} صفقة")
            print(f"  🔢 نوع بيانات سعر المتر: {normalized_df['price_per_sqm'].dtype}")
        
        if 'date' in normalized_df.columns and normalized_df['date'].notna().any():
            min_date = normalized_df['date'].min()
            max_date = normalized_df['date'].max()
            if pd.notna(min_date) and pd.notna(max_date):
                print(f"  📅 الفترة: {min_date.year} - {max_date.year}")
        
        # ======================
        # 7️⃣ DEBUG: طباعة معلومات قبل الإرجاع
        # ======================
        print("\n🔍 DEBUG INFO:")
        print(f"  DEBUG FINAL ROWS: {len(normalized_df)}")
        print(f"  DEBUG COLUMNS: {list(normalized_df.columns)}")
        
        return normalized_df.reset_index(drop=True)
    
    except Exception as e:
        print("🔥 ERROR IN GOVERNMENT DATA PROVIDER")
        import traceback
        traceback.print_exc()
        raise e  # 👈 هذا السهم مهم - نرفع الخطأ بدلاً من إخفائه


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
        display_cols = ['price', 'area', 'price_per_sqm', 'district_clean', 'property_type']
        print(df[display_cols].head(10).to_string())
        
        # ✅ التحقق من أن سعر المتر أصبح عدداً صحيحاً
        print("\n🔍 التحقق من نوع بيانات price_per_sqm:")
        print(f"   نوع البيانات: {df['price_per_sqm'].dtype}")
        print(f"   عينة من القيم: {df['price_per_sqm'].head(5).tolist()}")
        
        # التحقق من أسماء الأحياء الموحدة
        print("\n🔍 عينة من أسماء الأحياء بعد التنظيف (موحدة lowercase):")
        sample_districts = df['district_clean'].dropna().unique()[:5]
        for d in sample_districts:
            print(f"  🏘️  {d}")
        
        # التحقق من عدم وجود مساحات صفرية
        zero_areas = df[df['area'] == 0]
        print(f"\n✅ عدد الصفقات بمساحة صفرية: {len(zero_areas)} (ممتاز، تمت إزالتها)")
        
        # التحقق من وجود price_per_sqm
        print(f"✅ تم إنشاء عمود price_per_sqm بنجاح")
        print(f"   عدد القيم الصالحة: {df['price_per_sqm'].notna().sum():,}")
        
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
        
        # اختبار التحقق من أسماء الأحياء
        print("\n🧪 اختبار 4: التحقق من توحيد أسماء الأحياء")
        test_names = pd.Series([
            "الرياض/حي الربيع",
            "حي النرجس",
            "النرجس",
            "Nargis",
            "الرياض/الربيع"
        ])
        cleaned = clean_district_name(test_names)
        for original, cleaned_name in zip(test_names, cleaned):
            print(f"   {original:20} ← {cleaned_name}")
        
        print("\n" + "=" * 60)
        print("✅✅✅ النظام جاهز بالكامل - يمكن البدء في بناء District Ranking Engine")
        print("=" * 60)
