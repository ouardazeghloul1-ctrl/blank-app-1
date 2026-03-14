# =========================================
# Warda Intelligence
# District Narrative Engine
# محرك التقرير الاستثماري للأحياء
# =========================================

import pandas as pd

# =========================================
# Data Schema (أسماء الأعمدة القياسية)
# =========================================
# تعتمد المنصة على الأعمدة التالية في بيانات الصفقات:
#
# city     : اسم المدينة
# district : اسم الحي بصيغة "المدينة/الحي"
# price    : سعر الصفقة
# area     : مساحة العقار بالمتر
# property_type : نوع العقار (شقة / فيلا / أرض ...)
# date     : تاريخ الصفقة بصيغة YYYY-MM-DD
#
# مثال:
# city = الرياض
# district = الرياض/الصفاء


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

    # =========================================
    # استخراج البيانات الأساسية
    # =========================================

    district = district_metrics.get("district_name", "غير محدد")
    city = district_metrics.get("city_name", "غير محدد")
    
    # إضافة نوع العقار من user_info
    property_type = user_info.get("property_type", "عقار")
    
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

    district_price = district_metrics.get("district_avg_price", 0)
    city_price = district_metrics.get("city_avg_price", 0)

    transactions = district_metrics.get("transactions_count", 0)

    # حماية من القسمة على صفر
    if city_price > 0:
        price_ratio = district_price / city_price
    else:
        price_ratio = 1

    # =========================================
    # تهيئة متغيرات التقرير
    # =========================================

    report_sections = []
    
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

--------------------------------------------------

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
--------------------------------------------------

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
--------------------------------------------------

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
--------------------------------------------------

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
    # Price Ranking داخل المدينة
    # =========================================
    price_rank_section = ""
    rank = None
    total = None
    try:
        if real_data is not None and "district" in real_data.columns:
            # فلترة بيانات المدينة فقط
            df_city = real_data[
                real_data["district"]
                .astype(str)
                .str.strip()
                .str.startswith(city)
            ].copy()
            
            # التأكد من وجود بيانات بعد الفلترة
            if len(df_city) > 0:
                # تنظيف أسماء الأحياء
                df_city["district_clean"] = (
                    df_city["district"]
                    .astype(str)
                    .str.split("/")
                    .str[-1]
                    .str.strip()
                )
                
                # تحويل price إلى أرقام
                df_city["price"] = pd.to_numeric(df_city["price"], errors="coerce")
                
                # ✅ تنظيف المساحة قبل حساب سعر المتر
                df_city["area"] = pd.to_numeric(df_city["area"], errors="coerce")
                df_city = df_city[df_city["area"] > 0]
                df_city["price_sqm"] = df_city["price"] / df_city["area"]
                
                # ✅ إزالة القيم الفارغة قبل الترتيب
                df_city = df_city[df_city["price_sqm"].notna()]
                
                # استخدام median بدلاً من mean لتجنب تأثير الصفقات الشاذة
                district_prices = df_city.groupby("district_clean")["price_sqm"].median()
                # ✅ إزالة الأحياء التي ليس لديها بيانات صالحة
                district_prices = district_prices.dropna()
                district_prices = district_prices.sort_values()
                
                # الحصول على ترتيب الحي الحالي
                clean_district = str(district).strip()
                if clean_district in district_prices.index:
                    rank = list(district_prices.index).index(clean_district) + 1
                    total = len(district_prices)
                    # تصحيح percentile: المرتبة 1 = 100%
                    percentile = ((total - rank + 1) / total) * 100
                    
                    # ✅ التعديل الصحيح: استخدام >= لأن المرتبة 1 = 100%
                    if percentile >= 80:
                        label = "ضمن أعلى 20% من الأحياء سعراً في المدينة"
                    elif percentile >= 50:
                        label = "ضمن الشريحة السعرية المتوسطة"
                    else:
                        label = "ضمن الشريحة السعرية الاقتصادية"
                    
                    price_rank_section = f"""
--------------------------------------------------

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
        if real_data is not None and "district" in real_data.columns:
            # تنظيف أسماء الأحياء لمدينة فقط
            clean_districts = (
                real_data[
                    real_data["district"]
                    .astype(str)
                    .str.strip()
                    .str.startswith(city)
                ]["district"]
                .astype(str)
                .str.split("/")
                .str[-1]
                .str.strip()
            )
            
            # حساب عدد الصفقات لكل حي مع الترتيب
            district_counts = clean_districts.value_counts().sort_values(ascending=False)
            
            # الحصول على ترتيب الحي الحالي
            clean_district = str(district).strip()
            if clean_district in district_counts.index:
                rank_l = list(district_counts.index).index(clean_district) + 1
                total_l = len(district_counts)
                
                liquidity_rank_section = f"""
