# user_profiler.py - محلل احتياجات المستخدم الذكي
import pandas as pd
import numpy as np
from datetime import datetime

class UserProfiler:
    def __init__(self):
        self.user_needs = {
            "مستثمر": {
                "primary_need": "زيادة العوائد المالية",
                "key_questions": [
                    "ما هي أفضل الفرص الاستثمارية حالياً؟",
                    "ما هو العائد المتوقع على استثماري؟",
                    "كيف يمكنني تقليل المخاطر؟",
                    "ما هي المناطق الأكثر نمواً؟"
                ]
            },
            "مالك عقار": {
                "primary_need": "تحقيق أقصى قيمة للعقار", 
                "key_questions": [
                    "كم تبلغ قيمة عقاري الحالية؟",
                    "ما هو أفضل وقت للبيع؟",
                    "كيف يمكنني زيادة قيمة العقار؟",
                    "ما هي أسعار المنافسين في منطقتي؟"
                ]
            },
            "فرد": {
                "primary_need": "إيجاد سكن مناسب بميزانية معقولة",
                "key_questions": [
                    "ما هي المناطق المناسبة لميزانيتي؟",
                    "ما هي خيارات التمويل المتاحة؟",
                    "أيهما أفضل: الشراء أم التأجير؟",
                    "ما هي المساحات المناسبة للأسرة؟"
                ]
            }
        }
    
    def analyze_user_profile(self, user_info, market_data, real_data):
        """تحليل متعمق لاحتياجات المستخدم"""
        user_type = user_info.get('user_type', 'مستثمر')
        profile = self.user_needs.get(user_type, self.user_needs['مستثمر'])
        
        analysis = {
            "user_type": user_type,
            "primary_need": profile["primary_need"],
            "key_questions": profile["key_questions"],
            "recommendations": self._generate_recommendations(user_info, market_data, real_data, profile)
        }
        
        return analysis
    
    def _generate_recommendations(self, user_info, market_data, real_data, profile):
        """توليد توصيات مخصصة"""
        recommendations = []
        
        if profile["primary_need"] == "زيادة العوائد المالية":
            recommendations = [
                "التركيز على المناطق النامية ذات البنية التحتية الجديدة",
                "تنويع المحفظة بين العقارات السكنية والتجارية",
                "الاستثمار في مشاريع قيد التطوير بأسعار ما قبل الإطلاق"
            ]
        elif profile["primary_need"] == "تحقيق أقصى قيمة للعقار":
            recommendations = [
                "تحسين الواجهة الخارجية والداخلية للعقار",
                "الانتظار 3-6 أشهر إذا كان السوق في اتجاه صاعد",
                "العرض في أكثر من منصة لتوسيع قاعدة المشترين"
            ]
        elif profile["primary_need"] == "إيجاد سكن مناسب بميزانية معقولة":
            recommendations = [
                "البحث في المناطق المتوسطة الأسعار ذات الخدمات الجيدة",
                "الاستفادة من برامج التمويل المدعوم",
                "النظر في خيارات التأجير كبديل مؤقت"
            ]
            
        return recommendations

# اختبار النظام
if __name__ == "__main__":
    profiler = UserProfiler()
    print("✅ محلل احتياجات المستخدم جاهز!")
