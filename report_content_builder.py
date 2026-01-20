"""
Advanced Real Estate Investment Report Builder
Version: 2.0.0 (Production)
"""

# =========================
# PACKAGES DEFINITION
# =========================
PACKAGES = {
    "free": {"name": "مجانية", "pages": 15},
    "silver": {"name": "فضية", "pages": 35},
    "gold": {"name": "ذهبية", "pages": 60},
    "diamond": {"name": "ماسية", "pages": 90},
    "diamond_plus": {"name": "ماسية متميزة", "pages": 120},
}

PACKAGE_ALIASES = {
    "مجانية": "free",
    "فضية": "silver",
    "ذهبية": "gold",
    "ماسية": "diamond",
    "ماسية متميزة": "diamond_plus",
    "free": "free",
    "silver": "silver",
    "gold": "gold",
    "diamond": "diamond",
    "diamond_plus": "diamond_plus",
}

# =========================
# CHAPTER 1 – REALISTIC SCENARIO
# =========================
def chapter_1_blocks(user_info):
    city = user_info.get("المدينة", "المدينة")
    prop = user_info.get("نوع_العقار", "العقار")

    return [
        {
            "type": "chapter_title",
            "content": f"الفصل الأول – السيناريو الواقعي لمستقبل {prop} في {city}",
            "show_in": PACKAGES.keys(),
        },
        {
            "type": "context",
            "content": "هذا الفصل يقدم قراءة واقعية للسوق بعيدًا عن التفاؤل أو التخويف.",
            "show_in": PACKAGES.keys(),
        },
        {
            "type": "analysis",
            "content": f"سوق {prop} في {city} تحكمه عوامل طلب حقيقية وسلوك استثماري متغير.",
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
        },
        {
            "type": "chart",
            "chart_key": "chapter_1_price_distribution",
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
        },
        {
            "type": "scenario",
            "content": "السيناريو الأساسي، المتفائل، والمحافظ بناءً على معطيات محلية.",
            "show_in": ["diamond", "diamond_plus"],
        },
        {
            "type": "reference_context",
            "content": "في الأسواق الناضجة، لا تُبنى القرارات على التوقع بل على القدرة على التحمل.",
            "show_in": ["diamond_plus"],
        },
        {
            "type": "conclusion",
            "content": "هذا الفصل ليس توقعًا، بل إطار تفكير.",
            "show_in": PACKAGES.keys(),
        },
    ]

# =========================
# CHAPTER 2 – HIDDEN RISKS
# =========================
def chapter_2_blocks(user_info):
    city = user_info.get("المدينة", "المدينة")

    return [
        {
            "type": "chapter_title",
            "content": f"الفصل الثاني – المخاطر الخفية في سوق {city}",
            "show_in": PACKAGES.keys(),
        },
        {
            "type": "analysis",
            "content": "أخطر المخاطر ليست في السعر بل في السيولة والتوقيت.",
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
        },
        {
            "type": "chart",
            "chart_key": "chapter_2_price_volatility",
            "show_in": ["gold", "diamond", "diamond_plus"],
        },
        {
            "type": "scenario",
            "content": "ماذا يحدث إذا تغيّر السياق وليس السعر؟",
            "show_in": ["diamond", "diamond_plus"],
        },
        {
            "type": "reference_context",
            "content": "الأسواق التي لا تناقش المخاطر غالبًا تسعّرها متأخرًا.",
            "show_in": ["diamond_plus"],
        },
        {
            "type": "conclusion",
            "content": "إدارة المخاطر أهم من تجنبها.",
            "show_in": PACKAGES.keys(),
        },
    ]