--------------------------------------------------

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
--------------------------------------------------

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
        if real_data is not None and hasattr(real_data, "columns") and "district" in real_data.columns:
            # تنظيف أسماء الأحياء قبل حساب التكرارات
            clean_districts = real_data["district"].astype(str).str.split("/").str[-1].str.strip()
            district_counts = clean_districts.value_counts()
            total_districts = len(district_counts)
            
            # تنظيف اسم الحي للمقارنة
            clean_district = str(district).strip()
            
            if clean_district in district_counts.index:
                # طريقة أكثر أماناً للحصول على الترتيب
                district_rank = list(district_counts.index).index(clean_district) + 1
                district_transactions = district_counts[clean_district]
                
                if district_rank <= 5:
                    rank_label = "ضمن الأحياء الأكثر نشاطاً في المدينة"
                elif district_rank <= 15:
                    rank_label = "ضمن الأحياء النشطة في السوق العقاري"
                else:
                    rank_label = "ضمن الأحياء الأقل نشاطاً نسبياً"
                    
                ranking_section = f"""
--------------------------------------------------

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
        ranking_section = ""

    # إضافة القسم بدون شرط
    report_sections.append(ranking_section)

    # =========================================
    # الأحياء الأكثر نشاطاً في المدينة (TOP 5)
    # =========================================

    top_districts_section = ""
    try:
        if real_data is not None and "district" in real_data.columns:
            # تنظيف أسماء الأحياء لمدينة فقط مع strip
            clean_districts = (
                real_data[
                    real_data["district"]
                    .astype(str)
                    .str.strip()
                    .str.startswith(city)
                ]["district"]
                .astype(str)
                .str.split("/")
                .str[-1]
                .str.strip()
            )
            
            # حساب عدد الصفقات لكل حي وأخذ أول 5
            district_counts = clean_districts.value_counts().sort_values(ascending=False)
            top_districts = district_counts.head(5)
            
            # بناء نص الجدول
            lines = ""
            for i, (name, count) in enumerate(top_districts.items(), start=1):
                lines += f"{i}. {name} — {count:,} صفقة\n"
            
            top_districts_section = f"""
--------------------------------------------------

الأحياء الأكثر نشاطاً في السوق العقاري

بحسب تحليل بيانات الصفقات العقارية في مدينة {city}،
تظهر الأحياء التالية كأكثر المناطق نشاطاً في السوق:

{lines}
"""
    except Exception as e:
        print("Top Districts Error:", e)
        top_districts_section = ""

    # إضافة القسم
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
--------------------------------------------------

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
            price = d.get("avg_price", 0)

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
--------------------------------------------------

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
--------------------------------------------------

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
        if real_data is not None and hasattr(real_data, "columns") and "date" in real_data.columns:
            # تنظيف اسم الحي أثناء الفلترة
            df = real_data[ 
                real_data["district"]
                .astype(str)
                .str.split("/")
                .str[-1]
                .str.strip()
                .str.lower() == str(district).strip().lower()
            ].copy()
            
            # تحسين الأداء 1: استخدام subset محدد لـ drop_duplicates
            df = df.drop_duplicates(subset=["price", "area", "date"])
            
            # تحسين معالجة التاريخ
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df = df[df["date"].notna()]
            
            # تحويل القيم الرقمية
            df["price"] = pd.to_numeric(df["price"], errors="coerce")
            
            # ✅ تنظيف المساحة قبل حساب سعر المتر
            df["area"] = pd.to_numeric(df["area"], errors="coerce")
            df = df[df["area"] > 0]
            df["price_per_sqm"] = df["price"] / df["area"]
            
            # ✅ إزالة القيم الفارغة بعد الحساب
            df = df[df["price_per_sqm"].notna()]
            
            df = df.sort_values("date")
            
            # استخدام التقسيم الزمني بدلاً من التقسيم النصفي
            if len(df) >= 2:
                midpoint_date = df["date"].median()
                first_period = df[df["date"] <= midpoint_date]
                last_period = df[df["date"] > midpoint_date]
                
                if not first_period.empty and not last_period.empty:
                    first_price = first_period["price_per_sqm"].mean()
                    last_price = last_period["price_per_sqm"].mean()
                    
                    # منع القسمة على صفر في حساب التغير
                    if first_price > 0:
                        change = ((last_price - first_price) / first_price) * 100
                    else:
                        change = 0
                    
                    if change > 3:
                        trend = "اتجاه صعودي"
                    elif change < -3:
                        trend = "اتجاه هبوطي"
                    else:
                        trend = "استقرار نسبي"
                        
                    trend_section = f"""
--------------------------------------------------

اتجاه السوق داخل الفترة المدروسة

