import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, dataframe):
        self.df = dataframe
    
    def clean_data(self):
        """تنظيف شامل للبيانات"""
        self.remove_duplicates()
        self.filter_invalid_prices()
        self.filter_invalid_areas()
        self.calculate_price_per_sqm()
        self.remove_outliers()
        return self.df
    
    def remove_duplicates(self):
        """إزالة التكرارات"""
        self.df = self.df.drop_duplicates(
            subset=['Title', 'Price', 'Area', 'City', 'District'], 
            keep='first'
        )
    
    def filter_invalid_prices(self):
        """تصفية الأسعار غير المنطقية"""
        self.df = self.df[
            (self.df['Price'] >= 10000) & 
            (self.df['Price'] <= 50000000)  # حتى 50 مليون ريال
        ]
    
    def filter_invalid_areas(self):
        """تصفية المساحات غير المنطقية"""
        self.df = self.df[
            (self.df['Area'] >= 10) & 
            (self.df['Area'] <= 5000)  # حتى 5000 متر
        ]
    
    def calculate_price_per_sqm(self):
        """حساب سعر المتر المربع"""
        self.df['Price_Per_SQM'] = self.df['Price'] / self.df['Area']
        # إزالة القيم المتطرفة في سعر المتر
        self.df = self.df[
            (self.df['Price_Per_SQM'] >= 100) & 
            (self.df['Price_Per_SQM'] <= 50000)
        ]
    
    def remove_outliers(self):
        """إزالة القيم المتطرفة باستخدام IQR"""
        for column in ['Price', 'Area', 'Price_Per_SQM']:
            if column in self.df.columns:
                Q1 = self.df[column].quantile(0.25)
                Q3 = self.df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                self.df = self.df[
                    (self.df[column] >= lower_bound) & 
                    (self.df[column] <= upper_bound)
                ]
