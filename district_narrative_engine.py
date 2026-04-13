# =========================================
# Warda Intelligence
# District Narrative Engine (الإصدار النهائي للإنتاج مع المشاريع القريبة)
# محرك التقرير الاستثماري للأحياء
# =========================================

import pandas as pd
from ai_executive_summary import generate_executive_summary

# ✅ استيراد دوال تحميل البيانات
from government_data_provider import (
    load_districts_data,
    load_projects_data
)
import math

# =========================================
# ✅ تحميل البيانات مرة واحدة فقط عند تشغيل الملف (تحسين الأداء)
# =========================================
DISTRICTS_DATA = load_districts_data()
PROJECTS_DATA = load_projects_data()

# =========================================
# ✅ الحد الأقصى لعدد المشاريع المعروضة في التقرير
# =========================================
MAX_PROJECTS = 10


# =========================================
# دالة حساب المسافة بين نقطتين (Haversine) - مع تحسين معالجة الأخطاء
# =========================================
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    حساب المسافة بالكيلومتر بين نقطتين جغرافيتين
    """
    try:
        R = 6371  # نصف قطر الأرض بالكيلومتر
        lat1 = math.radians(float(lat1))
        lon1 = math.radians(float(lon1))
        lat2 = math.radians(float(lat2))
        lon2 = math.radians(float(lon2))
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = (
            math.sin(dlat / 2) ** 2 +
            math.cos(lat1) * math.cos(lat2) *
            math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return round(distance, 2)
    except Exception as e:
        print(f"⚠️ خطأ في حساب المسافة: {e}")
        return None


def generate_district_narrative(
        user_info,
        district_metrics,
        nearby_districts,
        dpi_score,
        market_data,
        real_data,
        projects_data=None
):
    """
    إنشاء تقرير تحليلي احترافي لحي داخل مدينة
    يعتمد على بيانات الصفقات العقارية الفعلية
    """

    # =========================================
    # ✅ التحسينات الأمنية الأساسية (حماية 100%)
    # =========================================
    
    district_metrics = district_metrics or {}
    dpi_score = float(dpi_score or 0)
    user_info = user_info or {}
    
    # =========================================
    # ✅ تعريف investment_score بشكل نظيف ومستقر
    # =========================================
    investment_score = user_info.get("investment_score")
    if investment_score is None:
        investment_score = round(dpi_score * 0.77, 1)
    
    # =========================================
    # استخراج البيانات الأساسية
    # =========================================

    district = district_metrics.get("district_name", "غير محدد")
    city = district_metrics.get("city_name", "غير محدد")
    
    district_price = float(district_metrics.get("district_avg_price", 0) or 0)
    city_price = float(district_metrics.get("city_avg_price", 0) or 0)
    transactions = int(district_metrics.get("transactions_count", 0) or 0)
    property_type = user_info.get("property_type", "عقار")
    
    clean_district_base = str(district).split("/")[-1].strip()
    
    if property_type == "شقة":
        property_market = "الشقق"
    elif property_type == "فيلا":
        property_market = "الفلل"
    elif property_type == "تاون هاوس":
        property_market = "التاون هاوس"
    elif property_type == "أرض":
        property_market = "الأراضي"
    elif property_type == "محل تجاري":
        property_market = "المحلات التجارية"
    else:
        property_market = property_type

    if city_price > 0:
        price_ratio = district_price / city_price
    else:
        price_ratio = 1

    # =========================================
    # استخدام البيانات المحملة مرة واحدة
    # =========================================
    districts_df = DISTRICTS_DATA
    projects_df = projects_data if projects_data is not None else PROJECTS_DATA

    # ✅ سطر تشخيصي حاسم - يكشف مصدر البيانات
    print("="*50)
    print("PROJECTS SOURCE:", "passed data" if projects_data is not None else "global data")
    print("PROJECTS ROW COUNT:", len(projects_df) if projects_df is not None else "None")
    if projects_df is not None and not projects_df.empty:
        print("PROJECTS FIRST ROW:", projects_df.iloc[0].to_dict() if len(projects_df) > 0 else "Empty")
    print("="*50)

    # =========================================
    # جلب إحداثيات الحي الحالي
    # ✅ التعديل الحاسم: استخدام اسم العمود الصحيح "اسم الحي"
    # =========================================
    district_lat = None
    district_lon = None
    try:
        if districts_df is not None and not districts_df.empty:
            # ✅ سطور تشخيصية لمعرفة سبب عدم العثور على الإحداثيات
            print("CITY:", city)
            print("DISTRICT:", clean_district_base)
            
            # ✅ عرض أسماء الأعمدة للتأكد من وجود "اسم الحي"
            print("AVAILABLE COLUMNS:", list(districts_df.columns))
            
            if "اسم الحي" not in districts_df.columns:
                print("❌ عمود 'اسم الحي' غير موجود في ملف الأحياء!")
                print("📋 الأعمدة المتاحة:", list(districts_df.columns))
            else:
                print("AVAILABLE DISTRICTS SAMPLE:", districts_df["اسم الحي"].head(10).tolist())
            
            # ✅ تنظيف أسماء المدن والأحياء للمقارنة المرنة
            city_clean = str(city).strip().lower()
            
            # تنظيف اسم الحي المطلوب
            district_clean = str(clean_district_base).strip().replace("حي", "").strip().lower()
            
            # ✅ البحث المرن باستخدام اسم العمود الصحيح "اسم الحي"
            match = districts_df[
                (districts_df["المدينة"].astype(str).str.strip().str.lower() == city_clean) &
                (districts_df["اسم الحي"].astype(str).str.strip().str.replace("حي", "").str.strip().str.lower() == district_clean)
            ]
            
            if not match.empty:
                district_lat = match.iloc[0]["خط_العرض"]
                district_lon = match.iloc[0]["خط_الطول"]
                print(f"📍 تم العثور على إحداثيات الحي {clean_district_base}: {district_lat}, {district_lon}")
            else:
                # محاولة البحث الجزئي إذا لم يجد تطابق تام
                print(f"⚠️ لم يتم العثور على تطابق تام، جاري البحث الجزئي...")
                match_partial = districts_df[
                    (districts_df["المدينة"].astype(str).str.strip().str.lower() == city_clean) &
                    (districts_df["اسم الحي"].astype(str).str.contains(district_clean, case=False, na=False))
                ]
                if not match_partial.empty:
                    district_lat = match_partial.iloc[0]["خط_العرض"]
                    district_lon = match_partial.iloc[0]["خط_الطول"]
                    print(f"📍 تم العثور على إحداثيات (بحث جزئي) للحي {clean_district_base}: {district_lat}, {district_lon}")
                else:
                    print(f"❌ لم يتم العثور على إحداثيات للحي {clean_district_base}")
    except Exception as e:
        print("خطأ في جلب إحداثيات الحي:", e)
        import traceback
        traceback.print_exc()

    # =========================================
    # حساب المشاريع القريبة
    # =========================================
    
    # =========================================
    # تحسين الأداء: إنشاء df_city مرة واحدة
    # =========================================
    
    city_districts_list = []
    city_transactions_by_district = pd.Series(dtype=int)
    city_price_by_district = pd.Series(dtype=float)
    total_city_transactions = 0
    df_city = pd.DataFrame()
    
    try:
        if isinstance(real_data, pd.DataFrame) and not real_data.empty and "district" in real_data.columns:
            print("="*50)
            print(f"تحليل مدينة: {city}")
            print(f"الحي المطلوب: {clean_district_base}")
            print(f"إجمالي البيانات المستقبلة: {len(real_data):,} صفقة")
            
            df_city = real_data.copy()
            print(f"✅ تم استخدام البيانات مباشرة بدون إعادة فلترة")
            print(f"صفقات المدينة: {len(df_city):,}")
            
            if not df_city.empty:
                df_city["district_clean"] = (
                    df_city["district"]
                    .astype(str)
                    .str.split("/")
                    .str[-1]
                    .str.strip()
                )
                
                df_city["price"] = pd.to_numeric(df_city["price"], errors="coerce")
                df_city["area"] = pd.to_numeric(df_city["area"], errors="coerce")
                df_city = df_city[df_city["area"] > 0]
                df_city["price_sqm"] = df_city["price"] / df_city["area"]
                df_city = df_city[df_city["price_sqm"].notna()]
                df_city = df_city[(df_city["price_sqm"] >= 50) & (df_city["price_sqm"] <= 200000)]
                
                total_city_transactions = len(df_city)
                city_transactions_by_district = df_city["district_clean"].value_counts(sort=True)
                city_districts_list = city_transactions_by_district.index.tolist()
                city_price_by_district = df_city.groupby("district_clean")["price_sqm"].median()
                city_price_by_district = city_price_by_district.dropna().sort_values(ascending=False)
                
                print(f"عدد الأحياء المكتشفة: {len(city_districts_list)}")
                
                if clean_district_base in city_districts_list:
                    print(f"✅ تم العثور على الحي: {clean_district_base}")
                    print(f"عدد صفقات الحي: {city_transactions_by_district[clean_district_base]:,}")
                else:
                    print(f"⚠️ الحي {clean_district_base} غير موجود في القائمة")
    except Exception as e:
        print(f"❌ خطأ في تجهيز بيانات المدينة: {e}")

    print("="*50)

    # =========================================
    # ✅ حساب المشاريع القريبة قبل إنشاء النص
    # =========================================
    nearby_projects = []
    try:
        # ✅ سطر الاختبار - قبل أي شرط ليكشف الحقيقة حتى لو البيانات فارغة
        print("DEBUG PROJECTS DF:", type(projects_df), "rows:", len(projects_df) if projects_df is not None else "None")
        
        # ✅ سطر إضافي لفحص الأعمدة
        print("DEBUG PROJECTS COLUMNS:", list(projects_df.columns) if projects_df is not None else "None")
        
        if (district_lat is not None and district_lon is not None and
            projects_df is not None and not projects_df.empty):
            
            print(f"🔍 جاري البحث عن مشاريع قريبة من {clean_district_base}...")
            print(f"📋 أعمدة المشاريع المتاحة: {list(projects_df.columns)}")
            
            # ✅ استخدام نطاق تأثير الحي (من user_info) مع الحد الأدنى 10 كم
            district_impact_radius = max(float(user_info.get("نطاق_التأثير", 5) or 5), 10)
            print(f"📍 نطاق تأثير الحي المستخدم للبحث: {district_impact_radius} كم")
            
            # ✅ التعديل الحاسم: استخدام iterrows بدلاً من itertuples
            for _, row in projects_df.iterrows():
                # ✅ سطر الاختبار الحاسم - يكشف السبب الحقيقي
                project_city = row.get("المدينة", None)
                project_lat = row.get("خط_العرض", None)
                project_lon = row.get("خط_الطول", None)
                
                # ✅ التعديل النهائي: استخدام اسم العمود الصحيح من ملف Excel
                project_name = (
                    row.get("اسم المشروع بالعربية") or 
                    row.get("اسم_المشروع") or 
                    row.get("Project Name (English)") or 
                    "غير محدد"
                )
                
                project_type = row.get("النوع", "غير محدد")
                project_status = row.get("الحالة", "غير محدد")
                
                print("DEBUG ROW:", project_city, project_lat, project_lon, project_name)
                
                # تنظيف اسم المدينة للمقارنة
                project_city_clean = str(project_city).split("/")[0].strip().lower() if project_city else ""
                city_clean = str(city).split("/")[0].strip().lower()
                
                print(f"DEBUG CITY COMPARE: project='{project_city_clean}', report='{city_clean}'")
                
                if project_city_clean != city_clean:
                    print(f"DEBUG SKIP: city mismatch - {project_city_clean} != {city_clean}")
                    continue
                
                if project_lat is None or project_lon is None:
                    print(f"DEBUG SKIP: missing coordinates for {project_name}")
                    continue
                
                distance = calculate_distance(
                    float(district_lat),
                    float(district_lon),
                    float(project_lat),
                    float(project_lon)
                )
                
                if distance is None:
                    continue
                
                print(f"DEBUG DISTANCE: {project_name} distance={distance}, radius={district_impact_radius}")
                
                if distance <= district_impact_radius:
                    nearby_projects.append({
                        "name": project_name,
                        "type": project_type,
                        "status": project_status,
                        "distance": distance,
                        "lat": float(project_lat),
                        "lon": float(project_lon)
                    })
                    print(f"✅ مشروع قريب: {project_name} ({project_type}) على بعد {distance} كم")
            
            nearby_projects.sort(key=lambda x: x["distance"])
            nearby_projects = nearby_projects[:MAX_PROJECTS]
            
            print(f"✅ تم العثور على {len(nearby_projects)} مشروع قريب (بحد أقصى {MAX_PROJECTS})")
            
    except Exception as e:
        print("خطأ في حساب المشاريع القريبة:", e)
        import traceback
        traceback.print_exc()

    print(f"DEBUG: عدد المشاريع المكتشفة: {len(nearby_projects)}")

    # =========================================
    # فقرة المشاريع — بدون فصل (كتلة واحدة فقط)
    # =========================================
    
    # بناء قائمة المشاريع للنص
    projects_list_text = ""
    if nearby_projects:
        for p in nearby_projects:
            name = p.get("name", "مشروع")
            status = p.get("status", "غير محدد")
            distance = round(float(p.get("distance", 0)), 2)
            projects_list_text += f"• {name} ({status}) — على بعد {distance} كم\n"
    
    # الفقرة النهائية للمشاريع (بدون أي عنوان "فصل")
    if nearby_projects:
        projects_paragraph = f"""المشاريع التنموية القريبة من الحي

