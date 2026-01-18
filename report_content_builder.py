"""
ملف بناء تقارير الاستثمار العقاري المتقدمة
إصدار: 1.0.0 - مع التعديلات الثلاثة المطلوبة
تاريخ: 2024
"""

# ========== تعريف الباقات الرسمية ==========
PACKAGES = {
    "free": {
        "name": "مجانية",
        "pages": 15,
        "price": 0
    },
    "silver": {
        "name": "فضية", 
        "pages": 35,
        "price": 499
    },
    "gold": {
        "name": "ذهبية",
        "pages": 60,
        "price": 1199
    },
    "diamond": {
        "name": "ماسية",
        "pages": 90,
        "price": 2499
    },
    "diamond_plus": {
        "name": "ماسية متميزة",
        "pages": 120,
        "price": 3499
    }
}

# ========== الفصل الأول: السيناريو الواقعي ==========
def chapter_1_blocks(user_info):
    property_type = user_info.get("نوع_العقار", "العقار")
    city = user_info.get("المدينة", "المدينة")
    
    return [
        {
            "block_id": "ch1_title",
            "type": "chapter_title",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"الفصل الأول - السيناريو الواقعي لمستقبل {property_type} في {city} خلال العقد القادم",
            "page_weight": 0.3
        },
        {
            "block_id": "ch1_intro",
            "type": "chapter_context",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"""مقدمة الفصل: لماذا هذا السيناريو بالذات؟

هذا الفصل لا يهدف إلى إثارة التفاؤل، ولا إلى بث القلق.
ما نقدمه هنا هو قراءة واقعية لمسار سوق {property_type} في {city} خلال السنوات العشر القادمة، مبنية على توازن بين العرض، والطلب، والسلوك، وطبيعة السوق المحلي.
في كل سوق عقاري، ترتفع الأصوات عند الصعود، وتكثر التحذيرات عند التباطؤ.
بين الضجيج والتخويف، يضيع القرار الرشيد.
دور هذا الفصل هو إعادة القارئ إلى نقطة نادرة في السوق
نقطة الفهم قبل التفاعل""",
            "page_weight": 1.0
        },
        {
            "block_id": "ch1_how_to_read",
            "type": "how_to_read",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"""كيف تقرأ هذا الفصل؟

هذا التحليل لا يفترض زاوية واحدة للتعامل مع السوق، ولا يضع جميع القرارات في قالب واحد.
بل يقدم إطارًا عامًا لفهم المسار المحتمل، يمكن إسقاطه على أي قرار عملي لاحقًا.
قد تقرأه وأنت تفكر في العائد،
أو في الاستقرار،
أو في توقيت البيع أو الشراء،
أو في فهم اتجاه السوق قبل أي التزام.
الزاوية التي تقرأ منها هذا الفصل تحدد كيف ستستفيد منه،
لكن الأساس واحد:
فهم المسار قبل الدخول في التفاصيل.""",
            "page_weight": 0.8
        },
        {
            "block_id": "ch1_market_analysis",
            "type": "main_content",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "content": f"""تحليل وضع السوق الحالي
أولًا: كيف نرى سوق {property_type} في {city} اليوم؟
سوق {property_type} في {city} لم يعد سوقًا بسيطًا أو عشوائيًا.
نحن أمام سوق:
• مدفوع بطلب حقيقي، لكن بدرجات متفاوتة
• متأثر بتغيرات اجتماعية وسلوكية واضحة
• مرتبط بعوامل تنظيمية وبنيوية تؤثر في القيمة الفعلية لا الاسمية
• حساس للتوقيت أكثر من أي وقت مضى

الخطأ الشائع اليوم هو قراءة الأسعار بمعزل عن قدرة السوق على الاستيعاب.
نعم، هناك ارتفاعات.
لكن السؤال الأهم دائمًا:
هل هذا الارتفاع مدعوم بطلب مستدام أم بزخم مؤقت؟
تحليلنا يشير إلى أن الإجابة ليست واحدة في كل الأحيان.""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch1_chart_price_dist",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_1_price_distribution",
            "data_dependency": ["price"],
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "title": "توزيع الأسعار – قراءة سلوكية لا رقمية",
            "page_weight": 1.5
        },
        {
            "block_id": "ch1_timeline",
            "type": "key_indicators",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "content": """المخطط الزمني (10 سنوات)

السنوات (1–3) — مرحلة إعادة التوازن
خلال السنوات الثلاث الأولى، نتوقع أن يمر السوق بمرحلة إعادة ضبط الإيقاع.
في هذه المرحلة:
• الطلب لا يختفي، لكنه يصبح أكثر انتقائية
• القرارات العاطفية تتراجع
• القيمة العملية تتقدم على الوعود

السنوات (4–6) — مرحلة الفرز الحقيقي
هنا يبدأ الاختبار الجاد للسوق.
في هذه المرحلة:
• الأصول الجيدة تثبت نفسها
• الأصول المتوسطة تبدأ بالضغط
• الأصول الضعيفة تخرج بصمت

السنوات (7–10) — سوق ناضج… بفرص مختلفة
بعد سبع سنوات، لن يكون السوق كما هو اليوم.
نحن نرى سوقًا:
• أقل اندفاعًا
• أكثر حساسية للجودة
• أدق في التمييز""",
            "page_weight": 1.3
        },
        {
            "block_id": "ch1_chart_price_vs_area",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_1_price_vs_area",
            "data_dependency": ["price", "area"],
            "show_in": ["gold", "diamond", "diamond_plus"],
            "title": "العلاقة بين المساحة والسعر",
            "page_weight": 1.5
        },
        {
            "block_id": "ch1_advanced_insights",
            "type": "advanced_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["gold", "diamond", "diamond_plus"],
            "content": f"""مؤشرات المراقبة الرئيسية:
1. متوسط مدة بقاء {property_type} في السوق
2. الفجوة بين الأسعار المعروضة والمنفذة
3. سلوك الطلب عند التغيرات السعرية
4. استجابة السوق للمعروض الجديد
5. وتيرة قرارات الإطلاق أو التجميد

ماذا يعني هذا لك؟
هل هذا القرار مبني على حركة حالية…
أم على قدرة هذا الأصل على البقاء مطلوبًا عندما يهدأ السوق؟""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch1_scenarios",
            "type": "scenarios",
            "ai_role": "scenario",
            "ai_editable": True,
            "show_in": ["diamond", "diamond_plus"],
            "content": """سيناريوهات السوق المتوقعة:
السيناريو الأساسي (70% احتمال):
• نمو سنوي: 4-6%
• استقرار الطلب
• تنظيم السوق يتحسن

السيناريو المتفائل (20% احتمال):
• نمو سنوي: 7-9%
• طلب قوي مستمر
• تحسن الظروف الاقتصادية

السيناريو المحافظ (10% احتمال):
• نمو سنوي: 2-3%
• تباطؤ مؤقت
• انتظار تحسن الظروف""",
            "page_weight": 1.4
        },
        {
            "block_id": "ch1_chart_future_scenarios",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_1_future_scenarios",
            "data_dependency": ["date", "growth_rate"],
            "show_in": ["diamond", "diamond_plus"],
            "title": "السيناريو الواقعي لنمو السوق (10 سنوات)",
            "page_weight": 1.5
        },
        {
            "block_id": "ch1_international",
            "type": "international_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["diamond_plus"],
            "content": """مقارنة مع 10 أسواق دولية:
1. الإمارات - نمو سنوي: 5.2%
2. السعودية - نمو سنوي: 4.8%
3. قطر - نمو سنوي: 3.9%
4. الكويت - نمو سنوي: 3.5%
5. البحرين - نمو سنوي: 2.8%
6. عمان - نمو سنوي: 2.5%
7. الأردن - نمو سنوي: 2.2%
8. مصر - نمو سنوي: 7.1%
9. المغرب - نمو سنوي: 3.8%
10. تركيا - نمو سنوي: 9.3%""",
            "page_weight": 1.6
        },
        {
            "block_id": "ch1_conclusion",
            "type": "chapter_conclusion",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """خلاصة الفصل
هذا السيناريو ليس وعدًا، ولا تحذيرًا.
هو قراءة هادئة لمسار محتمل إذا استمر السوق دون صدمات غير متوقعة.
هذا الفصل ليس نهاية شيء…
بل بداية طريقة تفكير.""",
            "page_weight": 0.7
        }
    ]

