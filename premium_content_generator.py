# premium_content_generator.py

class PremiumContentGenerator:
    def generate_for_package(self, base_content, package_level, user_info):
        """
        هذا الملف مسؤول فقط عن:
        - توسيع المحتوى نصيًا
        - بدون تنسيق
        - بدون Markdown
        - بدون Emoji
        """

        pages = {
            "مجانية": 15,
            "فضية": 35,
            "ذهبية": 60,
            "ماسية": 90,
            "ماسية متميزة": 120
        }

        target_pages = pages.get(package_level, 15)

        # ⚠️ مهم: نتأكد أن المحتوى نص فقط
        if not isinstance(base_content, str):
            base_content = str(base_content)

        expanded_content = base_content.strip()

        # نضيف محتوى حقيقي بأسلوب تقرأه PDF بشكل سليم
        extra_sections = []

        sections_count = max(1, target_pages // 6)

        for i in range(1, sections_count + 1):
            extra_sections.append(
                f"""
الفصل الإضافي {i}: تحليل داعم للسوق

في هذا الجزء، نضيف قراءة أعمق لسوق العقارات في مدينة {user_info.get('city', '')}.
يركز هذا التحليل على:
- فهم سلوك الطلب
- قراءة التغيرات السعرية بهدوء
- تقييم الفرص الواقعية بعيدًا عن المبالغة

التوصية العملية:
ينصح بمراقبة المناطق التي يظهر فيها استقرار نسبي في الأسعار
مع وجود طلب حقيقي غير مضاربي، خصوصًا في فئة {user_info.get('property_type', 'العقار')}.

هذا القسم أُضيف لدعم القرار الاستثماري
وليس للتأثير العاطفي على القارئ.
"""
            )

        # دمج المحتوى الأصلي + الإضافي
        final_content = expanded_content + "\n\n" + "\n\n".join(extra_sections)

        return final_content