تشير البيانات إلى وجود مشاريع تنموية قريبة من الحي، وهو عامل إيجابي يعزز جاذبية الموقع ويرفع من احتمالية استقرار الطلب العقاري ونمو القيمة السوقية للعقارات خلال السنوات القادمة.

{projects_list_text}

وجود هذه المشاريع قد يساهم في رفع الطلب العقاري وتحسين جاذبية الحي للمستثمرين خلال السنوات القادمة.
"""
    else:
        projects_paragraph = """المشاريع التنموية القريبة من الحي

لا تشير البيانات الحالية إلى وجود مشاريع تنموية مؤثرة ضمن نطاق التأثير الجغرافي للحي، وهو ما يعكس استقرار البيئة العمرانية الحالية دون وجود عوامل نمو إضافية في المدى القريب.

غياب المشاريع التنموية لا يمثل عامل خطر مباشر، لكنه قد يعني أن نمو الطلب العقاري يعتمد بشكل أساسي على خصائص الحي الحالية ومستوى الخدمات المتوفر فيه.
"""

    # تخزين المشاريع والإحداثيات لاستخدامها في الخريطة لاحقاً
    user_info["nearby_projects"] = nearby_projects
    if district_lat is not None:
        user_info["district_lat"] = float(district_lat)
    else:
        user_info["district_lat"] = None
    if district_lon is not None:
        user_info["district_lon"] = float(district_lon)
    else:
        user_info["district_lon"] = None

    # =========================================
    # تهيئة report_sections (بدون أي قسم للمشاريع)
    # =========================================
    report_sections = []

    # =========================================
    # Investment Snapshot (سيصبح الفصل الأول)
    # =========================================
    snapshot_section = f"""

