# =========================================
# Government Data Provider - الإصدار الأساسي (النسخة العاملة)
# =========================================
"""
🚀 مزود البيانات الحكومية - يقرأ ملفات وزارة العدل
"""

import pandas as pd
import re
from pathlib import Path
from typing import Optional

DATA_PATH = Path("market_transactions.csv")


def load_government_data(selected_city: Optional[str] = None, 
                        selected_property_type: Optional[str] = None) -> pd.DataFrame:
    """
    تحميل وتنظيف البيانات من ملف وزارة العدل
    """
    
    try:
        if not DATA_PATH.exists():
            print(f"❌ الملف غير موجود: {DATA_PATH}")
            return pd.DataFrame()
        
        print(f"📂 جاري قراءة: {DATA_PATH}")
        df = pd.read_csv(DATA_PATH, encoding='utf-8-sig')
        
        print(f"📊 إجمالي الصفوف: {len(df):,}")
        
        # تنظيف أساسي
        df = df.rename(columns={
            'رقم الصك': 'id',
            'تاريخ الصفقة': 'date',
            'نوع الصفقة': 'type',
            'الحي': 'district',
            'المدينة': 'city',
            'المساحة': 'area',
            'السعر': 'price'
        })
        
        # تحويل الأرقام
        if 'price' in df.columns:
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        if 'area' in df.columns:
            df['area'] = pd.to_numeric(df['area'], errors='coerce')
        
        # إزالة القيم الفارغة
        df = df.dropna(subset=['price'])
        
        # فلترة المدينة
        if selected_city and 'city' in df.columns:
            df = df[df['city'].astype(str).str.contains(selected_city, na=False)]
        
        print(f"✅ بعد التنظيف: {len(df):,} صفقة")
        return df
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return pd.DataFrame()
