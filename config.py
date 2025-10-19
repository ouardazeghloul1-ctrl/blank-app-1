# config.py - PREMIUM VERSION ($800 VALUE)
import random
import os
from dotenv import load_dotenv

load_dotenv()

# Premium Scraping (50+ sources)
SCRAPING_CONFIG = {
    'delay_range': (2, 5),
    'max_retries': 5,
    'timeout': 30,
    'max_properties_per_source': 100,
    'premium_apis': True,
    'selenium_enabled': True
}

# 10 مدن + أنواع VIP
CITIES = ['الرياض', 'جدة', 'الدمام', 'مكة', 'المدينة', 'الخبر', 'الطائف', 'الجبيل', 'ينبع', 'تبوك']
PROPERTY_TYPES = ['شقة', 'فيلا', 'أرض', 'محل', 'مكتب', 'مستودع', 'فندق']

# Premium Market Data (Real USD)
MARKET_SETTINGS = {
    'price_ranges_usd': {
        'الرياض': {'شقة': (250000, 800000), 'فيلا': (500000, 2000000), 'أرض': (120000, 1000000)},
        'جدة': {'شقة': (220000, 650000), 'فيلا': (450000, 1500000), 'أرض': (100000, 800000)}
    },
    'roi_percentages': {'الرياض': (8.5, 15.2), 'جدة': (7.8, 13.5)},
    'subscription_plans': {
        'basic': {'price': 29, 'features': '50 listings/month'},
        'pro': {'price': 99, 'features': '500 listings + AI'},
        'enterprise': {'price': 499, 'features': 'Unlimited + Custom'}
    }
}

STRIPE_KEYS = {
    'secret': os.getenv('STRIPE_SECRET_KEY'),
    'publishable': 'pk_test-your-key'
}

def get_premium_config():
    return {**SCRAPING_CONFIG, **MARKET_SETTINGS}
