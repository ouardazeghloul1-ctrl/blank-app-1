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
    
    cleaned = price_series.fillna('').astype(str)
    cleaned = cleaned.str.replace(r'[^\d.]', '', regex=True)
    numeric_prices = pd.to_numeric(cleaned, errors='coerce')
    valid_price_mask = (numeric_prices > 1000) & (numeric_prices < 1_000_000_000)
    numeric_prices[~valid_price_mask] = pd.NA
    
    return numeric_prices


def normalize_property_type(type_series: pd.Series) -> pd.Series:
    """🏠 توحيد تصنيفات العقارات لأنظمة التحليل الذكية"""
    
    type_map = {
        'شقة': 'سكني', 'فيلا': 'سكني', 'بيت': 'سكني', 'دور': 'سكني',
        'شاليه': 'سكني', 'سكني': 'سكني', 'سكن': 'سكني', 'منزل': 'سكني',
        'دوبلكس': 'سكني', 'تاون هاوس': 'سكني',
        'محل': 'تجاري', 'معرض': 'تجاري', 'مكتب': 'تجاري', 'عيادة': 'تجاري',
        'تجاري': 'تجاري', 'مركز': 'تجاري', 'مخزن': 'تجاري', 'مستودع': 'تجاري',
        'ارض': 'أرض', 'أرض': 'أرض', 'قطعة': 'أرض', 'ارض خام': 'أرض',
        'اراضي': 'أرض', 'قطعة ارض': 'أرض'
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
    """🎯 المحرك الرئيسي للبيانات - واجهة موحدة لجميع أنظمة المشروع"""
    
    try:
        if not DATA_PATH.exists():
            print(f"❌ ملف البيانات غير موجود في المسار: {DATA_PATH}")
            return pd.DataFrame()
        
        print(f"📂 جاري قراءة الملف: {DATA_PATH}")
        
        if DATA_PATH.suffix.lower() == ".xlsx":
            df = pd.read_excel(DATA_PATH)
        else:
            df = pd.read_csv(DATA_PATH, encoding="utf-8-sig", sep=";", low_memory=False)
        
        if df.empty:
            print("⚠️ الملف فارغ - لا توجد بيانات للتحليل")
            return df
        
        print(f"📊 إجمالي الصفوف في الملف الخام: {len(df):,}")
        
        column_mapping = smart_column_mapper(df)
        
        if 'price' not in column_mapping:
            print("❌ لا يمكن الاستمرار: لم يتم العثور على عمود السعر")
            return pd.DataFrame()
        
        normalized_df = pd.DataFrame()
        
        normalized_df['price_raw'] = clean_price(df[column_mapping['price']])
        normalized_df['price'] = normalized_df['price_raw'].copy()
        
        if 'area' in column_mapping:
            normalized_df['area'] = pd.to_numeric(df[column_mapping['area']], errors='coerce')
            normalized_df.loc[normalized_df['area'] <= 20, 'area'] = pd.NA
            normalized_df.loc[normalized_df['area'] > 5000, 'area'] = pd.NA
            median_area = normalized_df.loc[(normalized_df['area'] > 20) & (normalized_df['area'] < 5000), 'area'].median()
            if pd.isna(median_area):
                median_area = 120
            normalized_df['area'] = normalized_df['area'].fillna(median_area)
        else:
            normalized_df['area'] = 120
        
        if 'city' in column_mapping:
            normalized_df['city'] = df[column_mapping['city']].astype(str).str.strip()
            normalized_df['city'] = normalized_df['city'].str.replace("منطقة", "", regex=False)
            normalized_df['city'] = normalized_df['city'].str.replace("المنطقة", "", regex=False)
            normalized_df['city'] = normalized_df['city'].str.replace("الادارية", "", regex=False)
            normalized_df['city'] = normalized_df['city'].str.strip()
        else:
            normalized_df['city'] = 'غير محدد'
        
        if 'district' in column_mapping:
            normalized_df['district'] = (
                df[column_mapping['district']]
                .astype(str)
                .str.replace(r"\s+", " ", regex=True)
                .str.split("/")
                .str[-1]
                .str.strip()
            )
        else:
            normalized_df['district'] = 'غير محدد'
        
        if 'date' in column_mapping:
            normalized_df['date'] = pd.to_datetime(df[column_mapping['date']], errors='coerce')
            normalized_df['date'] = normalized_df['date'].ffill()
        else:
            normalized_df['date'] = None
        
        if 'property_type' in column_mapping:
            raw_types = df[column_mapping['property_type']].astype(str).str.strip()
            normalized_df['property_type_raw'] = raw_types
            normalized_df['property_type'] = normalize_property_type(raw_types)
        else:
            normalized_df['property_type'] = 'غير محدد'
            normalized_df['property_type_raw'] = 'غير محدد'
        
        if 'units' in column_mapping:
            normalized_df['units'] = pd.to_numeric(df[column_mapping['units']], errors='coerce')
        else:
            normalized_df['units'] = 1
        
        normalized_df['price'] = pd.to_numeric(normalized_df['price'], errors='coerce')
        
        district_median_price = normalized_df.groupby('district')['price'].transform('median')
        normalized_df['price'] = normalized_df['price'].fillna(district_median_price)
        
        city_median_price = normalized_df.groupby('city')['price'].transform('median')
        normalized_df['price'] = normalized_df['price'].fillna(city_median_price)
        
        global_median_price = normalized_df['price'].median()
        if pd.isna(global_median_price):
            global_median_price = 500000
        normalized_df['price'] = normalized_df['price'].fillna(global_median_price)
        
        normalized_df = normalized_df[(normalized_df["price"] > 10000) & (normalized_df["price"] < 200000000)]
        normalized_df = normalized_df[(normalized_df["area"] > 20) & (normalized_df["area"] < 5000)]
        
        normalized_df["price_per_sqm"] = normalized_df["price"] / normalized_df["area"].replace(0, pd.NA)
        normalized_df.loc[(normalized_df["price_per_sqm"] < 500) | (normalized_df["price_per_sqm"] > 20000), "price_per_sqm"] = pd.NA
        normalized_df['price_per_sqm'] = normalized_df['price_per_sqm'].round(0)
        normalized_df['units'] = normalized_df['units'].fillna(1)
        
        normalized_df['price_source'] = 'original'
        normalized_df.loc[normalized_df['price_raw'].isna(), 'price_source'] = 'estimated'
        
        normalized_df['price_validity'] = 'valid'
        normalized_df.loc[normalized_df['price_raw'].isna(), 'price_validity'] = 'estimated'
        normalized_df.loc[(normalized_df['price_per_sqm'].isna()) & (normalized_df['price_validity'] == 'valid'), 'price_validity'] = 'corrected'
        
        def classify_property_subtype(area, property_type):
            if property_type != "سكني":
                return "غير سكني"
            if pd.isna(area):
                return "غير محدد"
            if area < 200:
                return "شقة"
            elif 200 <= area < 300:
                return "تاون هاوس"
            elif area >= 300:
                return "فيلا"
            return "غير محدد"
        
        normalized_df["property_subtype"] = normalized_df.apply(lambda row: classify_property_subtype(row["area"], row["property_type"]), axis=1)
        
        if selected_city and selected_city != 'الكل':
            city_mask = normalized_df['city'].astype(str).str.strip().str.contains(selected_city.strip(), case=False, na=False)
            normalized_df = normalized_df[city_mask]
        
        if selected_property_type and selected_property_type != 'الكل':
            if selected_property_type in ['سكني', 'تجاري', 'أرض']:
                normalized_df = normalized_df[normalized_df['property_type'] == selected_property_type]
        
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
    """📁 قراءة ملف المشاريع (projects.xlsx)"""
    import pandas as pd
    
    try:
        projects = pd.read_excel("projects.xlsx")
        projects.columns = projects.columns.str.strip()
        
        # توحيد أسماء الأعمدة للمشاريع
        if "خط العرض" in projects.columns:
            projects = projects.rename(columns={"خط العرض": "خط_العرض"})
        if "خط الطول" in projects.columns:
            projects = projects.rename(columns={"خط الطول": "خط_الطول"})
        if "نطاق_التأثير_كم" in projects.columns:
            projects = projects.rename(columns={"نطاق_التأثير_كم": "نطاق_التأثير"})
        if "نطاق التأثير (كم)" in projects.columns:
            projects = projects.rename(columns={"نطاق التأثير (كم)": "نطاق_التأثير"})
        elif "نطاق التأثير" in projects.columns:
            projects = projects.rename(columns={"نطاق التأثير": "نطاق_التأثير"})
        
        print(f"✅ تم قراءة ملف المشاريع بنجاح")
        print(f"📊 عدد المشاريع: {len(projects)}")
        print(f"📋 أعمدة المشاريع: {list(projects.columns)}")
        
        return projects
    
    except FileNotFoundError:
        print("❌ خطأ: ملف projects.xlsx غير موجود")
        return None
    except Exception as e:
        print("❌ خطأ في قراءة ملف المشاريع:", e)
        return None


# =========================================
# ✅ الدالة لقراءة ملف الأحياء (مع توحيد اسم العمود)
# =========================================

def load_districts_data():
    """📁 قراءة ملف الأحياء (districts.xlsx)"""
    import pandas as pd
    
    try:
        districts = pd.read_excel("districts.xlsx")
        
        # تنظيف أسماء الأعمدة من الفراغات
        districts.columns = districts.columns.str.strip()
        
        # DEBUG: طباعة أسماء الأعمدة للتشخيص
        print("DEBUG: أعمدة ملف الأحياء:", list(districts.columns))
        
        # تنظيف اسم الحي (وقائي) - البحث عن أي عمود يحتوي على كلمة "حي"
        district_name_column = None
        for col in districts.columns:
            if "حي" in col:
                district_name_column = col
                break
        
        if district_name_column and district_name_column != "اسم الحي":
            print(f"DEBUG: تم العثور على عمود الأحياء باسم: {district_name_column}")
            districts = districts.rename(columns={district_name_column: "اسم الحي"})
        
        # تنظيف اسم الحي
        if "اسم الحي" in districts.columns:
            districts["اسم الحي"] = districts["اسم الحي"].astype(str).str.strip()
        
        # توحيد أسماء الأعمدة للإحداثيات
        if "خط العرض" in districts.columns:
            districts = districts.rename(columns={"خط العرض": "خط_العرض"})
        if "خط الطول" in districts.columns:
            districts = districts.rename(columns={"خط الطول": "خط_الطول"})
        if "نطاق التأثير (كم)" in districts.columns:
            districts = districts.rename(columns={"نطاق التأثير (كم)": "نطاق_التأثير"})
        
        print(f"✅ تم قراءة ملف الأحياء بنجاح")
        print(f"📊 عدد الأحياء: {len(districts)}")
        print(f"📋 الأعمدة بعد التوحيد: {list(districts.columns)}")
        
        return districts
    
    except FileNotFoundError:
        print("❌ خطأ: ملف districts.xlsx غير موجود")
        return None
    except Exception as e:
        print("❌ خطأ في قراءة ملف الأحياء:", e)
        return None


# =========================================
# اختبار شامل
# =========================================
if __name__ == "__main__":
    print("=" * 60)
    print("🏗️  اختبار Government Data Provider")
    print("=" * 60)
    
    df = load_government_data()
    if not df.empty:
        print(f"\n✅ تم تحميل {len(df)} صفقة")
    
    projects_df = load_projects_data()
    districts_df = load_districts_data()
    
    if districts_df is not None:
        print("\n🔍 أول 3 صفوف من الأحياء:")
        print(districts_df.head(3))