ملخص الاستثمار السريع

المدينة: {city}
الحي: {district}
نوع العقار: {property_type}

متوسط سعر المتر: {district_price:,.0f} ريال
متوسط سعر المدينة: {city_price:,.0f} ريال
عدد الصفقات: {transactions:,} صفقة
مؤشر قوة الحي (DPI): {dpi_score:.1f} / 100
النتيجة الاستثمارية: {investment_score} / 100

"""
    report_sections.append(snapshot_section)

    # ملخص تنفيذي
    summary_section = f"""
ملخص تنفيذي

يعرض هذا التقرير تحليلاً لسوق {property_market} في حي {district} بمدينة {city}.
يعتمد التحليل على {transactions:,} صفقة عقارية تم تسجيلها في السوق خلال الفترة المدروسة.

متوسط سعر المتر في الحي يبلغ {district_price:,.0f} ريال، مقارنة بمتوسط المدينة البالغ {city_price:,.0f} ريال.
هذا يضع الحي ضمن شريحة { "مرتفع السعر" if price_ratio > 1.1 else "متوسط السعر" if price_ratio > 0.9 else "منخفض السعر" } داخل السوق العقاري للمدينة.
"""
    report_sections.append(summary_section)

    # =========================================
    # بطاقة معلومات السوق
    # =========================================
    overview_section = f"""
تحليل سوق {property_market} في حي {district} – مدينة {city}

يعتمد هذا التقرير على تحليل بيانات الصفقات العقارية
المسجلة في السوق بهدف تقييم الجاذبية الاستثمارية
للحي وموقعه داخل السوق العقاري للمدينة.


بطاقة معلومات السوق العقاري

المدينة: {city}

الحي: {district}

نوع العقار محل التحليل: {property_type}

متوسط سعر المتر في الحي:
{district_price:,.0f} ريال

متوسط سعر المتر في المدينة:
{city_price:,.0f} ريال

عدد الصفقات المنفذة:
{transactions:,} صفقة

مؤشر قوة الحي (DPI):
{dpi_score:.1f} / 100
"""
    report_sections.append(overview_section)

    # =========================================
    # منهجية التحليل
    # =========================================
    data_method_section = f"""

منهجية التحليل

يعتمد هذا التقرير على تحليل بيانات الصفقات العقارية الفعلية المسجلة في السوق.
تم حساب متوسط سعر المتر باستخدام المعادلة التالية:
سعر المتر = سعر الصفقة ÷ مساحة العقار

ولتقليل تأثير الصفقات الشاذة تم استخدام القيمة الوسيطة (Median) بدلاً من المتوسط الحسابي في بعض المؤشرات.

يعتمد التقرير على {transactions:,} صفقة عقارية داخل حي {district} خلال الفترة المتاحة من البيانات.
"""
    report_sections.append(data_method_section)

    # =========================================
    # تحليل موقع الحي في السوق
    # =========================================
    if price_ratio > 1.15:
        price_position = "أعلى من متوسط أسعار المدينة بشكل واضح"
        price_analysis = f"""
تشير البيانات إلى أن أسعار المتر في حي {district}
أعلى من متوسط أسعار مدينة {city} بفارق ملحوظ.

هذا قد يدل على أن الحي يقع في شريحة سعرية مرتفعة داخل السوق،
وغالباً ما ترتبط هذه الحالة بارتفاع الطلب أو بوجود خصائص
عمرانية أو موقعية تجعل الحي أكثر جاذبية للمشترين.
"""
    elif price_ratio > 1.05:
        price_position = "أعلى قليلاً من متوسط السوق"
        price_analysis = f"""
أسعار المتر في حي {district} أعلى بشكل طفيف
من متوسط الأسعار في مدينة {city}.

هذا يشير عادة إلى سوق متوازن مع وجود طلب مستقر،
حيث يميل المشترون إلى دفع علاوة سعرية محدودة
مقابل موقع الحي أو جودة البيئة العمرانية فيه.
"""
    elif price_ratio < 0.85:
        price_position = "أقل من متوسط المدينة بشكل واضح"
        price_analysis = f"""
متوسط سعر المتر في حي {district} أقل بشكل واضح
من متوسط الأسعار في مدينة {city}.

في بعض الحالات قد يعكس هذا وجود فرصة استثمارية،
خصوصاً إذا كان الحي يشهد نشاطاً جيداً في عدد الصفقات
مما قد يشير إلى مرحلة تسعير أقل من القيمة الحقيقية.
"""
    elif price_ratio < 0.95:
        price_position = "أقل قليلاً من متوسط السوق"
        price_analysis = f"""
أسعار المتر في حي {district} أقل بشكل طفيف
من متوسط أسعار مدينة {city}.

هذا قد يجعل الحي خياراً مناسباً للمستثمرين
الباحثين عن دخول السوق عند مستويات سعرية
أقل من المتوسط العام للمدينة.
"""
    else:
        price_position = "قريب من متوسط السوق"
        price_analysis = f"""
تشير البيانات إلى أن أسعار حي {district}
تقع بالقرب من متوسط الأسعار في مدينة {city}.

هذا يدل عادة على أن الحي يتحرك ضمن النطاق
الطبيعي للسوق العقاري دون وجود انحرافات
سعرية كبيرة مقارنة ببقية الأحياء.
"""

    market_position_section = f"""

موقع الحي في السوق العقاري

الموقع السعري للحي:
{price_position}

{price_analysis}
"""
    report_sections.append(market_position_section)

    # =========================================
    # Price Gap Analysis
    # =========================================
    gap_section = ""
    try:
        if city_price > 0:
            gap = ((district_price - city_price) / city_price) * 100
            relation = "أعلى" if gap > 0 else "أقل"
            gap_section = f"""

فجوة السعر داخل المدينة

متوسط سعر المتر في حي {district}: {district_price:,.0f} ريال
متوسط سعر المتر في مدينة {city}: {city_price:,.0f} ريال

هذا يعني أن الحي {relation} من متوسط المدينة بنسبة: {abs(gap):.1f}%

يعطي هذا المؤشر فكرة عن موقع الحي السعري داخل السوق.
"""
    except Exception as e:
        print("Gap Analysis Error:", e)
    report_sections.append(gap_section)

    # =========================================
    # Market Benchmark
    # =========================================
    price_diff_percent = ((district_price - city_price) / city_price) * 100 if city_price > 0 else 0
    benchmark_section = f"""

مقارنة الحي مع متوسط السوق

متوسط سعر المتر في الحي: {district_price:,.0f} ريال
متوسط سعر المتر في المدينة: {city_price:,.0f} ريال

الفارق: {price_diff_percent:.1f}%

