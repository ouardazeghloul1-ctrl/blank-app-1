# =========================================
# Government Data Provider
# تحميل بيانات وزارة العدل وتحضيرها للنظام
# =========================================

import pandas as pd
from pathlib import Path

# تعديل المسار ليطابق موقع الملف الفعلي (في جذر المشروع)
DATA_PATH = Path("market_transactions.csv")

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
            print("📁 المسار الكامل:", DATA_PATH.absolute())
            return pd.DataFrame()

        # قراءة الملف مع دعم الترميز العربي
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
        
        # طباعة الأعمدة الموجودة للتشخيص
        print("📊 الأعمدة الموجودة في الملف:", df.columns.tolist())
        print("📝 نموذج من البيانات:", df.head(2).to_dict('records'))

        # ==============================
        # تحويل الأعمدة الرقمية باستخدام pd.to_numeric (أكثر أماناً من astype)
        # ==============================
        if "السعر" in df.columns:
            df["السعر"] = pd.to_numeric(df["السعر"], errors="coerce")
        else:
            print("⚠️ عمود 'السعر' غير موجود")

        if "المساحة" in df.columns:
            df["المساحة"] = pd.to_numeric(df["المساحة"], errors="coerce")
        else:
            print("⚠️ عمود 'المساحة' غير موجود")

        # ==============================
        # فلترة المدينة فقط - باستخدام اسم العمود الصحيح
        # ==============================
        if selected_city:
            # البحث في عمود "الحي / المدينة" كما هو موجود في الملف
            if "الحي / المدينة" in df.columns:
                df = df[df["الحي / المدينة"].astype(str).str.contains(selected_city, na=False)]
                print(f"🏙️ تمت الفلترة لمدينة {selected_city}")
            elif "المدينة" in df.columns:
                df = df[df["المدينة"].astype(str).str.contains(selected_city, na=False)]
                print(f"🏙️ تمت الفلترة لمدينة {selected_city}")
            else:
                print("⚠️ لا يوجد عمود للمدينة في البيانات")

        if df.empty and selected_city:
            print(f"⚠️ لا توجد بيانات لمدينة {selected_city}")
            return df

        # ==============================
        # حساب سعر المتر (بصيغة Vectorized - أسرع بكثير)
        # ==============================
        if "السعر" in df.columns and "المساحة" in df.columns:
            # حذف الصفوف التي فيها مساحة <= 0 (لتجنب القسمة على صفر)
            df = df[df["المساحة"] > 0].copy()
            
            # حساب سعر المتر بطريقة Vectorized (أسرع من apply)
            df["سعر_المتر"] = df["السعر"] / df["المساحة"]
            
            # تنظيف القيم اللانهائية
            df["سعر_المتر"] = df["سعر_المتر"].replace([float('inf'), -float('inf')], 0)
        else:
            df["سعر_المتر"] = 0

        # ==============================
        # توحيد اسم الحي إذا وجد
        # ==============================
        if "الحي / المدينة" in df.columns:
            df["الحي"] = df["الحي / المدينة"]
        elif "الحي" in df.columns:
            pass  # بالفعل موجود
        else:
            df["الحي"] = "غير محدد"

        # ==============================
        # إضافة عمود نوع العقار (افتراضي)
        # لأن الوزارة لا تفصل بين شقة/فيلا
        # ==============================
        df["نوع_العقار"] = "سكني"

        # إسقاط الصفوف التي فيها قيم مفقودة في الأعمدة الأساسية
        df = df.dropna(subset=["السعر", "المساحة"], how="any")

        print(f"✅ تم تحميل {len(df)} صفقة من {selected_city if selected_city else 'جميع المدن'}")

        return df

    except Exception as e:
        print(f"❌ خطأ في تحميل البيانات الحكومية: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

# للتشغيل المباشر للتجربة
if __name__ == "__main__":
    print("🧪 تجربة تحميل البيانات...")
    df = load_government_data()
    print(f"📊 شكل البيانات: {df.shape}")
    if not df.empty:
        print("✅ أول 3 صفوف:")
        print(df.head(3))
        print("✅ معلومات البيانات:")
        print(df.info())
