# =========================================
# Warda Intelligence
# District Narrative Engine
# محرك كتابة تقرير الحي المتقدم
# =========================================

from ai_report_reasoner import AIReportReasoner
from executive_decision_engine import generate_executive_summary


def generate_district_narrative(
        user_info,
        district_metrics,
        nearby_districts,
        dpi_score,
        market_data,
        real_data
):
    """
    إنشاء نص تقرير حي كامل
    """

    district = district_metrics.get("district_name", "غير محدد")
    city = district_metrics.get("city_name", "غير محدد")

    district_price = district_metrics.get("district_avg_price", 0)
    city_price = district_metrics.get("city_avg_price", 0)

    deviation = district_metrics.get("price_deviation_percent", 0)
    transactions = district_metrics.get("transactions_count", 0)

    # =========================================
    # تحديد الموقع السعري
    # =========================================

    if deviation > 10:
        price_position = "أعلى من متوسط المدينة بشكل ملحوظ"
    elif deviation > 3:
        price_position = "أعلى قليلاً من متوسط المدينة"
    elif deviation < -10:
        price_position = "أقل من متوسط المدينة بشكل واضح"
    elif deviation < -3:
        price_position = "أقل قليلاً من متوسط المدينة"
    else:
        price_position = "قريب من متوسط المدينة"

    # =========================================
    # تصنيف قوة الحي
    # =========================================

    if dpi_score < 40:
        dpi_label = "بيئة عقارية ضعيفة"
    elif dpi_score < 60:
        dpi_label = "استقرار حذر"
    elif dpi_score < 75:
        dpi_label = "بيئة مستقرة"
    else:
        dpi_label = "بيئة قوية"

    # =========================================
    # تشغيل الذكاء الاصطناعي
    # =========================================

    ai_engine = AIReportReasoner()

    ai_insights = ai_engine.generate_all_insights(
        user_info=user_info,
        market_data=market_data,
        real_data=real_data
    )

    ai_market = ai_insights.get("ai_live_market", "")
    ai_opportunities = ai_insights.get("ai_opportunities", "")
    ai_risk = ai_insights.get("ai_risk", "")

    # =========================================
    # القرار التنفيذي
    # =========================================

    executive_decision = generate_executive_summary(
        user_info=user_info,
        market_data=market_data,
        real_data=real_data,
        package=user_info.get("package", "free")
    )

    # =========================================
    # جدول مقارنة الأحياء
    # =========================================

    comparison_table = ""

    for d in nearby_districts:

        name = d.get("district_name", "")
        price = d.get("avg_price", 0)

        if district_price > 0:
            diff = ((price - district_price) / district_price) * 100
        else:
            diff = 0

        comparison_table += f"{name} – {price} ريال – فرق {round(diff,2)}%\n"

    # =========================================
    # بناء التقرير
    # =========================================

    report_text = f"""
Warda Intelligence
District Intelligence Report

تحليل حي {district} – مدينة {city}

--------------------------------------------------

بطاقة معلومات الحي

المدينة: {city}
الحي: {district}

متوسط سعر المتر:
{district_price} ريال

متوسط سعر المتر في المدينة:
{city_price} ريال

الموقع السعري:
{price_position}

عدد الصفقات المنفذة:
{transactions} صفقة

--------------------------------------------------

تحليل السوق في الحي

يظهر حي {district} موقعاً سعرياً {price_position} مقارنة بمتوسط الأسعار
في مدينة {city}. هذا يعكس طبيعة الطلب على العقارات في الحي
ومستوى السيولة العقارية المرتبطة به.

--------------------------------------------------

مؤشر قوة الحي

قيمة المؤشر:
{dpi_score} / 100

تصنيف البيئة العقارية:
{dpi_label}

--------------------------------------------------

مقارنة الأحياء المجاورة

لمعرفة موقع الحي بشكل أفضل في السوق، تم تحليل بعض الأحياء
القريبة من حيث النشاط العقاري أو المستوى السعري.

{comparison_table}

تشير هذه المقارنة إلى موقع حي {district} ضمن نطاق الأسعار
المحلية للأحياء المجاورة في مدينة {city}.

--------------------------------------------------

تحليل السوق بالذكاء الاصطناعي

{ai_market}

--------------------------------------------------

الفرص المحتملة

{ai_opportunities}

--------------------------------------------------

المخاطر المحتملة

{ai_risk}

--------------------------------------------------

القرار التنفيذي

{executive_decision}

--------------------------------------------------

Warda Intelligence
تحليل عقاري مبني على بيانات السوق الفعلية
"""

    return report_text
