# =========================================
# Warda Intelligence
# District Narrative Engine
# محرك كتابة تقرير الحي
# =========================================


def generate_district_narrative(metrics: dict, dpi_score: float):
    """
    تحويل مؤشرات الحي إلى نص تقرير
    """

    district = metrics["district_name"]
    city = metrics["city_name"]
    district_price = metrics["district_avg_price"]
    city_price = metrics["city_avg_price"]
    deviation = metrics["price_deviation_percent"]
    transactions = metrics["transactions_count"]

    # تحديد وصف الانحراف السعري
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

    # تصنيف مؤشر القوة
    if dpi_score < 40:
        dpi_label = "بيئة ضعيفة"
        decision = "يوصى بالانتظار قبل اتخاذ قرار الشراء"
    elif dpi_score < 60:
        dpi_label = "استقرار حذر"
        decision = "فرصة انتقائية تتطلب دراسة العقار بعناية"
    elif dpi_score < 75:
        dpi_label = "بيئة مستقرة"
        decision = "مناسب للاستثمار طويل المدى"
    else:
        dpi_label = "بيئة قوية"
        decision = "حي يتمتع بجاذبية استثمارية واضحة"

    report_text = f"""
Warda Intelligence
District Intelligence Report

تحليل حي {district} – مدينة {city}

------------------------------------

الخلاصة التنفيذية

متوسط سعر المتر في الحي:
{district_price} ريال

متوسط سعر المتر في المدينة:
{city_price} ريال

الموقع السعري:
الحي يقع {price_position}.

عدد الصفقات المنفذة:
{transactions} صفقة.

------------------------------------

مؤشر قوة الحي

قيمة المؤشر:
{dpi_score} / 100

التصنيف:
{dpi_label}

------------------------------------

القرار التنفيذي

استناداً إلى المؤشرات الرقمية الحالية،
فإن حي {district} يصنف ضمن فئة:

{decision}

يبقى هذا القرار مرتبطاً باستقرار المؤشرات
المبنية على الصفقات العقارية المنفذة.
"""

    return report_text