بمقارنة الصفقات الأولى مع أحدث الصفقات في حي {district}
يظهر أن متوسط سعر المتر تغير بنسبة {change:.1f}%.

هذا يشير إلى {trend} في السوق العقاري داخل الحي
خلال الفترة المتاحة من البيانات.
"""
    except Exception as e:
        print("Narrative Engine Error (Trend):", e)
        trend_section = ""

    # إضافة القسم بدون شرط
    report_sections.append(trend_section)

    # =========================================
    # Market Cycle Detection
    # =========================================
    cycle_section = ""
    try:
        if real_data is not None and "date" in real_data.columns:
            df = real_data.copy()
            
            # تنظيف اسم الحي
            df["district_clean"] = (
                df["district"]
                .astype(str)
                .str.split("/")
                .str[-1]
                .str.strip()
            )
            
            # فلترة الحي
            df = df[
                df["district_clean"].str.lower() == str(district).strip().lower()
            ]
            
            # تحويل التاريخ
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df = df[df["date"].notna()]
            
            # تحويل القيم الرقمية
            df["price"] = pd.to_numeric(df["price"], errors="coerce")
            
            # ✅ تنظيف المساحة قبل حساب سعر المتر
            df["area"] = pd.to_numeric(df["area"], errors="coerce")
            df = df[df["area"] > 0]
            df["price_sqm"] = df["price"] / df["area"]
            
            # ✅ إزالة القيم الفارغة بعد الحساب
            df = df[df["price_sqm"].notna()]
            
            # استخراج السنة
            df["year"] = df["date"].dt.year
            # استخدام median بدلاً من mean لتجنب تأثير الصفقات الشاذة
            yearly_prices = df.groupby("year")["price_sqm"].median()
            
            if len(yearly_prices) >= 2:
                first_price = yearly_prices.iloc[0]
                last_price = yearly_prices.iloc[-1]
                
                if first_price > 0:
                    change = ((last_price - first_price) / first_price) * 100
                else:
                    change = 0
                
                if change > 8:
                    cycle = "مرحلة نمو في السوق العقاري"
                    explanation = "تشير البيانات إلى ارتفاع واضح في متوسط أسعار المتر خلال السنوات الأخيرة."
                elif change < -5:
                    cycle = "مرحلة تصحيح سعري"
                    explanation = "تشير البيانات إلى تراجع في متوسط الأسعار خلال الفترة المدروسة."
                else:
                    cycle = "مرحلة استقرار في السوق"
                    explanation = "الأسعار تتحرك ضمن نطاق مستقر دون تغيرات كبيرة."
                
                cycle_section = f"""
--------------------------------------------------

دورة السوق العقاري

بناءً على تحليل تطور أسعار المتر عبر السنوات،
يبدو أن السوق في حي {district} يمر حالياً بـ:

{cycle}

{explanation}
"""
    except Exception as e:
        print("Market Cycle Error:", e)
    
    report_sections.append(cycle_section)

    # =========================================
    # Investment Intelligence Score
    # =========================================

    score_section = ""
    try:
        # ------------------------------
        # حساب نقاط السعر
        # ------------------------------
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

        # ------------------------------
        # حساب نقاط السيولة
        # ------------------------------
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

        # ------------------------------
        # قوة الحي
        # ------------------------------
        dpi_component = dpi_score

        # ------------------------------
        # حساب النتيجة النهائية
        # ------------------------------
        investment_score = (
            price_score * 0.30 +
            liquidity_score * 0.30 +
            dpi_component * 0.40
        )
        investment_score = round(investment_score, 1)

        score_section = f"""
--------------------------------------------------

Investment Intelligence Score
التقييم الكلي لجاذبية الاستثمار في الحي

النتيجة النهائية: {investment_score} / 100

يعتمد هذا التقييم على عدة عوامل رئيسية تشمل:
- مستوى الأسعار مقارنة بمتوسط المدينة
- نشاط السوق العقاري وعدد الصفقات
- مؤشر قوة الحي الاستثماري (DPI)
"""
    except Exception as e:
        print("Narrative Engine Error (Score):", e)
        score_section = ""

    if score_section:
        report_sections.append(score_section)

    # =========================================
    # Investment Grade Rating
    # =========================================
    grade_section = ""
    try:
        # استخدام locals().get للحماية من الأخطاء
        score = locals().get("investment_score", 0)
        if score >= 85:
            grade = "A+"
            label = "فرصة استثمارية ممتازة"
        elif score >= 75:
            grade = "A"
            label = "فرصة استثمارية قوية"
        elif score >= 65:
            grade = "B+"
            label = "فرصة استثمارية جيدة"
        elif score >= 55:
            grade = "B"
            label = "فرصة استثمارية متوسطة"
        elif score >= 45:
            grade = "C"
            label = "فرصة استثمارية محدودة"
        else:
            grade = "D"
            label = "جاذبية استثمارية ضعيفة"
        
        grade_section = f"""
