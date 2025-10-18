# config.py - الإصدار المحسن
import random

# إعدادات الأمان والتهيئة
SCRAPING_CONFIG = {
    'delay_range': (3, 6),  # زيادة التأخير لتفادي الحظر
    'max_retries': 3,
    'timeout': 20,
    'max_properties_per_source': 20,  # تقليل العدد لتفادي الحظر
    'respect_robots_txt': True,
}

# المدن وأنواع العقارات المستهدفة
CITIES = ['الرياض', 'جدة', 'الدمام', 'مكة المكرمة', 'المدينة المنورة']
PROPERTY_TYPES = ['شقة', 'فيلا', 'أرض', 'محل تجاري']

# إعدادات User-Agent محدثة
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36'
]

# إعدادات السوق الواقعية
MARKET_SETTINGS = {
    'price_ranges': {
        'الرياض': {'شقة': (2500, 8000), 'فيلا': (1800, 6000), 'أرض': (1200, 4000), 'محل تجاري': (4000, 12000)},
        'جدة': {'شقة': (2200, 6500), 'فيلا': (1600, 5000), 'أرض': (1000, 3500), 'محل تجاري': (3500, 10000)},
        'الدمام': {'شقة': (2000, 5500), 'فيلا': (1400, 4500), 'أرض': (800, 3000), 'محل تجاري': (3000, 8500)}
    },
    'growth_rates': {
        'الرياض': (1.8, 5.5),
        'جدة': (1.5, 4.8),
        'الدمام': (1.2, 4.2)
    }
}

def get_random_delay():
    return random.uniform(*SCRAPING_CONFIG['delay_range'])

def get_random_user_agent():
    return random.choice(USER_AGENTS)