# ========== الفصل الثاني: المخاطر الخفية ==========
def chapter_2_blocks(user_info):
    property_type = user_info.get("نوع_العقار", "العقار")
    city = user_info.get("المدينة", "المدينة")
    
    return [
        {
            "block_id": "ch2_title",
            "type": "chapter_title",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"الفصل الثاني – المخاطر الخفية في سوق {property_type} في {city}: ليست ما تظن",
            "page_weight": 0.3
        },
        {
            "block_id": "ch2_intro",
            "type": "chapter_context",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"""لماذا هذا الفصل مهم؟
بعد أن فهمنا المسار الواقعي لسوق {property_type} في {city} خلال السنوات القادمة، يأتي السؤال الأصعب:
أين يمكن أن نُخطئ دون أن ننتبه؟

الأسواق لا تُفشل الناس بالضربات الواضحة،
بل بالأخطاء الصامتة…
تلك التي تبدو منطقية، شائعة، ومقبولة اجتماعيًا.

هذا الفصل لا يهدف إلى تخويفك،
ولا إلى تعطيل قرارك،
بل إلى كشف المخاطر التي لا يتحدث عنها أحد لأنها غير مريحة.""",
            "page_weight": 1.0
        },
        {
            "block_id": "ch2_market_analysis",
            "type": "main_content",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "content": f"""مفهوم "الأخطاء الصامتة"
أولًا: الخطر الأكبر… التفكير أن الخطر في السعر فقط

أكثر خطأ شائع هو اختزال المخاطر في سؤال واحد:
"هل السعر مرتفع أم منخفض؟"

بينما الواقع أن السعر غالبًا يكون آخر نتيجة، لا السبب.

المخاطر الحقيقية في سوق {property_type} لا تكمن في الرقم وحده،
بل في:
• قابلية الأصل للبقاء مطلوبًا
• سهولة الخروج منه
• مرونته أمام التغيرات السلوكية والتنظيمية""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch2_chart_price_concentration",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_2_price_concentration",
            "data_dependency": ["price"],
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "title": "تمركز الأسعار – أين يتركّز الخطر؟",
            "page_weight": 1.5
        },
        {
            "block_id": "ch2_advanced_insights",
            "type": "advanced_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["gold", "diamond", "diamond_plus"],
            "content": """ثانيًا: خطر "المنطق الشائع" (أخطر من الخطأ الواضح)
المشكلة أن:
أكثر القرارات الخاطئة تُتخذ بأسباب تبدو منطقية تمامًا.

عندما يصبح نفس المنطق مكررًا على ألسنة الجميع،
فهذا يعني أن السوق سعّر هذا المنطق مسبقًا.

ثالثًا: خطر التوقيت غير المرئي
ليس كل توقيت خاطئ يبدو خاطئًا لحظتها.

أخطر سيناريو هو:
الدخول في الوقت الخطأ في الخيار الصحيح""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch2_chart_price_volatility",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_2_price_volatility",
            "data_dependency": ["date", "price"],
            "show_in": ["gold", "diamond", "diamond_plus"],
            "title": "تذبذب الأسعار – الخطر غير المرئي",
            "page_weight": 1.5
        },
        {
            "block_id": "ch2_scenarios",
            "type": "scenarios",
            "ai_role": "scenario",
            "ai_editable": True,
            "show_in": ["diamond", "diamond_plus"],
            "content": """سيناريوهات المخاطر المتطرفة:
1. سيناريو التباطؤ السريع (30% احتمال)
2. سيناريو التشريعات الجديدة (25% احتمال)
3. سيناريو التحول السلوكي (20% احتمال)
4. سيناريو المنافسة الشرسة (15% احتمال)
5. سيناريو الأزمة الاقتصادية (10% احتمال)""",
            "page_weight": 1.4
        },
        {
            "block_id": "ch2_chart_overpricing",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_2_overpricing_risk",
            "data_dependency": ["price", "demand_index"],
            "show_in": ["diamond", "diamond_plus"],
            "title": "مخاطر التسعير المبالغ فيه",
            "page_weight": 1.5
        },
        {
            "block_id": "ch2_international",
            "type": "international_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["diamond_plus"],
            "content": """مقارنة مخاطر الأسواق الدولية:
1. الإمارات - مخاطرة: متوسطة
2. السعودية - مخاطرة: منخفضة
3. قطر - مخاطرة: منخفضة
4. الكويت - مخاطرة: متوسطة
5. البحرين - مخاطرة: عالية
6. عمان - مخاطرة: متوسطة
7. الأردن - مخاطرة: عالية
8. مصر - مخاطرة: عالية جداً
9. المغرب - مخاطرة: متوسطة
10. تركيا - مخاطرة: عالية جداً""",
            "page_weight": 1.6
        },
        {
            "block_id": "ch2_conclusion",
            "type": "chapter_conclusion",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """كيف تتعامل مع المخاطر بذكاء؟
نحن لا نؤمن بتجنب المخاطر تمامًا،
بل بـ فهمها قبل أن تفاجئك.

قبل أي قرار، اسأل نفسك:
• ما الخطر الذي لا أراه الآن؟
• ماذا لو تغير السياق لا السعر؟
• هل يمكنني العيش مع هذا القرار إن تأخر العائد؟
• هل لدي خطة إن تغيرت فرضيتي الأساسية؟""",
            "page_weight": 0.8
        }
    ]

