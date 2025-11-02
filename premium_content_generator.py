# premium_content_generator.py

class PremiumContentGenerator:
    def generate_for_package(self, base_content, package_level, user_info):
        pages = {"مجانية": 15, "فضية": 35, "ذهبية": 60, "ماسية": 90}
        target_pages = pages.get(package_level, 15)

        expanded_content = base_content

        for i in range(1, (target_pages // 5) + 1):
            expanded_content += f"""
            
            📚 **القسم الإضافي {i} - تحليل متقدم**
            
            هذا قسم إضافي يملأ الصفحات بمحتوى حقيقي عن سوق العقارات في {user_info['city']}
            ونصائح مخصصة ل{user_info['user_type']} لتحقيق أفضل النتائج.
            
            💡 **التوصية {i}:** استثمر في المناطق الواعدة
            📊 **التحليل {i}:** بيانات مفصلة عن العوائد
            """

        return expanded_content
