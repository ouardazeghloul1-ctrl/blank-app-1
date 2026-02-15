# =========================================
# Executive Predictive Decision Engine
# Warda Intelligence – Diamond Version
# =========================================
# ملاحظة معمارية:
# الخلاصة التنفيذية للقرار هي مظلة موحدة لكل الباقات.
# يختلف عمق المؤشرات والتنبؤات حسب مستوى الباقة، دون تغيير هيكل القرار.
# =========================================

from smart_opportunities import SmartOpportunityFinder
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

def compute_forecast(real_data: pd.DataFrame, years=10):
    """
    حساب تنبؤ زمني مبني فقط على البيانات الحية
    مع إمكانية تحديد عدد السنوات حسب الباقة
    """
    if real_data is None or real_data.empty or "price" not in real_data.columns:
        return {
            "short_term": 0.0,
            "medium_term": 0.0,
            "long_term": 0.0,
            "cumulative_min": 0.0,
            "cumulative_max": 0.0,
            "volatility": 0.0
        }

    if "date" in real_data.columns:
        real_data = real_data.sort_values("date")
    
    prices = real_data["price"].dropna()
    annual_growth = prices.pct_change().median()
    annual_growth = annual_growth if pd.notna(annual_growth) else 0.01
    volatility = safe_pct(prices.pct_change().std())

    # تقسيم حسب عدد السنوات المطلوبة
    if years <= 2:
        short_term = safe_pct(annual_growth * 0.8)
        return {
            "short_term": short_term,
            "medium_term": 0.0,
            "long_term": 0.0,
            "cumulative_min": safe_pct((1 + annual_growth * 0.7) ** years - 1),
            "cumulative_max": safe_pct((1 + annual_growth * 1.2) ** years - 1),
            "volatility": volatility
        }
    elif years <= 5:
        short_term = safe_pct(annual_growth * 0.7)
        medium_term = safe_pct(annual_growth * 1.1)
        return {
            "short_term": short_term,
            "medium_term": medium_term,
            "long_term": 0.0,
            "cumulative_min": safe_pct((1 + annual_growth * 0.6) ** years - 1),
            "cumulative_max": safe_pct((1 + annual_growth * 1.2) ** years - 1),
            "volatility": volatility
        }
    else:
        short_term = safe_pct(annual_growth * 0.7)
        medium_term = safe_pct(annual_growth * 1.2)
        long_term = safe_pct(annual_growth * 1.7)
        return {
            "short_term": short_term,
            "medium_term": medium_term,
            "long_term": long_term,
            "cumulative_min": safe_pct((1 + annual_growth * 0.6) ** years - 1),
            "cumulative_max": safe_pct((1 + annual_growth * 1.1) ** years - 1),
            "volatility": volatility
        }

