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
                ],
                "metrics": ["العائد_المتوقع", "مستوى_الخطورة", "نمو_السعر", "السيولة"]
            },
            "مالك عقار": {
                "primary_need": "تحقيق أقصى قيمة للعقار", 
                "key_questions": [
                    "كم تبلغ قيمة عقاري الحالية؟",
                    "ما هو أفضل وقت للبيع؟",
                    "كيف يمكنني زيادة قيمة العقار؟",
                    "ما هي أسعار المنافسين في منطقتي؟"
                ],
                "metrics": ["سعر_المتر", "القيمة_السوقية", "العرض_والطلب", "الاتجاهات"]
            },
            "فرد": {
                "primary_need": "إيجاد سكن مناسب بميزانية معقولة",
                "key_questions": [
                    "ما هي المناطق المناسبة لميزانيتي؟",
                    "ما هي خيارات التمويل المتاحة؟",
                    "أيهما أفضل: الشراء أم التأجير؟",
                    "ما هي المساحات المناسبة للأسرة؟"
                ],
                "metrics": ["السعر", "المساحة", "الموقع", "المرافق"]
            },
            "وسيط عقاري": {
                "primary_need": "زيادة الصفقات وتحقيق عمولات أعلى",
                "key_questions": [
                    "ما هي العقارات الأكثر طلباً؟",
                    "كيف أجد عملاء جدد؟",
                    "ما هي أسعار السوق الحالية؟",
                    "كيف أتفاوض على أفضل الأسعار؟"
                ],
                "metrics": ["حجم_التداول", "الطلبات", "المنافسة", "الاتجاهات"]
            },
            "شركة تطوير": {
                "primary_need": "تخطيط مشاريع مربحة وتقييم الفرص",
                "key_questions": [
                    "أين توجد أفضل الأراضي للتطوير؟",
                    "ما هو الطلب المتوقع على المشروع؟",
                    "كيف أتفوق على المنافسين؟",
                    "ما هي تكاليف التطوير والتشغيل؟"
                ],
                "metrics": ["الطلب_المستقبلي", "التكاليف", "العوائد", "المخاطر"]
            },
            "باحث عن فرصة": {
                "primary_need": "اكتشاف فرص استثنائية وغير تقليدية",
                "key_questions": [
                    "أين توجد الصفقات الاستثنائية؟",
                    "كيف أكتشف الفرص قبل الآخرين؟",
                    "ما هي الاستراتيجيات غير التقليدية؟",
                    "كيف أستفيد من تقلبات السوق؟"
                ],
                "metrics": ["الفرص_الخاصة", "التوقيت", "الابتكار", "المخاطرة"]
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
            "personalized_analysis": self._generate_personalized_analysis(user_info, market_data, real_data, profile),
            "recommendations": self._generate_recommendations(user_info, market_data, real_data, profile)
        }
        
        return analysis
    
    def _generate_personalized_analysis(self, user_info, market_data, real_data, profile):
        """تحليل مخصص بناءً على بيانات المستخدم والسوق"""
        user_city = user_info.get('city', 'الرياض')
        property_type = user_info.get('property_type', 'شقة')
        user_budget = user_info.get('area', 120) * 5000  # تقدير مبدئي
        
        analysis = f"""
        🔍 **التحليل الشخصي لاحتياجاتك:**
        
        **المدينة:** {user_city}
        **نوع العقار:** {property_type} 
        **الميزانية المقدرة:** {user_budget:,.0f} ريال
        
        """
        
        # إضافة تحليل حسب نوع المستخدم
        if profile["primary_need"] == "زيادة العوائد المالية":
            analysis += self._investor_analysis(real_data, user_budget)
        elif profile["primary_need"] == "تحقيق أقصى قيمة للعقار":
            analysis += self._owner_analysis(real_data, user_info)
        elif profile["primary_need"] == "إيجاد سكن مناسب بميزانية معقولة":
            analysis += self._individual_analysis(real_data, user_budget)
            
        return analysis
    
    def _investor_analysis(self, real_data, budget):
        """تحليل المستثمر"""
        if real_data.empty:
            return "لا توجد بيانات كافية للتحليل"
        
        high_return = real_data[real_data['العائد_المتوقع'] > real_data['العائد_المتوقع'].mean()]
        affordable_high_return = high_return[high_return['السعر'] <= budget * 1.2]
        
        analysis = f"""
        📈 **تحليل المستثمر:**
        
        • **عدد الفرص ذات العوائد المرتفعة:** {len(affordable_high_return)} عقار
        • **متوسط العائد في السوق:** {real_data['العائد_المتوقع'].mean():.1f}%
        • **أعلى عائد متاح:** {real_data['العائد_المتوقع'].max():.1f}%
        
        💼 **الفرص المتاحة ضمن ميزانيتك:**
        """
        
        if not affordable_high_return.empty:
            for _, prop in affordable_high_return.head(3).iterrows():
                analysis += f"\n   • {prop['العقار']} - عائد {prop['العائد_المتوقع']}%"
        else:
            analysis += "\n   • نوصي بمراجعة الميزانية أو نوع العقار"
            
        return analysis
    
    def _generate_recommendations(self, user_info, market_data, real_data, profile):
        """توليد توصيات مخصصة"""
        recommendations = []
        
        if profile["primary_need"] == "زيادة العوائد المالية":
            recommendations = [
                "التركيز على المناطق النامية ذات البنية التحتية الجديدة",
                "تنويع المحفظة بين العقارات السكنية والتجارية",
                "الاستثمار في مشاريع قيد التطوير بأسعار ما قبل الإطلاق",
                "متابعة مؤشرات السيولة شهرياً لتحقيق أرباح سريعة"
            ]
        elif profile["primary_need"] == "تحقيق أقصى قيمة للعقار":
            recommendations = [
                "تحسين الواجهة الخارجية والداخلية للعقار",
                "الانتظار 3-6 أشهر إذا كان السوق في اتجاه صاعد",
                "العرض في أكثر من منصة لتوسيع قاعدة المشترين",
                "إبراز المميزات الفريدة للعقار في الإعلان"
            ]
            
        return recommendations
