# =========================================
# Warda Intelligence
# District Narrative Engine
# =========================================

def generate_district_narrative(
        user_info,
        district_metrics,
        nearby_districts,
        dpi_score,
        market_data,
        real_data
):

    district = district_metrics.get("district_name", "غير محدد")
    city = district_metrics.get("city_name", "غير محدد")

    district_price = district_metrics.get("district_avg_price", 0)
    city_price = district_metrics.get("city_avg_price", 0)

    deviation = district_metrics.get("price_deviation_percent", 0)
    transactions = district_metrics.get("transactions_count", 0)

    # تنسيق الأرقام
    district_price_display = f"{district_price:,.0f}"
    city_price_display = f"{city_price:,.0f}"
    transactions_display = f"{transactions:,}"
    dpi_display = f"{dpi_score:.0f}"

    # =========================================
    # تحليل موقع السعر داخل السوق
    # =========================================

    if deviation > 10:
        price_position = "أعلى بكثير من متوسط المدينة"
    elif deviation > 3:
        price_position = "أعلى من متوسط المدينة"
    elif deviation < -10:
        price_position = "أقل بكثير من متوسط المدينة"
    elif deviation < -3:
        price_position = "أقل من متوسط المدينة"
    else:
        price_position = "قريب من متوسط المدينة"

    # =========================================
    # تصنيف البيئة الاستثمارية
    # =========================================

    if dpi_score >= 75:
        investment_env = "بيئة استثمارية قوية"
    elif dpi_score >= 60:
        investment_env = "بيئة استثمارية مستقرة"
    elif dpi_score >= 45:
        investment_env = "بيئة استثمارية متوسطة"
    else:
        investment_env = "بيئة استثمارية ضعيفة"

    # =========================================
    # تحليل السيولة
    # =========================================

    if transactions >= 30:
        liquidity_level = "سيولة مرتفعة"
    elif transactions >= 15:
        liquidity_level = "سيولة جيدة"
    elif transactions >= 8:
        liquidity_level = "سيولة متوسطة"
    else:
        liquidity_level = "سيولة محدودة"

    # =========================================
    # تحليل الأحياء المجاورة
    # =========================================

    comparison_text = ""

    if nearby_districts:

        for d in nearby_districts:

            name = d.get("district_name", "")
            price = d.get("avg_price", 0)

            diff = ((price - district_price) / district_price) * 100 if district_price else 0

            comparison_text += f"{name} بمتوسط {price:,.0f} ريال للمتر (فرق {diff:.1f}%)\n"

    else:

        comparison_text = "لا توجد بيانات كافية لمقارنة الأحياء المجاورة حالياً."

    # =========================================
    # Market Overview
    # =========================================

    market_overview = f"""
يظهر تحليل بيانات الصفقات العقارية أن حي {district} في مدينة {city}
سجل {transactions_display} صفقة عقارية خلال الفترة محل الدراسة.

يبلغ متوسط سعر المتر في الحي نحو {district_price_display} ريال،
مقارنة بمتوسط المدينة البالغ {city_price_display} ريال،
ما يعني أن أسعار الحي تقع {price_position}.

هذا المستوى السعري يعكس موقع الحي داخل السوق العقاري للمدينة
ويشير إلى طبيعة الطلب على العقارات داخل المنطقة.
"""

    # =========================================
    # Liquidity Analysis
    # =========================================

    liquidity_analysis = f"""
يظهر نشاط التداول في حي {district} مستوى سيولة يصنف كـ {liquidity_level}،
حيث بلغ عدد الصفقات المنفذة {transactions_display} صفقة.

حجم التداول يعد مؤشراً مهماً على قدرة السوق
على استيعاب عمليات البيع والشراء،
كما يعكس مستوى اهتمام المشترين والمستثمرين بالحي.
"""

    # =========================================
    # Price Positioning
    # =========================================

    price_positioning = f"""
بمقارنة أسعار حي {district} مع متوسط أسعار مدينة {city}،
يظهر أن الحي يقع {price_position}.

هذا الفارق السعري قد يعكس عدة عوامل
من بينها الموقع الجغرافي للحي،
مستوى الخدمات والبنية التحتية،
إضافة إلى طبيعة الطلب على العقارات داخل المنطقة.
"""

    # =========================================
    # Risk Analysis
    # =========================================

    risk_analysis = f"""
تحليل المخاطر الاستثمارية في حي {district}
يشير إلى أن السوق يتمتع بدرجة استقرار مرتبطة
بحجم النشاط العقاري ومستوى الأسعار.

ففي الأسواق ذات السيولة المرتفعة
تكون مخاطر الخروج من الاستثمار أقل نسبياً،
بينما قد تواجه الأسواق منخفضة النشاط
فترات أطول لإتمام عمليات البيع.
"""

    # =========================================
    # Strategic Insight
    # =========================================

    strategic_insight = f"""
تشير المؤشرات العقارية المتاحة إلى أن حي {district}
يمتلك خصائص سوقية يمكن أن تجعله
موقعاً مناسباً لبعض أنواع الاستثمار العقاري.

مؤشر قوة الحي يبلغ {dpi_display} نقطة،
ما يصنفه ضمن فئة {investment_env} داخل سوق {city}.
"""

    # =========================================
    # Final Investment Verdict
    # =========================================

    final_verdict = f"""
بناءً على تحليل البيانات المتاحة
يظهر أن حي {district} يقدم مزيجاً من
الموقع السعري {price_position}
مع مستوى سيولة يصنف كـ {liquidity_level}.

تشير هذه المؤشرات إلى سوق يتمتع بدرجة
من النشاط والاستقرار النسبي،
ما يجعل الحي خياراً قابلاً للدراسة
ضمن استراتيجيات الاستثمار العقاري في مدينة {city}.
"""

    # =========================================
    # التقرير النهائي
    # =========================================

    report_text = f"""
تحليل السوق العقاري
Warda Intelligence

تحليل حي {district} – مدينة {city}

--------------------------------------------------

نظرة عامة على السوق

{market_overview}

--------------------------------------------------

نشاط السوق والسيولة

{liquidity_analysis}

--------------------------------------------------

الموقع السعري داخل المدينة

{price_positioning}

--------------------------------------------------

مقارنة الأحياء المجاورة

{comparison_text}

--------------------------------------------------

تحليل المخاطر الاستثمارية

{risk_analysis}

--------------------------------------------------

الرؤية الاستثمارية

{strategic_insight}

--------------------------------------------------

الحكم الاستثماري

{final_verdict}

--------------------------------------------------

Warda Intelligence
تحليل عقاري مبني على بيانات السوق
"""

    return report_text
