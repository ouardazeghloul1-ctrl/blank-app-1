# =========================================
# Executive Predictive Decision Engine
# Warda Intelligence – Diamond Version
# =========================================
# ملاحظة معمارية:
# الخلاصة التنفيذية للقرار هي مظلة موحدة لكل الباقات.
# يختلف عمق المؤشرات والتنبؤات حسب مستوى الباقة، دون تغيير هيكل القرار.
# =========================================

# TODO: سيتم استخدام SmartOpportunityFinder لاحقاً في تحليل الفرص المتقدم
# from smart_opportunities import SmartOpportunityFinder
from gold_decision_engine import generate_gold_decision_metrics
from decision_terminology import TERMS
import numpy as np
import pandas as pd

# =========================================
# تكوين الباقات - يتحكم في عمق المحتوى المعروض
# =========================================
PACKAGE_CONFIG = {
    "free": {
        "name": "مجانية",
        "forecast_years": 0,
        "show_dci": True,
        "show_vgs": True,
        "show_raos": False,
        "show_scm": False,
        "show_10year_forecast": False,
        "show_cumulative_return": False,
        "show_protocol": False,
        "show_validity_conditions": False,
        "show_risk_level": True,
        "show_differentiators": False,
        "executive_depth": "basic",
        "scm_title": "تقاطع السيناريوهات التحليلية"
    },
    "silver": {
        "name": "فضية",
        "forecast_years": 1.5,
        "show_dci": True,
        "show_vgs": True,
        "show_raos": True,
        "show_scm": True,
        "show_10year_forecast": False,
        "show_cumulative_return": False,
        "show_protocol": False,
        "show_validity_conditions": False,
        "show_risk_level": True,
        "show_differentiators": True,
        "executive_depth": "intermediate",
        "scm_title": "تقاطع السيناريوهات التحليلية"
    },
    "gold": {
        "name": "ذهبية",
        "forecast_years": 5,
        "show_dci": True,
        "show_vgs": True,
        "show_raos": True,
        "show_scm": True,
        "show_10year_forecast": False,
        "show_cumulative_return": True,
        "show_protocol": True,
        "show_validity_conditions": False,
        "show_risk_level": True,
        "show_differentiators": True,
        "executive_depth": "advanced",
        "scm_title": "تقاطع السيناريوهات التنبؤية"
    },
    "diamond": {
        "name": "ماسية",
        "forecast_years": 7,
        "show_dci": True,
        "show_vgs": True,
        "show_raos": True,
        "show_scm": True,
        "show_10year_forecast": False,
        "show_cumulative_return": True,
        "show_protocol": True,
        "show_validity_conditions": True,
        "show_risk_level": True,
        "show_differentiators": True,
        "executive_depth": "strategic",
        "scm_title": "تقاطع السيناريوهات التنبؤية"
    },
    "diamond_plus": {
        "name": "ماسية متميزة",
        "forecast_years": 10,
        "show_dci": True,
        "show_vgs": True,
        "show_raos": True,
        "show_scm": True,
        "show_10year_forecast": True,
        "show_cumulative_return": True,
        "show_protocol": True,
        "show_validity_conditions": True,
        "show_risk_level": True,
        "show_differentiators": True,
        "executive_depth": "comprehensive",
        "scm_title": "تقاطع السيناريوهات التنبؤية"
    }
}

def safe_pct(x, default=0.0):
    try:
        return round(float(x * 100), 2)
    except Exception:
        return default

def format_forecast_period(years):
    """تنسيق فترة التنبؤ بشكل readable للمستخدم"""
    if years == 0:
        return ""
    elif years == 1.5:
        return "18 شهراً"
    elif years == int(years):
        return f"{int(years)} سنوات"
    else:
        return f"{years} سنوات"

