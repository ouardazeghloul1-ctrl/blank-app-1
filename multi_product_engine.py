# =========================================
# Multi Product Engine
# يولد آلاف التقارير
# =========================================

PROPERTY_TYPES = [
    "شقة",
    "فيلا",
    "أرض",
    "تاون هاوس",
    "محل تجاري"
]

PRODUCT_TYPES = [
    {
        "key": "investment",
        "title": "تقرير استثماري",
    },
    {
        "key": "decision",
        "title": "هل أشتري في هذا الحي؟",
    },
    {
        "key": "opportunity",
        "title": "فرصة استثمارية",
    },
    {
        "key": "analysis",
        "title": "تحليل عقاري",
    },
    {
        "key": "comparison",
        "title": "مقارنة مع أحياء أخرى",
    }
]


def generate_product_matrix(cities, districts):
    """
    يولد جميع التركيبات الممكنة
    """

    products = []

    for city in cities:
        for district in districts:
            for property_type in PROPERTY_TYPES:
                for product in PRODUCT_TYPES:

                    products.append({
                        "city": city,
                        "district": district,
                        "property_type": property_type,
                        "product_type": product["key"],
                        "product_title": product["title"]
                    })

    return products