هذا المؤشر يساعد المستثمر على فهم ما إذا كان الحي يتداول عند خصم سعري أو بعلاوة سعرية مقارنة بالسوق.
"""
    report_sections.append(benchmark_section)

    # =========================================
    # Price Ranking داخل المدينة
    # =========================================
    price_rank_section = ""
    rank = None
    total = None
    try:
        if not city_price_by_district.empty and clean_district_base in city_price_by_district.index:
            rank = list(city_price_by_district.index).index(clean_district_base) + 1
            total = len(city_price_by_district)
            if total > 0:
                percentile = ((total - rank + 1) / total) * 100
            else:
                percentile = 0
            
            if percentile >= 80:
                label = "ضمن أعلى 20% من الأحياء سعراً في المدينة"
            elif percentile >= 50:
                label = "ضمن الشريحة السعرية المتوسطة"
            else:
                label = "ضمن الشريحة السعرية الاقتصادية"
            
            price_rank_section = f"""

ترتيب الحي من حيث الأسعار داخل المدينة

يحتل حي {district} المرتبة {rank} من أصل {total} حي
من حيث متوسط سعر المتر.

هذا يضع الحي {label}.
"""
    except Exception as e:
        print("Price Rank Error:", e)
    report_sections.append(price_rank_section)

    # =========================================
    # Liquidity Ranking
    # =========================================
    liquidity_rank_section = ""
    try:
        if not city_transactions_by_district.empty and clean_district_base in city_transactions_by_district.index:
            rank_l = list(city_transactions_by_district.index).index(clean_district_base) + 1
            total_l = len(city_transactions_by_district)
            liquidity_rank_section = f"""

ترتيب الحي من حيث السيولة العقارية

يحتل حي {district} المرتبة {rank_l} من أصل {total_l} حي
من حيث عدد الصفقات العقارية في المدينة.

كلما كان الترتيب أقرب إلى المركز الأول كان السوق أكثر سيولة.
"""
    except Exception as e:
        print("Liquidity Rank Error:", e)
    report_sections.append(liquidity_rank_section)

    # =========================================
    # تحليل السيولة العقارية
    # =========================================
    if transactions >= 40:
        liquidity_level = "سيولة عالية جداً"
        liquidity_analysis = f"""
يسجل حي {district} مستوى نشاط مرتفع في السوق العقاري،
حيث بلغ عدد الصفقات المنفذة {transactions:,} صفقة.

هذا الحجم من النشاط يشير عادة إلى سوق يتمتع بدرجة
عالية من السيولة، مما يسهل عمليات البيع والشراء
ويقلل من فترات انتظار بيع العقار.
"""
    elif transactions >= 20:
        liquidity_level = "سيولة جيدة"
        liquidity_analysis = f"""
بلغ عدد الصفقات العقارية في حي {district}
حوالي {transactions:,} صفقة خلال الفترة محل التحليل.

يشير هذا المستوى من النشاط إلى وجود سيولة جيدة
في السوق العقاري للحي، حيث توجد حركة بيع وشراء
مستمرة نسبياً مقارنة بعدد من الأحياء الأخرى.
"""
    elif transactions >= 10:
        liquidity_level = "سيولة متوسطة"
        liquidity_analysis = f"""
سجل حي {district} نحو {transactions:,} صفقة عقارية
خلال الفترة محل التحليل.

هذا يشير إلى وجود نشاط عقاري متوسط،
حيث يمكن تنفيذ عمليات البيع والشراء
لكن قد تستغرق بعض العمليات وقتاً أطول.
"""
    else:
        liquidity_level = "سيولة منخفضة"
        liquidity_analysis = f"""
بلغ عدد الصفقات العقارية في حي {district}
حوالي {transactions:,} صفقة فقط.

انخفاض عدد الصفقات قد يشير إلى سوق
بطيء نسبياً من ناحية السيولة،
مما قد يعني أن بيع العقار قد يستغرق
فترة أطول مقارنة بالأحياء الأكثر نشاطاً.
"""

    liquidity_section = f"""

تحليل السيولة العقارية

مستوى السيولة في الحي:
{liquidity_level}

{liquidity_analysis}
"""
    report_sections.append(liquidity_section)

    # =========================================
    # ترتيب الحي داخل المدينة حسب النشاط
    # =========================================
    ranking_section = ""
    try:
        if not city_transactions_by_district.empty and clean_district_base in city_transactions_by_district.index:
            district_rank = list(city_transactions_by_district.index).index(clean_district_base) + 1
            district_transactions = city_transactions_by_district[clean_district_base]
            total_districts = len(city_transactions_by_district)
            
            if district_rank <= 5:
                rank_label = "ضمن الأحياء الأكثر نشاطاً في المدينة"
            elif district_rank <= 15:
                rank_label = "ضمن الأحياء النشطة في السوق العقاري"
            else:
                rank_label = "ضمن الأحياء الأقل نشاطاً نسبياً"
                
            ranking_section = f"""

موقع الحي من حيث النشاط العقاري داخل المدينة

بحسب تحليل بيانات الصفقات العقارية في مدينة {city}،
يحتل حي {district} المرتبة {district_rank} من أصل {total_districts} حي
من حيث عدد الصفقات.

بلغ إجمالي الصفقات المسجلة في الحي
{district_transactions:,} صفقة خلال الفترة المدروسة.

هذا يضع الحي {rank_label} مقارنة ببقية الأحياء داخل المدينة.
"""
    except Exception as e:
        print("Narrative Engine Error (Ranking):", e)
    report_sections.append(ranking_section)

    # =========================================
    # الأحياء الأكثر نشاطاً في المدينة (TOP 5)
    # =========================================
    top_districts_section = ""
    try:
        if not city_transactions_by_district.empty:
            top_districts = city_transactions_by_district.sort_values(ascending=False).head(5)
            if not top_districts.empty:
                lines = ""
                for i, (name, count) in enumerate(top_districts.items(), start=1):
                    market_share = (count / total_city_transactions) * 100 if total_city_transactions > 0 else 0
                    lines += f"{i}. {name} — {count:,} صفقة ({market_share:.1f}% من السوق)\n"
                
                if clean_district_base in city_transactions_by_district.index:
                    current_rank = list(city_transactions_by_district.index).index(clean_district_base) + 1
                    if current_rank <= 5:
                        rank_note = f"\n📍 حي {district} من ضمن هذه القائمة في المرتبة {current_rank}."
                    else:
                        rank_note = f"\n📍 حي {district} يحتل المرتبة {current_rank} خارج هذه القائمة."
                else:
                    rank_note = ""
                
                top_districts_section = f"""

🏆 الأحياء الأكثر نشاطاً في السوق العقاري

بحسب تحليل بيانات الصفقات العقارية في مدينة {city}،
تظهر الأحياء التالية كأكثر المناطق نشاطاً في السوق:

{lines}
{rank_note}
"""
    except Exception as e:
        print("Top Districts Error:", e)
    report_sections.append(top_districts_section)

    # =========================================
    # تحليل الفجوة السعرية وفرصة الاستثمار
    # =========================================
    if price_ratio < 0.85 and transactions >= 15:
        opportunity_type = "فرصة استثمارية قوية"
        opportunity_analysis = f"""
تشير البيانات إلى أن متوسط سعر المتر في حي {district}
أقل بشكل ملحوظ من متوسط الأسعار في مدينة {city}.

في الوقت نفسه يظهر الحي نشاطاً جيداً في عدد الصفقات
حيث بلغ إجمالي الصفقات {transactions:,} صفقة.

هذا الجمع بين السعر المنخفض نسبياً والنشاط الجيد
قد يشير إلى وجود فرصة استثمارية، حيث يمكن أن يكون
الحي في مرحلة تسعير أقل من قيمته السوقية مقارنة
ببقية أحياء المدينة.
"""
    elif price_ratio < 0.95:
        opportunity_type = "فرصة استثمارية محتملة"
        opportunity_analysis = f"""
