# ai_executive_summary.py
# =========================================
# Executive Decision Engine – Warda Intelligence
# يولد خلاصة استشارية نهائية مبنية على بيانات حقيقية
# =========================================

import pandas as pd
from smart_opportunities import SmartOpportunityFinder


def generate_executive_summary(user_info, market_data, real_data):
    """
    يولد نص الخلاصة الاستشارية النهائية
    بدون مخاطبة فئة معينة
    """

    city = user_info.get("city", "")
    property_type = user_info.get("property_type", "")

    # -----------------------------
    # حماية أساسية
    # -----------------------------
    if real_data is None or real_data.empty:
        return (
            "تعذر توليد خلاصة استشارية دقيقة بسبب نقص البيانات الفعلية. "
            "يوصى بعدم اتخاذ أي قرار قبل توفر بيانات سوقية موثوقة."
        )

    # -----------------------------
    # أرقام حقيقية من السوق
    # -----------------------------
    total_properties = len(real_data)

    avg_price_m2 = real_data["سعر_المتر"].mean()
    min_price_m2 = real_data["سعر_المتر"].min()
    max_price_m2 = real_data["سعر_المتر"].max()

    # -----------------------------
    # الفرص الذكية
    # -----------------------------
    finder = SmartOpportunityFinder()
    opportunities = finder.find_undervalued_properties(real_data, city)
    rising_areas = finder.predict_rising_areas(real_data, city)

    undervalued_count = len(opportunities)
    best_discount = (
        max([float(o["الخصم"].replace("%", "")) for o in opportunities])
        if opportunities else 0
    )

    top_areas = [a["المنطقة"] for a in rising_areas[:3]]

    # -----------------------------
    # مؤشرات السوق
    # -----------------------------
    growth = market_data.get("معدل_النمو_الشهري", 0)
    liquidity = market_data.get("مؤشر_السيولة", 0)

    # -----------------------------
    # النص التنفيذي (لغة قرار)
    # -----------------------------
    summary = f"""
بعد تحليل {total_properties} عقارًا فعليًا ضمن نطاق {city} لفئة {property_type}،
تبيّن أن متوسط سعر المتر يبلغ {avg_price_m2:,.0f} ريال،
ضمن نطاق سعري يتراوح بين {min_price_m2:,.0f} و {max_price_m2:,.0f} ريال للمتر.

أظهر التحليل أن {undervalued_count} عقارًا حاليًا
يتم تسعيرها بأقل من متوسط مناطقها،
مع خصومات فعلية وصلت في بعض الحالات إلى {best_discount:.1f}%،
وهي فجوة سعرية لا تظهر في المقارنات السطحية أو الإعلانات العامة.

كما رُصدت مناطق تُظهر سلوكًا صاعدًا من حيث الطلب والعائد،
أبرزها: {", ".join(top_areas) if top_areas else "—"}،
مدعومة ببيانات تداول فعلية وليس بتوقعات نظرية.

من ناحية ديناميكية السوق،
يسجّل السوق معدل نمو شهري يقارب {growth:.1f}%،
مع مستوى سيولة عند {liquidity:.0f}،
وهو ما يشير إلى سوق نشط يتطلب قرارات دقيقة لا عشوائية.

الخلاصة العملية:
القرارات التي لا تعتمد على مقارنة السعر بسياق منطقته الفعلية
قد تؤدي إلى دفع قيمة أعلى دون ميزة حقيقية.
التحرك الذكي في هذه المرحلة يكون بالتركيز على الفجوات السعرية المؤقتة
ضمن مناطق تُظهر مؤشرات نمو واستقرار تشغيلي.
"""

    return summary.strip()