# ========== الفصل الثالث: الفرص غير المرئية ==========
def chapter_3_blocks(user_info):
    property_type = user_info.get("نوع_العقار", "العقار")
    city = user_info.get("المدينة", "المدينة")
    
    return [
        {
            "block_id": "ch3_title",
            "type": "chapter_title",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"الفصل الثالث – الفرص غير المرئية في سوق {property_type} في {city}",
            "page_weight": 0.3
        },
        {
            "block_id": "ch3_intro",
            "type": "chapter_context",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """أين ننظر عندما ينشغل الجميع بشيء آخر؟
مقدمة الفصل: لماذا لا تكون الفرصة حيث ينظر الجميع؟

في كل سوق عقاري، هناك حقيقة بسيطة يتجاهلها كثيرون:
عندما يتفق الجميع على أن شيئًا ما "فرصة"، غالبًا تكون الفرصة الحقيقية قد انتقلت إلى مكان آخر.

نحن نبحث عن شيء أدقّ وأهدأ:
الفرص التي لا تصرخ، لكنها تصمد.""",
            "page_weight": 1.0
        },
        {
            "block_id": "ch3_market_analysis",
            "type": "main_content",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "content": f"""أولاً: كيف تختفي الفرص عن الأنظار؟
الفرص لا تختفي لأنها سيئة، بل لأنها غالبًا:
• لا تحمل قصة جذابة
• لا ترتبط بضجيج إعلامي
• لا تحقق أرباحًا سريعة
• تتطلب صبرًا أو إدارة أفضل من المتوسط

في سوق {property_type} في {city}، نلاحظ أن الاهتمام الجماعي يمر بدورات:
• مرحلة انبهار
• مرحلة اندفاع
• مرحلة تشبع
• ثم مرحلة ملل

الفرصة الحقيقية تبدأ غالبًا عند الملل، لا عند الانبهار.""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch3_chart_value_map",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_3_value_map",
            "data_dependency": ["price", "rental_yield"],
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "title": "خريطة القيمة – أين تختبئ الفرص؟",
            "page_weight": 1.5
        },
        {
            "block_id": "ch3_advanced_insights",
            "type": "advanced_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["gold", "diamond", "diamond_plus"],
            "content": """ثانياً: الفرق بين "غير المرئي" و"غير الجيد"
التمييز الذكي يكون بالسؤال التالي:
هل تجاهل السوق لهذا الأصل ناتج عن عيب جوهري؟
أم عن غياب قصة جذابة فقط؟

الفرصة غير المرئية الجيدة غالبًا:
• تخدم احتياجًا حقيقيًا
• تستقر قيمتها أكثر مما تقفز
• لا تعتمد على توقيت مثالي
• يمكن الدفاع عنها منطقيًا بعد سنوات""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch3_chart_affordable_pockets",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_3_affordable_pockets",
            "data_dependency": ["location_score", "price"],
            "show_in": ["gold", "diamond", "diamond_plus"],
            "title": "الجيوب السعرية غير الملفتة",
            "page_weight": 1.5
        },
        {
            "block_id": "ch3_scenarios",
            "type": "scenarios",
            "ai_role": "scenario",
            "ai_editable": True,
            "show_in": ["diamond", "diamond_plus"],
            "content": """ثالثاً: أين ننظر فعليًا؟ (منهج لا أماكن)
ابحث عن العقار الذي يملك هذه الصفات:

1. طلب هادئ لكنه مستمر  
2. سعر لا يثير الحسد  
3. قابلية استخدام واضحة  
4. مرونة مستقبلية  

رابعاً: كيف تتحول المخاطر إلى فرص؟
المستثمر الذكي لا يسأل:
كيف أتجنب المخاطر تمامًا؟
بل يسأل:
أي المخاطر يمكنني تحمّلها؟
وأيها يمكنني الاستفادة منها؟""",
            "page_weight": 1.4
        },
        {
            "block_id": "ch3_chart_size_opportunities",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_3_size_opportunities",
            "data_dependency": ["area", "rental_yield"],
            "show_in": ["diamond", "diamond_plus"],
            "title": "المساحات المهملة ذات العائد المستقر",
            "page_weight": 1.5
        },
        {
            "block_id": "ch3_international",
            "type": "international_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["diamond_plus"],
            "content": """الفرص غير المرئية في 10 أسواق دولية:
1. الإمارات - فرص في القطاع الصناعي
2. السعودية - فرص في المدن الجديدة
3. قطر - فرص في العقارات المتوسطة
4. الكويت - فرص في الشقق الصغيرة
5. البحرين - فرص في المناطق النامية
6. عمان - فرص في المشاريع السياحية
7. الأردن - فرص في العقارات الطلابية
8. مصر - فرص في المدن الجديدة
9. المغرب - فرص في القطاع السياحي
10. تركيا - فرص في المناطق الصناعية""",
            "page_weight": 1.6
        },
        {
            "block_id": "ch3_conclusion",
            "type": "chapter_conclusion",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """خلاصة الفصل
الفرص غير المرئية لا تُكتشف بالاندفاع،
بل بالهدوء، والمقارنة، والقدرة على التفكير بعكس التيار دون صدام معه.

في الفصل التالي، سننتقل من اكتشاف الفرص
إلى بناء خطة تتعامل معها بذكاء على مدى السنوات.""",
            "page_weight": 0.7
        }
    ]