def compute_forecast(real_data: pd.DataFrame, years=10, scm=100):
    """
    حساب تنبؤ زمني مبني فقط على البيانات الحية
    مع إمكانية تحديد عدد السنوات حسب الباقة
    مع تأثير SCM على النمو المتوقع
    
    تم التحديث: استخدام معدل النمو المركب السنوي الحقيقي (CAGR)
    بدلاً من تحويل النمو الشهري إلى سنوي بطريقة أسية
    تم التحديث: سقف مؤسسي محافظ 18% كحد أقصى و -10% كحد أدنى
    """
    # تهيئة قيم افتراضية آمنة
    forecast = None
    forecast_error = None
    
    if real_data is None or real_data.empty or "price" not in real_data.columns:
        raise ValueError("لا يمكن حساب التنبؤ بدون بيانات سعر حقيقية.")

    if "date" in real_data.columns:
        real_data = real_data.dropna(subset=["date"]).sort_values("date")
    
    prices = real_data["price"].dropna()
    
    if len(prices) < 3:
        raise ValueError("البيانات غير كافية لحساب التنبؤ (أقل من 3 نقاط سعرية).")
    
    # ============================================
    # ✅ حساب النمو السنوي الحقيقي (CAGR)
    # ============================================
    # البيانات مرتبة زمنياً بالفعل من الخطوة السابقة
    prices_sorted = prices  # prices مأخوذة من real_data المرتبة
    first_price = prices_sorted.iloc[0]
    last_price = prices_sorted.iloc[-1]
    
    # حساب عدد السنوات الفعلية بين أول وآخر صفقة
    years_diff = 1.0  # قيمة افتراضية
    
    if "date" in real_data.columns:
        dates = pd.to_datetime(real_data["date"], errors="coerce").dropna()
        if len(dates) >= 2:
            days_diff = (dates.max() - dates.min()).days
            years_diff = max(days_diff / 365, 0.25)  # حد أدنى 3 أشهر
    
    # معدل النمو المركب السنوي (CAGR)
    if first_price > 0 and last_price > 0:
        annual_growth = (last_price / first_price) ** (1 / years_diff) - 1
    else:
        annual_growth = 0.02  # 2% افتراضي
    
    # سقف مؤسسي محافظ (18% كحد أقصى، -10% كحد أدنى)
    annual_growth = max(min(annual_growth, 0.18), -0.10)
    
    # تقليل النمو إذا كان SCM ضعيف (فقط إذا كان النمو إيجابياً)
    if annual_growth > 0:
        if scm < 50:
            annual_growth *= 0.7
        elif scm < 60:
            annual_growth *= 0.85
    
    # ضبط النمو إذا كان الاتجاه ضعيفاً للسنوات الطويلة
    if years >= 5 and annual_growth > 0.10:
        annual_growth = min(annual_growth, 0.12)
    
    # ============================================
    # ✅ حساب التذبذب بشكل آمن
    # ============================================
    volatility_raw = prices.pct_change().dropna().std()
    if pd.notna(volatility_raw):
        volatility_raw = min(volatility_raw, 0.30)  # سقف 30%
    else:
        volatility_raw = 0.05  # 5% افتراضي
    
    volatility = round(volatility_raw * 100, 2)
    volatility = max(volatility, 3.0)  # حد أدنى 3%

    # ============================================
    # تقسيم حسب عدد السنوات المطلوبة
    # ============================================
    if years <= 2:
        short_term = safe_pct(annual_growth * 0.9)
        return {
            "short_term": short_term,
            "medium_term": 0.0,
            "long_term": 0.0,
            "cumulative_min": safe_pct((1 + annual_growth * 0.7) ** years - 1),
            "cumulative_max": safe_pct((1 + annual_growth * 1.1) ** years - 1),
            "volatility": volatility
        }
    elif years <= 5:
        short_term = safe_pct(annual_growth * 0.8)
        medium_term = safe_pct(annual_growth * 1.0)
        return {
            "short_term": short_term,
            "medium_term": medium_term,
            "long_term": 0.0,
            "cumulative_min": safe_pct((1 + annual_growth * 0.6) ** years - 1),
            "cumulative_max": safe_pct((1 + annual_growth * 1.1) ** years - 1),
            "volatility": volatility
        }
    else:
        short_term = safe_pct(annual_growth * 0.7)
        medium_term = safe_pct(annual_growth * 0.9)
        long_term = safe_pct(annual_growth * 1.0)  # نفس المعدل السنوي دون تضخيم
        return {
            "short_term": short_term,
            "medium_term": medium_term,
            "long_term": long_term,
            "cumulative_min": safe_pct((1 + annual_growth * 0.6) ** years - 1),
            "cumulative_max": safe_pct((1 + annual_growth * 0.9) ** years - 1),
            "volatility": volatility
        }

def get_decision_state(dci, vgs, raos, scm):
    """
    تحديد حالة القرار بناءً على المؤشرات الرقمية الفعلية
    """
    if dci >= 70 and vgs <= 5 and vgs >= -8 and raos >= 60 and scm >= 65:
        return "positive"
    elif dci <= 45 or vgs > 8 or vgs < -12 or raos <= 40 or scm <= 50:
        return "negative"
    else:
        return "neutral"