أسعار المتر في حي {district} أقل قليلاً من متوسط
الأسعار في مدينة {city}.

هذا قد يمنح المستثمرين فرصة للدخول إلى السوق
عند مستويات سعرية أقل من المتوسط العام،
خصوصاً إذا استمر النشاط العقاري في الحي
خلال الفترات القادمة.
"""
    elif price_ratio > 1.15:
        opportunity_type = "سوق مرتفع السعر"
        opportunity_analysis = f"""
تشير البيانات إلى أن أسعار المتر في حي {district}
أعلى بشكل واضح من متوسط الأسعار في مدينة {city}.

هذا قد يعني أن الحي وصل إلى مستويات سعرية
مرتفعة مقارنة بالسوق العام، وهو ما قد يقلل
من هامش الارتفاع السعري المستقبلي في المدى القريب.
"""
    else:
        opportunity_type = "سوق متوازن"
        opportunity_analysis = f"""
البيانات تشير إلى أن أسعار حي {district}
تقع ضمن النطاق الطبيعي للأسعار في مدينة {city}.

في هذه الحالة يعتمد القرار الاستثماري
بشكل أكبر على نوع العقار وموقعه داخل الحي
بدلاً من وجود فجوة سعرية واضحة في السوق.
"""

    opportunity_section = f"""

تحليل القيمة الاستثمارية للحي

تقييم الفرصة الاستثمارية:
{opportunity_type}

{opportunity_analysis}
"""
    report_sections.append(opportunity_section)

    # =========================================
    # مقارنة الحي مع الأحياء القريبة
    # =========================================
    comparison_lines = ""
    if not nearby_districts:
        comparison_lines = "لا توجد بيانات كافية لإجراء مقارنة مع الأحياء المجاورة."
    else:
        for d in nearby_districts:
            name = d.get("district_name", "")
            price = float(d.get("avg_price", 0) or 0)
            diff = ((price - district_price) / district_price) * 100 if district_price > 0 else 0
            relation = "أعلى" if diff > 0 else "أقل" if diff < 0 else "مساوٍ"
            comparison_lines += f"""
حي {name}
متوسط السعر: {price:,.0f} ريال للمتر
الفرق عن حي {district}: {abs(diff):.1f}% ({relation})
"""

    comparison_section = f"""

مقارنة الأسعار مع الأحياء القريبة

لفهم موقع حي {district} بشكل أفضل داخل السوق،
تمت مقارنة متوسط سعر المتر مع عدد من الأحياء
القريبة أو المشابهة في المستوى السعري.

{comparison_lines}
"""
    report_sections.append(comparison_section)

    # =========================================
    # تحليل المخاطر الاستثمارية
    # =========================================
    if transactions < 10:
        liquidity_risk = "مخاطر سيولة مرتفعة"
        liquidity_risk_text = f"""
انخفاض عدد الصفقات في حي {district} قد يشير
إلى محدودية السيولة في السوق العقاري.

في هذه الحالة قد تستغرق عملية بيع العقار
فترة أطول مقارنة بالأحياء الأكثر نشاطاً.
"""
    elif transactions < 25:
        liquidity_risk = "مخاطر سيولة متوسطة"
        liquidity_risk_text = f"""
مستوى النشاط العقاري في حي {district}
يشير إلى سيولة متوسطة في السوق.

هذا يعني أن البيع ممكن لكن قد يعتمد
بشكل كبير على نوع العقار وموقعه داخل الحي.
"""
    else:
        liquidity_risk = "مخاطر سيولة منخفضة"
        liquidity_risk_text = f"""
عدد الصفقات المرتفع في حي {district}
يشير إلى سوق يتمتع بسيولة جيدة.

هذا يقلل عادة من مخاطر صعوبة البيع
ويجعل السوق أكثر مرونة للمستثمرين.
"""

    if price_ratio > 1.2:
        price_risk = "مخاطر سعرية مرتفعة"
        price_risk_text = f"""
أسعار المتر في حي {district} أعلى بكثير
من متوسط أسعار مدينة {city}.

في بعض الحالات قد يزيد ذلك من احتمال
حدوث تصحيح سعري إذا انخفض الطلب مستقبلاً.
"""
    elif price_ratio > 1.05:
        price_risk = "مخاطر سعرية محدودة"
        price_risk_text = f"""
الحي يقع في شريحة سعرية أعلى قليلاً
من متوسط السوق في مدينة {city}.

هذا لا يمثل خطراً كبيراً عادة،
لكن قد يحد من سرعة الارتفاع السعري.
"""
    else:
        price_risk = "مخاطر سعرية منخفضة"
        price_risk_text = f"""
أسعار حي {district} تقع ضمن النطاق
الطبيعي أو الأقل من متوسط السوق.

هذا يقلل عادة من مخاطر التصحيح السعري
ويجعل الدخول الاستثماري أكثر أماناً.
"""

    risk_section = f"""

تحليل المخاطر الاستثمارية

مخاطر السيولة:
{liquidity_risk}

{liquidity_risk_text}

مخاطر السعر:
{price_risk}

{price_risk_text}
"""
    report_sections.append(risk_section)

    # =========================================
    # تحليل اتجاه السعر داخل الفترة المتاحة
    # =========================================
    trend_section = ""
    try:
        if not df_city.empty and "date" in df_city.columns:
            df_trend = df_city[df_city["district_clean"].str.lower() == clean_district_base.lower()].copy()
            if not df_trend.empty:
                df_trend["date"] = pd.to_datetime(df_trend["date"], errors="coerce")
                df_trend = df_trend[df_trend["date"].notna()].sort_values("date")
                if len(df_trend) >= 4:
                    midpoint = len(df_trend) // 2
                    first_price = df_trend.iloc[:midpoint]["price_sqm"].median()
                    last_price = df_trend.iloc[midpoint:]["price_sqm"].median()
                    change = ((last_price - first_price) / first_price) * 100 if first_price > 0 else 0
                    trend = "اتجاه صعودي" if change > 3 else "اتجاه هبوطي" if change < -3 else "استقرار نسبي"
                    trend_section = f"""

اتجاه السوق داخل الفترة المدروسة

بمقارنة الصفقات الأولى مع أحدث الصفقات في حي {district}
يظهر أن متوسط سعر المتر تغير بنسبة {change:.1f}%.

هذا يشير إلى {trend} في السوق العقاري داخل الحي
خلال الفترة المتاحة من البيانات.
"""
                else:
                    trend_section = f"""

اتجاه السوق داخل الفترة المدروسة

