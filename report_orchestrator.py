from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from bidi.algorithm import get_display
import arabic_reshaper


def ar(text):
    if not text:
        return ""
    try:
        return get_display(arabic_reshaper.reshape(str(text)))
    except Exception:
        return str(text)


def build_report_story(user_info, styles):
    story = []

    # نمط عربي أساسي
    arabic_style = ParagraphStyle(
        'Arabic',
        parent=styles['Normal'],
        fontName='Amiri',
        fontSize=12,
        leading=20,
        alignment=2
    )

    title_style = ParagraphStyle(
        'ArabicTitle',
        parent=styles['Title'],
        fontName='Amiri',
        fontSize=18,
        alignment=2,
        spaceAfter=20
    )

    subtitle_style = ParagraphStyle(
        'ArabicSubtitle',
        parent=styles['Heading2'],
        fontName='Amiri',
        fontSize=14,
        alignment=2,
        spaceAfter=14
    )

    city = user_info.get("city", "{{المدينة}}")
    prop = user_info.get("property_type", "{{نوع_العقار}}")

    # =====================================================
    # الفصل الأول – صفحة العنوان
    # =====================================================
    story.append(Paragraph(ar(
        f"الفصل الأول - السيناريو الواقعي لمستقبل {prop} في {city} خلال العقد القادم"
    ), title_style))

    story.append(PageBreak())

    # =====================================================
    # مقدمة الفصل
    # =====================================================
    story.append(Paragraph(ar("مقدمة الفصل: لماذا هذا السيناريو بالذات؟"), subtitle_style))

    intro_text = f"""
هذا الفصل لا يهدف إلى إثارة التفاؤل، ولا إلى بث القلق.
ما نقدمه هنا هو قراءة واقعية لمسار سوق {prop} في {city} خلال السنوات العشر القادمة، مبنية على توازن بين العرض، والطلب، والسلوك، وطبيعة السوق المحلي.
في كل سوق عقاري، ترتفع الأصوات عند الصعود، وتكثر التحذيرات عند التباطؤ.
بين الضجيج والتخويف، يضيع القرار الرشيد.
دور هذا الفصل هو إعادة القارئ إلى نقطة نادرة في السوق.
نقطة الفهم قبل التفاعل.
"""
    story.append(Paragraph(ar(intro_text), arabic_style))
    story.append(PageBreak())

    # =====================================================
    # 1.2 كيف نرى السوق اليوم؟
    # =====================================================
    story.append(Paragraph(ar(f"كيف نرى سوق {prop} في {city} اليوم؟"), subtitle_style))

    text_12 = f"""
هذا التحليل لا يفترض زاوية واحدة للتعامل مع السوق، ولا يضع جميع القرارات في قالب واحد.
بل يقدم إطارًا عامًا لفهم المسار المحتمل، يمكن إسقاطه على أي قرار عملي لاحقًا.

قد تقرأه وأنت تفكر في العائد،
أو في الاستقرار،
أو في توقيت البيع أو الشراء،
أو في فهم اتجاه السوق قبل أي التزام.

الزاوية التي تقرأ منها هذا الفصل تحدد كيف ستستفيد منه،
لكن الأساس واحد:
فهم المسار قبل الدخول في التفاصيل.
"""
    story.append(Paragraph(ar(text_12), arabic_style))
    story.append(PageBreak())

    # =====================================================
    # تحليل وضع السوق الحالي
    # =====================================================
    story.append(Paragraph(ar("تحليل وضع السوق الحالي"), subtitle_style))

    market_text = f"""
سوق {prop} في {city} لم يعد سوقًا بسيطًا أو عشوائيًا.
نحن أمام سوق:
• مدفوع بطلب حقيقي، لكن بدرجات متفاوتة
• متأثر بتغيرات اجتماعية وسلوكية واضحة
• مرتبط بعوامل تنظيمية وبنيوية تؤثر في القيمة الفعلية لا الاسمية
• حساس للتوقيت أكثر من أي وقت مضى

الخطأ الشائع اليوم هو قراءة الأسعار بمعزل عن قدرة السوق على الاستيعاب.
نعم، هناك ارتفاعات.
لكن السؤال الأهم دائمًا:
هل هذا الارتفاع مدعوم بطلب مستدام أم بزخم مؤقت؟
"""
    story.append(Paragraph(ar(market_text), arabic_style))
    story.append(PageBreak())

    # =====================================================
    # المخطط الزمني (10 سنوات)
    # =====================================================
    story.append(Paragraph(ar("المخطط الزمني (10 سنوات)"), subtitle_style))

    timeline_text = """
السنوات (1–3) — مرحلة إعادة التوازن
• الطلب لا يختفي، لكنه يصبح أكثر انتقائية
• القرارات العاطفية تتراجع
• القيمة العملية تتقدم على الوعود

السنوات (4–6) — مرحلة الفرز الحقيقي
• الأصول الجيدة تثبت نفسها
• الأصول الضعيفة تخرج بصمت

السنوات (7–10) — سوق ناضج
• أقل اندفاعًا
• أكثر حساسية للجودة
• أدق في التمييز بين أصل وآخر
"""
    story.append(Paragraph(ar(timeline_text), arabic_style))
    story.append(PageBreak())

    # =====================================================
    # مؤشرات المراقبة
    # =====================================================
    story.append(Paragraph(ar("مؤشرات المراقبة الرئيسية"), subtitle_style))

    indicators = f"""
1. متوسط مدة بقاء {prop} في السوق
2. الفجوة بين الأسعار المعروضة والمنفذة
3. سلوك الطلب عند التغيرات السعرية
4. استجابة السوق للمعروض الجديد
5. وتيرة قرارات الإطلاق أو التجميد
"""
    story.append(Paragraph(ar(indicators), arabic_style))
    story.append(PageBreak())

    # =====================================================
    # الخلاصة
    # =====================================================
    story.append(Paragraph(ar("خلاصة الفصل"), subtitle_style))

    conclusion = """
هذا السيناريو ليس وعدًا، ولا تحذيرًا.
هو قراءة هادئة لمسار محتمل.
هذا الفصل ليس نهاية شيء…
بل بداية طريقة تفكير.
"""
    story.append(Paragraph(ar(conclusion), arabic_style))
    story.append(PageBreak())

    return story