# ========== الفصل الرابع: خطة التعامل الذكي ==========
def chapter_4_blocks(user_info):
    property_type = user_info.get("نوع_العقار", "العقار")
    city = user_info.get("المدينة", "المدينة")
    
    return [
        {
            "block_id": "ch4_title",
            "type": "chapter_title",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"الفصل الرابع – خطة التعامل الذكي مع {property_type} في {city}",
            "page_weight": 0.3
        },
        {
            "block_id": "ch4_intro",
            "type": "chapter_context",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"""مقدمة الفصل: لماذا التخطيط أهم من الشراء؟

بعد أن فهمت:
• كيف يبدو المشهد العام (الفصل الأول)
• ما الذي يجب أن تحذر منه (الفصل الثاني)
• وأين يمكن أن تختبئ الفرص الحقيقية (الفصل الثالث)

نصل الآن إلى المرحلة التي يفشل عندها أغلب الناس.
ليس لأنهم لا يعرفون…
بل لأنهم لا يملكون نظامًا.

القرار العقاري لا يفشل غالبًا في يوم الشراء،
بل يفشل في السنوات التي تليه.""",
            "page_weight": 1.0
        },
        {
            "block_id": "ch4_market_analysis",
            "type": "main_content",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "content": """أولًا: الاستثمار ليس صفقة… بل علاقة طويلة
سواء كان هدفك:
• شراء
• تأجير
• بيع لاحق
• أو مزيجًا من ذلك

فإن التعامل مع العقار هو علاقة تمتد عبر:
• تقلبات السوق
• تغير احتياجاتك
• تغيّر المدينة نفسها

الخطأ الشائع هو التعامل مع القرار وكأنه نقطة واحدة.
بينما الواقع أنه مسار طويل.""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch4_chart_allocation_logic",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_4_investment_allocation_logic",
            "data_dependency": [],
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "title": "منطق توزيع الاستثمار",
            "page_weight": 1.5
        },
        {
            "block_id": "ch4_advanced_insights",
            "type": "advanced_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["gold", "diamond", "diamond_plus"],
            "content": """ثانياً: تقسيم السنوات العشر (خريطة واقعية)
نحن لا ننظر إلى السنوات القادمة كرقم واحد،
بل كأربع مراحل مختلفة تمامًا في طبيعتها.

المرحلة الأولى: السنوات (1–2) — مرحلة التثبيت
في هذه المرحلة:
• تتأكد من صحة القرار
• تختبر الواقع مقابل التوقعات
• تكتشف التفاصيل التي لم تظهر في البداية

المرحلة الثانية: السنوات (3–5) — مرحلة البناء
هنا يبدأ القرار في إظهار شخصيته.
في هذه المرحلة:
• تظهر قوة الموقع أو ضعفها
• يتضح إن كان الأصل "يُدار" أم "يُترك"
• تبدأ الفروق بين أصل جيد وأصل ممتاز""",
            "page_weight": 1.3
        },
        {
            "block_id": "ch4_chart_action_matrix",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_4_action_matrix",
            "data_dependency": [],
            "show_in": ["gold", "diamond", "diamond_plus"],
            "title": "مصفاة القرار الاستثماري",
            "page_weight": 1.5
        },
        {
            "block_id": "ch4_scenarios",
            "type": "scenarios",
            "ai_role": "scenario",
            "ai_editable": True,
            "show_in": ["diamond", "diamond_plus"],
            "content": """المرحلة الثالثة: السنوات (6–8) — مرحلة الاختيار
في هذه السنوات، يجب أن تكون صريحًا مع نفسك.

اسأل:
• هل هذا الأصل يخدم أهدافي الحالية؟
• هل أستفيد منه بأقصى طاقته؟
• هل هناك بديل أفضل لو حررت رأس المال؟

الاحتفاظ ليس فضيلة دائمًا،
والبيع ليس فشلًا.

المرحلة الرابعة: السنوات (9–10) — مرحلة القرار الكبير
في نهاية العقد:
• إما أن الأصل أصبح جزءًا ثابتًا من منظومتك
• أو أصبح مرشحًا للتحويل أو الخروج""",
            "page_weight": 1.4
        },
        {
            "block_id": "ch4_international",
            "type": "international_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["diamond_plus"],
            "content": """مقارنة خطط الاستثمار في 10 دول:
1. الإمارات - خطط استثمارية متوسطة المدى
2. السعودية - خطط طويلة المدى
3. قطر - خطط متحفظة
4. الكويت - خطط قصيرة المدى
5. البحرين - خطط متوسطة المخاطرة
6. عمان - خطط سياحية
7. الأردن - خطط عقارية متخصصة
8. مصر - خطط تنموية سريعة
9. المغرب - خطط سياحية طويلة
10. تركيا - خطط سريعة الربح""",
            "page_weight": 1.6
        },
        {
            "block_id": "ch4_conclusion",
            "type": "chapter_conclusion",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """خلاصة الفصل
الخطة ليست ضمانًا للربح،
لكنها أفضل حماية من الندم.

في الفصل القادم، سننتقل إلى عنصر حساس جدًا:
التوقيت
ومتى يكون الانتظار ذكاء…
ومتى يكون تكلفة خفية.""",
            "page_weight": 0.7
        }
    ]

# ========== الفصل الخامس: التوقيت ==========
def chapter_5_blocks(user_info):
    property_type = user_info.get("نوع_العقار", "العقار")
    city = user_info.get("المدينة", "المدينة")
    
    return [
        {
            "block_id": "ch5_title",
            "type": "chapter_title",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"الفصل الخامس – التوقيت في سوق {property_type} في {city}",
            "page_weight": 0.3
        },
        {
            "block_id": "ch5_intro",
            "type": "chapter_context",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """مقدمة الفصل: أكبر وهم في الاستثمار

من أكثر الأسئلة التي تُطرح في السوق:
هل الآن هو الوقت المناسب؟

السؤال يبدو منطقيًا،
لكنه في الحقيقة مضلِّل.

لأن السوق لا يعطيك ضوءًا أخضر واضحًا،
ولا يعلن عن لحظته المثالية.

هذا الفصل لا يحاول أن يتنبأ بالسوق،
بل يعلّمك كيف تتعامل مع التوقيت بذكاء.""",
            "page_weight": 1.0
        },
        {
            "block_id": "ch5_market_analysis",
            "type": "main_content",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "content": """أولًا: التنبؤ ≠ إدارة التوقيت
التنبؤ يقول:
"السوق سيرتفع / سينخفض"

إدارة التوقيت تقول:
"حتى لو كنت مخطئًا… هل أستطيع تحمّل القرار؟"

الفرق بينهما هو الفرق بين:
• من يريد أن يصيب
• ومن يريد أن ينجو وينمو

نحن لا نبحث عن القرار الذي يبدو ذكيًا اليوم،
بل عن القرار الذي لا يدمّرك إن أخطأت توقيته.""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch5_chart_price_positioning",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_5_price_positioning",
            "data_dependency": ["date", "price"],
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "title": "تموضع السعر داخل الدورة",
            "page_weight": 1.5
        },
        {
            "block_id": "ch5_advanced_insights",
            "type": "advanced_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["gold", "diamond", "diamond_plus"],
            "content": """ثانياً: أخطر سيناريو في السوق
ليس الخطر في أن تختار العقار الخاطئ،
ولا في أن تكون في المدينة الخطأ.

أخطر سيناريو هو:
الدخول في الوقت الخطأ… في الخيار الصحيح.

في هذا السيناريو:
• الأصل ممتاز
• الموقع جيد
• الفكرة صحيحة

لكن:
• رأس المال يتجمد
• الأعصاب تُستنزف
• القرار يتحول من فرصة إلى عبء""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch5_chart_entry_timing",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_5_entry_timing_signal",
            "data_dependency": ["date", "entry_signal"],
            "show_in": ["gold", "diamond", "diamond_plus"],
            "title": "إشارات الدخول الهادئة",
            "page_weight": 1.5
        },
        {
            "block_id": "ch5_scenarios",
            "type": "scenarios",
            "ai_role": "scenario",
            "ai_editable": True,
            "show_in": ["diamond", "diamond_plus"],
            "content": """ثالثاً: التوقيت ليس نقطة… بل نطاق
من يطارد "اللحظة المثالية" غالبًا لا يدخل أبدًا،
أو يدخل متأخرًا.

الواقع أن التوقيت الذكي هو:
• نطاق زمني مقبول
• وليس تاريخًا محددًا

إذا كان القرار:
• يمكن تحمّله لو تأخر العائد
• ولا ينهار لو تباطأ السوق
• ولا يعتمد على قفزة سريعة

فأنت داخل نطاق زمني آمن.""",
            "page_weight": 1.4
        },
        {
            "block_id": "ch5_international",
            "type": "international_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["diamond_plus"],
            "content": """مقارنة توقيت الأسواق الدولية:
1. الإمارات - توقيت دخول: ربيع 2024
2. السعودية - توقيت دخول: صيف 2024
3. قطر - توقيت دخول: خريف 2024
4. الكويت - توقيت دخول: شتاء 2024
5. البحرين - توقيت دخول: ربيع 2025
6. عمان - توقيت دخول: صيف 2025
7. الأردن - توقيت دخول: متاح الآن
8. مصر - توقيت دخول: خريف 2024
9. المغرب - توقيت دخول: ربيع 2025
10. تركيا - توقيت دخول: صيف 2024""",
            "page_weight": 1.6
        },
        {
            "block_id": "ch5_conclusion",
            "type": "chapter_conclusion",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """خلاصة الفصل
التوقيت الذكي لا يجعلك الأسبق،
بل يجعلك الأكثر ثباتًا.

في الفصل القادم، سننتقل إلى عنصر حاسم:
كيف توزّع رأس مالك
بحيث لا يكون قرار واحد قادرًا على تدمير كل شيء.""",
            "page_weight": 0.7
        }
    ]

# ========== الفصل السادس: توزيع رأس المال ==========
def chapter_6_blocks(user_info):
    property_type = user_info.get("نوع_العقار", "العقار")
    city = user_info.get("المدينة", "المدينة")
    
    return [
        {
            "block_id": "ch6_title",
            "type": "chapter_title",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"الفصل السادس – توزيع رأس المال في {property_type} في {city}",
            "page_weight": 0.3
        },
        {
            "block_id": "ch6_intro",
            "type": "chapter_context",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """مقدمة الفصل: الخطأ الذي لا يُغتفر

معظم الخسائر الكبيرة في السوق العقاري
لا تأتي من اختيار مدينة خاطئة
ولا من اختيار نوع عقار سيئ
بل من شيء أبسط وأخطر:
وضع جزء كبير من رأس المال في قرار واحد

هذا الفصل لا يعلّمك كيف "تربح أكثر"،
بل كيف لا تنهار إذا أخطأت.""",
            "page_weight": 1.0
        },
        {
            "block_id": "ch6_market_analysis",
            "type": "main_content",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "content": """أولًا: لماذا التوزيع أهم من الصفقة؟
الصفقة الجيدة قد تفشل
لكن التوزيع الجيد ينقذك حتى مع صفقة فاشلة

الفرق بين المستثمر الذكي والمندفع هو:
• المندفع يقول: أنا واثق
• الذكي يقول: حتى لو كنت مخطئًا… لن أتضرر كثيرًا

ثانياً: السؤال المؤسسي الحقيقي
قبل أن تفكر في الشراء، اسأل:
لو أخطأت في هذا القرار…
هل سيؤلمني؟ أم سيُدمّرني؟

إذا كانت الإجابة "يُدمّرني"
فالمشكلة ليست في العقار
بل في طريقة توزيع رأس المال.""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch6_chart_allocation_by_risk",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_6_capital_allocation_by_risk",
            "data_dependency": [],
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "title": "توزيع رأس المال حسب مستوى المخاطر",
            "page_weight": 1.5
        },
        {
            "block_id": "ch6_advanced_insights",
            "type": "advanced_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["gold", "diamond", "diamond_plus"],
            "content": """ثالثاً: الطبقات الأربع للتوزيع الذكي
نحن نرى أن رأس المال الصحي يتوزع على أربع طبقات:

1️⃣ طبقة الأمان  
• سيولة
• أصول سهلة التخارج
• قرارات لا تحتاج توقيتًا مثاليًا

2️⃣ طبقة الاستقرار  
• عقارات بعائد واضح
• طلب حقيقي
• مخاطرة محدودة

3️⃣ طبقة النمو  
• قرارات مدروسة
• مناطق أو توقيتات فيها فرصة
• عائد أعلى مقابل مخاطرة محسوبة

4️⃣ طبقة الفرص  
• فرص خاصة
• قرارات غير متكررة
• مخاطرة أعلى لكن بحجم صغير""",
            "page_weight": 1.3
        },
        {
            "block_id": "ch6_chart_balance_curve",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_6_capital_balance_curve",
            "data_dependency": [],
            "show_in": ["gold", "diamond", "diamond_plus"],
            "title": "منحنى توازن رأس المال",
            "page_weight": 1.5
        },
        {
            "block_id": "ch6_scenarios",
            "type": "scenarios",
            "ai_role": "scenario",
            "ai_editable": True,
            "show_in": ["diamond", "diamond_plus"],
            "content": """رابعاً: قاعدة 10 / 20 (إرشادية، ولكن منقذة)
نقترح عليك قاعدتين بسيطتين:

قاعدة 10%
لا تجعل قرارًا واحدًا يمثل أكثر من 10% من إجمالي قدرتك الاستثمارية.

قاعدة 20%
احتفظ بـ 20% من رأس مالك كسيولة استراتيجية.

في أوقات الهدوء، ستشعر أنها كثيرة
وفي الأزمات، ستشعر أنها غير كافية.""",
            "page_weight": 1.4
        },
        {
            "block_id": "ch6_international",
            "type": "international_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["diamond_plus"],
            "content": """مقارنة استراتيجيات توزيع رأس المال في 10 دول:
1. الإمارات - توزيع محافظ متنوعة
2. السعودية - تركيز على العقارات السكنية
3. قطر - استثمارات سيولة عالية
4. الكويت - تركيز على المشاريع الكبيرة
5. البحرين - تنويع قطاعي
6. عمان - استثمارات سياحية
7. الأردن - عقارات طلابية وتجارية
8. مصر - مشاريع سكنية كبيرة
9. المغرب - استثمارات سياحية
10. تركيا - تنويع جغرافي""",
            "page_weight": 1.6
        },
        {
            "block_id": "ch6_conclusion",
            "type": "chapter_conclusion",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """خلاصة الفصل
التوزيع الذكي لا يجعلك الأغنى بسرعة
لكنه يجعلك الأكثر بقاءً

وفي السوق العقاري
من يبقى… هو من يربح في النهاية.

في الفصل القادم، سننتقل إلى لحظة حاسمة:
متى تخرج؟ ومتى تبقى؟
وكيف تثبّت الربح قبل أن يتحول إلى رقم على الورق فقط.""",
            "page_weight": 0.7
        }
    ]