عدد الصفقات المتاحة لحي {district} ({len(df_trend)} صفقة) لا يسمح بإجراء تحليل موثوق لاتجاه السوق.
يوصى بتجميع المزيد من البيانات للحصول على قراءة أدق لاتجاه الأسعار.
"""
    except Exception as e:
        print("Narrative Engine Error (Trend):", e)
    report_sections.append(trend_section)

    # =========================================
    # Market Momentum Analysis
    # =========================================
    cycle_section = ""
    try:
        if not df_city.empty and "date" in df_city.columns:
            df_cycle = df_city[df_city["district_clean"].str.lower() == clean_district_base.lower()].copy()
            if not df_cycle.empty:
                df_cycle["date"] = pd.to_datetime(df_cycle["date"], errors="coerce")
                df_cycle = df_cycle[df_cycle["date"].notna()].sort_values("date")
                if len(df_cycle) >= 10:
                    midpoint = len(df_cycle) // 2
                    first_price = df_cycle.iloc[:midpoint]["price_sqm"].median()
                    last_price = df_cycle.iloc[midpoint:]["price_sqm"].median()
                    change = ((last_price - first_price) / first_price) * 100 if first_price > 0 else 0
                    if change > 5:
                        trend = "اتجاه صعودي واضح"
                        interpretation = "يشير هذا إلى زيادة الطلب أو تحسن في مستويات التسعير داخل الحي."
                    elif change < -5:
                        trend = "اتجاه هبوطي ملحوظ"
                        interpretation = "قد يعكس هذا تراجعاً في الطلب أو تصحيحاً في مستويات الأسعار."
                    else:
                        trend = "استقرار نسبي في الأسعار"
                        interpretation = "السوق يتحرك ضمن نطاق سعري مستقر دون تغيرات كبيرة."
                    cycle_section = f"""

تحليل الزخم السعري في السوق

تم تحليل حركة أسعار المتر في حي {district} خلال الفترة الزمنية المتاحة من البيانات.
أظهر التحليل أن متوسط سعر المتر تغير بنسبة {change:.1f}%.

هذا يشير إلى {trend} في السوق العقاري داخل الحي خلال الأشهر الأخيرة.
{interpretation}
"""
                else:
                    cycle_section = f"""

تحليل الزخم السعري في السوق

البيانات المتاحة لحي {district} محدودة زمنياً ({len(df_cycle)} صفقة) ولا تحتوي على عدد كافٍ من الصفقات لإجراء تحليل دقيق لاتجاه الأسعار.
يوصى بمتابعة السوق خلال الأشهر القادمة للحصول على قراءة أوضح لاتجاه الأسعار.
"""
    except Exception as e:
        print("Market Momentum Error:", e)
    report_sections.append(cycle_section)

    # =========================================
    # Investment Strategy
    # =========================================
    if price_ratio < 0.9:
        strategy_text = f"""
الاستراتيجية المقترحة:
• البحث عن عقارات أقل من متوسط سعر الحي.
• التركيز على المواقع القريبة من الخدمات.
• الاحتفاظ بالعقار لمدة 3 إلى 5 سنوات للاستفادة من نمو الأسعار.
"""
    elif price_ratio > 1.1:
        strategy_text = f"""
الاستراتيجية المقترحة:
• اختيار عقارات مميزة داخل الحي.
• الاستثمار طويل الأجل.
• التركيز على المواقع ذات الطلب المرتفع.
"""
    else:
        strategy_text = f"""
الاستراتيجية المقترحة:
• اختيار عقارات بسعر السوق أو أقل قليلاً.
• التركيز على السيولة وسهولة إعادة البيع.
"""
    strategy_section = f"""

استراتيجية الاستثمار في الحي
{strategy_text}
"""
    report_sections.append(strategy_section)

    # =========================================
    # Capital Growth Potential
    # =========================================
    if price_ratio < 0.9 and transactions >= 20:
        growth = "مرتفعة"
        range_text = "12% إلى 20% خلال 3 إلى 5 سنوات"
    elif price_ratio <= 1.0:
        growth = "متوسطة"
        range_text = "6% إلى 12% خلال 3 إلى 5 سنوات"
    elif price_ratio <= 1.15:
        growth = "محدودة"
        range_text = "3% إلى 8% خلال 3 إلى 5 سنوات"
    else:
        growth = "ضعيفة"
        range_text = "0% إلى 5% خلال 3 إلى 5 سنوات"
    
    growth_section = f"""

إمكانية النمو الرأسمالي

تقدير النمو المحتمل للأسعار في الحي:
مستوى النمو المتوقع: {growth}
النطاق التقديري: {range_text}

يعتمد هذا التقدير على:
• موقع الحي السعري (أقل/أعلى من متوسط المدينة)
• نشاط السوق (عدد الصفقات)
• مؤشر قوة الحي (DPI)
"""
    report_sections.append(growth_section)

    # =========================================
    # Investment Intelligence Score
    # =========================================
    score_section = f"""

التقييم الكلي لجاذبية الاستثمار في الحي

النتيجة النهائية: {investment_score} / 100

يعتمد هذا التقييم على عدة عوامل رئيسية تشمل:
- مستوى الأسعار مقارنة بمتوسط المدينة
- نشاط السوق العقاري وعدد الصفقات
- مؤشر قوة الحي الاستثماري (DPI)
"""
    report_sections.append(score_section)

    # =========================================
    # Investment Grade Rating
    # =========================================
    grade_section = ""
    try:
        if investment_score >= 85:
            grade = "A+"
            label = "فرصة استثمارية ممتازة"
        elif investment_score >= 75:
            grade = "A"
            label = "فرصة استثمارية قوية"
        elif investment_score >= 65:
            grade = "B+"
            label = "فرصة استثمارية جيدة"
        elif investment_score >= 55:
            grade = "B"
            label = "فرصة استثمارية متوسطة"
        elif investment_score >= 45:
            grade = "C"
            label = "فرصة استثمارية محدودة"
        else:
            grade = "D"
            label = "جاذبية استثمارية ضعيفة"
        grade_section = f"""

التصنيف الاستثماري للحي

التصنيف: {grade}
التقييم: {label}

يعتمد هذا التصنيف على تحليل شامل لمستوى الأسعار،
نشاط السوق العقاري، ومؤشر قوة الحي الاستثماري.
"""
    except Exception as e:
        print("Grade Error:", e)
    report_sections.append(grade_section)

    # =========================================
    # Market Position Percentile
    # =========================================
    position_section = ""
    try:
        if rank is not None and total is not None and total > 0:
            percentile = ((total - rank + 1) / total) * 100
            if percentile >= 80:
                tier = "ضمن أعلى 20% من الأحياء سعراً في المدينة"
            elif percentile >= 60:
                tier = "ضمن الشريحة السعرية المرتفعة"
            elif percentile >= 40:
                tier = "ضمن الشريحة السعرية المتوسطة"
            elif percentile >= 20:
                tier = "ضمن الشريحة السعرية المنخفضة"
            else:
                tier = "ضمن أقل 20% من الأحياء سعراً في المدينة"
            position_section = f"""

موقع الحي في الهيكل السعري للمدينة

يحتل حي {district} موقعاً {tier}
عند مقارنة متوسط الأسعار مع بقية أحياء مدينة {city}.
"""
    except Exception as e:
        print("Position Error:", e)
    report_sections.append(position_section)

    # =========================================
    # Market Liquidity Speed
    # =========================================
    if transactions >= 60:
        speed = "سوق سريع جداً"
        speed_text = "العقارات في هذا الحي غالباً ما تباع بسرعة بسبب الطلب المرتفع."
    elif transactions >= 30:
        speed = "سوق نشط"
        speed_text = "السوق يتمتع بحركة بيع وشراء جيدة مقارنة بعدد من الأحياء."
    elif transactions >= 15:
        speed = "سوق متوسط النشاط"
        speed_text = "السيولة متوسطة وقد تستغرق بعض الصفقات وقتاً أطول."
    else:
        speed = "سوق بطيء نسبياً"
        speed_text = "حجم الصفقات منخفض نسبياً مما قد يعني فترة بيع أطول."
    
    speed_section = f"""

سرعة السوق العقاري

تصنيف سرعة السوق: {speed}

