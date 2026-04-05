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
            
            # فلترة المساحات غير المنطقية (20 - 5000 متر)
            normalized_df.loc[normalized_df['area'] <= 20, 'area'] = pd.NA
            normalized_df.loc[normalized_df['area'] > 5000, 'area'] = pd.NA
            
            # حساب متوسط المساحة من القيم المنطقية فقط
            median_area = normalized_df.loc[
                (normalized_df['area'] > 20) & (normalized_df['area'] < 5000), 
                'area'
            ].median()
            
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
        
        # إزالة الصفقات غير المنطقية قبل التحليل
        normalized_df = normalized_df[
            (normalized_df["price"] > 10000) & 
            (normalized_df["price"] < 200000000)
        ]
        normalized_df = normalized_df[
            (normalized_df["area"] > 20) & 
            (normalized_df["area"] < 5000)
        ]
        
        # ======================
        # 6️⃣ حساب سعر المتر بعد تصحيح الأسعار
        # ======================
        
        # ✅ التحسين الثالث (احترافي): حماية من القسمة على صفر
        normalized_df["price_per_sqm"] = normalized_df["price"] / normalized_df["area"].replace(0, pd.NA)
        
        # إزالة القيم غير المنطقية (بدون استخدام clip الذي يخفي الأخطاء)
        normalized_df.loc[
            (normalized_df["price_per_sqm"] < 500) | 
            (normalized_df["price_per_sqm"] > 20000), 
            "price_per_sqm"
        ] = pd.NA
        
        # ✅ التحسين الأول: تبسيط تحويل سعر المتر إلى عدد صحيح (بدون تحويل إلى Int64)
        normalized_df['price_per_sqm'] = normalized_df['price_per_sqm'].round(0)
        
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
            
            # تصحيح تصنيف العقار السكني
            # شقة
            if area < 200:
                return "شقة"
            # تاون هاوس
            elif 200 <= area < 300:
                return "تاون هاوس"
            # فيلا
            elif area >= 300:
                return "فيلا"
            
            return "غير محدد"
        
        # ✅ التحسين الثاني (أداء): سيتم تحسينه لاحقاً إلى vectorized logic للصفوف الكبيرة
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
            
            # إحصائيات سعر المتر التفصيلية
            print(f"\n📊 إحصائيات سعر المتر (price_per_sqm):")
            price_stats = normalized_df['price_per_sqm'].describe()
            print(f"   min:  {price_stats['min']:.0f}")
            print(f"   25%:  {price_stats['25%']:.0f}")
            print(f"   50%:  {price_stats['50%']:.0f}")
            print(f"   75%:  {price_stats['75%']:.0f}")
            print(f"   max:  {price_stats['max']:.0f}")
            
            # إحصائيات أنواع العقارات الفرعية
            subtype_counts = normalized_df['property_subtype'].value_counts()
            print(f"\n  📊 توزيع أنواع العقارات الفرعية:")
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
# ✅ الدالة لقراءة ملف المشاريع (مع توحيد اسم العمود)
# =========================================

def load_projects_data():
    """
    📁 قراءة ملف المشاريع (projects.xlsx)
    
    المخرجات: DataFrame يحتوي على:
    - المدينة
    - النوع
    - الحالة
    - خط_العرض
    - خط_الطول
    - نطاق_التأثير (تم توحيد الاسم)
    """
    import pandas as pd
    
    try:
        projects = pd.read_excel("projects.xlsx")
        
        # تنظيف أسماء الأعمدة من الفراغات
        projects.columns = projects.columns.str.strip()
        
        # ✅ توحيد اسم عمود نطاق التأثير
        if "نطاق التأثير (كم)" in projects.columns:
            projects = projects.rename(columns={"نطاق التأثير (كم)": "نطاق_التأثير"})
        elif "نطاق التأثير" in projects.columns:
            projects = projects.rename(columns={"نطاق التأثير": "نطاق_التأثير"})
        
        print(f"✅ تم قراءة ملف المشاريع بنجاح")
        print(f"📊 عدد المشاريع: {len(projects)}")
        print(f"📋 الأعمدة: {list(projects.columns)}")
        
        return projects
    
    except FileNotFoundError:
        print("❌ خطأ: ملف projects.xlsx غير موجود")
        print("📌 يرجى التأكد من وجود الملف في نفس المجلد")
        return None
    except Exception as e:
        print("❌ خطأ في قراءة ملف المشاريع:", e)
        return None