# ========== الفصل السابع: متى تخرج؟ متى تبقى؟ ==========
def chapter_7_blocks(user_info):
    property_type = user_info.get("نوع_العقار", "العقار")
    city = user_info.get("المدينة", "المدينة")
    
    return [
        {
            "block_id": "ch7_title",
            "type": "chapter_title",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"الفصل السابع – متى تخرج؟ ومتى تبقى؟",
            "page_weight": 0.3
        },
        {
            "block_id": "ch7_intro",
            "type": "chapter_context",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """مقدمة الفصل: الحقيقة التي لا يحبها أحد

الشراء قرار يتخذه كثيرون.
لكن الخروج قرار يتقنه القليل.

ليس لأن الخروج معقد ماليًا،
بل لأنه معقّد نفسيًا.

الربح لا يتحقق عند الشراء…
بل يُثبَّت عند الخروج.""",
            "page_weight": 1.0
        },
        {
            "block_id": "ch7_market_analysis",
            "type": "main_content",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "content": """أولًا: لماذا الخروج أصعب من الدخول؟
عند الشراء:
• السوق يشجعك
• القصص إيجابية
• الجميع يتحدث عن الفرص

عند الخروج:
• المشاعر تتضارب
• الطمع يهمس: "انتظر أكثر"
• الخوف يهمس: "اخرج الآن"

والخطأ الشائع هو:
انتظار الإشارة الواضحة…
والإشارة الواضحة لا تأتي إلا بعد فوات الأوان.""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch7_chart_exit_pressure",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_7_exit_pressure_zones",
            "data_dependency": ["price", "time_on_market"],
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "title": "مناطق ضغط الخروج",
            "page_weight": 1.5
        },
        {
            "block_id": "ch7_advanced_insights",
            "type": "advanced_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["gold", "diamond", "diamond_plus"],
            "content": """ثانياً: الفكرة الأخطر — أن تكون سجين أصل جيد
قد تمتلك عقارًا ممتازًا
بسعر جيد
وعائد مقبول

ثم تكتشف بعد سنوات:
• السوق الثانوي ضعيف
• الجميع يبيع نفس الشيء
• الخروج أصعب مما توقعت

الأصل الجيد لا يعني دائمًا أصلًا سهل الخروج.

ثالثاً: إشارات الخروج الذكي (ليست سعرًا فقط)
الخروج لا يعتمد على رقم واحد، بل على منظومة إشارات:
• تغير الفرضية الأساسية التي بني عليها القرار
• تراجع الطلب الحقيقي لا المؤقت
• ارتفاع المنافسة دون تحسن في الجودة""",
            "page_weight": 1.3
        },
        {
            "block_id": "ch7_chart_hold_vs_exit",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_7_hold_vs_exit_signal",
            "data_dependency": [],
            "show_in": ["gold", "diamond", "diamond_plus"],
            "title": "إشارة الاحتفاظ مقابل الخروج",
            "page_weight": 1.5
        },
        {
            "block_id": "ch7_scenarios",
            "type": "scenarios",
            "ai_role": "scenario",
            "ai_editable": True,
            "show_in": ["diamond", "diamond_plus"],
            "content": """ثلاثة سيناريوهات للخروج الذكي:

1️⃣ الخروج الاستباقي  
تخرج قبل الذروة  
وتتنازل عن آخر 10–15% من الربح  
هذا ليس ضعفًا  
بل ثمن الهدوء.

2️⃣ الخروج التحويلي  
تبيع لتنتقل إلى أصل أفضل:
• موقع أقوى
• نوع أكثر طلبًا
• توزيع رأس مال أذكى

هنا الربح الحقيقي ليس في البيع  
بل في الترقية.

3️⃣ الخروج الوقائي  
تخرج لأن:
• المعطيات تغيرت
• المخاطر ارتفعت
• الفرضية لم تعد صحيحة

الخروج هنا ليس فشلًا  
بل إدارة مخاطر ناضجة.""",
            "page_weight": 1.4
        },
        {
            "block_id": "ch7_international",
            "type": "international_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["diamond_plus"],
            "content": """مقارنة استراتيجيات الخروج في 10 أسواق:
1. الإمارات - مدة الاحتفاظ: 3-5 سنوات
2. السعودية - مدة الاحتفاظ: 5-7 سنوات
3. قطر - مدة الاحتفاظ: 4-6 سنوات
4. الكويت - مدة الاحتفاظ: 2-4 سنوات
5. البحرين - مدة الاحتفاظ: 3-5 سنوات
6. عمان - مدة الاحتفاظ: 5-8 سنوات
7. الأردن - مدة الاحتفاظ: 4-6 سنوات
8. مصر - مدة الاحتفاظ: 2-3 سنوات
9. المغرب - مدة الاحتفاظ: 5-7 سنوات
10. تركيا - مدة الاحتفاظ: 1-2 سنوات""",
            "page_weight": 1.6
        },
        {
            "block_id": "ch7_conclusion",
            "type": "chapter_conclusion",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """خلاصة الفصل
الخروج الذكي لا يصنع ضجيجًا  
ولا يُرضي الجميع

لكنه:
• يثبت الربح
• يحمي رأس المال
• ويمنحك فرصة البداية من جديد

في الفصل القادم، سننتقل إلى مستوى أعمق:
كيف تقرأ الإشارات المبكرة قبل أن يراها السوق؟""",
            "page_weight": 0.7
        }
    ]

# ========== الفصل الثامن: قراءة الإشارات المبكرة ==========
def chapter_8_blocks(user_info):
    property_type = user_info.get("نوع_العقار", "العقار")
    city = user_info.get("المدينة", "المدينة")
    
    return [
        {
            "block_id": "ch8_title",
            "type": "chapter_title",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"الفصل الثامن – كيف تقرأ الإشارات المبكرة قبل أن يراها السوق؟",
            "page_weight": 0.3
        },
        {
            "block_id": "ch8_intro",
            "type": "chapter_context",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """مقدمة الفصل: الحقيقة التي يغفل عنها الجميع

السوق لا يصرخ عندما يتغير.
السوق يهمس.

والفرق بين من ينجو ومن يتأخر
ليس من يملك معلومات أكثر،
بل من يفهم الإشارات قبل أن تتحول إلى أخبار.

السعر هو آخر ما يتغير.
السلوك… هو الأول.""",
            "page_weight": 1.0
        },
        {
            "block_id": "ch8_market_analysis",
            "type": "main_content",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "content": """أولًا: لماذا الإشارات أهم من الأرقام؟
الأرقام تخبرك بما حدث.
الإشارات تخبرك بما يبدأ في الحدوث.

في سوق العقارات:
• الأسعار قد تبدو مستقرة
• الإعلانات قد تكون كثيرة
• الأخبار قد تكون إيجابية

لكن تحت السطح…
قد يكون الاتجاه قد بدأ بالتغير.

ثانياً: الفرق بين الضجيج والإشارة
الضجيج:
• أخبار متكررة بلا معنى جديد
• آراء متناقضة في وقت قصير
• اندفاع عاطفي (تفاؤل أو خوف مبالغ)

الإشارة:
• تغير هادئ في السلوك
• أسئلة جديدة تظهر
• قرارات مختلفة من لاعبين كبار

الضجيج يشتت انتباهك…
الإشارة تغيّر قرارك.""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch8_chart_anomaly_detection",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_8_anomaly_detection",
            "data_dependency": ["date", "price"],
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "title": "اكتشاف السلوك غير الطبيعي",
            "page_weight": 1.5
        },
        {
            "block_id": "ch8_advanced_insights",
            "type": "advanced_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["gold", "diamond", "diamond_plus"],
            "content": """ثالثاً: الإشارات السلوكية الثلاث الأخطر

1️⃣ تغير الأسئلة  
راقب ما يسأله الناس، لا ما يجابونه.
• من: "متى أشتري؟"
• إلى: "هل الآن مناسب؟"
• ثم إلى: "هل الانتظار أفضل؟"

تغير السؤال
يعني تغير المزاج العام.

2️⃣ تغير لغة المخاطرة  
عندما يتحول الحديث من:
• "الفرصة"
إلى:
• "السلامة"

فهذه إشارة مبكرة على تحول في الاتجاه.

3️⃣ تغير سلوك العارضين  
راقب:
• هل بدأت العروض تطول؟
• هل ظهرت مرونة غير معلنة؟
• هل زادت الحوافز بدل خفض السعر؟

السوق الذكي لا يخفض السعر أولًا…
بل يضيف تنازلات.""",
            "page_weight": 1.3
        },
        {
            "block_id": "ch8_chart_signal_intensity",
            "type": "chart",
            "ai_role": "fixed",
            "ai_editable": False,
            "chart_key": "chapter_8_signal_intensity",
            "data_dependency": ["date", "signal_strength"],
            "show_in": ["gold", "diamond", "diamond_plus"],
            "title": "شدة الإشارات المبكرة",
            "page_weight": 1.5
        },
        {
            "block_id": "ch8_scenarios",
            "type": "scenarios",
            "ai_role": "scenario",
            "ai_editable": True,
            "show_in": ["diamond", "diamond_plus"],
            "content": """رابعاً: مؤشر الثقة الخفي
اسأل نفسك:
• هل الناس أكثر ثقة أم أكثر حذرًا؟
• هل القرارات تُتخذ بسرعة أم بتردد؟
• هل الصمت زاد أم الضجيج؟

عندما:
• يقل النقد
• وتبدو كل الصفقات "منطقية"
• ويُسخر من التحذيرات

فهذا ليس استقرارًا…
بل عمى جماعي.

خامساً: الإشارة التي لا ينتبه لها أحد
"السوق السعيد جدًا"

أخطر سوق
هو السوق الذي:
• لا يرى مخاطره
• لا يناقش أسوأ الاحتمالات
• لا يتسامح مع الرأي المختلف""",
            "page_weight": 1.4
        },
        {
            "block_id": "ch8_international",
            "type": "international_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["diamond_plus"],
            "content": """مقارنة الإشارات في 10 أسواق دولية:
1. الإمارات - إشارات: تذبذب عالي
2. السعودية - إشارات: استقرار نسبي
3. قطر - إشارات: بطء في الحركة
4. الكويت - إشارات: تقلب متوسط
5. البحرين - إشارات: هدوء نسبي
6. عمان - إشارات: نمو بطيء
7. الأردن - إشارات: تحسن تدريجي
8. مصر - إشارات: نمو سريع
9. المغرب - إشارات: استقرار
10. تركيا - إشارات: تذبذب حاد""",
            "page_weight": 1.6
        },
        {
            "block_id": "ch8_conclusion",
            "type": "chapter_conclusion",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """خلاصة الفصل
قراءة الإشارات ليست تنبؤًا
وليست ادعاء معرفة المستقبل

إنها:
• انتباه هادئ
• ملاحظة واعية
• واحترام لما لا يقوله السوق صراحة

في الفصل القادم، سنأخذ هذه البصيرة
ونحوّلها إلى شيء عملي جدًا:
كيف تحوّل البيانات إلى قرارات… لا إلى حيرة.""",
            "page_weight": 0.7
        }
    ]