{speed_text}
"""
    report_sections.append(speed_section)

    # =========================================
    # Market Heat Index
    # =========================================
    heat_section = ""
    try:
        heat_score = min(100, int(0.6 * dpi_score + 0.4 * min(transactions, 100)))
        if heat_score >= 80:
            heat_label = "شديد السخونة"
            heat_description = "نشاط مرتفع جداً، سرعة في تنفيذ الصفقات"
        elif heat_score >= 60:
            heat_label = "ساخن"
            heat_description = "سوق نشط، طلب جيد على العقارات"
        elif heat_score >= 40:
            heat_label = "دافئ"
            heat_description = "حركة متوسطة، فرص متاحة"
        else:
            heat_label = "هادئ"
            heat_description = "سوق هادئ، يحتاج إلى متابعة"
        heat_section = f"""

مؤشر حرارة السوق العقاري

درجة حرارة السوق: {heat_score} / 100
التصنيف: {heat_label}
الوصف: {heat_description}

يشير هذا المؤشر إلى مستوى النشاط والطلب في السوق العقاري
داخل الحي مقارنة ببقية أحياء المدينة.
"""
    except Exception as e:
        print("Narrative Engine Error (Heat):", e)
    if heat_section:
        report_sections.append(heat_section)

    # =========================================
    # What Smart Investors Do
    # =========================================
    smart_section = ""
    try:
        if price_ratio < 0.9 and transactions >= 15:
            smart_text = f"""
تشير البيانات إلى أن حي {district} قد يقدم فرصاً مناسبة
للمستثمرين الباحثين عن دخول السوق عند مستويات سعرية
أقل من متوسط المدينة.

قد يركز المستثمر الذكي في هذه الحالة على:

• شراء العقارات التي يقل سعرها عن متوسط سعر الحي
  لتحقيق هامش أمان أكبر.

• اختيار العقارات القريبة من الطرق الرئيسية أو الخدمات
  لضمان سيولة أعلى عند إعادة البيع.

• الاحتفاظ بالعقار لفترة تتراوح بين 3 إلى 5 سنوات
  للاستفادة من النمو المحتمل في الأسعار.
"""
        elif price_ratio > 1.1:
            smart_text = f"""
بما أن أسعار حي {district} أعلى من متوسط مدينة {city}،
فإن المستثمرين غالباً يركزون على العقارات المميزة داخل الحي.

الاستراتيجية الشائعة في هذه الحالة تشمل:

• اختيار مواقع متميزة داخل الحي ذات طلب مرتفع
  مثل العقارات القريبة من الحدائق أو المراكز التجارية.

• التركيز على العقارات ذات المواصفات العالية
  التي تحافظ على قيمتها حتى في فترات تراجع السوق.

• الاستثمار طويل الأجل بدلاً من المضاربة القصيرة،
  حيث أن العوائد تأتي من التملك وليس من التداول السريع.
"""
        else:
            smart_text = f"""
السوق في حي {district} يظهر حالة توازن نسبي بين الأسعار
والنشاط العقاري.

في هذه الحالة قد يركز المستثمرون على:

• اختيار العقارات ذات السعر المناسب مقارنة بالعقارات المشابهة
  في نفس الحي أو الأحياء المجاورة.

• متابعة تطور السوق خلال الفترات القادمة
  قبل اتخاذ قرارات استثمارية كبيرة.

• تنويع المحفظة العقارية بين عدة عقارات في الحي
  لتوزيع المخاطر وزيادة فرص العائد.
"""
        smart_section = f"""

ماذا يفعل المستثمر الذكي في هذا الحي
{smart_text}
"""
    except Exception as e:
        print("Narrative Engine Error (Smart):", e)
    if smart_section:
        report_sections.append(smart_section)

    # =========================================
    # Future Market Scenario
    # =========================================
    future_section = ""
    try:
        if price_ratio < 0.9 and transactions >= 15:
            optimistic = "قد تشهد الأسعار نمواً إضافياً يتراوح بين 8% و 15% خلال السنوات القادمة."
            balanced = "من المرجح أن يستمر السوق في مسار نمو تدريجي مع ارتفاعات معتدلة."
            pessimistic = "في حالة تباطؤ الطلب قد يحدث تصحيح محدود لا يتجاوز 5%."
        elif price_ratio > 1.1:
            optimistic = "قد تستمر الأسعار في الارتفاع ولكن بوتيرة أبطأ نظراً لوصول السوق إلى مستويات مرتفعة."
            balanced = "من المتوقع أن تتحرك الأسعار ضمن نطاق مستقر قريب من المستويات الحالية."
            pessimistic = "قد يحدث تصحيح سعري محدود إذا تراجع الطلب في السوق."
        else:
            optimistic = "قد يشهد الحي نمواً تدريجياً في الأسعار مع تحسن النشاط العقاري."
            balanced = "من المتوقع أن تبقى الأسعار ضمن نطاق مستقر خلال الفترة القادمة."
            pessimistic = "في حالة ضعف الطلب قد يحدث انخفاض طفيف في الأسعار."
        future_section = f"""

السيناريو المستقبلي للسوق العقاري

بناءً على المؤشرات الحالية في حي {district}
يمكن تصور ثلاثة سيناريوهات محتملة للسوق خلال السنوات القادمة.

السيناريو المتفائل:
{optimistic}

السيناريو المتوازن:
{balanced}

السيناريو المتحفظ:
{pessimistic}
"""
    except Exception as e:
        print("Narrative Engine Error (Future):", e)
    if future_section:
        report_sections.append(future_section)

    # =========================================
    # Investment Horizon
    # =========================================
    horizon_section = ""
    try:
        if price_ratio < 0.9 and transactions >= 15:
            horizon = "استثمار متوسط الأجل (3 إلى 5 سنوات)"
            horizon_text = "تسمح هذه الفترة للاستفادة من النمو المتوقع في الأسعار مع تجنب مخاطر التقلبات القصيرة."
        elif price_ratio > 1.1 and transactions >= 20:
            horizon = "استثمار طويل الأجل (5 إلى 10 سنوات)"
            horizon_text = "السوق وصل لمستويات سعرية مرتفعة، لذلك الأفق الطويل يساعد على تجاوز أي تصحيحات سعرية محتملة."
        elif transactions >= 30:
            horizon = "استثمار قصير إلى متوسط الأجل (1 إلى 4 سنوات)"
            horizon_text = "النشاط العالي في الحي يسمح بمرونة في إعادة البيع عند الحاجة."
        else:
            horizon = "استثمار متوسط إلى طويل الأجل (4 إلى 8 سنوات)"
            horizon_text = "هذا الأفق يمنح السوق وقتاً كافياً للنمو وتحقيق عوائد مناسبة."
        horizon_section = f"""

الأفق الاستثماري المقترح

بناءً على تحليل البيانات الحالية فإن الأفق الاستثماري الأنسب
في حي {district} هو:

{horizon}

{horizon_text}
"""
    except Exception as e:
        print("Narrative Engine Error (Horizon):", e)
    if horizon_section:
        report_sections.append(horizon_section)

    # =========================================
    # Investment Decision
    # =========================================
    decision_section = ""
    try:
        if price_ratio < 0.9 and transactions >= 20 and dpi_score >= 70:
            decision = "شراء"
            reasoning = f"""
البيانات تشير إلى أن حي {district} يوفر فرصة استثمارية جيدة حالياً.
السبب الرئيسي:
• سعر المتر أقل من متوسط المدينة
• نشاط السوق جيد ({transactions:,} صفقة)
• مؤشر قوة الحي مرتفع ({dpi_score}/100)