# =========================
# CHAPTER 3 – INVISIBLE OPPORTUNITIES
# =========================
def chapter_3_blocks(user_info):
    city = user_info.get("المدينة", "المدينة")

    return [
        {
            "type": "chapter_title",
            "content": f"الفصل الثالث – الفرص غير المرئية في {city}",
            "show_in": PACKAGES.keys(),
        },
        {
            "type": "analysis",
            "content": "الفرص لا تكون حيث ينظر الجميع.",
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
        },
        {
            "type": "chart",
            "chart_key": "chapter_3_value_map",
            "show_in": ["gold", "diamond", "diamond_plus"],
        },
        {
            "type": "scenario",
            "content": "كيف يتحول الإهمال السوقي إلى فرصة؟",
            "show_in": ["diamond", "diamond_plus"],
        },
        {
            "type": "reference_context",
            "content": "الهدوء في الأصل قد يكون علامة قوة لا ضعف.",
            "show_in": ["diamond_plus"],
        },
        {
            "type": "conclusion",
            "content": "الفرص الجيدة لا تصرخ.",
            "show_in": PACKAGES.keys(),
        },
    ]

# =========================
# CHAPTER 4 – SMART STRATEGY
# =========================
def chapter_4_blocks(user_info):
    return [
        {
            "type": "chapter_title",
            "content": "الفصل الرابع – خطة التعامل الذكي",
            "show_in": PACKAGES.keys(),
        },
        {
            "type": "analysis",
            "content": "الاستثمار علاقة طويلة لا صفقة سريعة.",
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
        },
        {
            "type": "chart",
            "chart_key": "chapter_4_action_matrix",
            "show_in": ["gold", "diamond", "diamond_plus"],
        },
        {
            "type": "scenario",
            "content": "متى تحتفظ؟ متى تحوّل؟",
            "show_in": ["diamond", "diamond_plus"],
        },
        {
            "type": "reference_context",
            "content": "أفضل الخطط مرنة لا مثالية.",
            "show_in": ["diamond_plus"],
        },
    ]

# =========================
# CHAPTER 5 – TIMING
# =========================
def chapter_5_blocks(user_info):
    return [
        {
            "type": "chapter_title",
            "content": "الفصل الخامس – التوقيت",
            "show_in": PACKAGES.keys(),
        },
        {
            "type": "analysis",
            "content": "التوقيت ليس لحظة بل نطاق.",
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
        },
        {
            "type": "chart",
            "chart_key": "chapter_5_entry_timing_signal",
            "show_in": ["gold", "diamond", "diamond_plus"],
        },
        {
            "type": "scenario",
            "content": "مخاطر الدخول في الوقت الخطأ.",
            "show_in": ["diamond", "diamond_plus"],
        },
        {
            "type": "reference_context",
            "content": "الانتظار أحيانًا قرار.",
            "show_in": ["diamond_plus"],
        },
    ]
# =========================
# CHAPTER 6 – CAPITAL DISTRIBUTION
# =========================
def chapter_6_blocks(user_info):
    return [
        {
            "type": "chapter_title",
            "content": "الفصل السادس – توزيع رأس المال",
            "show_in": PACKAGES.keys(),
        },
        {
            "type": "analysis",
            "content": "الخسائر الكبيرة لا تأتي من أصل سيئ بل من تركيز مفرط.",
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
        },
        {
            "type": "chart",
            "chart_key": "chapter_6_capital_allocation",
            "show_in": ["gold", "diamond", "diamond_plus"],
        },
        {
            "type": "scenario",
            "content": "قاعدة 10% و20% لحماية رأس المال.",
            "show_in": ["diamond", "diamond_plus"],
        },
        {
            "type": "reference_context",
            "content": "السيولة ليست ضعفًا، بل خيارًا استراتيجيًا.",
            "show_in": ["diamond_plus"],
        },
    ]