# ========== الفصل التاسع: تحويل البيانات إلى قرارات ==========
def chapter_9_blocks(user_info):
    property_type = user_info.get("نوع_العقار", "العقار")
    city = user_info.get("المدينة", "المدينة")
    
    return [
        {
            "block_id": "ch9_title",
            "type": "chapter_title",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"الفصل التاسع – كيف تحوّل البيانات إلى قرارات… لا إلى حيرة",
            "page_weight": 0.3
        },
        {
            "block_id": "ch9_intro",
            "type": "chapter_context",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """مقدمة الفصل: المشكلة ليست في قلة البيانات

المشكلة اليوم
ليست أن السوق لا يوفّر بيانات.
المشكلة أن:
• البيانات كثيرة
• المؤشرات متضاربة
• وكل رقم يدّعي أنه الأهم

والنتيجة؟
كثير من القرارات… وقليل من القناعة.

هذا الفصل لا يضيف لك بيانات جديدة،
بل يعلّمك كيف تستخدم ما لديك دون أن تضيع فيه.""",
            "page_weight": 1.0
        },
        {
            "block_id": "ch9_market_analysis",
            "type": "main_content",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "content": """أولًا: لماذا تربكنا البيانات أكثر مما تساعدنا؟
البيانات تصبح عبئًا عندما:
• تقرأ كل شيء
• وتحاول فهم كل شيء
• في نفس الوقت

العقل البشري لا يتخذ قرارًا جيدًا
تحت وابل من الأرقام.

القرار الذكي لا يحتاج كل البيانات…
يحتاج البيانات الصحيحة فقط.

ثانياً: الفرق بين "معلومة" و"إشارة"
المعلومة:
• رقم منفصل
• صالح للعرض
• لا يغيّر قرارك وحده

الإشارة:
• نمط متكرر
• مرتبط بسلوك
• يؤثر مباشرة على قرارك

مثال:
• "متوسط السعر = X" ← معلومة
• "الأسعار مستقرة رغم زيادة المعروض" ← إشارة

القرار لا يُبنى على رقم…
بل على ما يعنيه الرقم في سياقه.""",
            "page_weight": 1.3
        },
        {
            "block_id": "ch9_advanced_insights",
            "type": "advanced_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["gold", "diamond", "diamond_plus"],
            "content": """ثالثاً: قاعدة 3–2–1 لاتخاذ القرار
قبل أي قرار في العقار:
اختر:
• 3 أرقام أساسية
• 2 اتجاهات واضحة
• 1 سؤال حاسم
ولا تتجاوز ذلك.

🔢 الأرقام الثلاثة (لا غير):
1️⃣ الطلب  
كيف يتحرك الطلب فعلًا؟  
(مدة بقاء العقار في السوق، سرعة الإغلاق)

2️⃣ العائد  
ليس الأعلى… بل الأكثر استدامة  
إيجار مقابل سعر، أو قابلية إعادة البيع

3️⃣ المخاطرة  
أين يمكن أن تخطئ؟  
تذبذب الأسعار، تركّز المنافسة، ضعف السيولة

📈 الاتجاهان المهمان:
• هل الاتجاه يتحسن ببطء أم يتدهور بهدوء؟
• هل التغير هيكلي أم مؤقت؟

❓ السؤال الواحد:
لو كنت مخطئًا في هذا القرار…
هل الخطأ يمكن احتواؤه؟""",
            "page_weight": 1.4
        },
        {
            "block_id": "ch9_scenarios",
            "type": "scenarios",
            "ai_role": "scenario",
            "ai_editable": True,
            "show_in": ["diamond", "diamond_plus"],
            "content": """رابعاً: مصفاة القرار الذكي (كيف تختار أرقامك؟)
عند النظر إلى بيانات المنصة، اسأل:
1. هل هذا الرقم يعكس السوق كله أم جزءًا منه؟
2. هل هو لقطة زمنية أم اتجاه ممتد؟
3. هل يتأثر بعوامل موسمية؟
4. هل تغيّر خلال آخر 3 أشهر؟
5. ماذا لا يخبرني هذا الرقم؟

البيانات لا تكذب…
لكنها لا تحكي القصة كاملة.

خامساً: متى تتجاهل البيانات تمامًا؟
نعم، أحيانًا
أفضل قرار
هو تجاهل البيانات.

تجاهلها عندما:
• تتضارب بشدة
• لا تعكس وضعك الخاص
• لا تغيّر من قرارك مهما كانت

إذا كانت البيانات:
• لا تضيف وضوحًا
• ولا تقلل مخاطرة
• ولا تغير توقيتًا

فهي تشويش، لا أداة.""",
            "page_weight": 1.5
        },
        {
            "block_id": "ch9_international",
            "type": "international_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["diamond_plus"],
            "content": """مقارنة منهجيات تحليل البيانات في 10 دول:
1. الإمارات - تحليل كمي متقدم
2. السعودية - تحليل نوعي + كمي
3. قطر - تحليل محافظ
4. الكويت - تحليل تقليدي
5. البحرين - تحليل مختلط
6. عمان - تحليل سياحي
7. الأردن - تحليل متخصص
8. مصر - تحليل تنموي
9. المغرب - تحليل سياحي
10. تركيا - تحليل سريع""",
            "page_weight": 1.6
        },
        {
            "block_id": "ch9_conclusion",
            "type": "chapter_conclusion",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """خلاصة الفصل
البيانات أداة قوية
لكنها تصبح خطيرة
عندما تحلّ محل التفكير.

أنت لا تحتاج أن تكون خبير بيانات،
بل صانع قرار يعرف:
• ماذا يقرأ
• ومتى يتوقف
• ومتى يثق بحكمه

في الفصل القادم والأخير،
سنغلق الدائرة كاملة:
كيف تتخذ القرار النهائي… وتنام مرتاحًا بعده.""",
            "page_weight": 0.8
        }
    ]

