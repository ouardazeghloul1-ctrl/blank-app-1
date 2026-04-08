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
from functools import lru_cache
import time

# =========================================
# ✅ Caching للبيانات (تحميل مرة واحدة لكل عملية)
# =========================================
@lru_cache(maxsize=1)
def get_districts_data():
    """
    تحميل بيانات الأحياء مع caching لتحسين الأداء في الإنتاج
    """
    print("🔄 تحميل بيانات الأحياء من المصدر (cached after first load)")
    return load_districts_data()


@lru_cache(maxsize=1)
def get_projects_data():
    """
    تحميل بيانات المشاريع مع caching لتحسين الأداء في الإنتاج
    """
    print("🔄 تحميل بيانات المشاريع من المصدر (cached after first load)")
    return load_projects_data()


# =========================================
# ✅ الحد الأقصى لعدد المشاريع المعروضة في التقرير
# =========================================
MAX_PROJECTS = 10


# =========================================
# ✅ دالة تطبيع النصوص (Unicode-safe) - معرفة مرة واحدة للاستخدام المتكرر
# =========================================
def normalize_text(text):
    """
    توحيد النصوص العربية لمقارنة آمنة ضد الاختلافات الإملائية والمسافات
    """
    if pd.isna(text):
        return ""
    text = str(text)
    # إزالة كلمة "حي" إذا وجدت في البداية أو النهاية
    text = text.replace("حي", "")
    # توحيد الألف الممدودة والمقصورة
    text = text.replace("أ", "ا")
    text = text.replace("إ", "ا")
    text = text.replace("آ", "ا")
    text = text.replace("ة", "ه")
    return text.strip().lower()


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
        real_data
):
    """
    إنشاء تقرير تحليلي احترافي لحي داخل مدينة
    يعتمد على بيانات الصفقات العقارية الفعلية
    """
    
    # ✅ تتبع زمن تنفيذ التقرير (performance tracking)
    start_time = time.time()

    # =========================================
    # ✅ التحسينات الأمنية الأساسية (حماية 100%)
    # =========================================
    
    # التحسين 1: حماية district_metrics من None
    district_metrics = district_metrics or {}
    
    # التحسين 2: حماية dpi_score من None
    dpi_score = float(dpi_score or 0)
    
    # التحسين 3: حماية user_info من None
    user_info = user_info or {}
    
    # =========================================
    # استخراج البيانات الأساسية
    # =========================================

    district = district_metrics.get("district_name", "غير محدد")
    city = district_metrics.get("city_name", "غير محدد")
    
    # ✅ حماية القيم الرقمية من None والنصوص
    district_price = float(district_metrics.get("district_avg_price", 0) or 0)
    city_price = float(district_metrics.get("city_avg_price", 0) or 0)
    
    # ✅ تحويل عدد الصفقات إلى integer بشكل آمن
    transactions = int(district_metrics.get("transactions_count", 0) or 0)
    
    # ✅ نوع العقار مع حماية كاملة
    property_type = user_info.get("property_type", "عقار")
    
    # ✅ توحيد تنظيف اسم الحي ليطابق طريقة تنظيف البيانات
    clean_district_base = str(district).split("/")[-1].strip()
    
    # تحويل نوع العقار إلى صيغة السوق (شقق / فلل)
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

    # حماية من القسمة على صفر
    if city_price > 0:
        price_ratio = district_price / city_price
    else:
        price_ratio = 1

    # =========================================
    # استخدام البيانات المحملة مع Caching (تحسين الأداء)
    # =========================================
    districts_df = get_districts_data()
    projects_df = get_projects_data()

    # ✅ تحسين تشخيصي: عرض عدد المشاريع المحملة
    if projects_df is not None:
        print(f"DEBUG projects loaded: {len(projects_df)} rows")

    # =========================================
    # ✅ جلب إحداثيات الحي الحالي (مع تطبيع النصوص Unicode-safe)
    # =========================================
    district_lat = None
    district_lon = None
    
    # ✅ تطبيع القيم المستهدفة (للاستخدام في البحث عن المشاريع أيضاً)
    target_city = normalize_text(city)
    target_district = normalize_text(clean_district_base)
    
    try:
        if districts_df is not None and not districts_df.empty:
            # ✅ منع SettingWithCopyWarning
            districts_df = districts_df.copy()
            
            # ✅ إضافة أعمدة normalized للتطابق الآمن
            districts_df["normalized_district"] = districts_df["اسم الحي"].apply(normalize_text)
            districts_df["normalized_city"] = districts_df["المدينة"].apply(normalize_text)
            
            # ✅ سطر تشخيصي للتأكد من الأعمدة
            print("DEBUG columns:", districts_df.columns.tolist())
            print(f"🔍 Target normalized: city='{target_city}', district='{target_district}'")
            
            # ✅ البحث باستخدام الأعمدة المقيسة
            match = districts_df[
                (districts_df["normalized_city"] == target_city) &
                (districts_df["normalized_district"] == target_district)
            ]
            
            if not match.empty:
                # ✅ تحويل الإحداثيات إلى float بشكل آمن
                district_lat = float(match.iloc[0]["خط_العرض"])
                district_lon = float(match.iloc[0]["خط_الطول"])
                print(f"📍 تم العثور على إحداثيات الحي {clean_district_base}: {district_lat}, {district_lon}")
            else:
                print(f"⚠️ لم يتم العثور على إحداثيات للحي {clean_district_base}")
                # عرض الأسماء المقيسة المتاحة للتشخيص
                print(f"   متاح normalized districts: {districts_df['normalized_district'].unique()[:10]}")
    except Exception as e:
        print("خطأ في جلب إحداثيات الحي:", e)
        import traceback
        traceback.print_exc()

    # =========================================
    # ✅ حساب المشاريع القريبة (مع جميع تحسينات الإنتاج)
    # =========================================
    nearby_projects = []
    try:
        # ✅ حماية NaN للإحداثيات (ليست فقط None)
        if (not pd.isna(district_lat) and not pd.isna(district_lon) and
            projects_df is not None and not projects_df.empty):
            
            print(f"🔍 جاري البحث عن مشاريع قريبة من {clean_district_base}...")
            
            # ✅ تحسين الأداء: حفظ reference للدالة
            normalize = normalize_text
            
            # ✅ استخدام itertuples بدلاً من iterrows لتحسين الأداء
            for row in projects_df.itertuples(index=False):
                # الوصول للحقول باستخدام النقطة (أسرع)
                project_city = getattr(row, "المدينة", None)
                
                # ✅ تطبيق Unicode-safe على مقارنة المدينة
                if normalize(project_city) != target_city:
                    continue
                
                project_lat = getattr(row, "خط_العرض", None)
                project_lon = getattr(row, "خط_الطول", None)
                
                # ✅ حماية NaN (ليست فقط None)
                if pd.isna(project_lat) or pd.isna(project_lon):
                    continue
                
                # ✅ حماية الإحداثيات من القيم الخارجة عن النطاق الطبيعي
                try:
                    lat = float(project_lat)
                    lon = float(project_lon)
                    if not (-90 <= lat <= 90):
                        continue
                    if not (-180 <= lon <= 180):
                        continue
                except (ValueError, TypeError):
                    continue
                
                # تحويل الإحداثيات إلى float لضمان الحساب الصحيح
                distance = calculate_distance(
                    float(district_lat),
                    float(district_lon),
                    lat,
                    lon
                )
                
                if distance is None:
                    continue
                
                # ✅ حماية impact_radius من القيم غير الصالحة (NaN, '', text, negative)
                raw_radius = getattr(row, "نطاق_التأثير", 2)
                try:
                    impact_radius = float(raw_radius)
                    if impact_radius <= 0:
                        impact_radius = 2
                except (ValueError, TypeError):
                    impact_radius = 2
                
                if distance <= impact_radius:
                    nearby_projects.append({
                        "type": getattr(row, "النوع", "غير محدد"),
                        "status": getattr(row, "الحالة", "غير محدد"),
                        "distance": distance,
                        "lat": lat,
                        "lon": lon
                    })
            
            # ترتيب المشاريع حسب الأقرب
            nearby_projects.sort(key=lambda x: x["distance"])
            
            # ✅ تطبيق الحد الأقصى لعدد المشاريع المعروضة
            nearby_projects = nearby_projects[:MAX_PROJECTS]
            
            # ✅ إضافة log مطابق للواقع (لا يذكر radius ثابت)
            print(f"Map: found {len(nearby_projects)} nearby projects within impact radius")
            
    except Exception as e:
        print("خطأ في حساب المشاريع القريبة:", e)
        import traceback
        traceback.print_exc()

    # ✅ performance tracking: عرض زمن تنفيذ التقرير
    elapsed_time = time.time() - start_time
    print(f"⏱️ تقرير {district} تم إنشاؤه في {elapsed_time:.2f} ثانية")

    # =========================================
    # تهيئة متغيرات التقرير
    # =========================================

    report_sections = []

    # =========================================
    # Investment Intelligence Score (محسوب مسبقاً للاستخدام)
    # =========================================
    try:
        # حساب نقاط السعر
        price_score = 50
        if price_ratio < 0.85:
            price_score = 85
        elif price_ratio < 0.95:
            price_score = 70
        elif price_ratio <= 1.05:
            price_score = 60
        elif price_ratio <= 1.15:
            price_score = 50
        else:
            price_score = 40

        # حساب نقاط السيولة
        if transactions >= 40:
            liquidity_score = 90
        elif transactions >= 25:
            liquidity_score = 75
        elif transactions >= 15:
            liquidity_score = 60
        elif transactions >= 8:
            liquidity_score = 45
        else:
            liquidity_score = 30

        # حساب النتيجة النهائية
        investment_score = (
            price_score * 0.30 +
            liquidity_score * 0.30 +
            dpi_score * 0.40
        )
        investment_score = round(investment_score, 1)
        
        # Confidence محسّن
        confidence = int(0.7 * dpi_score + 0.3 * min(transactions, 60))
        confidence = min(95, max(30, confidence))
        
    except Exception as e:
        print("Error calculating scores:", e)
        investment_score = 50
        confidence = 50

    # =========================================
    # Investment Snapshot
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
    
    # =========================================
    # المشاريع القريبة من الحي (مع الإحداثيات للخرائط)
    # =========================================
    projects_section = ""
    if nearby_projects:
        lines = ""
        # تخزين المشاريع والإحداثيات لاستخدامها في الخريطة لاحقاً
        user_info["nearby_projects"] = nearby_projects
        # التحقق الاحترافي من الإحداثيات (باستثناء None)
        if district_lat is not None:
            user_info["district_lat"] = float(district_lat)
        else:
            user_info["district_lat"] = None
            
        if district_lon is not None:
            user_info["district_lon"] = float(district_lon)
        else:
            user_info["district_lon"] = None
        
        for p in nearby_projects:
            lines += (
                f"• {p['type']} "
                f"({p['status']}) "
                f"على بعد {p['distance']} كم\n"
            )
        projects_section = f"""

المشاريع التنموية القريبة من الحي

تشير البيانات إلى وجود عدد من المشاريع التنموية المؤثرة بالقرب من حي {district}.

{lines}

وجود هذه المشاريع قد يساهم في رفع الطلب العقاري وتحسين جاذبية الحي للمستثمرين خلال السنوات القادمة.
"""
    else:
        projects_section = f"""

المشاريع التنموية القريبة من الحي

لا توجد حالياً مشاريع مؤثرة ضمن نطاق التأثير المحدد حول حي {district}.
"""
    report_sections.append(projects_section)

    # =========================================
    # ✅ جدول المشاريع القريبة من الحي (تمت الإضافة هنا)
    # =========================================
    projects_table_section = ""
    if nearby_projects:
        table_lines = ""
        for i, p in enumerate(nearby_projects, start=1):
            # تحديد مستوى التأثير حسب المسافة
            distance = p.get("distance", 0)
            if distance <= 1:
                impact_level = "تأثير عالي"
            elif distance <= 2:
                impact_level = "تأثير متوسط"
            else:
                impact_level = "تأثير محدود"
            
            table_lines += (
                f"{i}. "
                f"{p.get('type', 'غير محدد')} — "
                f"{p.get('status', 'غير محدد')} — "
                f"{distance} كم — "
                f"{impact_level}\n"
            )
        projects_table_section = f"""

جدول المشاريع التنموية القريبة من الحي

عدد المشاريع المؤثرة: {len(nearby_projects)}

{table_lines}

يعرض هذا الجدول المشاريع الواقعة ضمن نطاق التأثير الجغرافي للحي مرتبة حسب القرب من الموقع.
"""
    else:
        projects_table_section = f"""

جدول المشاريع التنموية القريبة من الحي

لا توجد حالياً مشاريع ضمن نطاق التأثير المحدد حول الحي.
"""
    report_sections.append(projects_table_section)
    
    # ملخص تنفيذي محسن
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
    # منهجية التحليل (مصدر البيانات)
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
            if gap > 0:
                relation = "أعلى"
            else:
                relation = "أقل"
            
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
    if city_price > 0:
        price_diff_percent = ((district_price - city_price) / city_price) * 100
    else:
        price_diff_percent = 0
    
    benchmark_section = f"""

مقارنة الحي مع متوسط السوق

متوسط سعر المتر في الحي: {district_price:,.0f} ريال
متوسط سعر المتر في المدينة: {city_price:,.0f} ريال

الفارق: {price_diff_percent:.1f}%

هذا المؤشر يساعد المستثمر على فهم ما إذا كان الحي يتداول عند خصم سعري أو بعلاوة سعرية مقارنة بالسوق.
"""
    report_sections.append(benchmark_section)

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

            if district_price > 0:
                diff = ((price - district_price) / district_price) * 100
            else:
                diff = 0

            if diff > 0:
                relation = "أعلى"
            elif diff < 0:
                relation = "أقل"
            else:
                relation = "مساوٍ"

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

    # مخاطر السيولة
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

    # مخاطر السعر
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
    # استراتيجية الاستثمار في الحي
    # =========================================
    strategy_section = ""
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
    growth_section = ""
    
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
    # مؤشر حرارة السوق العقاري
    # =========================================

    heat_section = ""
    try:
        heat_score = int(0.6 * dpi_score + 0.4 * min(transactions, 100))
        heat_score = min(100, heat_score)
        
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
        heat_section = ""

    if heat_section:
        report_sections.append(heat_section)

    # =========================================
    # ماذا يفعل المستثمر الذكي في هذا الحي
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
        smart_section = ""

    if smart_section:
        report_sections.append(smart_section)

    # =========================================
    # السيناريو المستقبلي للسوق العقاري
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
        future_section = ""

    if future_section:
        report_sections.append(future_section)

    # =========================================
    # الأفق الاستثماري المقترح
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
        horizon_section = ""

    if horizon_section:
        report_sections.append(horizon_section)

    # =========================================
    # قرار الاستثمار
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
    
    # الفصول التي تحتوي الرسومات
    chart_chapters = [4,7,11,16,21,24,28]
    
    final_report = ""
    for i, section in enumerate(report_sections, start=1):
        chapter_title = chapter_names[i-1] if i <= len(chapter_names) else str(i)
        final_report += f"الفصل {chapter_title}\n"
        
        if i in chart_chapters:
            final_report += "[[ANCHOR_CHART]]\n\n"
        
        if section.strip():
            final_report += section.strip()
        else:
            final_report += "لا توجد بيانات كافية لهذا التحليل."
        final_report += "\n"

    final_report += "\nWarda Intelligence\n"
    final_report += "منصة التحليل الاستثماري العقاري المعتمدة على بيانات الصفقات الفعلية في السوق.\n"

    return final_report
