# =========================================
# Warda Intelligence
# District Narrative Engine
# محرك كتابة تقرير الحي المتقدم
# =========================================

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
    # تنسيق الأرقام لعرض احترافي
    # =========================================
    district_price_display = f"{district_price:,.0f}"
    city_price_display = f"{city_price:,.0f}"
    transactions_display = f"{transactions:,}"
    dpi_display = f"{dpi_score:.0f}"

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
    # تقييم القيمة السعرية
    # =========================================
    
    price_ratio = 0
    if city_price > 0:
        price_ratio = district_price / city_price
        
    if price_ratio < 0.85:
        value_label = "أقل من القيمة السوقية"
        value_explanation = f"أسعار حي {district} تقل بشكل ملحوظ عن متوسط مدينة {city}، مما قد يشير إلى فرصة دخول استثماري جيدة."
    elif price_ratio < 1.05:
        value_label = "قريبة من القيمة العادلة"
        value_explanation = f"أسعار حي {district} تتحرك بالقرب من متوسط الأسعار في مدينة {city}."
    else:
        value_label = "أعلى من القيمة السوقية"
        value_explanation = f"أسعار حي {district} أعلى من متوسط مدينة {city}، ما قد يشير إلى سوق نشط لكن مع احتمالية انخفاض هامش الربح."

    # =========================================
    # تحليل السيولة العقارية
    # =========================================
    
    if transactions >= 20:
        liquidity_level = "قوية"
        liquidity_note = f"عدد الصفقات المرتفع ({transactions_display}) يعكس سيولة نشطة وسهولة في البيع والشراء."
    elif transactions >= 8:
        liquidity_level = "متوسطة"
        liquidity_note = f"عدد الصفقات ({transactions_display}) يشير إلى سيولة مقبولة مع إمكانية تحسن النشاط."
    else:
        liquidity_level = "ضعيفة"
        liquidity_note = f"انخفاض عدد الصفقات ({transactions_display}) قد يعني محدودية السيولة وصعوبة نسبية في التنفيذ السريع."

    # =========================================
    # مرحلة دورة السوق
    # =========================================
    
    if deviation > 10 and transactions > 20:
        market_cycle = "مرحلة صعود قوي"
        cycle_note = f"الطلب في حي {district} مرتفع والأسعار أعلى من متوسط المدينة."
    elif deviation > 5:
        market_cycle = "مرحلة نمو"
        cycle_note = f"الحي يظهر مؤشرات نمو سعري تدريجي."
    elif deviation < -5 and transactions > 10:
        market_cycle = "مرحلة فرصة شراء"
        cycle_note = f"الأسعار أقل من المتوسط مع نشاط ملحوظ في الصفقات."
    else:
        market_cycle = "مرحلة استقرار"
        cycle_note = "السوق يتحرك ضمن نطاق متوازن دون تغيرات حادة."

    # =========================================
    # نوع الاستثمار الأنسب
    # =========================================
    
    if dpi_score >= 80 and transactions > 15:
        investment_style = "استثمار نمو سريع"
    elif dpi_score >= 65 and transactions > 10:
        investment_style = "استثمار متوسط المدى"
    elif dpi_score >= 50:
        investment_style = "استثمار طويل الأجل"
    else:
        investment_style = "استثمار عالي المخاطر"

    # =========================================
    # مؤشر حرارة السوق
    # =========================================
    
    market_heat = min(100, int((transactions * 2) + (dpi_score * 0.5)))
    
    if market_heat >= 80:
        heat_label = "سوق ساخن 🔥"
    elif market_heat >= 60:
        heat_label = "سوق نشط"
    elif market_heat >= 40:
        heat_label = "سوق متوازن"
    else:
        heat_label = "سوق بطيء"

    # =========================================
    # توقع الاتجاه السعري
    # =========================================
    
    if price_ratio < 0.9 and transactions > 10:
        price_outlook = "مرشح للارتفاع 📈"
    elif price_ratio > 1.15:
        price_outlook = "مرشح لتصحيح سعري 📉"
    else:
        price_outlook = "مرشح للاستقرار ➡️"

    # =========================================
    # مؤشر فرصة الاستثمار
    # =========================================
    
    # بناء مؤشر مركب من عدة عوامل
    investment_score = 50  # نقطة البداية
    
    # عامل السعر (30 نقطة كحد أقصى)
    if price_ratio < 0.85:
        investment_score += 25  # فرصة سعرية ممتازة
    elif price_ratio < 0.95:
        investment_score += 15  # فرصة سعرية جيدة
    elif price_ratio > 1.15:
        investment_score -= 20  # غالي جداً
    elif price_ratio > 1.05:
        investment_score -= 10  # غالي
    
    # عامل السيولة (30 نقطة)
    if transactions >= 30:
        investment_score += 25
    elif transactions >= 20:
        investment_score += 20
    elif transactions >= 10:
        investment_score += 10
    elif transactions < 5:
        investment_score -= 15
    
    # عامل قوة الحي (40 نقطة)
    if dpi_score >= 80:
        investment_score += 35
    elif dpi_score >= 70:
        investment_score += 25
    elif dpi_score >= 60:
        investment_score += 15
    elif dpi_score >= 50:
        investment_score += 5
    else:
        investment_score -= 20
    
    # ضمان أن النتيجة بين 0 و 100
    investment_score = max(0, min(100, investment_score))
    
    # تصنيف فرصة الاستثمار
    if investment_score >= 80:
        opportunity_class = "فرصة استثمارية قوية جداً"
        opportunity_note = f"جميع المؤشرات إيجابية في حي {district}، مما يجعله خياراً استثمارياً ممتازاً."
    elif investment_score >= 65:
        opportunity_class = "فرصة استثمارية جيدة"
        opportunity_note = f"يتمتع حي {district} بمقومات استثمارية إيجابية مع بعض عوامل الاستقرار."
    elif investment_score >= 45:
        opportunity_class = "فرصة استثمارية متوسطة"
        opportunity_note = f"حي {district} يقدم فرصة متوازنة تناسب المستثمرين الباحثين عن استقرار."
    else:
        opportunity_class = "فرصة استثمارية تحت المراقبة"
        opportunity_note = f"مؤشرات حي {district} تتطلب متابعة دقيقة قبل اتخاذ قرار استثماري."

    # =========================================
    # التقييم الاستثماري
    # =========================================
    
    if investment_score >= 85:
        investment_grade = "A+"
    elif investment_score >= 75:
        investment_grade = "A"
    elif investment_score >= 65:
        investment_grade = "B+"
    elif investment_score >= 55:
        investment_grade = "B"
    elif investment_score >= 45:
        investment_grade = "C"
    else:
        investment_grade = "D"

    # =========================================
    # موقع الحي في السوق
    # =========================================
    
    if price_ratio < 0.85:
        market_position = "حي منخفض السعر مقارنة بالسوق"
    elif price_ratio < 1.05:
        market_position = "حي ضمن متوسط السوق"
    else:
        market_position = "حي مرتفع السعر مقارنة بالسوق"

    # =========================================
    # رصد الفرص الاستثمارية
    # =========================================
    
    opportunity_flag = False
    opportunity_text = ""
    
    if price_ratio < 0.9 and transactions > 10 and dpi_score > 60:
        opportunity_flag = True
        opportunity_text = f"""
تم رصد فرصة استثمارية محتملة في حي {district}.
الأسعار الحالية أقل من متوسط المدينة مع وجود نشاط صفقات جيد، مما قد يشير إلى مرحلة دخول استثماري مبكر.
"""
    elif price_ratio < 0.85:
        opportunity_flag = True
        opportunity_text = f"""
الحي يظهر فجوة سعرية واضحة مقارنة بمتوسط أسعار مدينة {city}.
هذا قد يعكس مرحلة تسعير منخفض قد تجذب المستثمرين الباحثين عن فرص.
"""
    else:
        opportunity_text = "لم يتم رصد فرصة استثمارية واضحة في الحي حالياً."

    # =========================================
    # Investment Horizon
    # =========================================
    
    if investment_score >= 80:
        investment_horizon = "قصير إلى متوسط (1 – 3 سنوات)"
    elif investment_score >= 60:
        investment_horizon = "متوسط (3 – 5 سنوات)"
    else:
        investment_horizon = "طويل الأجل (5 – 10 سنوات)"

    # =========================================
    # Liquidity Speed
    # =========================================
    
    if transactions >= 30:
        liquidity_speed = "سريعة جداً"
    elif transactions >= 15:
        liquidity_speed = "متوسطة إلى سريعة"
    elif transactions >= 8:
        liquidity_speed = "متوسطة"
    else:
        liquidity_speed = "بطيئة نسبياً"

    # =========================================
    # المقارنة السعرية
    # =========================================
    
    benchmark_text = ""
    if price_ratio < 0.9:
        benchmark_text = f"""
أسعار الحي أقل من متوسط مدينة {city} بفارق يقارب {round((1-price_ratio)*100)}%.
"""
    elif price_ratio > 1.1:
        benchmark_text = f"""
أسعار الحي أعلى من متوسط مدينة {city} بفارق يقارب {round((price_ratio-1)*100)}%.
"""
    else:
        benchmark_text = "الحي يتحرك ضمن النطاق السعري الطبيعي للمدينة."

    # =========================================
    # الحكم الاستثماري النهائي
    # =========================================
    
    if investment_score >= 80:
        verdict = "حي استثماري قوي جداً"
    elif investment_score >= 65:
        verdict = "حي استثماري جيد"
    elif investment_score >= 50:
        verdict = "حي استثماري متوسط"
    else:
        verdict = "حي يحتاج مراقبة قبل الاستثمار"

    # =========================================
    # تحليل المخاطر
    # =========================================
    
    # مخاطر السيولة
    if transactions < 8:
        liquidity_risk = "مرتفع"
        liquidity_risk_note = f"قلة الصفقات ({transactions_display}) تعني صعوبة محتملة في البيع لاحقاً."
    elif transactions < 15:
        liquidity_risk = "متوسط"
        liquidity_risk_note = "سيولة متوسطة قد تؤثر على سرعة التنفيذ."
    else:
        liquidity_risk = "منخفض"
        liquidity_risk_note = "سيولة مرتفعة تسهل عمليات البيع والشراء."
    
    # مخاطر السعر
    if price_ratio > 1.2:
        price_risk = "مرتفع"
        price_risk_note = f"الأسعار أعلى بنسبة {round((price_ratio-1)*100)}% من متوسط المدينة، مع احتمالية تصحيح."
    elif price_ratio > 1.1:
        price_risk = "متوسط"
        price_risk_note = "ارتفاع ملحوظ في الأسعار قد يحد من هامش الربح."
    else:
        price_risk = "منخفض"
        price_risk_note = "الأسعار ضمن النطاق الطبيعي للسوق."

    # =========================================
    # البصمة الاستثمارية للحي
    # =========================================
    
    # Liquidity DNA
    if transactions >= 20:
        dna_liquidity = "سيولة عالية"
    elif transactions >= 10:
        dna_liquidity = "سيولة متوسطة"
    else:
        dna_liquidity = "سيولة منخفضة"
    
    # Growth DNA
    if price_ratio < 0.9:
        dna_growth = "نمو مرتفع محتمل"
    elif price_ratio < 1.05:
        dna_growth = "نمو مستقر"
    else:
        dna_growth = "نمو محدود"
    
    # Risk DNA
    if liquidity_risk == "مرتفع" or price_risk == "مرتفع":
        dna_risk = "مخاطرة عالية"
    elif liquidity_risk == "متوسط" or price_risk == "متوسط":
        dna_risk = "مخاطرة متوسطة"
    else:
        dna_risk = "مخاطرة منخفضة"
    
    district_dna = f""" السيولة: {dna_liquidity}
 النمو المتوقع: {dna_growth}
 مستوى المخاطر: {dna_risk} """

    # =========================================
    # District Ranking داخل المدينة
    # =========================================
    
    district_rank_note = ""
    try:
        if real_data is not None and hasattr(real_data, 'columns') and "district" in real_data.columns:
            ranking = (real_data.groupby("district")["price"].count().sort_values(ascending=False))
            if district in ranking.index:
                rank_position = ranking.index.get_loc(district) + 1
                total_districts = len(ranking)
                district_rank_note = f"يحتل حي {district} المرتبة {rank_position} من بين {total_districts} حي من حيث النشاط العقاري."
                if rank_position <= 10:
                    district_rank_note += " ويصنف ضمن الأحياء الأكثر نشاطاً في المدينة."
    except:
        district_rank_note = "لا توجد بيانات كافية لترتيب الحي داخل المدينة حالياً."

    # =========================================
    # الملخص التحليلي للحي
    # =========================================
    
    intelligence_summary = f""" يظهر تحليل البيانات أن حي {district} في مدينة {city} سجل {transactions_display} صفقة عقارية بمتوسط سعر متر يبلغ {district_price_display} ريال. تشير مؤشرات السوق إلى أن الحي يقع {value_label} مع تصنيف سوقي {heat_label} ومرحلة سوق {market_cycle}. """

    # =========================================
    # قصة السوق
    # =========================================
    
    if market_heat >= 80:
        market_story = f"""
تشير البيانات إلى أن حي {district} يمر حالياً بمرحلة نشاط مرتفع في السوق العقاري داخل مدينة {city}.
ارتفاع عدد الصفقات مقترناً بمؤشرات الطلب قد يعكس مرحلة توسع في السوق.
"""
    elif market_heat >= 60:
        market_story = f"""
السوق في حي {district} يظهر مستوى نشاط جيد مع استقرار نسبي في الأسعار داخل مدينة {city}.
هذا يشير إلى سوق متوازن يجذب المستثمرين الباحثين عن فرص مستقرة.
"""
    else:
        market_story = f"""
النشاط العقاري في حي {district} أقل نسبياً مقارنة ببعض الأحياء الأخرى في مدينة {city}.
قد يعكس ذلك مرحلة هدوء في السوق أو فرصة دخول استثماري مبكر.
"""

    # =========================================
    # التوصية الاستثمارية النهائية
    # =========================================
    
    if investment_score >= 75 and price_ratio < 1.05:
        final_recommendation = "يوصى بالاستثمار في الحي حالياً، خاصة مع توفر فرص سعرية جيدة."
    elif investment_score >= 60 and transactions > 10:
        final_recommendation = "يوصى بدراسة الفرص المتاحة مع التركيز على العقارات ذات الأسعار المنافسة."
    elif investment_score >= 45:
        final_recommendation = "يفضل الانتظار ومراقبة تطورات السوق خلال الأشهر القادمة."
    else:
        final_recommendation = "ينصح بالحذر حالياً والبحث في أحياء بديلة ذات مؤشرات أفضل."

    # =========================================
    # تحليل السوق داخل الحي
    # =========================================

    if deviation > 5:
        ai_market = f"يشير المستوى السعري في حي {district} إلى وجود طلب مرتفع مقارنة بمتوسط مدينة {city}."
    elif deviation < -5:
        ai_market = f"يظهر حي {district} أسعاراً أقل من متوسط مدينة {city} مما قد يشير إلى فرص دخول استثماري جيدة."
    else:
        ai_market = f"يتحرك حي {district} ضمن النطاق السعري الطبيعي لمدينة {city}."

    # القرار التنفيذي
    executive_decision = f"""
بناءً على البيانات المتاحة، يظهر حي {district} في مدينة {city}
مستوى سعري {price_position} مع مؤشر قوة يبلغ {dpi_display} نقطة.

يشير ذلك إلى بيئة عقارية {dpi_label}
مع مستوى نشاط بلغ {transactions_display} صفقة.
مؤشر حرارة السوق: {heat_label} ({market_heat}/100)
نوع الاستثمار المناسب: {investment_style}

الخلاصة الاستثمارية: {verdict}
التقييم الاستثماري: {investment_grade}
موقع الحي السعري: {market_position}

{final_recommendation}
"""

    # =========================================
    # جدول مقارنة الأحياء
    # =========================================

    comparison_table = ""
    
    if not nearby_districts:
        comparison_table = "لا توجد بيانات كافية لمقارنة الأحياء المجاورة حالياً."
    else:
        for d in nearby_districts:
            name = d.get("district_name", "")
            price = d.get("avg_price", 0)

            if district_price > 0:
                diff = ((price - district_price) / district_price) * 100
            else:
                diff = 0

            comparison_table += f"{name} | {price:,.0f} ريال | فرق {round(diff,1)}%\n"

    # =========================================
    # بناء التقرير
    # =========================================

    report_text = f"""# تحليل الحي
Warda Intelligence
District Intelligence Report

تحليل حي {district} – مدينة {city}

--------------------------------------------------

بطاقة معلومات الحي

المدينة: {city}
الحي: {district}

متوسط سعر المتر:
{district_price_display} ريال

متوسط سعر المتر في المدينة:
{city_price_display} ريال

الموقع السعري:
{price_position}

تقييم القيمة السعرية:
{value_label}
{value_explanation}

عدد الصفقات المنفذة:
{transactions_display} صفقة

--------------------------------------------------

تحليل السيولة العقارية

مستوى السيولة: {liquidity_level}
{liquidity_note}

سرعة السيولة في السوق: {liquidity_speed}

--------------------------------------------------

مرحلة دورة السوق

{market_cycle}
{cycle_note}

--------------------------------------------------

مؤشر حرارة السوق

مستوى النشاط: {market_heat} / 100
التصنيف: {heat_label}

--------------------------------------------------

نوع الاستثمار المناسب

{investment_style}

--------------------------------------------------

الأفق الاستثماري المتوقع

{investment_horizon}

--------------------------------------------------

توقع الاتجاه السعري

{price_outlook}

--------------------------------------------------

مؤشر قوة الحي

قيمة المؤشر:
{dpi_display} / 100

تصنيف البيئة العقارية:
{dpi_label}

--------------------------------------------------

مؤشر فرصة الاستثمار

نقاط الفرصة الاستثمارية:
{investment_score} / 100

التصنيف: {opportunity_class}
{opportunity_note}

--------------------------------------------------

التقييم الاستثماري

تقييم الحي الاستثماري: {investment_grade}

--------------------------------------------------

موقع الحي في السوق

{market_position}

--------------------------------------------------

رصد الفرص الاستثمارية

{opportunity_text}

--------------------------------------------------

تحليل المخاطر

مخاطر السيولة: {liquidity_risk}
{liquidity_risk_note}

مخاطر السعر: {price_risk}
{price_risk_note}

--------------------------------------------------

مقارنة الأحياء المجاورة

لمعرفة موقع الحي بشكل أفضل في السوق، تم تحليل بعض الأحياء
القريبة من حيث النشاط العقاري أو المستوى السعري.

{comparison_table}

تشير هذه المقارنة إلى موقع حي {district} ضمن نطاق الأسعار
المحلية للأحياء المجاورة في مدينة {city}.

--------------------------------------------------

المقارنة السعرية

{benchmark_text}

--------------------------------------------------

البصمة الاستثمارية للحي

{district_dna}

--------------------------------------------------

موقع الحي داخل المدينة

{district_rank_note}

--------------------------------------------------

الملخص التحليلي للحي

{intelligence_summary}

--------------------------------------------------

قصة السوق

{market_story}

--------------------------------------------------

الحكم الاستثماري النهائي

{verdict}

--------------------------------------------------

تحليل السوق داخل الحي

{ai_market}

--------------------------------------------------

التوصية الاستثمارية

{final_recommendation}

--------------------------------------------------

القرار التنفيذي

{executive_decision}

--------------------------------------------------

Warda Intelligence
تحليل عقاري مبني على بيانات السوق الفعلية
"""

    return report_text
