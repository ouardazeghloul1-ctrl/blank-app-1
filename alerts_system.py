# =========================================
# ALERTS SYSTEM – نظام التنبيهات الموحد
# =========================================
# يجمع هذا الملف كل وظائف التنبيهات في مكان واحد:
# 1️⃣ القواعد والثوابت
# 2️⃣ محرك استخراج الفرص
# 3️⃣ تجميع كل المدن
# 4️⃣ التخزين المؤقت والواجهة
# =========================================

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# ==============================
# 1️⃣ القواعد والثوابت (Alert Rules)
# ==============================

# المدن المستهدفة
CITIES = ["الرياض", "جدة", "مكة المكرمة", "المدينة المنورة", "الدمام"]

# أنواع العقارات
PROPERTY_TYPES = ["شقة", "فيلا", "أرض"]

# الحد الأدنى للخصم لاعتبارها فرصة ذهبية
MIN_DISCOUNT_PERCENT = 15

# مدة التخزين المؤقت (بالساعات)
CACHE_HOURS = 6

# مسار ملف التخزين الدائم
ALERTS_FILE = Path("alerts/alerts_db.json")

# أنواع التنبيهات
ALERT_TYPES = {
    "GOLDEN_OPPORTUNITY": "💰 فرصة ذهبية - خصم قوي عن السوق",
    "MARKET_SHIFT": "📊 تحول سعري غير طبيعي",
    "RISK_WARNING": "⚠️ خطر خفي يظهر",
}

# ==============================
# 2️⃣ التخزين الدائم (Alert Storage)
# ==============================

def ensure_alerts_directory():
    """التأكد من وجود مجلد التنبيهات"""
    ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_alerts():
    """تحميل جميع التنبيهات المخزنة"""
    ensure_alerts_directory()
    if not ALERTS_FILE.exists():
        return []
    try:
        return json.loads(ALERTS_FILE.read_text(encoding="utf-8"))
    except:
        return []

