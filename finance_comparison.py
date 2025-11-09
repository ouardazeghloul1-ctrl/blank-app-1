# finance_comparison.py - نظام مقارنة التمويل الذكي
import pandas as pd
import streamlit as st

class FinanceComparator:
    def __init__(self):
        self.banks_data = self._load_banks_data()
    
    def _load_banks_data(self):
        """بيانات البنوك وشركات التمويل في السعودية"""
        return [
            {
                'name': 'الراجحي',
                'type': 'بنك إسلامي',
                'interest_rate': 4.2,
                'max_financing': 5000000,
                'min_salary': 5000,
                'features': ['تمويل إسلامي', 'مرونة في السداد', 'فتر سماح'],
                'processing_time': '3-5 أيام'
            },
            {
                'name': 'الأهلي',
                'type': 'بنك تجاري',
                'interest_rate': 4.5,
                'max_financing': 7000000,
                'min_salary': 6000,
                'features': ['تمويل سريع', 'خدمة عملاء 24/7', 'تغطية شاملة'],
                'processing_time': '2-4 أيام'
            },
            {
                'name': 'ساب',
                'type': 'بنك تجاري',
                'interest_rate': 4.3,
                'max_financing': 6000000,
                'min_salary': 5500,
                'features': ['حلول متكاملة', 'فترات سداد طويلة', 'خصومات للعملاء'],
                'processing_time': '3-6 أيام'
            },
            {
                'name': 'صندوق التنمية العقارية',
                'type': 'حكومي',
                'interest_rate': 3.5,
                'max_financing': 3000000,
                'min_salary': 3000,
                'features': ['أقل فائدة', 'شروط ميسرة', 'مخصص للمواطنين'],
                'processing_time': '7-10 أيام'
            },
            {
                'name': 'الإنماء',
                'type': 'بنك إسلامي',
                'interest_rate': 4.4,
                'max_financing': 5500000,
                'min_salary': 5200,
                'features': ['برامج تمويل متخصصة', 'مرونة عالية', 'خدمة متميزة'],
                'processing_time': '4-7 أيام'
            }
        ]
    
    def compare_financing_options(self, property_price, user_salary, financing_percentage=70):
        """مقارنة خيارات التمويل بناءً على سعر العقار وراتب المستخدم"""
        max_financing = property_price * (financing_percentage / 100)
        
        suitable_options = []
        for bank in self.banks_data:
            if user_salary >= bank['min_salary'] and max_financing <= bank['max_financing']:
                monthly_installment = self._calculate_monthly_payment(
                    max_financing, bank['interest_rate'], 25  # 25 سنة
                )
                
                suitable_options.append({
                    'اسم_البنك': bank['name'],
                    'نوع_التمويل': bank['type'],
                    'نسبة_الفائدة': f"{bank['interest_rate']}%",
                    'التمويل_المتاح': f"{max_financing:,.0f} ريال",
                    'القسط_الشهري': f"{monthly_installment:,.0f} ريال",
                    'مدة_التمويل': '25 سنة',
                    'مميزات': '، '.join(bank['features']),
                    'مدة_المعالجة': bank['processing_time'],
                    'ملاءمة_الراتب': 'مناسب' if user_salary >= bank['min_salary'] * 1.5 else 'مقبول'
                })
        
        return sorted(suitable_options, key=lambda x: float(x['نسبة_الفائدة'][:-1]))
    
    def _calculate_monthly_payment(self, principal, annual_interest, years):
        """حساب القسط الشهري"""
        monthly_interest = annual_interest / 100 / 12
        num_payments = years * 12
        
        if monthly_interest == 0:
            return principal / num_payments
        
        monthly_payment = principal * (monthly_interest * (1 + monthly_interest) ** num_payments) / ((1 + monthly_interest) ** num_payments - 1)
        return monthly_payment
    
    def get_best_financing_option(self, property_price, user_salary):
        """الحصول على أفضل خيار تمويلي"""
        options = self.compare_financing_options(property_price, user_salary)
        if options:
            return options[0]  # أقل فائدة
        return None
    
    def generate_financing_report(self, user_info, property_price):
        """تقرير التمويل المتكامل"""
        user_salary = user_info.get('salary', 10000)  # راتب افتراضي
        
        return {
            'خيارات_التمويل': self.compare_financing_options(property_price, user_salary),
            'أفضل_خيار': self.get_best_financing_option(property_price, user_salary),
            'نصيحة_التمويل': self._get_financing_advice(property_price, user_salary),
            'حاسبة_التمويل': self._create_financing_calculator(property_price)
        }
    
    def _get_financing_advice(self, property_price, user_salary):
        """نصائح تمويلية ذكية"""
        max_affordable_price = user_salary * 150  # قاعدة بسيطة
        
        if property_price > max_affordable_price:
            return "💡 ننصح بالبحث عن عقار بسعر أقل أو زيادة المقدم"
        else:
            return "🎯 السعر مناسب - يمكنك المضي قدماً في التمويل"
    
    def _create_financing_calculator(self, property_price):
        """إنشاء حاسبة تمويل تفاعلية"""
        return {
            'سعر_العقار': f"{property_price:,.0f} ريال",
            'التمويل_المتوقع': f"{property_price * 0.7:,.0f} ريال (70%)",
            'المقدم_المطلوب': f"{property_price * 0.3:,.0f} ريال (30%)"
        }
