# =========================================
# Warda Intelligence
# District Narrative Engine PRO
# =========================================

def generate_district_narrative(
        user_info,
        district_metrics,
        nearby_districts,
        dpi_score,
        ranking_row,
        advanced_metrics
):

    district = district_metrics.get("district_name", "غير محدد")
    city = district_metrics.get("city_name", "غير محدد")

    district_price = district_metrics.get("district_avg_price", 0)
    city_price = district_metrics.get("city_avg_price", 0)
    deviation = district_metrics.get("price_deviation_percent", 0)
    transactions = district_metrics.get("transactions_count", 0)

    # ترتيب الحي
    rank = ranking_row.get("rank", 0)
    total_districts = ranking_row.get("total_districts", 0)

    # مؤشرات إضافية
    market_value = advanced_metrics.get("market_value", 0)
    avg_transaction = advanced_metrics.get("avg_transaction_value", 0)
    avg_area = advanced_metrics.get("avg_area", 0)
    min_price = advanced_metrics.get("min_price_sqm", 0)
    max_price = advanced_metrics.get("max_price_sqm", 0)
    tx_per_month = advanced_metrics.get("transactions_per_month", 0)

    # تنسيق الأرقام
    district_price_display = f"{district_price:,.0f}"
    city_price_display = f"{city_price:,.0f}"
    transactions_display = f"{transactions:,}"
    market_value_display = f"{market_value:,.0f}"
    avg_transaction_display = f"{avg_transaction:,.0f}"
    avg_area_display = f"{avg_area:,.0f}"
    min_price_display = f"{min_price:,.0f}"
    max_price_display = f"{max_price:,.0f}"
    tx_month_display = f"{tx_per_month:.1f}"
    dpi_display = f"{dpi_score:.0f}"

    # ----------------------------------
    # موقع السعر داخل المدينة
    # ----------------------------------

    if deviation > 15:
        price_position = "أعلى بكثير من متوسط المدينة"
    elif deviation > 5:
        price_position = "أعلى من متوسط المدينة"
    elif deviation < -15:
        price_position = "أقل بكثير من متوسط المدينة"
    elif deviation < -5:
        price_position = "أقل من متوسط المدينة"
    else:
        price_position = "قريب من متوسط المدينة"

    # ----------------------------------
    # تحليل السيولة
    # ----------------------------------

    if transactions >= 40:
        liquidity_level = "سيولة مرتفعة"
    elif transactions >= 20:
        liquidity_level = "سيولة جيدة"
    elif transactions >= 10:
        liquidity_level = "سيولة متوسطة"
    else:
        liquidity_level = "سيولة محدودة"

    # ----------------------------------
    # البيئة الاستثمارية
    # ----------------------------------

    if dpi_score >= 75:
        investment_env = "بيئة استثمارية قوية"
    elif dpi_score >= 60:
        investment_env = "بيئة مستقرة"
    elif dpi_score >= 45:
        investment_env = "بيئة متوسطة"
    else:
        investment_env = "بيئة استثمارية ضعيفة"

    # ----------------------------------
    # مقارنة الأحياء المجاورة
    # ----------------------------------

    comparison_text = ""

    if nearby_districts:

        for d in nearby_districts:

            name = d.get("district_name", "")
            price = d.get("avg_price", 0)

            diff = ((price - district_price) / district_price) * 100 if district_price else 0

            comparison_text += f"{name} بمتوسط {price:,.0f} ريال للمتر (فرق {diff:.1f}%)\n"

    else:
        comparison_text = "لا توجد بيانات كافية للمقارنة حالياً."

    # =========================================
    # Market Overview
    # =========================================

    market_overview = f"""
سجل حي {district} في مدينة {city} عدد {transactions_display} صفقة
خلال الفترة محل الدراسة.

يبلغ متوسط سعر المتر في الحي نحو {district_price_display} ريال،
مقارنة بمتوسط المدينة البالغ {city_price_display} ريال،
ما يعني أن أسعار الحي تقع {price_position}.
"""

    # =========================================
    # Price Analysis
    # =========================================

    price_analysis = f"""
يتراوح سعر المتر في الحي بين
{min_price_display} ريال
و {max_price_display} ريال للمتر المربع.

ويبلغ متوسط السعر نحو {district_price_display} ريال للمتر،
ما يعكس موقع الحي داخل هيكل الأسعار في مدينة {city}.
"""

    # =========================================
    # Liquidity Analysis
    # =========================================

    liquidity_analysis = f"""
يشهد الحي مستوى نشاط يصنف كـ {liquidity_level}،
حيث بلغ عدد الصفقات {transactions_display} صفقة.

ويبلغ متوسط عدد الصفقات الشهرية
نحو {tx_month_display} صفقة،
ما يعكس مستوى الطلب في السوق المحلي.
"""

    # =========================================
    # Market Size
    # =========================================

    market_size = f"""
بلغ إجمالي قيمة الصفقات العقارية في الحي
نحو {market_value_display} ريال.

كما يبلغ متوسط قيمة الصفقة الواحدة
{avg_transaction_display} ريال،
بمتوسط مساحة يقارب {avg_area_display} متر مربع.
"""

    # =========================================
    # District Ranking
    # =========================================

    ranking_text = f"""
وفق مؤشر قوة الأحياء العقارية (DPI)
يحتل حي {district} المرتبة
{rank} من أصل {total_districts} حي
داخل مدينة {city}.

ويبلغ المؤشر الاستثماري للحي
{dpi_display} نقطة،
ما يصنفه ضمن فئة {investment_env}.
"""

    # =========================================
    # Risk Analysis
    # =========================================

    risk_analysis = f"""
يرتبط مستوى المخاطر في الاستثمار العقاري
بمستوى السيولة واستقرار الأسعار.

في حالة حي {district} تشير المؤشرات
إلى سوق يتمتع بدرجة من النشاط
مع استقرار نسبي في حركة الأسعار.
"""

    # =========================================
    # Strategic Insight
    # =========================================

    strategic_insight = f"""
تشير المؤشرات العقارية المتاحة
إلى أن الحي يمتلك خصائص سوقية
تجعله مناسباً لبعض أنواع الاستثمار العقاري،
خصوصاً في ظل موقعه السعري داخل سوق {city}.
"""

    # =========================================
    # Final Verdict
    # =========================================

    final_verdict = f"""
بناءً على تحليل البيانات المتاحة،
يقدم حي {district} مزيجاً من
مستوى سعري {price_position}
مع سيولة سوقية تصنف كـ {liquidity_level}.

تشير هذه المؤشرات إلى سوق يتمتع
بدرجة من الاستقرار والنشاط
ما يجعله خياراً قابلاً للدراسة
ضمن استراتيجيات الاستثمار العقاري
في مدينة {city}.
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

تحليل الأسعار

{price_analysis}

--------------------------------------------------

نشاط السوق والسيولة

{liquidity_analysis}

--------------------------------------------------

حجم السوق العقاري

{market_size}

--------------------------------------------------

ترتيب الحي داخل المدينة

{ranking_text}

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