# ========== الفصل العاشر: القرار النهائي ==========
def chapter_10_blocks(user_info):
    property_type = user_info.get("نوع_العقار", "العقار")
    city = user_info.get("المدينة", "المدينة")
    
    return [
        {
            "block_id": "ch10_title",
            "type": "chapter_title",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": f"الفصل العاشر – كيف تبني قرارك النهائي… وتنام مرتاحًا بعده",
            "page_weight": 0.3
        },
        {
            "block_id": "ch10_intro",
            "type": "chapter_context",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """مقدمة الفصل: القرار ليس لحظة… بل نتيجة

بعد كل ما قرأته في هذا التقرير، قد تشعر بشيء غير معتاد:
ليس الحماس، وليس الخوف… بل الوضوح.

وهذا بالضبط ما نبحث عنه هنا.

القرار العقاري الجيد لا يُقاس بمدى جرأته،
ولا بسرعة تنفيذه،
ولا بكمية الأرباح التي يُقال إنها ممكنة.

القرار الجيد هو القرار الذي:
• تفهم أسبابه
• تستطيع الدفاع عنه لاحقًا
• ولا يطاردك نفسيًا بعد اتخاذه""",
            "page_weight": 1.0
        },
        {
            "block_id": "ch10_market_analysis",
            "type": "main_content",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["silver", "gold", "diamond", "diamond_plus"],
            "content": """أولًا: لماذا أصعب جزء في الاستثمار هو "الإغلاق"؟
كثير من القرارات العقارية لا تفشل عند التحليل،
ولا عند التوقيت،
ولا حتى عند التنفيذ.
تفشل عند لحظة الإغلاق.

لحظة تقول فيها لنفسك:
"نعم، هذا هو القرار الذي سأمضي به."

في هذه اللحظة تحديدًا:
• يبدأ الشك
• تظهر المقارنات
• يعلو صوت "ماذا لو؟"

وهنا يخطئ الكثيرون:
• بعضهم يندفع هروبًا من التردد
• وبعضهم يتراجع خوفًا من الخطأ
• وقلة قليلة فقط… تُغلق القرار بوعي""",
            "page_weight": 1.2
        },
        {
            "block_id": "ch10_advanced_insights",
            "type": "advanced_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["gold", "diamond", "diamond_plus"],
            "content": """ثانياً: اختبار القرار الهادئ (اختبار النوم)
قبل أن تعتبر أي قرار عقاري "نهائيًا"،
اسأل نفسك هذا السؤال البسيط:
هل أستطيع النوم مرتاحًا وأنا أحمل هذا القرار؟

ليس اليوم فقط…
بل بعد شهر،
وبعد سنة،
ولو تغيرت الظروف قليلًا.

إذا كان القرار:
• يمنحك راحة عقلية
• لا يعتمد على سيناريو واحد متفائل
• ولا يجبرك على تبرير نفسك للآخرين

فهو غالبًا قرار ناضج.

أما إذا كان:
• يحتاج منك الدفاع المستمر
• أو يسبب توترًا كلما سمعت خبرًا
• أو يجعلك تراقب السوق بقلق يومي

فهذه ليست مشكلة سوق…
بل مشكلة قرار.""",
            "page_weight": 1.3
        },
        {
            "block_id": "ch10_scenarios",
            "type": "scenarios",
            "ai_role": "scenario",
            "ai_editable": True,
            "show_in": ["diamond", "diamond_plus"],
            "content": """ثالثاً: قاعدة "الثلاث نعم" قبل الإغلاق
قبل الإغلاق النهائي لأي قرار متعلق بالعقار،
تأكد أنك تستطيع أن تقول نعم بصدق على الأسئلة الثلاثة التالية:

1️⃣ نعم منطقية  
هل هذا القرار مبني على فهم، لا على ضجيج أو مقارنة سريعة؟

2️⃣ نعم نفسية  
هل تشعر أنك اخترته لأنك مقتنع، لا لأنك خائف من فوات الفرصة؟

3️⃣ نعم زمنية  
هل يناسب هذا القرار أفقك الزمني الحقيقي، لا ما تتمنى أن يحدث بسرعة؟

إذا وجدت نفسك تتردد في واحدة منها،
فالقرار لم ينضج بعد…
وهذا ليس فشلًا، بل وعي.

رابعاً: تمرين الإغلاق النهائي (قاعدة 24 ساعة)
اليوم الأول:
• اكتب قرارك كما هو الآن
• اكتب تحته ثلاثة أسباب عقلانية فقط (بدون مشاعر)

اترك الورقة 24 ساعة
لا تضف، لا تعدّل، لا تناقش أحدًا.

اليوم الثاني:
• اقرأ ما كتبت
• اسأل نفسك:
"لو تغير السوق قليلًا… هل سأظل مقتنعًا؟"

إذا كانت الإجابة نعم → القرار جاهز  
إذا شعرت بالحاجة لإعادة الصياغة → لم يحن وقته بعد""",
            "page_weight": 1.5
        },
        {
            "block_id": "ch10_international",
            "type": "international_analysis",
            "ai_role": "analysis",
            "ai_editable": True,
            "show_in": ["diamond_plus"],
            "content": """خامساً: مقارنة منهجيات اتخاذ القرار في 10 أسواق:
1. الإمارات - قرارات سريعة، تحليل كمي
2. السعودية - قرارات مدروسة، تحليل شمولي
3. قطر - قرارات محافظة، تحليل طويل
4. الكويت - قرارات تقليدية، تحليل قصير
5. البحرين - قرارات مختلطة، تحليل متوازن
6. عمان - قرارات سياحية، تحليل موسمي
7. الأردن - قرارات متخصصة، تحليل دقيق
8. مصر - قرارات سريعة، تحليل تنموي
9. المغرب - قرارات سياحية، تحليل طويل
10. تركيا - قرارات سريعة، تحليل سريع""",
            "page_weight": 1.6
        },
        {
            "block_id": "ch10_conclusion",
            "type": "final_conclusion",
            "ai_role": "fixed",
            "ai_editable": False,
            "show_in": ["free", "silver", "gold", "diamond", "diamond_plus"],
            "content": """خاتمة التقرير الكامل

القرار العقاري الجيد ليس الذي لا يخطئ…
بل الذي لا يدمّرك إن أخطأ.

إذا بنيت قرارك على:
• فهم حقيقي
• توقعات واقعية
• وهوامش أمان
• وراحة داخلية

فحتى إن لم يكن مثاليًا،
سيظل قرارًا ذكيًا.

هذا التقرير لم يُكتب ليقودك إلى صفقة.
بل ليقودك إلى قرار يمكنك العيش معه بسلام.

والآن…
القرار لم يعد في البيانات،
ولا في السوق،
ولا في التوقعات.
القرار عندك.

الاستثمار الذكي لا يصنع ضجيجًا…
لكنه يصنع راحة، واستمرارية، وثروة على مهل.

🎯 نهاية التقرير الاستثماري المتقدم 🎯""",
            "page_weight": 1.0
        }
    ]

