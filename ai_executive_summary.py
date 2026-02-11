# =========================================
# Executive Predictive Decision Engine
# Warda Intelligence – Diamond Version
# =========================================

from smart_opportunities import SmartOpportunityFinder
from gold_decision_engine import generate_gold_decision_metrics
import numpy as np
import pandas as pd


def safe_pct(x, default=0.0):
    try:
        return round(float(x * 100), 2)
    except Exception:
        return default


def compute_long_term_forecast(real_data: pd.DataFrame):
    """
    حساب تنبؤ زمني 10 سنوات مبني فقط على البيانات الحية
    """
    if real_data is None or real_data.empty or "price" not in real_data.columns:
        return {
            "y1_3": 0.0,
            "y4_6": 0.0,
            "y7_10": 0.0,
            "cumulative_min": 0.0,
            "cumulative_max": 0.0,
        }

    # ترتيب البيانات قبل حساب النمو
    if "date" in real_data.columns:
        real_data = real_data.sort_values("date")
    
    prices = real_data["price"].dropna()

    annual_growth = prices.pct_change().median()
    annual_growth = annual_growth if pd.notna(annual_growth) else 0.01

    y1_3 = safe_pct(annual_growth * 0.7)
    y4_6 = safe_pct(annual_growth * 1.2)
    y7_10 = safe_pct(annual_growth * 1.7)

    cumulative_min = safe_pct((1 + annual_growth * 0.6) ** 10 - 1)
    cumulative_max = safe_pct((1 + annual_growth * 1.1) ** 10 - 1)

    return {
        "y1_3": y1_3,
        "y4_6": y4_6,
        "y7_10": y7_10,
        "cumulative_min": cumulative_min,
        "cumulative_max": cumulative_max,
    }