--------------------------------------------------

Investment Grade Rating
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
        if 'rank' in locals() and rank is not None and total is not None:
            # استخدام الصيغة المحسنة: المرتبة 1 = 100%
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
--------------------------------------------------

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
    speed_section = ""
    try:
        if transactions >= 60:
            speed = "سوق سريع جداً"
            text = "العقارات في هذا الحي غالباً ما تباع بسرعة بسبب الطلب المرتفع."
        elif transactions >= 30:
            speed = "سوق نشط"
            text = "السوق يتمتع بحركة بيع وشراء جيدة مقارنة بعدد من الأحياء."
        elif transactions >= 15:
            speed = "سوق متوسط النشاط"
            text = "السيولة متوسطة وقد تستغرق بعض الصفقات وقتاً أطول."
        else:
            speed = "سوق بطيء نسبياً"
            text = "حجم الصفقات منخفض نسبياً مما قد يعني فترة بيع أطول."
        
        speed_section = f"""
--------------------------------------------------

سرعة السوق العقاري

تصنيف سرعة السوق: {speed}

{text}
"""
    except Exception as e:
        print("Speed Error:", e)
    
    report_sections.append(speed_section)

    # =========================================
    # Market Heat Index (محسن)
    # =========================================

    heat_section = ""
    try:
        # ✅ حساب مؤشر حرارة السوق مع حد أقصى 60 صفقة لمنع التشبع
        heat_score = min(100, int((min(transactions, 60) / 60 * 50) + (dpi_score * 0.5)))
        
        if heat_score >= 80:
            heat_label = "سوق شديد السخونة"
        elif heat_score >= 60:
            heat_label = "سوق ساخن"
        elif heat_score >= 40:
            heat_label = "سوق دافئ"
        else:
            heat_label = "سوق هادئ"
            
        heat_section = f"""
--------------------------------------------------

مؤشر حرارة السوق العقاري

درجة حرارة السوق: {heat_score} / 100
التصنيف: {heat_label}

يشير هذا المؤشر إلى مستوى النشاط والطلب في السوق العقاري
داخل الحي مقارنة ببقية أحياء المدينة.

القيم المرتفعة تعني سوقاً نشطاً وسرعة أكبر في تنفيذ الصفقات.
"""
    except Exception as e:
        print("Narrative Engine Error (Heat):", e)
        heat_section = ""

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
--------------------------------------------------

ماذا يفعل المستثمر الذكي في هذا الحي
{smart_text}
"""
    except Exception as e:
        print("Narrative Engine Error (Smart):", e)
        smart_section = ""

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
--------------------------------------------------

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
--------------------------------------------------

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
    # Investment Decision (قرار الاستثمار المباشر)
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
--------------------------------------------------

قرار الاستثمار

التوصية الأساسية: {decision}

{reasoning}
"""
    except Exception as e:
        print("Decision Section Error:", e)
    
    report_sections.append(decision_section)

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
--------------------------------------------------

الخلاصة الاستثمارية

التقييم العام للحي:
{verdict}

{verdict_text}
"""

    report_sections.append(verdict_section)

    # =========================================
    # ✅ تجميع التقرير مع عناوين الفصول بالكلمات العربية وإدراج الرسومات
    # =========================================

    chapter_names = [
        "الأول","الثاني","الثالث","الرابع","الخامس",
        "السادس","السابع","الثامن","التاسع","العاشر",
        "الحادي عشر","الثاني عشر","الثالث عشر","الرابع عشر","الخامس عشر",
        "السادس عشر","السابع عشر","الثامن عشر","التاسع عشر","العشرون",
        "الحادي والعشرون","الثاني والعشرون","الثالث والعشرون","الرابع والعشرون"
    ]
    
    # الفصول التي تحتوي الرسومات
    chart_chapters = [4,7,11,16,21]
    
    final_report = ""
    for i, section in enumerate(report_sections, start=1):
        chapter_title = chapter_names[i-1] if i <= len(chapter_names) else str(i)
        final_report += f"الفصل {chapter_title}\n"
        final_report += "-" * 40 + "\n\n"
        
        # إدراج الرسم في الفصول المحددة - بالضبط بدون مسافات إضافية
        if i in chart_chapters:
            final_report += "[[ANCHOR_CHART]]\n\n"
        
        if section.strip():
            final_report += section.strip()
        else:
            final_report += "لا توجد بيانات كافية لهذا التحليل."
        final_report += "\n\n"

    final_report += """
--------------------------------------------------
Warda Intelligence
منصة التحليل الاستثماري العقاري المعتمدة على بيانات الصفقات الفعلية في السوق.
"""

    return final_report
