# إعدادات الأمان والتهيئة
SCRAPING_CONFIG = {
    'delay_range': (2, 4),
    'max_retries': 3,
    'timeout': 15,
    'max_properties_per_source': 25,
    'respect_robots_txt': True,
}

# المدن وأنواع العقارات المستهدفة
CITIES = ['الرياض', 'جدة', 'الدمام', 'مكة', 'المدينة']
PROPERTY_TYPES = ['شقة', 'فيلا', 'أرض']

# إعدادات User-Agent
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]