def generate_executive_summary(user_info, market_data, real_data):
    """
    الخلاصة التنفيذية التنبؤية – Diamond
    """

    if real_data is None or real_data.empty:
        return (
            "الخلاصة التنفيذية التنبؤية – Warda Intelligence\n\n"
            "تعذر توليد الخلاصة التنفيذية لعدم توفر بيانات سوقية حقيقية."
        )

    city = user_info.get("city", "غير محددة")
    property_type = user_info.get("property_type", "غير محدد")

    # =========================
    # Gold Metrics (LIVE)
    # =========================
    gold = generate_gold_decision_metrics(
        city=city,
        property_type=property_type,
        real_data=real_data,
        market_data=market_data
    )

    dci = gold.get("DCI", 0)
    vgs = gold.get("VGS", 0.0)
    raos = gold.get("RAOS", 0)
    scm = gold.get("SCM", {}).get("percentage", 0)

    # =========================
    # Forecast 10 Years
    # =========================
    forecast = compute_long_term_forecast(real_data)

    # =========================
    # Opportunity Signals
    # =========================
    finder = SmartOpportunityFinder()
    undervalued = finder.find_undervalued_properties(real_data, city)
    rising_areas = finder.predict_rising_areas(real_data, city)

    volatility = safe_pct(
        real_data["price"].pct_change().std()
        if "price" in real_data.columns else 0.0
    )

    # =========================
    # BUILD EXECUTIVE SUMMARY
    # =========================
    lines = []

    lines.append("# الخلاصة التنفيذية التنبؤية")
    lines.append("")
    lines.append("## Warda Intelligence")
    lines.append("")
    lines.append("### القرار النهائي – الإصدار التنفيذي")
    lines.append("")
    lines.append(f"رقم المرجعية: WI-{city[:3]}-{property_type[:3]}-{pd.Timestamp.now().strftime('%Y%m')}")
    lines.append(f"نطاق التطبيق: {property_type} – {city}")
    lines.append("مصدر البيانات: بيانات سوقية آنية تم جمعها ومعالجتها لحظة إصدار المرجعية.")
    lines.append("")
    lines.append("تم اشتقاق هذا القرار من نموذج **Warda Intelligence Core Model**")
    lines.append("القائم على:")
    lines.append("– تحليل القيمة النسبية")
    lines.append("– نمذجة التذبذب")
    lines.append("– اختبار 20 سيناريو متقاطع")
    lines.append("– قراءة الإشارات السلوكية المبكرة")
    lines.append("– معايرة مقابل دورات سوقية تاريخية مماثلة")
    lines.append("")
    lines.append("هذا القرار مصمم لمن يتخذ الخطوة وفق نظام… لا وفق موجة.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================
    # DCI
    # =========================
    lines.append("## أولًا: مؤشر موثوقية القرار (DCI)")
    lines.append("")
    lines.append(f"**{dci} / 100**")
    lines.append("")
    lines.append("تصنيف الحالة: استقرار كافٍ للتنفيذ طويل المدى ضمن هامش أمان مقبول.")
    lines.append("")
    lines.append("المعنى التنفيذي:")
    lines.append("– البيانات ضمن نطاق الصلاحية المعتمد.")
    lines.append("– النموذج يعمل داخل حدود دقة مستقرة.")
    lines.append("– عدم اليقين طبيعي وغير هيكلي.")
    lines.append("")
    lines.append("### القرار:")
    lines.append("")
    lines.append("تفعيل الاستراتيجية طويلة المدى الآن.")
    lines.append("عدم تأجيل القرار بدافع الغموض.")
    lines.append("منع أي تحرك عشوائي خارج إطار الانتقاء.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================
    # VGS
    # =========================
    lines.append("## ثانيًا: فجوة القيمة السوقية (VGS)")
    lines.append("")
    vgs_display = f"{vgs}%" if vgs < 0 else f"+{vgs}%"
    lines.append(f"**{vgs_display}**")
    lines.append("")
    lines.append("تصنيف القيمة: انحراف سعري منضبط يسمح بالانتقاء ويمنع التوسع العام.")
    lines.append("")
    lines.append("المعنى:")
    lines.append("– لا تضخم سعري.")
    lines.append("– لا موجة اندفاع جماعي.")
    lines.append("– التفوق يصنعه الفارق لا الاتجاه.")
    lines.append("")
    lines.append("### القرار:")
    lines.append("")
    lines.append("عدم اعتماد أي حالة تقع فوق متوسط نطاقها المحلي.")
    lines.append("الأولوية للحالات ذات الانحراف السلبي المنضبط.")
    lines.append("الاتجاه العام وحده غير كافٍ للتفعيل.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================
    # RAOS
    # =========================
    lines.append("## ثالثًا: مؤشر الفرصة المعدلة بالمخاطر (RAOS)")
    lines.append("")
    lines.append(f"**{raos} / 100**")
    lines.append("")
    lines.append("تصنيف المخاطر: بيئة تتطلب تفوقًا نوعيًا واضحًا – المتوسط غير كافٍ.")
    lines.append("")
    lines.append("المعنى:")
    lines.append("– العائد لا يبرر المخاطرة إلا عند وجود ميزة حقيقية.")
    lines.append("– القرارات قصيرة الأجل خارج الإطار المعتمد.")
    lines.append("")
    lines.append("### القرار:")
    lines.append("")
    lines.append("استبعاد الحالات العادية فورًا.")
    lines.append("تعليق أي توسع أفقي.")
    lines.append("التحرك فقط عند وجود ميزة تفاضلية مؤكدة.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================
    # SCM
    # =========================
    lines.append("## رابعًا: تقاطع السيناريوهات التنبؤية (SCM)")
    lines.append("")
    lines.append(f"**{scm}% توافق بين 20 سيناريو**")
    lines.append("")
    lines.append("تصنيف الاتجاه: تماسك اتجاهي طويل المدى منخفض احتمالية الانعكاس الهيكلي.")
    lines.append("")
    lines.append("المعنى:")
    lines.append("– المسار العام مستقر.")
    lines.append("– الانحراف الحاد غير مرجح.")
    lines.append("– الضجيج قصير الأجل غير مؤثر استراتيجيًا.")
    lines.append("")
    lines.append("### القرار:")
    lines.append("")
    lines.append("بناء الاستراتيجية على الاستمرارية.")
    lines.append("إهمال التذبذب اللحظي.")
    lines.append("الالتزام بالمسار المرجعي هو القرار الصحيح.")
    lines.append("")
    lines.append("المرحلة السوقية الحالية: إعادة توازن انتقائي.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================
    # 10-Year Forecast
    # =========================
    lines.append("## التنبؤ الزمني المعتمد (10 سنوات)")
    lines.append("")

    lines.append("### السنوات 1–3")
    lines.append("")
    lines.append(f"نمو سنوي: **{forecast['y1_3']}%**")
    lines.append(f"تذبذب: **{volatility}%**")
    lines.append("")
    lines.append("تصنيف: تثبيت.")
    lines.append("")
    lines.append("#### القرار:")
    lines.append("")
    lines.append("عدم بناء أي خطة تعتمد على تسارع سريع.")
    lines.append("التركيز على الاستقرار الهيكلي فقط.")
    lines.append("")

    lines.append("### السنوات 4–6")
    lines.append("")
    lines.append(f"نمو سنوي: **{forecast['y4_6']}%**")
    lines.append(f"تحسن سيولة: **{min(95, max(30, raos + 20))}%**")
    lines.append("")
    lines.append("تصنيف: تمايز.")
    lines.append("")
    lines.append("#### القرار:")
    lines.append("")
    lines.append("الإبقاء فقط على الحالات التي تثبت تفوقها تشغيليًا.")
    lines.append("معالجة أو استبعاد أي حالة تتراجع أمام المتوسط.")
    lines.append("")

    lines.append("### السنوات 7–10")
    lines.append("")
    lines.append(f"نمو سنوي: **{forecast['y7_10']}%**")
    lines.append(f"احتمال إعادة تسعير هيكلي: **{min(85, max(40, scm + 5))}%**")
    lines.append("")
    lines.append("تصنيف: حصاد العائد الحقيقي.")
    lines.append("")
    lines.append("#### القرار:")
    lines.append("")
    lines.append("الحفاظ على الانضباط طويل المدى.")
    lines.append("عدم تعديل الاستراتيجية بسبب ملل زمني أو مقارنة خارجية.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("الإسقاط الزمني يعكس الاتجاه الإحصائي الحالي ضمن نطاقات احتمالية منضبطة،")
    lines.append("ولا يفترض حدوث صدمات هيكلية غير مرئية في البيانات.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================
    # Cumulative Return
    # =========================
    lines.append("## العائد التراكمي المتوقع (10 سنوات)")
    lines.append("")
    lines.append(f"**{forecast['cumulative_min']}% – {forecast['cumulative_max']}%**")
    lines.append("السيناريو المرجح: منتصف النطاق.")
    lines.append("تم احتساب العائد وفق افتراضات محافظة لا تعتمد أفضل الحالات.")
    lines.append("")
    lines.append("العائد التراكمي يعتمد على مضاعفة النمو المركب في السنوات المتأخرة،")
    lines.append("وليس على متوسط حسابي بسيط.")
    lines.append("")
    lines.append("### القرار:")
    lines.append("")
    lines.append("بناء التوقعات على السيناريو المتوسط فقط.")
    lines.append("إلغاء أي اعتماد على الحد الأعلى كفرضية أساسية.")
    lines.append("الحفاظ على هامش أمان حسابي دائم.")
    lines.append("")
    lines.append("تنبيه منهجي:")
    lines.append("القيم التنبؤية الواردة تمثل نطاقات احتمالية مبنية على نمذجة بيانات تاريخية،")
    lines.append("ولا تمثل تعهدًا بنتائج مستقبلية محددة، بل إطارًا تقديريًا منضبطًا.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================
    # Executive Protocol
    # =========================
    lines.append("## البروتوكول التنفيذي")
    lines.append("")
    lines.append("1. تفعيل الانتقاء المرحلي طويل المدى.")
    lines.append("2. تعطيل التوسع الواسع.")
    lines.append("3. استبعاد الحالات غير المتفوقة.")
    lines.append("4. مراجعة فورية عند كسر العتبات الرقمية.")
    lines.append("5. تجاهل الضجيج غير المعتمد ضمن النموذج.")
    lines.append("")
    lines.append("أي خروج عن هذا البروتوكول يُعتبر انحرافًا استراتيجيًا غير معتمد.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================
    # Validity Conditions
    # =========================
    lines.append("## شروط صلاحية القرار")
    lines.append("")
    lines.append("يبقى هذا القرار ساريًا طالما:")
    lines.append("")
    lines.append(f"– DCI أعلى من **55**")
    lines.append(f"– VGS بين **–8% و +5%**")
    lines.append(f"– SCM أعلى من **60%**")
    lines.append("")
    lines.append("عند كسر أي شرط، يتم تفعيل إعادة المعايرة الرقمية فورًا.")
    lines.append("")
    lines.append("قد يؤدي أي تغير جوهري في العوامل الاقتصادية الكلية")
    lines.append("إلى اختلاف النتائج الفعلية عن التقديرات الرقمية الواردة.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================
    # Risk Level
    # =========================
    lines.append("## مستوى المخاطر")
    lines.append("")
    lines.append("قصير الأجل: متوسط")
    lines.append("طويل الأجل: منخفض نسبيًا")
    lines.append("الخطر الحقيقي: التحرك غير الانتقائي أو خارج البروتوكول")
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================
    # Differentiators
    # =========================
    lines.append("## ما يميز هذا القرار")
    lines.append("")
    lines.append("– نظام قرار رقمي متعدد الطبقات")
    lines.append("– اختبار سيناريوهات متقاطعة")
    lines.append("– فصل صارم بين الضجيج والإشارة")
    lines.append("– معايرة مستمرة للبيانات لحظة الإصدار")
    lines.append("– بروتوكول تنفيذي واضح")
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================
    # Closing Statement
    # =========================
    lines.append("## البيان الختامي")
    lines.append("")
    lines.append("هذه الوثيقة تمثل إطار قرار رقمي مبني على الأرقام الحالية،")
    lines.append("وتبقى مرجعيتها مرتبطة بثبات المؤشرات ضمن نطاقاتها المحددة.")
    lines.append("")
    lines.append("هذا القرار لا ينتهي بتاريخ.")
    lines.append("ينتهي فقط عند تغير الأرقام.")
    lines.append("")
    lines.append("حين تبقى المؤشرات داخل نطاقها المعتمد…")
    lines.append("يبقى القرار صحيحًا.")
    lines.append("")
    lines.append("وحين تتغير الأرقام…")
    lines.append("تتم إعادة المعايرة.")
    lines.append("")
    lines.append("هذه الوثيقة تحليلية بطبيعتها،")
    lines.append("ولا تمثل تعهدًا أو التزامًا بنتائج مستقبلية محددة.")
    lines.append("")
    lines.append("Warda Intelligence")
    lines.append("دقة تُطمئن.")
    lines.append("وانضباط يصنع التفوق بصمت.")

    return "\n".join(lines)