def generate_executive_summary(user_info, market_data, real_data, package):
    """
    الخلاصة التنفيذية للقرار – Warda Intelligence
    يتم التحكم في عمق المحتوى حسب الباقة المحددة
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
    # Forecast
    # =========================
    forecast = compute_forecast(real_data, config["forecast_years"])

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
    lines.append(f"رقم المرجعية: WI-{city[:3]}-{property_type[:3]}-{pd.Timestamp.now().strftime('%Y%m')}")
    lines.append(f"نطاق التطبيق: {property_type} – {city}")
    lines.append(f"مصدر البيانات: بيانات سوقية آنية تم جمعها ومعالجتها لحظة إصدار المرجعية.")
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
            lines.append("تصنيف الحالة: استقرار كافٍ للدراسة.")
            lines.append("")
            lines.append("التوجه:")
            lines.append("إمكانية دراسة التحرك ضمن هامش أمان.")
        else:
            lines.append("تصنيف الحالة: استقرار كافٍ للتنفيذ طويل المدى ضمن هامش أمان مقبول.")
            lines.append("")
            lines.append("المعنى التنفيذي:")
            lines.append("البيانات ضمن نطاق الصلاحية المعتمد.")
            lines.append("النموذج يعمل داخل حدود دقة مستقرة.")
            lines.append("عدم اليقين طبيعي وغير هيكلي.")
            lines.append("")
            lines.append("القرار:")
            lines.append("تفعيل الاستراتيجية طويلة المدى الآن.")
            lines.append("عدم تأجيل القرار بدافع الغموض.")
            if config["executive_depth"] in ["strategic", "comprehensive"]:
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
        vgs_display = f"{vgs}%" if vgs < 0 else f"+{vgs}%"
        lines.append(f"{vgs_display}")
        lines.append("")
        
        if config["executive_depth"] == "basic":
            lines.append("تصنيف القيمة: انحراف سعري منضبط.")
            lines.append("")
            lines.append("التوجه:")
            lines.append("التركيز على دراسة العقارات ذات التسعير المناسب.")
        else:
            lines.append("تصنيف القيمة: انحراف سعري منضبط يسمح بالانتقاء ويمنع التوسع العام.")
            lines.append("")
            lines.append("المعنى:")
            lines.append("لا تضخم سعري.")
            lines.append("لا موجة اندفاع جماعي.")
            if config["executive_depth"] in ["advanced", "strategic", "comprehensive"]:
                lines.append("التفوق يصنعه الفارق لا الاتجاه.")
            lines.append("")
            lines.append("القرار:")
            lines.append("عدم اعتماد أي حالة تقع فوق متوسط نطاقها المحلي.")
            lines.append("الأولوية للحالات ذات الانحراف السلبي المنضبط.")
            if config["executive_depth"] in ["strategic", "comprehensive"]:
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
            lines.append("تصنيف المخاطر: مستوى متوسط.")
            lines.append("")
            lines.append("التوجه:")
            lines.append("انتقاء الفرص بحذر.")
        else:
            lines.append("تصنيف المخاطر: بيئة تتطلب تفوقاً نوعياً واضحاً – المتوسط غير كافٍ.")
            lines.append("")
            lines.append("المعنى:")
            lines.append("العائد لا يبرر المخاطرة إلا عند وجود ميزة حقيقية.")
            lines.append("القرارات قصيرة الأجل خارج الإطار المعتمد.")
            lines.append("")
            lines.append("القرار:")
            lines.append("استبعاد الحالات العادية فوراً.")
            lines.append("تعليق أي توسع أفقي.")
            if config["executive_depth"] in ["strategic", "comprehensive"]:
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
        
        if config["executive_depth"] == "intermediate":
            lines.append("")
            lines.append("تصنيف الاتجاه: مستقر.")
            lines.append("")
            lines.append("التوجه:")
            lines.append("بناء الاستراتيجية على الاستمرارية.")
        else:
            lines.append(" توافق بين 20 سيناريو")
            lines.append("")
            lines.append("تصنيف الاتجاه: تماسك اتجاهي طويل المدى منخفض احتمالية الانعكاس الهيكلي.")
            lines.append("")
            lines.append("المعنى:")
            lines.append("المسار العام مستقر.")
            lines.append("الانحراف الحاد غير مرجح.")
            lines.append("الضجيج قصير الأجل غير مؤثر استراتيجياً.")
            lines.append("")
            lines.append("القرار:")
            lines.append("بناء الاستراتيجية على الاستمرارية.")
            lines.append("إهمال التذبذب اللحظي.")
            if config["executive_depth"] in ["strategic", "comprehensive"]:
                lines.append("الالتزام بالمسار المرجعي هو القرار الصحيح.")
                lines.append("")
                lines.append("المرحلة السوقية الحالية: إعادة توازن انتقائي.")
        
        lines.append("")
        lines.append("---")
        lines.append("")

    # =========================
    # Forecast حسب الباقة
    # =========================
    if config["forecast_years"] > 0:
        forecast_period = format_forecast_period(config["forecast_years"])
        
        if config["forecast_years"] <= 2:
            lines.append(f"التنبؤ الزمني ({forecast_period})")
            lines.append("")
            lines.append(f"معدل النمو المتوقع: {forecast['short_term']}%")
            lines.append(f"مؤشر التذبذب: {forecast['volatility']}%")
            lines.append("")
            lines.append("التوجه:")
            lines.append("التركيز على دراسة الفرص قصيرة المدى.")
            
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
            lines.append("استراتيجية نمو متدرجة.")
            
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

    # =========================
    # Cumulative Return
    # =========================
    if config["show_cumulative_return"]:
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
        
        if config["executive_depth"] == "comprehensive":
            lines.append(f"{TERMS['SCM']['display']} أعلى من 60%")
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
        
        if config["executive_depth"] == "basic":
            lines.append("مخاطر السوق: متوسطة")
            lines.append("ينصح بدراسة السوق بحذر.")
        else:
            lines.append("قصير الأجل: متوسط")
            lines.append("طويل الأجل: منخفض نسبياً")
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
    # Closing Statement (موحد مع اختلاف بسيط)
    # =========================
    lines.append("البيان الختامي")
    lines.append("")
    
    if config["executive_depth"] == "basic":
        lines.append("هذه الوثيقة تمثل إطاراً تحليلياً أولياً للقرار، مبني على الأرقام الحالية.")
        lines.append("")
        lines.append("Warda Intelligence")
        lines.append("دقة تُطمئن.")
    else:
        lines.append("هذه الوثيقة تمثل إطار قرار رقمي مبني على الأرقام الحالية،")
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