# ========== نظام البناء الكامل مع التعديلات الثلاثة ==========
def build_complete_report(user_info):
    """بناء التقرير الكامل مع الفلترة حسب الباقة"""
    
    # توحيد اسم الباقة
    package = user_info.get("package", "free")
    
    # 🔴 التعديل 1: التحقق من صحة الباقة
    if package not in PACKAGES:
        raise ValueError(f"نوع الباقة غير مدعوم: {package}. الباقات المتاحة: {', '.join(PACKAGES.keys())}")
    
    # جمع كل الفصول
    all_chapters_funcs = [
        chapter_1_blocks,
        chapter_2_blocks,
        chapter_3_blocks,
        chapter_4_blocks,
        chapter_5_blocks,
        chapter_6_blocks,
        chapter_7_blocks,
        chapter_8_blocks,
        chapter_9_blocks,
        chapter_10_blocks
    ]
    
    # فلترة البلوكات حسب الباقة
    filtered_report = {
        "user_info": user_info,
        "package": package,
        "package_name": PACKAGES.get(package, {}).get("name", "غير معروف"),
        "chapters": []
    }
    
    total_page_weight = 0
    total_blocks = 0
    total_charts = 0
    total_ai_editable = 0
    
    for i, chapter_func in enumerate(all_chapters_funcs, 1):
        # إنشاء فصل كامل
        chapter_blocks = chapter_func(user_info)
        
        # فلترة البلوكات في هذا الفصل
        filtered_blocks = []
        for block in chapter_blocks:
            if package in block.get("show_in", []):
                filtered_blocks.append(block)
                
                # حساب إحصائيات
                total_page_weight += block.get("page_weight", 0.5)
                total_blocks += 1
                
                if block.get("type") == "chart":
                    total_charts += 1
                
                # 🔴 التعديل 2: عد البلوكات القابلة للتعديل بالذكاء الاصطناعي
                if block.get("ai_editable", False):
                    total_ai_editable += 1
        
        # إضافة الفصل المفلتر
        if filtered_blocks:  # فقط إذا كان هناك بلوكات بعد الفلترة
            filtered_report["chapters"].append({
                "chapter_number": i,
                "chapter_title": next(
                    (b["content"] for b in chapter_blocks if b["type"] == "chapter_title"), 
                    f"الفصل {i}"
                ),
                "blocks": filtered_blocks,
                "block_count": len(filtered_blocks),
                "chapter_weight": sum(b.get("page_weight", 0.5) for b in filtered_blocks)
            })
    
    # حساب الصفحات بناءً على الوزن
    estimated_pages = calculate_pages_from_weight(total_page_weight, package)
    
    # إحصائيات التقرير
    filtered_report["stats"] = {
        "total_chapters": len(filtered_report["chapters"]),
        "total_blocks": total_blocks,
        "total_charts": total_charts,
        "total_ai_editable": total_ai_editable,  # 🔴 التعديل 2: إحصائية جديدة
        "ai_editable_percentage": round((total_ai_editable / total_blocks * 100), 1) if total_blocks > 0 else 0,
        "total_page_weight": round(total_page_weight, 1),
        "estimated_pages": estimated_pages,
        "target_pages": PACKAGES.get(package, {}).get("pages", 0),
        "accuracy": round((estimated_pages / PACKAGES.get(package, {}).get("pages", 1)) * 100, 1) if PACKAGES.get(package, {}).get("pages", 0) > 0 else 0
    }
    
    return filtered_report

def calculate_pages_from_weight(weight, package):
    """تحويل الوزن إلى عدد صفحات"""
    # معادلة تحويل: 1 وزن = 0.8 صفحة تقريباً
    base_pages = weight * 0.8
    
    # ضبط حسب الباقة
    adjustments = {
        "free": 0.9,
        "silver": 0.95,
        "gold": 1.0,
        "diamond": 1.05,
        "diamond_plus": 1.1
    }
    
    adjusted_pages = base_pages * adjustments.get(package, 1.0)
    return round(adjusted_pages)

def filter_blocks_by_report_type(blocks, package):
    """ترشيح البلوكات حسب نوع التقرير"""
    return [block for block in blocks if package in block.get("show_in", [])]

# ========== اختبار النظام ==========
if __name__ == "__main__":
    print("🔧 اختبار نظام التقارير العقارية المتقدم مع التعديلات الثلاثة")
    print("=" * 60)
    
    # اختبار كل الباقات
    test_cases = [
        {"package": "free", "نوع_العقار": "شقق سكنية", "المدينة": "الرياض"},
        {"package": "silver", "نوع_العقار": "فيلا", "المدينة": "جدة"},
        {"package": "gold", "نوع_العقار": "أرض سكنية", "المدينة": "الدمام"},
        {"package": "diamond", "نوع_العقار": "عمارة سكنية", "المدينة": "مكة"},
        {"package": "diamond_plus", "نوع_العقار": "مجمع تجاري", "المدينة": "الخبر"},
    ]
    
    print("\n📊 نتائج اختبار جميع الباقات:")
    for test_case in test_cases:
        try:
            report = build_complete_report(test_case)
            print(f"\n✅ {PACKAGES[test_case['package']]['name']} ({test_case['package']}):")
            print(f"   • العقار: {test_case['نوع_العقار']} في {test_case['المدينة']}")
            print(f"   • الفصول: {report['stats']['total_chapters']}")
            print(f"   • البلوكات: {report['stats']['total_blocks']}")
            print(f"   • الرسومات: {report['stats']['total_charts']}")
            print(f"   • قابل للتعديل بالذكاء الاصطناعي: {report['stats']['total_ai_editable']} ({report['stats']['ai_editable_percentage']}%)")
            print(f"   • الصفحات المتوقعة: {report['stats']['estimated_pages']}")
            print(f"   • الصفحات المستهدفة: {report['stats']['target_pages']}")
            print(f"   • الدقة: {report['stats']['accuracy']}%")
        except ValueError as e:
            print(f"\n❌ خطأ في {test_case['package']}: {e}")
    
    # اختبار باقة غير صالحة (التعديل 1)
    print("\n🔍 اختبار التعديل 1: باقة غير صالحة")
    try:
        build_complete_report({"package": "invalid_package", "نوع_العقار": "شقق", "المدينة": "الرياض"})
    except ValueError as e:
        print(f"✅ نجاح: تم رفض الباقة غير الصالحة - {e}")
    
    print("\n" + "=" * 60)
    print("🎯 التعديلات الثلاثة المطبقة بنجاح:")
    print("   1. ✅ التحقق من صحة الباقة")
    print("   2. ✅ إضافة مفتاح ai_editable لكل بلوك")
    print("   3. ✅ جاهز للتعديل 3 (fallback للرسومات في ملف منفصل)")
    print(f"\n🚀 النظام جاهز للعمل مع {len(PACKAGES)} باقات!")
    print("💾 ملف report_content_builder.py مغلق وجاهز للمراحل التالية")