# =========================
# CHAPTER 7 – EXIT VS HOLD
# =========================
def chapter_7_blocks(user_info):
    return [
        {
            "type": "chapter_title",
            "content": "الفصل السابع – متى تخرج؟ ومتى تبقى؟",
            "show_in": PACKAGES.keys(),
        },
        {
            "type": "analysis",
            "content": "الخروج الذكي يثبت الربح.",
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
        },
        {
            "type": "chart",
            "chart_key": "chapter_7_exit_signal",
            "show_in": ["gold", "diamond", "diamond_plus"],
        },
        {
            "type": "scenario",
            "content": "الخروج الوقائي مقابل الخروج التحويلي.",
            "show_in": ["diamond", "diamond_plus"],
        },
        {
            "type": "reference_context",
            "content": "الأصل الجيد قد يصبح عبئًا إن تأخر الخروج.",
            "show_in": ["diamond_plus"],
        },
    ]

# =========================
# CHAPTER 8 – EARLY SIGNALS
# =========================
def chapter_8_blocks(user_info):
    return [
        {
            "type": "chapter_title",
            "content": "الفصل الثامن – قراءة الإشارات المبكرة",
            "show_in": PACKAGES.keys(),
        },
        {
            "type": "analysis",
            "content": "السوق يهمس قبل أن يصرخ.",
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
        },
        {
            "type": "chart",
            "chart_key": "chapter_8_signal_intensity",
            "show_in": ["gold", "diamond", "diamond_plus"],
        },
        {
            "type": "scenario",
            "content": "تغير الأسئلة أخطر من تغير الأسعار.",
            "show_in": ["diamond", "diamond_plus"],
        },
        {
            "type": "reference_context",
            "content": "السوق السعيد جدًا سوق خطير.",
            "show_in": ["diamond_plus"],
        },
    ]

# =========================
# CHAPTER 9 – DATA TO DECISION
# =========================
def chapter_9_blocks(user_info):
    return [
        {
            "type": "chapter_title",
            "content": "الفصل التاسع – تحويل البيانات إلى قرارات",
            "show_in": PACKAGES.keys(),
        },
        {
            "type": "analysis",
            "content": "القرار لا يُبنى على كثرة الأرقام بل على معناها.",
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
        },
        {
            "type": "scenario",
            "content": "قاعدة 3–2–1 لاتخاذ القرار.",
            "show_in": ["diamond", "diamond_plus"],
        },
        {
            "type": "reference_context",
            "content": "أحيانًا تجاهل البيانات هو القرار الصحيح.",
            "show_in": ["diamond_plus"],
        },
    ]

# =========================
# CHAPTER 10 – FINAL DECISION
# =========================
def chapter_10_blocks(user_info):
    return [
        {
            "type": "chapter_title",
            "content": "الفصل العاشر – القرار النهائي",
            "show_in": PACKAGES.keys(),
        },
        {
            "type": "analysis",
            "content": "القرار الجيد هو الذي تنام معه مرتاحًا.",
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
        },
        {
            "type": "scenario",
            "content": "اختبار الثلاث نعم قبل الإغلاق.",
            "show_in": ["diamond", "diamond_plus"],
        },
        {
            "type": "final_conclusion",
            "content": "هذا التقرير لم يُكتب ليقودك إلى صفقة، بل إلى قرار واعٍ.",
            "show_in": PACKAGES.keys(),
        },
    ]

# =========================
# BUILD COMPLETE REPORT
# =========================
def build_complete_report(user_info):
    raw_pkg = user_info.get("package", "free")
    package = PACKAGE_ALIASES.get(raw_pkg, "free")
    user_info["package"] = package

    chapters_funcs = [
        chapter_1_blocks,
        chapter_2_blocks,
        chapter_3_blocks,
        chapter_4_blocks,
        chapter_5_blocks,
        chapter_6_blocks,
        chapter_7_blocks,
        chapter_8_blocks,
        chapter_9_blocks,
        chapter_10_blocks,
    ]

    report = {
        "package": package,
        "package_name": PACKAGES[package]["name"],
        "chapters": [],
    }

    for idx, fn in enumerate(chapters_funcs, 1):
        blocks = [b for b in fn(user_info) if package in b["show_in"]]
        if blocks:
            report["chapters"].append(
                {
                    "chapter_number": idx,
                    "blocks": blocks,
                }
            )

    return report
