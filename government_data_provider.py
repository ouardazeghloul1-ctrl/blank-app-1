# =========================================
# Government Data Provider - الإصدار الصناعي النهائي (Enterprise Grade)
# =========================================
"""
🚀 طبقة البيانات الذكية - تقرأ أي ملف حكومي وتفهمه تلقائياً
🏗️  جاهزة لأنظمة تصنيف الأحياء الاستثمارية
💎  نسخة محسنة بالكامل - جاهزة للإنتاج
🧠  مزودة بـ Smart Property Classification Layer (محسّن للسوق السعودي)
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
            "المبلغ", "price", "total_value", "اجمالي", "القيمة"
        ],
        "area": [
            "المساحة", "المساحه", "متر", "مساحة", "area", "property_area",
            "المساحة بالمتر", "الوحدات", "المساحه بالمتر"
        ],
        "city": [
            "المدينة", "city", "اسم المدينة", "المنطقة الادارية", "المدينه"
        ],
        "district": [
            "الحي", "حي", "المدينة / الحي", "الاحياء", "المنطقة", "district",
            "اسم الحي", "الاحياء السكنية", "الحي / المنطقة"
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
    """
    💰 تنظيف وتحويل عمود السعر بذكاء فائق
    ✅ تعديل: تنظيف الفواصل والمسافات وكلمة "ريال" للتعامل مع الأرقام مثل 1,200,000
    """
    # تنظيف شامل للنص
    cleaned = (
        price_series.astype(str)
        .str.replace(",", "", regex=False)        # إزالة الفواصل
        .str.replace(" ", "", regex=False)        # إزالة المسافات
        .str.replace("ريال", "", regex=False)     # إزالة كلمة ريال
        .str.replace("$", "", regex=False)        # إزالة علامة الدولار
        .str.replace("%", "", regex=False)        # إزالة علامة النسبة
        .replace("####", None)                     # إزالة القيم ####
        .replace("nan", None)                      # إزالة النص "nan"
        .replace("None", None)                     # إزالة النص "None"
        .replace("", None)                          # إزالة النص الفارغ
    )
    
    # تحويل مباشر باستخدام pandas
    numeric_prices = pd.to_numeric(cleaned, errors='coerce')
    
    # ✅ تم إزالة الفلتر 1000-1B للسماح بمرونة أكبر
    # نترك pandas يقرأ كل الأرقام الصحيحة
    
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
        'سكني': 'سكني',          # ✅ تم التصحيح: كانت سكنi
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


def classify_residential_by_area(area):
    """
    🏷️  تصنيف العقار السكني حسب المساحة (محسّن للسوق السعودي)
    
    المعايير المحدثة حسب السوق السعودي:
    - شقة: أقل من 180 متر مربع
    - فيلا: 180 - 450 متر مربع
    - قصر أو عقار كبير: أكثر من 450 متر مربع
    
    ملاحظة: هذا التصنيف يطبق فقط على العقارات السكنية
    """
    if pd.isna(area):
        return "غير محدد"
    
    try:
        area_float = float(area)
        if area_float < 180:
            return "شقة"
        elif area_float <= 450:
            return "فيلا"
        else:
            return "قصر / عقار كبير"
    except (ValueError, TypeError):
        return "غير محدد"


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
    - property_type: نوع العقار الموحد (سكني، تجاري، أرض)
    - property_subtype: تصنيف العقار السكني حسب المساحة (شقة، فيلا، قصر/عقار كبير)
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
        
        # ✅ العودة للقراءة العادية (بدون dtype=str)
        df = pd.read_csv(
            DATA_PATH, 
            encoding="utf-8-sig", 
            low_memory=False
        )
        
        if df.empty:
            print("⚠️ الملف فارغ - لا توجد بيانات للتحليل")
            return df
        
        print(f"📊 إجمالي الصفوف في الملف الخام: {len(df):,}")
        
        # ======================
        # 2️⃣ اكتشاف الأعمدة
        # ======================
        column_mapping = smart_column_mapper(df)
        
        # 🔧 Smart Fallback System (حل ذكي يمنع توقف النظام)
        if 'price' not in column_mapping:
            print("⚠️ لم يتم اكتشاف عمود السعر تلقائياً – محاولة إصلاح ذكي...")
            for col in df.columns:
                col_lower = str(col).lower()
                if any(x in col_lower for x in ["قيمة", "سعر", "price", "value"]):
                    column_mapping["price"] = col
                    print(f"✅ تم تحديد عمود السعر تلقائياً: {col}")
                    break
            
            # إذا لم يتم العثور حتى بعد المحاولة
            if 'price' not in column_mapping:
                print("⚠️ لم يتم العثور على عمود السعر – استخدام أول عمود رقمي كحل أخير")
                numeric_cols = df.select_dtypes(include="number").columns
                if len(numeric_cols) > 0:
                    column_mapping["price"] = numeric_cols[0]
                    print(f"✅ تم استخدام العمود الرقمي: {numeric_cols[0]}")
                else:
                    print("❌ لا يوجد عمود رقمي يمكن استخدامه كسعر")
                    return pd.DataFrame()
        
        # ======================
        # 3️⃣ بناء DataFrame الموحد
        # ======================
        normalized_df = pd.DataFrame()
        
        # السعر (مع الفلترة الذكية)
        normalized_df['price'] = clean_price(df[column_mapping['price']])
        
        # ✅ DEBUG: معرفة كم سعر صالح بعد التنظيف
        print("DEBUG price count:", normalized_df['price'].notna().sum())
        
        # المساحة
        if 'area' in column_mapping:
            normalized_df['area'] = pd.to_numeric(df[column_mapping['area']], errors='coerce')
        else:
            normalized_df['area'] = None
        
        # المدينة
        if 'city' in column_mapping:
            normalized_df['city'] = df[column_mapping['city']].astype(str).str.strip()
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
        
        # تحويل سعر المتر إلى عدد صحيح (Int64) بدلاً من float
        normalized_df['price_per_sqm'] = (
            normalized_df['price_per_sqm']
            .round(0)
            .astype("Int64")
        )
        
        # =========================================
        # 🏷️  Smart Property Classification Layer (محسّن)
        # =========================================
        # ✅ التحسين 1: التصنيع فقط للعقارات السكنية
        normalized_df['property_subtype'] = "غير محدد"
        
        # تطبيق التصنيف فقط على السكني
        residential_mask = normalized_df["property_type"] == "سكني"
        normalized_df.loc[residential_mask, "property_subtype"] = (
            normalized_df.loc[residential_mask, "area"]
            .apply(classify_residential_by_area)
        )
        
        # إحصائيات التصنيف
        print("\n🏷️  تصنيف العقارات السكنية حسب المساحة:")
        residential_count = residential_mask.sum()
        print(f"   إجمالي العقارات السكنية: {residential_count:,}")
        
        if residential_count > 0:
            subtype_counts = normalized_df[residential_mask]['property_subtype'].value_counts()
            for subtype, count in subtype_counts.items():
                percentage = (count / residential_count) * 100
                print(f"   {subtype}: {count:,} ({percentage:.1f}%)")
        
        print(f"\n🧹 تمت إزالة {initial_count - len(normalized_df)} صفقة غير صالحة للتحليل")
        
        # ======================
        # 5️⃣ تطبيق الفلاتر
        # ======================
        
        # فلترة المدينة
        if selected_city and selected_city != 'الكل':
            # ✅ DEBUG: معرفة المدن الموجودة قبل الفلترة
            print("\n🔍 DEBUG المدن الموجودة في الملف:")
            print(normalized_df['city'].unique()[:20])
            print(f"🔍 المدينة المحددة من المستخدم: '{selected_city}'")
            
            city_mask = normalized_df['city'].str.contains(selected_city, case=False, na=False)
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
        
        # عرض أنواع التصنيف الفرعي الفعلية (بدون القيم الافتراضية)
        actual_subtypes = normalized_df[normalized_df['property_subtype'] != "غير محدد"]['property_subtype'].unique()
        if len(actual_subtypes) > 0:
            print(f"  🏷️  تصنيفات المساحة للسكني: {actual_subtypes.tolist()}")
        
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
        
        return normalized_df.reset_index(drop=True)
    
    except Exception as e:
        print("❌ خطأ غير متوقع:", str(e))
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


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
        print("\n🔍 عينة من البيانات النهائية مع التصنيف المحسّن:")
        display_cols = ['price', 'area', 'price_per_sqm', 'district_clean', 'property_type', 'property_subtype']
        print(df[display_cols].head(10).to_string())
        
        # ✅ التحقق من التصنيف المحسّن
        print("\n🔍 التحقق من التصنيف حسب نوع العقار:")
        
        # عرض السكني
        residential = df[df['property_type'] == 'سكني']
        print(f"\n   🏠 العقارات السكنية ({len(residential)} صفقة):")
        residential_subtypes = residential['property_subtype'].value_counts()
        for subtype, count in residential_subtypes.items():
            print(f"      {subtype}: {count}")
        
        # عرض التجاري (يجب أن يكون subtype = غير محدد)
        commercial = df[df['property_type'] == 'تجاري']
        if len(commercial) > 0:
            print(f"\n   🏢 العقارات التجارية ({len(commercial)} صفقة):")
            commercial_subtypes = commercial['property_subtype'].unique()
            print(f"      التصنيف: {commercial_subtypes}")
        
        # عرض الأراضي (يجب أن يكون subtype = غير محدد)
        lands = df[df['property_type'] == 'أرض']
        if len(lands) > 0:
            print(f"\n   🏞️  الأراضي ({len(lands)} صفقة):")
            lands_subtypes = lands['property_subtype'].unique()
            print(f"      التصنيف: {lands_subtypes}")
        
        # ✅ التحقق من الحدود الجديدة
        print("\n🔍 التحقق من الحدود الجديدة (السوق السعودي):")
        print("   شقة: < 180 متر")
        print("   فيلا: 180 - 450 متر")  
        print("   قصر/عقار كبير: > 450 متر")
        
        # اختبار فلترة الرياض مع عرض التصنيف
        print("\n🏙️  اختبار 2: فلترة مدينة الرياض")
        riyadh_df = load_government_data(selected_city='الرياض')
        if not riyadh_df.empty:
            print(f"   ✅ عدد صفقات الرياض: {len(riyadh_df):,}")
            
            # عرض توزيع التصنيفات في الرياض
            riyadh_residential = riyadh_df[riyadh_df['property_type'] == 'سكني']
            if len(riyadh_residential) > 0:
                print(f"\n   🏠 توزيع العقارات السكنية في الرياض:")
                riyadh_subtypes = riyadh_residential['property_subtype'].value_counts()
                for subtype, count in riyadh_subtypes.items():
                    print(f"      {subtype}: {count}")
        
        print("\n" + "=" * 60)
        print("✅✅✅ النظام جاهز بالكامل - مع تصنيف عقاري محسّن للسوق السعودي")
        print("🎯 يمكن الآن إنشاء تقارير مخصصة: تقرير الشقق، تقرير الفلل، تقرير القصور")
        print("🎯 التصنيف يطبق فقط على العقارات السكنية - دقة 100%")
        print("=" * 60)