الاستراتيجية المقترحة:
شراء عقار بسعر قريب أو أقل من متوسط سعر الحي والاحتفاظ به لمدة 3 إلى 5 سنوات.
"""
        elif price_ratio > 1.15 and transactions < 20:
            decision = "الانتظار"
            reasoning = f"""
أسعار الحي مرتفعة مقارنة بمتوسط السوق مع نشاط محدود في عدد الصفقات.
في هذه الحالة قد يكون من الأفضل انتظار فرص شراء بأسعار أفضل.
"""
        else:
            decision = "شراء انتقائي"
            reasoning = f"""
السوق في حي {district} متوازن نسبياً.
يمكن الاستثمار بشرط اختيار عقار بسعر مناسب وموقع جيد داخل الحي.
"""
        decision_section = f"""

قرار الاستثمار

التوصية الأساسية: {decision}
درجة الثقة في القرار: {confidence}%

{reasoning}
"""
    except Exception as e:
        print("Decision Section Error:", e)
    report_sections.append(decision_section)

    # =========================================
    # Executive Decision Engine
    # =========================================
    try:
        executive_summary = generate_executive_summary(
            user_info=user_info,
            market_data=market_data,
            real_data=real_data,
            package="gold"
        )
        if executive_summary:
            executive_section = f"""

📊 القرار التنفيذي للاستثمار
{executive_summary}
"""
            report_sections.append(executive_section)
    except Exception as e:
        print("Executive Summary Error:", e)

    # =========================================
    # الحكم الاستثماري النهائي
    # =========================================
    if price_ratio < 0.9 and transactions >= 20 and dpi_score >= 70:
        verdict = "حي يتمتع بجاذبية استثمارية قوية"
        verdict_text = f"""
تشير المؤشرات العقارية إلى أن حي {district}
يتمتع بمقومات استثمارية قوية داخل سوق
مدينة {city}.

الأسعار في الحي أقل من متوسط السوق
مع وجود نشاط جيد في عدد الصفقات،
إضافة إلى مؤشر قوة حي مرتفع.

هذه العوامل مجتمعة قد تجعل الحي
مناسباً للمستثمرين الباحثين عن فرص
نمو رأسمالي في السوق العقاري.
"""
    elif dpi_score >= 60:
        verdict = "حي مستقر استثمارياً"
        verdict_text = f"""
يظهر حي {district} مستوى جيداً من
الاستقرار في السوق العقاري.

الأسعار تتحرك بالقرب من متوسط السوق
مع وجود نشاط مقبول في الصفقات،
مما يجعله خياراً مناسباً للمستثمرين
الباحثين عن استثمار مستقر نسبياً.
"""
    elif dpi_score >= 45:
        verdict = "حي استثماري متوسط"
        verdict_text = f"""
البيانات تشير إلى أن حي {district}
يقع ضمن الفئة المتوسطة من حيث
الجاذبية الاستثمارية داخل مدينة {city}.

في هذه الحالة يعتمد القرار الاستثماري
بشكل كبير على اختيار العقار المناسب
وموقعه داخل الحي.
"""
    else:
        verdict = "حي يحتاج إلى دراسة إضافية"
        verdict_text = f"""
تشير المؤشرات الحالية إلى أن
السوق العقاري في حي {district}
قد يحتاج إلى دراسة إضافية قبل
اتخاذ قرار استثماري.

قد يكون من المفيد مقارنة الحي
بأحياء أخرى داخل مدينة {city}
قبل اتخاذ القرار النهائي.
"""

    verdict_section = f"""

الخلاصة الاستثمارية

التقييم العام للحي:
{verdict}

{verdict_text}
"""
    report_sections.append(verdict_section)

    # =========================================
    # الفصل الثامن والعشرون - السيناريو المستقبلي للسوق العقاري
    # =========================================
    district_metrics = district_metrics or {}
    try:
        dpi_score = float(dpi_score or 0)
    except:
        dpi_score = 0
    transactions = int(
        district_metrics.get("transactions_count", 0) or 0
    )
    clean_district_base = locals().get(
        "clean_district_base", "الحي محل الدراسة"
    )

    # تحديد اتجاه السوق بناءً على DPI
    if dpi_score >= 80:
        outlook = "إيجابي"
    elif dpi_score >= 60:
        outlook = "مستقر"
    else:
        outlook = "حذر"

    section_28 = f"""السيناريو المستقبلي للسوق العقاري

تشير المؤشرات الحالية في حي {clean_district_base} إلى اتجاه {outlook} للسوق خلال السنوات القادمة.
يمكن تصور ثلاثة سيناريوهات محتملة:

السيناريو المتفائل:
قد تستمر الأسعار في الارتفاع بوتيرة أعلى إذا استمر الطلب في النمو وتحسنت مستويات السيولة العقارية داخل الحي.

السيناريو المتوازن:
من المتوقع أن تتحرك الأسعار ضمن نطاق مستقر قريب من المستويات الحالية مع استمرار النشاط العقاري دون تغيرات حادة.

السيناريو المتحفظ:
قد يحدث تصحيح سعري محدود إذا تراجع الطلب في السوق أو ارتفعت معدلات العرض بشكل ملحوظ.
"""
    report_sections.append(section_28)

    # =========================================
    # تجميع التقرير مع عناوين الفصول
    # =========================================
    chapter_names = [
        "الأول","الثاني","الثالث","الرابع","الخامس",
        "السادس","السابع","الثامن","التاسع","العاشر",
        "الحادي عشر","الثاني عشر","الثالث عشر","الرابع عشر","الخامس عشر",
        "السادس عشر","السابع عشر","الثامن عشر","التاسع عشر","العشرون",
        "الحادي والعشرون","الثاني والعشرون","الثالث والعشرون","الرابع والعشرون",
        "الخامس والعشرون","السادس والعشرون","السابع والعشرون","الثامن والعشرون",
        "التاسع والعشرون","الثلاثون"
    ]
    
    # بناء التقرير النهائي
    final_report = ""
    
    # إضافة فقرة المشاريع أولاً (بدون أي عنوان "فصل")
    final_report += projects_paragraph + "\n"
    
    # إضافة باقي الأقسام مع ترقيم الفصول
    for i, section in enumerate(report_sections, start=1):
        chapter_index = i
        chapter_title = (
            chapter_names[chapter_index - 1] if chapter_index <= len(chapter_names) else str(chapter_index)
        )
        final_report += f"الفصل {chapter_title}\n"
        
        # مواقع الرسومات
        if chapter_index == 4:
            final_report += "[[ANCHOR_CHART]]\n\n"
        elif chapter_index == 7:
            final_report += "[[ANCHOR_CHART]]\n\n"
        elif chapter_index == 11:
            final_report += "[[RHYTHM_CHART]]\n\n"
        elif chapter_index == 16:
            final_report += "[[ANCHOR_CHART]]\n\n"
        elif chapter_index == 21:
            final_report += "[[ANCHOR_CHART]]\n\n"
        
        if section.strip():
            final_report += section.strip()
        else:
            final_report += "لا توجد بيانات كافية لهذا التحليل."
        final_report += "\n"

    final_report += "\nWarda Intelligence\n"
    final_report += "منصة التحليل الاستثماري العقاري المعتمدة على بيانات الصفقات الفعلية في السوق.\n"

    return final_report
```
