from government_data_provider import load_government_data


def get_market_data(city=None, property_type=None):
    """
    طبقة وسيطة لجلب بيانات السوق

    ملاحظة:
    Government Data Provider أصبح يقوم بكل عمليات:
    - قراءة الملف
    - تنظيف البيانات
    - الفلترة

    لذلك هنا نقوم فقط بتحميل البيانات بدون فلترة
    لتجنب حذف الصفوف مرتين.
    """

    # تحميل البيانات بدون فلترة
    df = load_government_data()

    # التحقق من وجود بيانات
    if df is None or df.empty:
        raise Exception("❌ لا توجد بيانات متاحة في ملف الصفقات")

    # إعادة ترتيب الفهرس
    return df.reset_index(drop=True)