# =========================================
# ✅ الدالة لقراءة ملف الأحياء (مع توحيد اسم العمود)
# =========================================

def load_districts_data():
    """
    📁 قراءة ملف الأحياء (districts.xlsx)
    
    المخرجات: DataFrame يحتوي على:
    - المدينة
    - الحي
    - خط_العرض
    - خط_الطول
    - نطاق_التأثير (تم توحيد الاسم)
    """
    import pandas as pd
    
    try:
        districts = pd.read_excel("districts.xlsx")
        
        # تنظيف أسماء الأعمدة من الفراغات
        districts.columns = districts.columns.str.strip()
        
        # ✅ توحيد اسم عمود نطاق التأثير
        if "نطاق التأثير (كم)" in districts.columns:
            districts = districts.rename(columns={"نطاق التأثير (كم)": "نطاق_التأثير"})
        elif "نطاق التأثير" in districts.columns:
            districts = districts.rename(columns={"نطاق التأثير": "نطاق_التأثير"})
        
        print(f"✅ تم قراءة ملف الأحياء بنجاح")
        print(f"📊 عدد الأحياء: {len(districts)}")
        print(f"📋 الأعمدة: {list(districts.columns)}")
        
        return districts
    
    except FileNotFoundError:
        print("❌ خطأ: ملف districts.xlsx غير موجود")
        print("📌 يرجى التأكد من وجود الملف في نفس المجلد")
        return None
    except Exception as e:
        print("❌ خطأ في قراءة ملف الأحياء:", e)
        return None


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
        display_cols = ['price', 'price_raw', 'area', 'price_per_sqm', 'district', 'property_type', 'property_subtype']
        available_cols = [col for col in display_cols if col in df.columns]
        print(df[available_cols].head(10))
    
    # اختبار 2: قراءة ملف المشاريع
    print("\n" + "=" * 60)
    print("📁 اختبار 2: قراءة ملف المشاريع")
    print("=" * 60)
    
    projects_df = load_projects_data()
    
    if projects_df is not None and not projects_df.empty:
        print("\n🔍 أول 5 صفوف من ملف المشاريع:")
        print(projects_df.head())
        
        print("\n📊 إحصائيات سريعة:")
        print(f"   عدد المشاريع: {len(projects_df)}")
        print(f"   المدن: {projects_df['المدينة'].unique().tolist() if 'المدينة' in projects_df.columns else 'غير موجود'}")
        print(f"   أنواع المشاريع: {projects_df['النوع'].unique().tolist() if 'النوع' in projects_df.columns else 'غير موجود'}")
    
    # اختبار 3: قراءة ملف الأحياء
    print("\n" + "=" * 60)
    print("🏘️  اختبار 3: قراءة ملف الأحياء")
    print("=" * 60)
    
    districts_df = load_districts_data()
    
    if districts_df is not None and not districts_df.empty:
        print("\n🔍 أول 5 صفوف من ملف الأحياء:")
        print(districts_df.head())
        
        print("\n📊 إحصائيات سريعة:")
        print(f"   عدد الأحياء: {len(districts_df)}")
        print(f"   المدن: {districts_df['المدينة'].unique().tolist() if 'المدينة' in districts_df.columns else 'غير موجود'}")
        print(f"   الأعمدة المتاحة: {list(districts_df.columns)}")