def generate_executive_summary(user_info, market_data, real_data, package):
    """
    الخلاصة التنفيذية للقرار – Warda Intelligence
    يتم التحكم في عمق المحتوى حسب الباقة المحددة
    القرار الفعلي يعتمد على المؤشرات وليس على قوالب ثابتة
    """
    
    if not package:
        raise ValueError("Package must be explicitly provided.")
    
    if package not in PACKAGE_CONFIG:
        raise ValueError(
            f"Invalid package '{package}'. "
            f"Allowed: {list(PACKAGE_CONFIG.keys())}"
        )
    
    if real_data is None or real_data.empty:
        return (
            f"{TERMS['DECISION']['label']} – Warda Intelligence\n\n"
            "تعذر توليد الخلاصة لعدم توفر بيانات سوقية حقيقية."
        )

    # =========================
    # إعدادات الباقة
    # =========================
    config = PACKAGE_CONFIG.get(package, PACKAGE_CONFIG["free"])
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
    # تحديد حالة القرار الفعلية
    # =========================
    decision_state = get_decision_state(dci, vgs, raos, scm)

    # =========================
    # Forecast (نحسب فقط إذا كانت الباقة تدعم التنبؤ)
    # =========================
    forecast = None
    forecast_error = None
    
    if config["forecast_years"] > 0:
        try:
            forecast = compute_forecast(real_data, config["forecast_years"], scm)
        except ValueError as e:
            forecast_error = str(e)

    # =========================
    # BUILD EXECUTIVE SUMMARY
    # =========================
    lines = []

    # =========================
    # العنوان الرئيسي (موحد لجميع الباقات)
    # =========================
    lines.append(TERMS['DECISION']['label'])
    lines.append("")
    lines.append("Warda Intelligence")
    lines.append("")
    lines.append(f"الإصدار التنفيذي - الباقة {config['name']}")
    lines.append("")
    
    # إصلاح المرجعية مع حماية النصوص القصيرة
    city_code = city[:3] if len(city) >= 3 else city
    prop_code = property_type[:3] if len(property_type) >= 3 else property_type
    ref_id = f"WI-{city_code}-{prop_code}-{pd.Timestamp.now().strftime('%Y%m%d%H%M')}"
    lines.append(f"رقم المرجعية: {ref_id}")
    
    lines.append(f"نطاق التطبيق: {property_type} – {city}")
    # ✅ نص دقيق قانونياً واستثمارياً
    lines.append("مصدر البيانات: صفقات عقارية فعلية منفذة في السوق وقت التحليل،")
    lines.append("تمت معالجتها كمياً وفق نموذج Warda Intelligence.")
    lines.append("")
    lines.append("تم اشتقاق هذا القرار من نموذج Warda Intelligence Core Model")
    lines.append("---")
    lines.append("")

    # =========================
    # DCI (يظهر للجميع لكن بمستويات مختلفة)
    # =========================
    if config["show_dci"]:
        lines.append(f"أولاً: {TERMS['DCI']['label']} (DCI)")
        lines.append("")
        lines.append(f"{dci} / 100")
        lines.append("")
        
        if config["executive_depth"] == "basic":
            if dci >= 60:
                lines.append("تصنيف الحالة: استقرار كافٍ للدراسة.")
            else:
                lines.append("تصنيف الحالة: يحتاج مراجعة قبل التحرك.")
            lines.append("")
            lines.append("التوجه:")
            if dci >= 60:
                lines.append("إمكانية دراسة التحرك ضمن هامش أمان.")
            else:
                lines.append("الدراسة فقط دون تنفيذ.")
        else:
            if dci >= 70:
                lines.append("تصنيف الحالة: استقرار كافٍ للتنفيذ طويل المدى ضمن هامش أمان مقبول.")
            elif dci >= 55:
                lines.append("تصنيف الحالة: استقرار متوسط يتطلب انتقاءً دقيقاً.")
            else:
                lines.append("تصنيف الحالة: غير مستقر كافياً للتنفيذ المباشر.")
            
            lines.append("")
            lines.append("المعنى التنفيذي:")
            if dci >= 70:
                lines.append("البيانات ضمن نطاق الصلاحية المعتمد.")
                lines.append("النموذج يعمل داخل حدود دقة مستقرة.")
                lines.append("عدم اليقين طبيعي وغير هيكلي.")
            elif dci >= 55:
                lines.append("البيانات ضمن النطاق الآمن نسبياً.")
                lines.append("يتطلب فحصاً أدق للحالات الفردية.")
            else:
                lines.append("البيانات خارج نطاق الصلاحية المعتمد.")
                lines.append("النموذج يحذّر من التحرك المباشر.")
            
            lines.append("")
            lines.append("القرار:")

            if decision_state == "positive":
                lines.append("تفعيل الاستراتيجية طويلة المدى الآن.")
                lines.append("عدم تأجيل القرار بدافع الغموض.")

            elif decision_state == "neutral":
                lines.append("تفعيل الاستراتيجية بشرط الانتقاء الصارم.")
                lines.append("عدم التوسع الأفقي.")

            else:
                lines.append("تعليق التحرك المباشر.")
                lines.append("الاقتصار على الدراسة فقط.")

                # ✅ تفسير السبب عند وجود DCI مرتفع لكن SCM منخفض
                if dci >= 65 and scm < 50:
                    lines.append("")
                    lines.append("ملاحظة تفسيرية:")
                    lines.append("رغم قوة موثوقية البيانات،")
                    lines.append("فإن ضعف تقاطع السيناريوهات يقلل وضوح الاتجاه العام،")
                    lines.append("مما يبرر تعليق التنفيذ حتى تحسن مؤشر الاتجاه.")
            
            if config["executive_depth"] in ["strategic", "comprehensive"] and decision_state == "positive":
                lines.append("منع أي تحرك عشوائي خارج إطار الانتقاء.")
        
        lines.append("")
        lines.append("---")
        lines.append("")

    # =========================
    # VGS (يظهر للجميع)
    # =========================
    if config["show_vgs"]:
        lines.append(f"ثانياً: {TERMS['VGS']['label']} (VGS)")
        lines.append("")
        
        # إصلاح عرض VGS لمعالجة حالة الصفر
        if vgs > 0:
            vgs_display = f"+{vgs}%"
        elif vgs < 0:
            vgs_display = f"{vgs}%"
        else:
            vgs_display = "0%"
        
        lines.append(f"{vgs_display}")
        lines.append("")
        
        if config["executive_depth"] == "basic":
            if abs(vgs) < 5:
                lines.append("تصنيف القيمة: انحراف سعري منضبط.")
            else:
                lines.append("تصنيف القيمة: انحراف سعري يحتاج مراجعة.")
            lines.append("")
            lines.append("التوجه:")
            lines.append("التركيز على دراسة العقارات ذات التسعير المناسب.")
        else:
            if abs(vgs) < 5:
                lines.append("تصنيف القيمة: انحراف سعري منضبط يسمح بالانتقاء ويمنع التوسع العام.")
            elif vgs < 0:
                lines.append("تصنيف القيمة: انحراف سلبي يدعم الانتقاء الانتقائي.")
            else:
                lines.append("تصنيف القيمة: انحراف إيجابي يتطلب حذراً إضافياً.")
            
            lines.append("")
            lines.append("المعنى:")
            if abs(vgs) < 5:
                lines.append("لا تضخم سعري.")
                lines.append("لا موجة اندفاع جماعي.")
            elif vgs < 0:
                lines.append("فرص انتقائية متاحة.")
                lines.append("أسعار تحت المتوسط المحلي.")
            else:
                lines.append("ارتفاع نسبي في الأسعار.")
                lines.append("الانتقاء يصبح أكثر أهمية.")
            
            if config["executive_depth"] in ["advanced", "strategic", "comprehensive"] and abs(vgs) < 5:
                lines.append("التفوق يصنعه الفارق لا الاتجاه.")
            lines.append("")
            lines.append("القرار:")
            if vgs <= 5 and vgs >= -8:
                lines.append("عدم اعتماد أي حالة تقع فوق متوسط نطاقها المحلي.")
                lines.append("الأولوية للحالات ذات الانحراف السلبي المنضبط.")
            else:
                lines.append("استبعاد الحالات غير المطابقة للمعايير.")
                lines.append("الانتظار حتى تحسن المؤشر.")
            
            if config["executive_depth"] in ["strategic", "comprehensive"] and abs(vgs) < 5:
                lines.append("الاتجاه العام وحده غير كافٍ للتفعيل.")
        
        lines.append("")
        lines.append("---")
        lines.append("")

    # =========================
    # RAOS (للباقات الفضية فأعلى)
    # =========================
    if config["show_raos"]:
        lines.append(f"ثالثاً: {TERMS['RAOS']['label']} (RAOS)")
        lines.append("")
        lines.append(f"{raos} / 100")
        lines.append("")
        
        if config["executive_depth"] == "intermediate":
            if raos >= 60:
                lines.append("تصنيف المخاطر: منخفض.")
            elif raos >= 40:
                lines.append("تصنيف المخاطر: متوسط.")
            else:
                lines.append("تصنيف المخاطر: مرتفع.")
            lines.append("")
            lines.append("التوجه:")
            if raos >= 60:
                lines.append("انتقاء الفرص بحذر.")
            else:
                lines.append("الدراسة فقط دون تنفيذ.")
        else:
            if raos >= 70:
                lines.append("تصنيف المخاطر: بيئة آمنة نسبياً للانتقاء.")
            elif raos >= 50:
                lines.append("تصنيف المخاطر: بيئة تتطلب تفوقاً نوعياً واضحاً – المتوسط غير كافٍ.")
            else:
                lines.append("تصنيف المخاطر: بيئة عالية المخاطر.")
            
            lines.append("")
            lines.append("المعنى:")
            if raos >= 70:
                lines.append("العائد يبرر المخاطرة.")
            elif raos >= 50:
                lines.append("العائد لا يبرر المخاطرة إلا عند وجود ميزة حقيقية.")
                lines.append("القرارات قصيرة الأجل خارج الإطار المعتمد.")
            else:
                lines.append("المخاطر تفوق العائد المحتمل.")
                lines.append("السوق غير مناسب للدخول حالياً.")
            
            lines.append("")
            lines.append("القرار:")
            if raos >= 70:
                lines.append("تفعيل الانتقاء مع الإبقاء على المعايير.")
            elif raos >= 50:
                lines.append("استبعاد الحالات العادية فوراً.")
                lines.append("تعليق أي توسع أفقي.")
            else:
                lines.append("تعليق أي تحرك.")
                lines.append("الاقتصار على المراقبة فقط.")
            
            if config["executive_depth"] in ["strategic", "comprehensive"] and raos >= 70:
                lines.append("التحرك فقط عند وجود ميزة تفاضلية مؤكدة.")
        
        lines.append("")
        lines.append("---")
        lines.append("")

    # =========================
    # SCM (للباقات الفضية فأعلى) - مع عنوان ديناميكي
    # =========================
    if config["show_scm"]:
        lines.append(f"رابعاً: {config['scm_title']} (SCM)")
        lines.append("")
        lines.append(f"{scm}% {TERMS['SCM']['display']}")
        lines.append("توافق بين 20 سيناريو")
        lines.append("")
        
        if config["executive_depth"] == "intermediate":
            if scm >= 60:
                lines.append("")
                lines.append("تصنيف الاتجاه: مستقر.")
            else:
                lines.append("")
                lines.append("تصنيف الاتجاه: غير مستقر.")
            lines.append("")
            lines.append("التوجه:")
            if scm >= 60:
                lines.append("بناء الاستراتيجية على الاستمرارية.")
            else:
                lines.append("الحذر من التقلبات.")
        else:
            if scm >= 70:
                lines.append("تصنيف الاتجاه: تماسك اتجاهي طويل المدى منخفض احتمالية الانعكاس الهيكلي.")
            elif scm >= 55:
                lines.append("تصنيف الاتجاه: استقرار متوسط قابل للانعكاس.")
            else:
                lines.append("تصنيف الاتجاه: عدم استقرار اتجاهي.")
            
            lines.append("")
            lines.append("المعنى:")
            if scm >= 70:
                lines.append("المسار العام مستقر.")
                lines.append("الانحراف الحاد غير مرجح.")
                lines.append("الضجيج قصير الأجل غير مؤثر استراتيجياً.")
            elif scm >= 55:
                lines.append("المسار العام مستقر نسبياً.")
                lines.append("احتمال انعكاس متوسط.")
            else:
                lines.append("المسار العام غير واضح.")
                lines.append("احتمال تغير اتجاهي مرتفع.")
            
            lines.append("")
            lines.append("القرار:")
            if scm >= 70:
                lines.append("بناء الاستراتيجية على الاستمرارية.")
                lines.append("إهمال التذبذب اللحظي.")
            elif scm >= 55:
                lines.append("الانتظار لتأكد الاتجاه.")
                lines.append("عدم الالتزام الكامل بالمسار.")
            else:
                lines.append("تعليق القرارات طويلة المدى.")
                lines.append("الاقتصار على المدى القصير فقط.")
            
            if config["executive_depth"] in ["strategic", "comprehensive"] and scm >= 70:
                lines.append("الالتزام بالمسار المرجعي هو القرار الصحيح.")
                lines.append("")
                lines.append("المرحلة السوقية الحالية: إعادة توازن انتقائي.")
        
        lines.append("")
        lines.append("---")
        lines.append("")

    # =========================
    # Forecast حسب الباقة
    # =========================
    if config["forecast_years"] > 0 and forecast is not None:
        forecast_period = format_forecast_period(config["forecast_years"])
        
        if config["forecast_years"] <= 2:
            lines.append(f"التنبؤ الزمني ({forecast_period})")
            lines.append("")
            lines.append(f"معدل النمو المتوقع: {forecast['short_term']}%")
            lines.append(f"مؤشر التذبذب: {forecast['volatility']}%")
            lines.append("")
            lines.append("التوجه:")
            if forecast['short_term'] > 0:
                lines.append("التركيز على دراسة الفرص قصيرة المدى.")
            else:
                lines.append("الحذر من الفرص قصيرة المدى.")
            
        elif config["forecast_years"] <= 5:
            lines.append(f"التنبؤ الزمني ({forecast_period})")
            lines.append("")
            lines.append("السنوات 1 – 2")
            lines.append(f"نمو: {forecast['short_term']}%")
            lines.append("")
            lines.append("السنوات 3 – 5")
            lines.append(f"نمو: {forecast['medium_term']}%")
            lines.append("")
            lines.append("القرار:")
            if forecast['medium_term'] > forecast['short_term']:
                lines.append("استراتيجية نمو متدرجة.")
            else:
                lines.append("استراتيجية ثبات مع انتقاء.")
            
        elif config["forecast_years"] <= 7:
            lines.append(f"التنبؤ الزمني ({forecast_period})")
            lines.append("")
            lines.append("المرحلة الأولى (1-3): تثبيت")
            lines.append(f"نمو: {forecast['short_term']}%")
            lines.append("")
            lines.append("المرحلة الثانية (4-7): تسارع")
            lines.append(f"نمو: {forecast['medium_term']}%")
            
        elif config["show_10year_forecast"]:
            lines.append("التنبؤ الزمني المعتمد (10 سنوات)")
            lines.append("")
            lines.append("السنوات 1 – 3")
            lines.append(f"نمو سنوي: {forecast['short_term']}%")
            lines.append(f"تذبذب: {forecast['volatility']}%")
            lines.append("")
            lines.append("تصنيف: تثبيت.")
            lines.append("")
            lines.append("القرار:")
            lines.append("عدم بناء أي خطة تعتمد على تسارع سريع.")
            lines.append("التركيز على الاستقرار الهيكلي فقط.")
            lines.append("")
            lines.append("السنوات 4 – 6")
            lines.append(f"نمو سنوي: {forecast['medium_term']}%")
            lines.append(f"تحسن سيولة: {min(95, max(30, raos + 20))}%")
            lines.append("")
            lines.append("تصنيف: تمايز.")
            lines.append("")
            lines.append("القرار:")
            lines.append("الإبقاء فقط على الحالات التي تثبت تفوقها تشغيلياً.")
            lines.append("معالجة أو استبعاد أي حالة تتراجع أمام المتوسط.")
            lines.append("")
            lines.append("السنوات 7 – 10")
            lines.append(f"نمو سنوي: {forecast['long_term']}%")
            lines.append(f"احتمال إعادة تسعير هيكلي: {min(85, max(40, scm + 5))}%")
            lines.append("")
            lines.append("تصنيف: حصاد العائد الحقيقي.")
            lines.append("")
            lines.append("القرار:")
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
    elif config["forecast_years"] > 0 and forecast is None and forecast_error is not None:
        lines.append("التنبؤ الزمني")
        lines.append("")
        lines.append(f"⚠️ {forecast_error}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # =========================
    # Cumulative Return
    # =========================
    if config["show_cumulative_return"] and forecast is not None:
        lines.append("العائد التراكمي المتوقع")
        lines.append("")
        lines.append(f"{forecast['cumulative_min']}% – {forecast['cumulative_max']}%")
        
        if config["executive_depth"] in ["advanced", "strategic", "comprehensive"]:
            lines.append("السيناريو المرجح: منتصف النطاق.")
            lines.append("تم احتساب العائد وفق افتراضات محافظة لا تعتمد أفضل الحالات.")
            lines.append("")
            lines.append("العائد التراكمي يعتمد على مضاعفة النمو المركب.")
        
        lines.append("")
        lines.append("القرار:")
        lines.append("بناء التوقعات على السيناريو المتوسط فقط.")
        
        if config["executive_depth"] in ["strategic", "comprehensive"]:
            lines.append("إلغاء أي اعتماد على الحد الأعلى كفرضية أساسية.")
            lines.append("الحفاظ على هامش أمان حسابي دائم.")
        
        lines.append("")
        lines.append("---")
        lines.append("")

    # =========================
    # Executive Protocol
    # =========================
    if config["show_protocol"]:
        lines.append(TERMS['PROTOCOL']['label'])
        lines.append("")
        
        if decision_state == "positive":
            if config["executive_depth"] == "advanced":
                lines.append("1. تفعيل الانتقاء المرحلي.")
                lines.append("2. تعطيل التوسع الواسع.")
                lines.append("3. استبعاد الحالات غير المتفوقة.")
            else:
                lines.append("1. تفعيل الانتقاء المرحلي طويل المدى.")
                lines.append("2. تعطيل التوسع الواسع.")
                lines.append("3. استبعاد الحالات غير المتفوقة.")
                lines.append("4. مراجعة فورية عند كسر العتبات الرقمية.")
                lines.append("5. تجاهل الضجيج غير المعتمد ضمن النموذج.")
                lines.append("")
                lines.append("أي خروج عن هذا البروتوكول يُعتبر انحرافاً استراتيجياً غير معتمد.")
        elif decision_state == "neutral":
            if config["executive_depth"] == "advanced":
                lines.append("1. الدراسة فقط دون تنفيذ.")
                lines.append("2. انتظار تحسن المؤشرات.")
            else:
                lines.append("1. تعليق التنفيذ المباشر.")
                lines.append("2. مواصلة المراقبة.")
                lines.append("3. عدم الالتزام بأي خطة طويلة المدى حالياً.")
        else:
            if config["executive_depth"] == "advanced":
                lines.append("1. تعليق جميع القرارات.")
                lines.append("2. العودة للدراسة فقط.")
            else:
                lines.append("1. وقف أي تحرك جديد.")
                lines.append("2. مراجعة شاملة للمؤشرات.")
                lines.append("3. إعادة التقييم عند تحسن الظروف.")
        
        lines.append("")
        lines.append("---")
        lines.append("")

    # =========================
    # Validity Conditions
    # =========================
    if config["show_validity_conditions"]:
        lines.append("شروط صلاحية القرار")
        lines.append("")
        lines.append("يبقى هذا القرار سارياً طالما:")
        lines.append("")
        lines.append(f"{TERMS['DCI']['label']} أعلى من 55")
        lines.append(f"{TERMS['VGS']['label']} بين –8% و +5%")
        
        # تنبيه إذا كان VGS خارج النطاق
        if vgs < -8 or vgs > 5:
            lines.append("")
            lines.append("تنبيه:")
            lines.append("فجوة القيمة خارج النطاق المعتمد لشروط الصلاحية.")
        
        # إظهار شرط SCM وتنبيهه لكل الباقات التي تظهر SCM
        if config["show_scm"]:
            lines.append(f"{TERMS['SCM']['display']} أعلى من 60%")
            
            # تنبيه إذا كان SCM أقل من 60%
            if scm < 60:
                lines.append("")
                lines.append("تنبيه:")
                lines.append("نسبة توافق السيناريوهات أقل من الحد الأدنى المعتمد.")
        
        if config["executive_depth"] == "comprehensive":
            lines.append("")
            lines.append("عند كسر أي شرط، يتم تفعيل إعادة المعايرة الرقمية فوراً.")
        
        lines.append("")
        lines.append("---")
        lines.append("")

    # =========================
    # Risk Level (موحد)
    # =========================
    if config["show_risk_level"]:
        lines.append("مستوى المخاطر")
        lines.append("")
        
        if raos >= 70:
            risk_text = "منخفض"
        elif raos >= 50:
            risk_text = "متوسط"
        else:
            risk_text = "مرتفع"
        
        if config["executive_depth"] == "basic":
            lines.append(f"مخاطر السوق: {risk_text}")
            if risk_text == "منخفض":
                lines.append("ينصح بدراسة السوق بحذر.")
            elif risk_text == "متوسط":
                lines.append("ينصح بدراسة السوق بحذر.")
            else:
                lines.append("ينصح بتأجيل الدخول.")
        else:
            lines.append(f"قصير الأجل: {risk_text}")
            if raos >= 70:
                lines.append("طويل الأجل: منخفض نسبياً")
            elif raos >= 50:
                lines.append("طويل الأجل: متوسط")
            else:
                lines.append("طويل الأجل: مرتفع")
            
            if config["executive_depth"] in ["strategic", "comprehensive"]:
                lines.append("الخطر الحقيقي: التحرك غير الانتقائي أو خارج البروتوكول")
        
        lines.append("")
        lines.append("---")
        lines.append("")

    # =========================
    # Differentiators
    # =========================
    if config["show_differentiators"]:
        lines.append("ما يميز هذا القرار")
        lines.append("")
        
        if config["executive_depth"] == "intermediate":
            lines.append("نظام قرار رقمي متكامل")
            lines.append("تحليل دقيق للبيانات")
        else:
            lines.append("نظام قرار رقمي متعدد الطبقات")
            lines.append("اختبار سيناريوهات متقاطعة")
            lines.append("فصل صارم بين الضجيج والإشارة")
            if config["executive_depth"] in ["strategic", "comprehensive"]:
                lines.append("معايرة مستمرة للبيانات لحظة الإصدار")
                lines.append("بروتوكول تنفيذي واضح")
        
        lines.append("")
        lines.append("---")
        lines.append("")

    # =========================
    # Closing Statement (موحد مع اختلاف بسيط حسب حالة القرار)
    # =========================
    lines.append("البيان الختامي")
    lines.append("")
    
    if config["executive_depth"] == "basic":
        if decision_state == "positive":
            lines.append("هذه الوثيقة تمثل إطاراً تحليلياً أولياً للقرار، مبني على الأرقام الحالية التي تدعم التحرك.")
        elif decision_state == "neutral":
            lines.append("هذه الوثيقة تمثل إطاراً تحليلياً أولياً للقرار، مبني على الأرقام الحالية التي تتطلب حذراً.")
        else:
            lines.append("هذه الوثيقة تمثل إطاراً تحليلياً أولياً للقرار، مبني على الأرقام الحالية التي تحذر من التحرك.")
        lines.append("")
        lines.append("Warda Intelligence")
        lines.append("دقة تُطمئن.")
    else:
        if decision_state == "positive":
            lines.append("هذه الوثيقة تمثل إطار قرار رقمي مبني على الأرقام الحالية التي تدعم التحرك،")
            lines.append("وتبقى مرجعيتها مرتبطة بثبات المؤشرات ضمن نطاقاتها المحددة.")
        elif decision_state == "neutral":
            lines.append("هذه الوثيقة تمثل إطار قرار رقمي مبني على الأرقام الحالية التي تتطلب انتقاءً،")
            lines.append("وتبقى مرجعيتها مرتبطة بثبات المؤشرات ضمن نطاقاتها المحددة.")
        else:
            lines.append("هذه الوثيقة تمثل إطار قرار رقمي مبني على الأرقام الحالية التي تحذر من التحرك،")
            lines.append("وتبقى مرجعيتها مرتبطة بثبات المؤشرات ضمن نطاقاتها المحددة.")
        
        lines.append("")
        lines.append("هذا القرار لا ينتهي بتاريخ.")
        lines.append("ينتهي فقط عند تغير الأرقام.")
        lines.append("")
        lines.append("حين تبقى المؤشرات داخل نطاقها المعتمد…")
        lines.append("يبقى القرار صحيحاً.")
        lines.append("")
        lines.append("وحين تتغير الأرقام…")
        lines.append("تتم إعادة المعايرة.")
        lines.append("")
        lines.append("هذه الوثيقة تحليلية بطبيعتها،")
        lines.append("ولا تمثل تعهداً أو التزاماً بنتائج مستقبلية محددة.")
        lines.append("")
        lines.append("Warda Intelligence")
        lines.append("دقة تُطمئن.")
        if config["executive_depth"] == "comprehensive":
            lines.append("وانضباط يصنع التفوق بصمت.")

    return "\n".join(lines)
