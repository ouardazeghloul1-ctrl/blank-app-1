import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, dataframe):
        self.df = dataframe
    
    def clean_data(self):
        self.remove_duplicates()
        self.filter_invalid_prices()
        self.filter_invalid_areas()
        self.calculate_price_per_sqm()
        self.remove_outliers()
        return self.df
    
    def remove_duplicates(self):
        self.df = self.df.drop_duplicates(subset=['العقار', 'السعر', 'المساحة', 'المنطقة'], keep='first')
    
    def filter_invalid_prices(self):
        self.df = self.df[(self.df['السعر'] >= 10000) & (self.df['السعر'] <= 50000000)]
    
    def filter_invalid_areas(self):
        self.df['Area(m²)'] = self.df['المساحة'].str.extract('(\d+)').astype(float)
        self.df = self.df[(self.df['Area(m²)'] >= 10) & (self.df['Area(m²)'] <= 5000)]
    
    def calculate_price_per_sqm(self):
        self.df['Price_Per_SQM'] = self.df['السعر'] / self.df['Area(m²)']
        self.df = self.df[(self.df['Price_Per_SQM'] >= 100) & (self.df['Price_Per_SQM'] <= 50000)]
    
    def remove_outliers(self):
        for column in ['السعر', 'Area(m²)', 'Price_Per_SQM']:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            self.df = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]