def save_alert(alert: dict):
    """حفظ تنبيه جديد في الملف الدائم"""
    alerts = load_alerts()
    alert["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alerts.append(alert)
    
    ensure_alerts_directory()
    ALERTS_FILE.write_text(
        json.dumps(alerts, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def get_today_stored_alerts(city: str = None):
    """جلب تنبيهات اليوم من الملف الدائم (للمدينة المحددة أو الكل)"""
    today = datetime.now().strftime("%Y-%m-%d")
    all_alerts = load_alerts()
    
    # تصفية حسب اليوم
    today_alerts = [
        a for a in all_alerts
        if a.get("generated_at", "").startswith(today)
    ]
    
    # تصفية حسب المدينة إذا طلبت
    if city:
        today_alerts = [a for a in today_alerts if a.get("city") == city]
    
    return today_alerts

# ==============================
# 3️⃣ محرك التنبيهات (Alert Engine)
# ==============================

from live_real_data_provider import get_live_real_data
from smart_opportunities import SmartOpportunityFinder

class AlertEngine:
    """محرك استخراج الفرص الذهبية من البيانات الحقيقية"""
    
    def __init__(self):
        self.opportunity_finder = SmartOpportunityFinder()

    def generate_city_alerts(self, city, property_type):
        """
        يولد جميع الفرص الذهبية لمدينة واحدة ونوع عقار محدد
        """
        # جلب البيانات الحقيقية
        real_data = get_live_real_data(
            city=city,
            property_type=property_type
        )

        if real_data.empty:
            return []

        # البحث عن العقارات المخفضة
        undervalued = self.opportunity_finder.find_undervalued_properties(
            real_data, city
        )

        if not undervalued:
            return []

        alerts = []

        # تحويل كل فرصة إلى تنبيه (بدون استثناء)
        for prop in undervalued:
            # تحويل الخصم من نص إلى رقم مع أمان
            discount_raw = prop.get("الخصم", "0").replace("%", "")
            try:
                discount = float(discount_raw)
            except:
                continue

            # تجاهل الخصومات الضعيفة
            if discount < MIN_DISCOUNT_PERCENT:
                continue

            # أمان لأسماء الحقول - نحاول أكثر من مفتاح
            current_price = prop.get("السعر_الحالي") or prop.get("السعر") or 0
            avg_price = prop.get("متوسط_المنطقة") or prop.get("متوسط_السعر") or 0
            district = prop.get("المنطقة") or prop.get("الحي") or "غير محدد"
            expected_return = prop.get("العائد_المتوقع", "غير متاح")
            
            # إنشاء كائن التنبيه
            alert = {
                "type": "GOLDEN_OPPORTUNITY",
                "city": city,
                "district": district,
                "title": "💰 فرصة ذهبية بخصم قوي",
                "description": f"عقار {property_type} في {district} بخصم {discount:.1f}% عن متوسط المنطقة",
                "signal": {
                    "discount_percent": discount,
                    "current_price": current_price,
                    "avg_area_price": avg_price,
                    "expected_return": expected_return,
                    "window_hours": 48,
                    "property_type": property_type
                },
                "confidence": "HIGH",
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "source": "AlertEngine",
                "property_type": property_type
            }
            
            alerts.append(alert)
            
            # 💾 حفظ تلقائي في الملف الدائم (اختياري)
            # يمكنك تفعيل هذا السطر إذا أردت حفظ كل تنبيه
            # save_alert(alert)

        return alerts

# ==============================
# 4️⃣ تجميع كل المدن (Daily Aggregator)
# ==============================

def generate_all_alerts():
    """
    يجمع كل التنبيهات من جميع المدن وجميع أنواع العقارات
    هذه هي الدالة الرئيسية لتوليد التنبيهات
    """
    engine = AlertEngine()
    all_alerts = []

    # جولة على جميع المدن
    for city in CITIES:
        # جولة على جميع أنواع العقارات
        for prop_type in PROPERTY_TYPES:
            # جمع التنبيهات لهذه المدينة ونوع العقار
            city_alerts = engine.generate_city_alerts(city, prop_type)
            all_alerts.extend(city_alerts)

    # ترتيب عشوائي لتنويع العرض (مرة واحدة فقط)
    random.shuffle(all_alerts)
    
    return all_alerts

# ==============================
# 5️⃣ التخزين المؤقت والواجهة (Integration + Cache)
# ==============================

# استيراد Streamlit بشكل آمن (لأنه قد لا يكون متاحًا في كل البيئات)
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    # إنشاء مخزن مؤقت بديل إذا لم يكن Streamlit موجودًا
    class SimpleCache:
        def __init__(self):
            self.alerts = []
            self.alerts_time = None
    st = SimpleCache()

def get_today_alerts(force_refresh=False):
    """
    ✅ المصدر الوحيد للتنبيهات في الواجهة
    يستخدم التخزين المؤقت لمدة 6 ساعات
    
    المعاملات:
        force_refresh: إذا كان True، يتجاهل الكاش ويجلب بيانات جديدة
    
    ترجع:
        قائمة التنبيهات
    """
    # التحقق من وجود التخزين المؤقت
    if not hasattr(st, 'alerts'):
        st.alerts = []
        st.alerts_time = None
    
    # إذا طلب تحديث إجباري
    if force_refresh:
        print("🔄 تحديث إجباري للتنبيهات...")
        alerts = generate_all_alerts()
        st.alerts = alerts
        st.alerts_time = datetime.now()
        return alerts
    
    # إذا كان هناك تخزين مؤقت ولم تنته مدته
    if st.alerts_time and hasattr(st, 'alerts'):
        try:
            time_diff = datetime.now() - st.alerts_time
            if time_diff < timedelta(hours=CACHE_HOURS):
                print(f"✅ استخدام التنبيهات المخزنة (آخر تحديث: {time_diff.seconds//60} دقيقة)")
                return st.alerts
        except:
            pass  # في حالة خطأ، نحدث التنبيهات
    
    # تحديث التنبيهات
    print("🔄 تحديث التنبيهات من المصدر الحي...")
    alerts = generate_all_alerts()
    st.alerts = alerts
    st.alerts_time = datetime.now()
    
    return alerts

def refresh_alerts():
    """تحديث إجباري للتنبيهات (للاستخدام اليدوي)"""
    return get_today_alerts(force_refresh=True)

def get_alerts_by_city(city):
    """ترجع تنبيهات مدينة محددة فقط"""
    all_alerts = get_today_alerts()
    return [a for a in all_alerts if a.get("city") == city]

def get_alerts_by_type(alert_type="GOLDEN_OPPORTUNITY"):
    """ترجع تنبيهات من نوع محدد"""
    all_alerts = get_today_alerts()
    return [a for a in all_alerts if a.get("type") == alert_type]

def get_alert_count():
    """ترجع عدد التنبيهات المتاحة اليوم"""
    return len(get_today_alerts())

# ==============================
# 6️⃣ أدوات التنسيق والعرض
# ==============================

def format_alert_for_display(alert):
    """
    تنسيق التنبيه ليظهر بشكل جميل في الواجهة
    """
    signal = alert.get("signal", {})
    discount = signal.get("discount_percent", 0)
    
    # تنسيق السعر مع فواصل للألاف
    current_price = signal.get('current_price', 0)
    if current_price:
        try:
            price_str = f"{int(current_price):,}"
        except:
            price_str = str(current_price)
    else:
        price_str = "غير متاح"
    
    # أيقونة حسب نوع التنبيه
    icon = "💰"
    if alert.get("type") == "MARKET_SHIFT":
        icon = "📊"
    elif alert.get("type") == "RISK_WARNING":
        icon = "⚠️"
    
    return {
        "icon": icon,
        "title": alert.get("title", "تنبيه جديد"),
        "description": alert.get("description", ""),
        "details": f"""
**المدينة:** {alert.get('city', 'غير محدد')} | **الحي:** {alert.get('district', 'غير محدد')}
**الخصم:** {discount:.1f}% | **السعر:** {price_str} ريال
**نافذة الفرصة:** {signal.get('window_hours', 48)} ساعة
        """,
        "confidence": alert.get("confidence", "MEDIUM"),
        "time": alert.get("generated_at", "وقت غير محدد")
    }

def print_alerts_summary():
    """طباعة ملخص التنبيهات (للتجربة في الطرفية)"""
    alerts = get_today_alerts()
    print(f"\n{'='*50}")
    print(f"📋 ملخص التنبيهات - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}")
    print(f"إجمالي التنبيهات: {len(alerts)}")
    
    # توزيع حسب المدينة
    for city in CITIES:
        city_count = len([a for a in alerts if a.get("city") == city])
        if city_count > 0:
            print(f"  • {city}: {city_count} تنبيه")
    
    # عرض أول 3 تنبيهات
    if alerts:
        print(f"\n📌 أبرز التنبيهات:")
        for i, alert in enumerate(alerts[:3]):
            signal = alert.get("signal", {})
            discount = signal.get("discount_percent", 0)
            print(f"  {i+1}. {alert['city']} - {alert.get('district', 'غير محدد')}: خصم {discount:.1f}%")

# ==============================
# 7️⃣ اختبار سريع (يشتغل فقط إذا شغلت الملف مباشرة)
# ==============================

if __name__ == "__main__":
    print("\n🧪 تشغيل اختبار نظام التنبيهات...")
    
    # اختبار توليد التنبيهات
    alerts = generate_all_alerts()
    print(f"✅ تم توليد {len(alerts)} تنبيه")
    
    # اختبار التخزين المؤقت
    cached = get_today_alerts()
    print(f"✅ التنبيهات بعد الكاش: {len(cached)}")
    
    # عرض ملخص
    print_alerts_summary()
    
    print("\n✅ نظام التنبيهات يعمل بكفاءة")
