# =========================================
# District Narrative Engine
# Warda Intelligence
# =========================================


# -----------------------------------------
# دالة السرد الرئيسية للحي
# -----------------------------------------
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
    """
    توليد تقرير سردي متكامل عن الحي بناءً على جميع المؤشرات
    """

    # استخراج مؤشرات الحي - مع دعم كلا الاسمين (district_name أو district_clean)
    district_name = district_metrics.get(
        "district_name", 
        district_metrics.get("district_clean", "الحي")
    )
    avg_price = district_metrics.get("district_avg_price", 0)
    transactions = district_metrics.get("transactions_count", 0)
    
    # المؤشرات - حالياً تعود للصفر وسيتم تعبئتها من ranking engine لاحقاً
    liquidity = district_metrics.get("liquidity_score", 0)
    stability = district_metrics.get("stability_score", 0)
    price_strength = district_metrics.get("price_strength", 0)

    # استخراج المؤشرات المتقدمة
    market_value = None
    avg_transaction_value = None
    avg_area = None
    transactions_per_month = None
    
    # التعديل: استخدام is not None بدلاً من if advanced_metrics:
    if advanced_metrics is not None:
        market_value = advanced_metrics.get("market_value")
        avg_transaction_value = advanced_metrics.get("avg_transaction_value")
        avg_area = advanced_metrics.get("avg_area")
        transactions_per_month = advanced_metrics.get("transactions_per_month")
        # ملاحظة: market_scope غير موجود في advanced_metrics حالياً - تم حذفه

    # معلومات الترتيب
    rank = None
    total_districts = None
    if ranking_row is not None and not ranking_row.empty:
        rank = ranking_row["rank"].iloc[0] if "rank" in ranking_row else None
        
        # حساب total_districts بطريقة آمنة - تجنب استخدام .get() مع DataFrame
        if real_data is not None and "district" in real_data.columns:
            total_districts = real_data["district"].nunique()
        elif "total_districts" in ranking_row.columns:
            total_districts = ranking_row["total_districts"].iloc[0]
        else:
            total_districts = None

    # =========================================
    # بناء النص السردي
    # =========================================

    # المقدمة
    narrative = f"""
    تقرير حي {district_name} – منصة واردا للذكاء العقاري
    ===================================================
    
    يعرض هذا التقرير تحليلاً مفصلاً لأداء حي {district_name} داخل السوق العقاري للمدينة اعتماداً على بيانات الصفقات الفعلية.

    بناءً على تحليل {transactions:,} صفقة عقارية في الحي، إليك ملخص أدائه:
    """

    # مؤشر DPI
    narrative += f"""
    
    مؤشر قوة الحي الاستثماري (DPI): {dpi_score:.1f} من 100
    ----------------------------------------
    """

    if dpi_score >= 80:
        narrative += "ممتاز – يعتبر هذا الحي من أقوى الأحياء استثمارياً."
    elif dpi_score >= 60:
        narrative += "جيد – مؤشرات إيجابية تجعل الحي خياراً استثمارياً مناسباً."
    elif dpi_score >= 40:
        narrative += "متوسط – يحتاج الحي إلى متابعة دقيقة قبل اتخاذ قرار استثماري."
    else:
        narrative += "ضعيف – يفضل البحث في أحياء أخرى أو إعادة تقييم الفرصة."

    # الترتيب
    if rank is not None and total_districts is not None:
        narrative += f"""
    
    ترتيب الحي: {rank} من أصل {total_districts} حي
    ----------------------------------------
    يحتل حي {district_name} المرتبة {rank} من بين {total_districts} حي في المدينة.
    """

    # المؤشرات الرئيسية
    narrative += f"""
    
    المؤشرات الرئيسية:
    -----------------
    متوسط سعر المتر: {avg_price:,.0f} ريال
    عدد الصفقات: {transactions:,} صفقة
    مؤشر السيولة: {liquidity:.1f} من 100
    مؤشر الاستقرار: {stability:.1f} من 100
    قوة السعر: {price_strength:.1f} من 100
    """
    
    # حجم السوق العقاري (المؤشرات المتقدمة)
    # التعديل: استخدام is not None بدلاً من if market_value:
    if market_value is not None and avg_transaction_value is not None and avg_area is not None:
        narrative += f"""
    
    حجم السوق العقاري:
    ------------------
    بلغ إجمالي قيمة الصفقات العقارية في الحي نحو {market_value:,.0f} ريال.
    كما بلغ متوسط قيمة الصفقة الواحدة حوالي {avg_transaction_value:,.0f} ريال،
    بمتوسط مساحة يقارب {avg_area:,.0f} متر مربع للعقار.
    """
    
    # إضافة مؤشر الصفقات الشهرية إذا كان متاحاً
    if transactions_per_month is not None:
        narrative += f"""
    
    معدل السيولة الشهرية:
    --------------------
    بلغ متوسط عدد الصفقات الشهرية في الحي حوالي {transactions_per_month:.1f} صفقة،
    مما يعطي مؤشراً على سرعة دوران السوق العقاري في الحي.
    """

    # تحليل السيولة
    narrative += "\n\nالسيولة:\n"
    if liquidity >= 70:
        narrative += "✓ سيولة عالية – عدد كبير من الصفقات يضمن سهولة البيع مستقبلاً."
    elif liquidity >= 40:
        narrative += "✓ سيولة متوسطة – يوجد نشاط عقاري يمكن الاعتماد عليه."
    else:
        narrative += "⚠ سيولة منخفضة – قلة الصفقات قد تصعّب البيع عند الحاجة."

    # تحليل الاستقرار
    narrative += "\n\nالاستقرار السعري:\n"
    if stability >= 70:
        narrative += "✓ استقرار ممتاز – الأسعار شبه ثابتة ومطمئنة."
    elif stability >= 40:
        narrative += "✓ استقرار مقبول – بعض التذبذب ولكن ضمن الحدود الطبيعية."
    else:
        narrative += "⚠ تذبذب مرتفع – الحي يشهد تغيرات سعرية كبيرة."

    # الأحياء المجاورة
    if nearby_districts:
        narrative += """
        
    مقارنة مع الأحياء المجاورة:
    -------------------------"""
        for neighbor in nearby_districts:
            neighbor_name = neighbor.get("district_name", "حي مجاور")
            neighbor_price = neighbor.get("avg_price", 0)
            diff = ((avg_price - neighbor_price) / neighbor_price) * 100 if neighbor_price > 0 else 0

            if diff > 10:
                trend = f"أعلى من {neighbor_name} بنسبة {diff:.0f}%"
            elif diff < -10:
                trend = f"أقل من {neighbor_name} بنسبة {abs(diff):.0f}%"
            else:
                trend = f"قريب من مستوى {neighbor_name}"

            narrative += f"\n   • {trend}"

    # توصية نهائية
    narrative += """
    
    التوصية النهائية:
    -----------------
    """

    if dpi_score >= 70:
        narrative += "✓ مؤشرات قوية – نوصي بالبدء في البحث عن فرص استثمارية بالحي."
    elif dpi_score >= 50:
        narrative += "✓ مؤشرات إيجابية – فرصة جيدة للاستثمار مع متابعة التطورات."
    else:
        narrative += "⚠ مؤشرات تحتاج مراجعة – الأفضل البحث في حي آخر يتناسب مع أهدافك الاستثمارية."

    narrative += "\n\nWarda Intelligence - تحليل عقاري مبني على بيانات السوق الفعلية"

    return narrative


# -----------------------------------------
# توليد تقرير سريع بدون تفاصيل المستخدم
# -----------------------------------------
def generate_quick_summary(district_metrics, ranking_df=None):

    """
    نسخة مختصرة من التقرير للاستخدامات العامة
    """

    district_name = district_metrics.get("district_name", district_metrics.get("district_clean", "الحي"))
    avg_price = district_metrics.get("district_avg_price", 0)
    transactions = district_metrics.get("transactions_count", 0)
    dpi = district_metrics.get("dpi", 0)

    summary = f"{district_name}: {dpi:.0f} نقطة DPI | سعر المتر {avg_price:,.0f} ريال | {transactions} صفقة"

    # إضافة الترتيب إذا وجد
    if ranking_df is not None and not ranking_df.empty:
        rank_row = ranking_df[ranking_df["district_clean"] == district_name]
        if not rank_row.empty:
            rank = rank_row["rank"].iloc[0]
            total = rank_row["total_districts"].iloc[0] if "total_districts" in rank_row.columns else "?"
            summary += f" | الترتيب {rank} من {total}"

    return summary
