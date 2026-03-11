# =========================================
# District Narrative Engine
# Warda Intelligence
# =========================================


def generate_district_narrative(
    user_info,
    district_metrics,
    nearby_districts,
    dpi_score,
    market_data=None,
    real_data=None,
    ranking_row=None,
    advanced_metrics=None
):

    # -----------------------------------------
    # استخراج البيانات الأساسية
    # -----------------------------------------

    district_name = district_metrics.get("district_name", "الحي")
    avg_price = district_metrics.get("district_avg_price", 0)
    transactions = district_metrics.get("transactions_count", 0)

    liquidity = district_metrics.get("liquidity_score", 0)
    stability = district_metrics.get("stability_score", 0)
    price_strength = district_metrics.get("price_strength", 0)

    # -----------------------------------------
    # المؤشرات المتقدمة
    # -----------------------------------------

    market_value = None
    avg_transaction_value = None
    avg_area = None
    min_price_sqm = None
    max_price_sqm = None
    transactions_per_month = None

    if advanced_metrics:

        market_value = advanced_metrics.get("market_value")
        avg_transaction_value = advanced_metrics.get("avg_transaction_value")
        avg_area = advanced_metrics.get("avg_area")
        min_price_sqm = advanced_metrics.get("min_price_sqm")
        max_price_sqm = advanced_metrics.get("max_price_sqm")
        transactions_per_month = advanced_metrics.get("transactions_per_month")

    # -----------------------------------------
    # ترتيب الحي
    # -----------------------------------------

    rank = None
    total_districts = None

    if ranking_row is not None and not ranking_row.empty:

        if "rank" in ranking_row.columns:
            rank = ranking_row["rank"].iloc[0]

        if real_data is not None and "district" in real_data.columns:
            total_districts = real_data["district"].nunique()

    # -----------------------------------------
    # حصة الحي من السوق
    # -----------------------------------------

    market_share = None

    if real_data is not None and "district" in real_data.columns:

        total_transactions = len(real_data)

        district_transactions = len(
            real_data[real_data["district"] == district_name]
        )

        if total_transactions > 0:
            market_share = (district_transactions / total_transactions) * 100

    # -----------------------------------------
    # تحليل السيولة
    # -----------------------------------------

    if transactions_per_month:

        if transactions_per_month > 20:
            liquidity_text = "سيولة مرتفعة في السوق مع نشاط قوي في عمليات البيع والشراء."
        elif transactions_per_month > 8:
            liquidity_text = "سيولة متوسطة تشير إلى وجود حركة تداول مستقرة في السوق."
        else:
            liquidity_text = "سيولة منخفضة نسبياً وقد يتطلب بيع العقار وقتاً أطول."

    else:
        liquidity_text = "لا توجد بيانات كافية لتحليل السيولة الشهرية."

    # -----------------------------------------
    # تحليل السعر
    # -----------------------------------------

    price_range_text = ""

    if min_price_sqm and max_price_sqm:

        price_range_text = f"""
يتراوح سعر المتر في الحي بين {min_price_sqm:,.0f} ريال و {max_price_sqm:,.0f} ريال
مما يعكس تنوعاً في المنتجات العقارية داخل الحي.
"""

    # -----------------------------------------
    # تحليل السوق
    # -----------------------------------------

    if dpi_score >= 80:
        market_stage = "حي استثماري قوي جداً"
    elif dpi_score >= 65:
        market_stage = "حي استثماري جيد"
    elif dpi_score >= 50:
        market_stage = "حي متوسط الجاذبية الاستثمارية"
    else:
        market_stage = "حي يحتاج مراقبة قبل الاستثمار"

    # -----------------------------------------
    # بناء التقرير
    # -----------------------------------------

    report = f"""
تحليل حي {district_name}

يعتمد هذا التقرير على تحليل بيانات الصفقات العقارية الفعلية
وذلك بهدف تقديم صورة دقيقة عن أداء السوق العقاري داخل الحي.

--------------------------------------------------

المؤشرات الأساسية

عدد الصفقات العقارية: {transactions:,} صفقة

متوسط سعر المتر: {avg_price:,.0f} ريال

مؤشر قوة الحي الاستثماري (DPI):
{dpi_score:.1f} من 100

--------------------------------------------------
"""

    # ترتيب الحي

    if rank and total_districts:

        report += f"""
ترتيب الحي داخل المدينة

يحتل حي {district_name} المرتبة {rank}
من بين {total_districts} حي داخل المدينة
من حيث قوة المؤشرات الاستثمارية.
"""

    # حجم السوق

    if market_value:

        report += f"""
--------------------------------------------------

حجم السوق العقاري في الحي

بلغ إجمالي قيمة الصفقات العقارية في الحي
نحو {market_value:,.0f} ريال
خلال الفترة التي تم تحليلها.
"""

    # متوسط الصفقة

    if avg_transaction_value:

        report += f"""
متوسط قيمة الصفقة العقارية

يبلغ متوسط قيمة الصفقة في الحي
حوالي {avg_transaction_value:,.0f} ريال.
"""

    # المساحة

    if avg_area:

        report += f"""
متوسط مساحة العقار

يبلغ متوسط مساحة العقار المتداول
حوالي {avg_area:,.0f} متر مربع.
"""

    # نطاق الأسعار

    if price_range_text:

        report += f"""
--------------------------------------------------

نطاق الأسعار في الحي

{price_range_text}
"""

    # سرعة السوق

    if transactions_per_month:

        report += f"""
--------------------------------------------------

سرعة السوق العقاري

يسجل الحي متوسط {transactions_per_month:.1f} صفقة عقارية شهرياً.

{liquidity_text}
"""

    # حصة السوق

    if market_share:

        report += f"""
--------------------------------------------------

حصة الحي من السوق العقاري

يمثل حي {district_name}
نحو {market_share:.2f}% من إجمالي الصفقات العقارية
داخل المدينة.
"""

    # مقارنة الأحياء

    if nearby_districts:

        report += """
--------------------------------------------------

مقارنة مع الأحياء القريبة
"""

        for d in nearby_districts:

            name = d.get("district_name", "")
            price = d.get("avg_price", 0)

            if avg_price > 0:
                diff = ((price - avg_price) / avg_price) * 100
            else:
                diff = 0

            report += f"{name} – {price:,.0f} ريال – فرق {diff:.1f}%\n"

    # الحكم الاستثماري

    report += f"""
--------------------------------------------------

الخلاصة الاستثمارية

بناءً على تحليل البيانات العقارية
يمكن تصنيف حي {district_name} على أنه:

{market_stage}

يعتمد القرار الاستثماري النهائي
على استراتيجية المستثمر
وأفق الاستثمار المستهدف.
"""

    report += """

--------------------------------------------------
Warda Intelligence
تحليل عقاري مبني على بيانات السوق الفعلية
"""

    return report
