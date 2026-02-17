# =========================================
# ALERTS SYSTEM – نظام التنبيهات الموحد (معدل نهائي)
# =========================================
# يجمع هذا الملف كل وظائف التنبيهات في مكان واحد:
# 1️⃣ القواعد والثوابت
# 2️⃣ محرك استخراج الفرص
# 3️⃣ تجميع كل المدن
# 4️⃣ التخزين الدائم مع منع التكرار
# 5️⃣ التخزين المؤقت للواجهة
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

# الحد الأدنى للخصم لاعتبارها فرصة (5% كحد أدنى للظهور)
MIN_DISCOUNT_PERCENT = 5

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
# 2️⃣ التخزين الدائم مع منع التكرار (Alert Storage)
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
    """
    حفظ تنبيه جديد في الملف الدائم مع منع التكرار
    ✅ لا يتم حفظ نفس التنبيه أكثر من مرة
    """
    alerts = load_alerts()

    # 🔥 منع التكرار: نفس المدينة + نفس الحي + نفس الخصم
    for existing in alerts:
        if (
            existing.get("city") == alert.get("city")
            and existing.get("district") == alert.get("district")
            and existing.get("signal", {}).get("discount_percent")
               == alert.get("signal", {}).get("discount_percent")
        ):
            print(f"⚠️ تنبيه مكرر تجاهل: {alert.get('city')} - {alert.get('district')}")
            return  # لا نحفظه مرة أخرى

    alert["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alerts.append(alert)

    ensure_alerts_directory()
    ALERTS_FILE.write_text(
        json.dumps(alerts, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"✅ تم حفظ تنبيه جديد: {alert.get('city')} - {alert.get('district')}")

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

def clear_old_alerts(days=30):
    """حذف التنبيهات الأقدم من عدد محدد من الأيام"""
    alerts = load_alerts()
    cutoff = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff.strftime("%Y-%m-%d")
    
    new_alerts = [
        a for a in alerts
        if a.get("generated_at", "").split()[0] >= cutoff_str
    ]
    
    if len(new_alerts) != len(alerts):
        ALERTS_FILE.write_text(
            json.dumps(new_alerts, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"🧹 تم حذف {len(alerts) - len(new_alerts)} تنبيه قديم")
    
    return new_alerts

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
        try:
            # جلب البيانات الحقيقية
            real_data = get_live_real_data(
                city=city,
                property_type=property_type
            )

            if real_data.empty:
                print(f"⚠️ {city}: لا توجد بيانات")
                return []

            # البحث عن العقارات المخفضة
            undervalued = self.opportunity_finder.find_undervalued_properties(
                real_data, city
            )

            if not undervalued:
                print(f"⚠️ {city}: لا توجد عقارات مخفضة")
                return []

            alerts = []

            # تحويل كل فرصة إلى تنبيه (بدون استثناء)
            for prop in undervalued:
                # تحويل الخصم من نص إلى رقم مع أمان
                discount_raw = prop.get("الخصم", "0").replace("%", "")
                try:
                    discount = float(discount_raw)
                except:
                    discount = 0

                # 🔥 تصنيف قوة التنبيه بدل إلغائه
                if discount >= 15:
                    confidence = "HIGH"
                elif discount >= 8:
                    confidence = "MEDIUM"
                elif discount >= 5:
                    confidence = "LOW"
                else:
                    continue  # أقل من 5% لا نعرضه

                # أمان لأسماء الحقول - نحاول أكثر من مفتاح
                current_price = prop.get("السعر_الحالي") or prop.get("السعر") or 0
                
                # 🔥 منع قتل التنبيهات إذا المتوسط مفقود
                avg_price = prop.get("متوسط_المنطقة") or prop.get("متوسط_السعر") or current_price * 1.1
                
                district = prop.get("المنطقة") or prop.get("الحي") or "غير محدد"
                expected_return = prop.get("العائد_المتوقع", "غير متاح")
                
                # إنشاء كائن التنبيه
                alert = {
                    "type": "GOLDEN_OPPORTUNITY",
                    "city": city,
                    "district": district,
                    "title": f"💰 فرصة {'قوية' if discount >= 15 else 'متوسطة' if discount >= 8 else 'خفيفة'} في {city}",
                    "description": f"عقار {property_type} في {district} بخصم {discount:.1f}% عن متوسط المنطقة",
                    "signal": {
                        "discount_percent": discount,
                        "current_price": current_price,
                        "avg_area_price": avg_price,
                        "expected_return": expected_return,
                        "window_hours": 48,
                        "property_type": property_type
                    },
                    "confidence": confidence,  # HIGH/MEDIUM/LOW حسب الخصم
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "source": "AlertEngine",
                    "property_type": property_type
                }
                
                alerts.append(alert)
                
                # 🔥 حفظ التنبيه مع منع التكرار
                save_alert(alert)
                
                print(f"✅ {city}: تم إنشاء تنبيه {confidence} بخصم {discount}%")

            return alerts
            
        except Exception as e:
            print(f"❌ خطأ في {city}: {str(e)}")
            return []

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
    
    print(f"📊 إجمالي التنبيهات: {len(all_alerts)}")
    return all_alerts

# ==============================
# 5️⃣ التخزين المؤقت (Cache Layer - منفصل عن Streamlit)
# ==============================

class AlertCache:
    """طبقة تخزين مؤقت مستقلة عن Streamlit"""
    
    def __init__(self):
        self.alerts = []
        self.alerts_time = None
        self.cache_hours = CACHE_HOURS
    
    def get(self, force_refresh=False):
        """الحصول على التنبيهات من الكاش"""
        if force_refresh:
            self.alerts = generate_all_alerts()
            self.alerts_time = datetime.now()
            return self.alerts
        
        if self.alerts_time:
            time_diff = datetime.now() - self.alerts_time
            if time_diff < timedelta(hours=self.cache_hours):
                return self.alerts
        
        self.alerts = generate_all_alerts()
        self.alerts_time = datetime.now()
        return self.alerts
    
    def refresh(self):
        """تحديث الكاش"""
        return self.get(force_refresh=True)

# إنشاء كائن الكاش العام (مرة واحدة)
_alert_cache = AlertCache()

# ==============================
# 6️⃣ واجهة الاستخدام (API) - للاستخدام من الملفات الأخرى
# ==============================

def get_today_alerts(force_refresh=False):
    """
    ✅ المصدر الوحيد للتنبيهات في الواجهة
    يستخدم التخزين المؤقت لمدة 6 ساعات
    
    المعاملات:
        force_refresh: إذا كان True، يتجاهل الكاش ويجلب بيانات جديدة
    
    ترجع:
        قائمة التنبيهات
    """
    return _alert_cache.get(force_refresh=force_refresh)

def refresh_alerts():
    """تحديث إجباري للتنبيهات (للاستخدام اليدوي)"""
    return _alert_cache.refresh()

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

def get_alerts_stats():
    """إحصائيات متقدمة عن التنبيهات"""
    alerts = get_today_alerts()
    
    stats = {
        "total": len(alerts),
        "by_city": {},
        "by_confidence": {
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }
    }
    
    for alert in alerts:
        city = alert.get("city", "أخرى")
        confidence = alert.get("confidence", "MEDIUM")
        
        stats["by_city"][city] = stats["by_city"].get(city, 0) + 1
        stats["by_confidence"][confidence] = stats["by_confidence"].get(confidence, 0) + 1
    
    return stats

# ==============================
# 7️⃣ أدوات التنسيق والعرض (مستقلة عن Streamlit)
# ==============================

def format_alert_for_display(alert):
    """
    تنسيق التنبيه ليظهر بشكل جميل في الواجهة
    (هذه دالة مستقلة، يمكن استخدامها مع أي واجهة)
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
    
    # أيقونة حسب نوع التنبيه ومستوى الثقة
    icon = "💰"
    if alert.get("type") == "MARKET_SHIFT":
        icon = "📊"
    elif alert.get("type") == "RISK_WARNING":
        icon = "⚠️"
    
    # إضافة رمز حسب مستوى الثقة
    confidence = alert.get("confidence", "MEDIUM")
    if confidence == "HIGH":
        confidence_icon = "🔴"
    elif confidence == "MEDIUM":
        confidence_icon = "🟡"
    else:
        confidence_icon = "🟢"
    
    return {
        "icon": icon,
        "confidence_icon": confidence_icon,
        "title": alert.get("title", "تنبيه جديد"),
        "description": alert.get("description", ""),
        "details": {
            "city": alert.get("city", "غير محدد"),
            "district": alert.get("district", "غير محدد"),
            "discount": discount,
            "price": price_str,
            "window": signal.get("window_hours", 48),
            "property_type": signal.get("property_type", "غير محدد"),
            "expected_return": signal.get("expected_return", "غير متاح")
        },
        "details_text": f"""
**المدينة:** {alert.get('city', 'غير محدد')} | **الحي:** {alert.get('district', 'غير محدد')}
**الخصم:** {discount:.1f}% | **السعر:** {price_str} ريال
**نافذة الفرصة:** {signal.get('window_hours', 48)} ساعة
        """,
        "confidence": confidence,
        "time": alert.get("generated_at", "وقت غير محدد")
    }

def print_alerts_summary():
    """طباعة ملخص التنبيهات (للتجربة في الطرفية)"""
    alerts = get_today_alerts()
    stats = get_alerts_stats()
    
    print(f"\n{'='*60}")
    print(f"📋 ملخص التنبيهات - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print(f"📊 إجمالي التنبيهات: {stats['total']}")
    
    # توزيع حسب مستوى الثقة
    print(f"\n🔴 توزيع التنبيهات حسب القوة:")
    for conf, count in stats["by_confidence"].items():
        icon = "🔴" if conf == "HIGH" else "🟡" if conf == "MEDIUM" else "🟢"
        print(f"  {icon} {conf}: {count}")
    
    # توزيع حسب المدينة
    print(f"\n📍 التوزيع حسب المدينة:")
    for city, count in stats["by_city"].items():
        print(f"  • {city}: {count} تنبيه")
    
    # عرض أول 5 تنبيهات
    if alerts:
        print(f"\n📌 أبرز التنبيهات:")
        for i, alert in enumerate(alerts[:5]):
            signal = alert.get("signal", {})
            discount = signal.get("discount_percent", 0)
            confidence = alert.get("confidence", "MEDIUM")
            icon = "🔴" if confidence == "HIGH" else "🟡" if confidence == "MEDIUM" else "🟢"
            print(f"  {i+1}. {icon} {alert['city']} - {alert.get('district', 'غير محدد')}: خصم {discount:.1f}% ({confidence})")

# ==============================
# 8️⃣ بيانات تجريبية للاختبار (اختياري)
# ==============================

def generate_test_alerts():
    """توليد تنبيهات تجريبية لاختبار المنصة"""
    test_alerts = []
    
    # تنبيهات تجريبية لجميع المدن
    for city in CITIES:
        for i, prop_type in enumerate(PROPERTY_TYPES):
            discount = 5 + i * 5  # 5%, 10%, 15%
            
            # تحديد مستوى الثقة حسب الخصم
            if discount >= 15:
                confidence = "HIGH"
            elif discount >= 8:
                confidence = "MEDIUM"
            else:
                confidence = "LOW"
            
            test_alerts.append({
                "type": "GOLDEN_OPPORTUNITY",
                "city": city,
                "district": f"حي تجريبي {i+1}",
                "title": f"💰 فرصة {'قوية' if discount >= 15 else 'متوسطة' if discount >= 8 else 'خفيفة'} في {city}",
                "description": f"عقار {prop_type} في {city} بخصم {discount}% عن متوسط السوق",
                "signal": {
                    "discount_percent": discount,
                    "current_price": 850000 + i * 50000,
                    "avg_area_price": 1000000,
                    "expected_return": f"{7 + i}%",
                    "window_hours": 48,
                    "property_type": prop_type
                },
                "confidence": confidence,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "source": "TEST_DATA"
            })
    
    return test_alerts

# ==============================
# 9️⃣ اختبار سريع (يشتغل فقط إذا شغلت الملف مباشرة)
# ==============================

if __name__ == "__main__":
    print("\n🧪 تشغيل اختبار نظام التنبيهات...")
    
    # تنظيف التنبيهات القديمة
    clear_old_alerts(days=30)
    
    # اختبار توليد التنبيهات الحقيقية
    print("\n🔍 جاري البحث عن تنبيهات حقيقية...")
    alerts = generate_all_alerts()
    print(f"✅ التنبيهات الحقيقية: {len(alerts)}")
    
    # عرض ملخص
    print_alerts_summary()
    
    # عرض مسار ملف التخزين
    print(f"\n💾 ملف التخزين: {ALERTS_FILE}")
    stored = load_alerts()
    print(f"✅ إجمالي التنبيهات المخزنة: {len(stored)}")
    
    # إحصائيات متقدمة
    stats = get_alerts_stats()
    print(f"\n📈 إحصائيات متقدمة:")
    print(f"  • إجمالي اليوم: {stats['total']}")
    print(f"  • توزيع المدن: {stats['by_city']}")
    
    print("\n✅ انتهى الاختبار")
