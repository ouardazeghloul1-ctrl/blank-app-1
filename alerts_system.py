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
# استيرادات ذاكرة السوق للمقارنة الزمنية
# ==============================
from market_memory import load_last_snapshots

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

# إضافة نوع تنبيه اختفاء المعروض
ALERT_TYPES.update({
    "SUPPLY_ABSORPTION": "🔥 اختفاء المعروض - السوق يشتري بصمت"
})

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

    # 🔥 منع التكرار: نفس المدينة + نفس الحي + نفس الخصم (لتنبيهات الخصم)
    # ولتنبيهات اختفاء المعروض: نفس المدينة + نفس نوع العقار + نفس النسبة + خلال 48 ساعة
    for existing in alerts:
        if alert.get("type") == "GOLDEN_OPPORTUNITY":
            if (
                existing.get("city") == alert.get("city")
                and existing.get("district") == alert.get("district")
                and existing.get("signal", {}).get("discount_percent")
                   == alert.get("signal", {}).get("discount_percent")
            ):
                print(f"⚠️ تنبيه خصم مكرر تجاهل: {alert.get('city')} - {alert.get('district')}")
                return
        elif alert.get("type") == "SUPPLY_ABSORPTION":
            if (
                existing.get("type") == "SUPPLY_ABSORPTION"
                and existing.get("city") == alert.get("city")
                and existing.get("property_type") == alert.get("property_type")
            ):
                # مقارنة النسبة مع تسامح 1%
                existing_pct = existing.get("signal", {}).get("supply_drop_percent", 0)
                new_pct = alert.get("signal", {}).get("supply_drop_percent", 0)
                
                # مقارنة الزمن (48 ساعة)
                existing_time = datetime.strptime(
                    existing.get("generated_at"), "%Y-%m-%d %H:%M"
                )
                new_time = datetime.strptime(
                    alert.get("generated_at"), "%Y-%m-%d %H:%M"
                )

                if (abs(existing_pct - new_pct) < 1 and 
                    abs((new_time - existing_time).total_seconds()) < 48 * 3600):
                    print(f"⚠️ تنبيه اختفاء معروض مكرر تجاهل: {alert.get('city')} - {alert.get('property_type')}")
                    return

    alert["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alerts.append(alert)

    ensure_alerts_directory()
    ALERTS_FILE.write_text(
        json.dumps(alerts, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"✅ تم حفظ تنبيه جديد: {alert.get('city')} - {alert.get('type')}")

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
        يعتمد على مقارنة زمنية بين آخر لقطتين من ذاكرة السوق
        """
        try:
            # 🔹 تحميل آخر لقطتين من ذاكرة السوق للمقارنة الزمنية
            snapshots = load_last_snapshots(city, property_type, limit=2)

            # 🔒 إذا لم تتوفر لقطتان، لا نولد تنبيهات (لا توجد ذاكرة كافية)
            if len(snapshots) < 2:
                print(f"ℹ️ {city} | {property_type}: لا توجد بيانات زمنية كافية بعد")
                return []

            previous_df, current_df = snapshots[1], snapshots[0]
            real_data = current_df

            # ==============================
            # 🔥 تنبيه اختفاء المعروض (Supply Absorption)
            # ==============================
            
            prev_count = len(previous_df)
            curr_count = len(current_df)

            # تحليل الأحياء المختفية
            prev_districts = set(previous_df.get("الحي", [])) if "الحي" in previous_df.columns else set()
            curr_districts = set(current_df.get("الحي", [])) if "الحي" in current_df.columns else set()

            districts_lost = prev_districts - curr_districts
            district_loss_ratio = (
                len(districts_lost) / len(prev_districts) * 100
                if prev_districts else 0
            )

            # نسبة التغير في المعروض
            if prev_count > 0:
                supply_change_pct = ((prev_count - curr_count) / prev_count) * 100
            else:
                supply_change_pct = 0

            # شروط إطلاق التنبيه
            alerts = []

            # ⛔ لا تنبيه إذا لم ينخفض المعروض بشكل حقيقي (عدد + أحياء)
            if supply_change_pct >= 10 and district_loss_ratio >= 15:
                # تصنيف القوة الأساسي
                if supply_change_pct >= 30:
                    confidence = "HIGH"
                elif supply_change_pct >= 20:
                    confidence = "MEDIUM"
                else:
                    confidence = "LOW"
                
                # ⭐ ترقية الثقة إذا اختفت 3 أحياء أو أكثر
                if len(districts_lost) >= 3:
                    if confidence == "MEDIUM":
                        confidence = "HIGH"
                    elif confidence == "LOW":
                        confidence = "MEDIUM"
                
                # عرض الأحياء المختفية (أول 3 فقط)
                districts_display = ", ".join(list(districts_lost)[:3]) or "عدة أحياء"

                alert = {
                    "type": "SUPPLY_ABSORPTION",
                    "city": city,
                    "district": districts_display,
                    "title": f"🔥 اختفاء معروض في {city}",
                    "description": (
                        f"انخفض عدد عقارات {property_type} المعروضة بنسبة "
                        f"{supply_change_pct:.1f}% خلال الفترة الأخيرة، "
                        f"ما يدل على امتصاص قوي من السوق."
                    ),
                    "signal": {
                        "supply_drop_percent": round(supply_change_pct, 1),
                        "previous_count": prev_count,
                        "current_count": curr_count,
                        "districts_lost": list(districts_lost)[:5],
                        "district_loss_ratio": round(district_loss_ratio, 1),
                        "window_hours": 72,
                        "property_type": property_type
                    },
                    "confidence": confidence,
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "source": "MarketMemory",
                    "property_type": property_type
                }

                alerts.append(alert)
                save_alert(alert)

                print(
                    f"🔥 {city} | {property_type}: اختفاء معروض "
                    f"{supply_change_pct:.1f}% من {len(districts_lost)} أحياء ({confidence})"
                )

            # ==============================
            # تنبيهات الخصم السعري (المنطق القديم)
            # ==============================

            # 🔇 منع التنبيهات إذا لم يحدث تغير كمي في السوق
            if len(current_df) == len(previous_df):
                print(f"⏸️ {city} | {property_type}: لا تغير كمي واضح في السوق")

            if real_data.empty:
                print(f"⚠️ {city}: لا توجد بيانات")
                return alerts

            # البحث عن العقارات المخفضة
            undervalued = self.opportunity_finder.find_undervalued_properties(
                real_data, city
            )

            if not undervalued:
                print(f"⚠️ {city}: لا توجد عقارات مخفضة")
                return alerts

            # تحويل كل فرصة إلى تنبيه (بدون استثناء)
            for prop in undervalued:
                # تحويل الخصم من نص إلى رقم مع أمان
                discount_raw = prop.get("الخصم", "0").replace("%", "")
                try:
                    discount = float(discount_raw)
                except:
                    discount = 0

                # 🔥 تجاهل التنبيه إذا لم يصل للحد الأدنى للخصم
                if discount < MIN_DISCOUNT_PERCENT:
                    continue

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
        },
        "by_type": {}
    }
    
    for alert in alerts:
        city = alert.get("city", "أخرى")
        confidence = alert.get("confidence", "MEDIUM")
        alert_type = alert.get("type", "OTHER")
        
        stats["by_city"][city] = stats["by_city"].get(city, 0) + 1
        stats["by_confidence"][confidence] = stats["by_confidence"].get(confidence, 0) + 1
        stats["by_type"][alert_type] = stats["by_type"].get(alert_type, 0) + 1
    
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
    alert_type = alert.get("type", "GOLDEN_OPPORTUNITY")
    
    # تنسيق حسب نوع التنبيه
    if alert_type == "SUPPLY_ABSORPTION":
        drop_pct = signal.get("supply_drop_percent", 0)
        prev_count = signal.get("previous_count", 0)
        curr_count = signal.get("current_count", 0)
        districts_lost = signal.get("districts_lost", [])
        district_loss_ratio = signal.get("district_loss_ratio", 0)
        
        icon = "🔥"
        title = alert.get("title", f"🔥 اختفاء معروض في {alert.get('city')}")
        description = alert.get("description", "")
        
        districts_text = ", ".join(districts_lost[:3]) if districts_lost else "عدة أحياء"
        
        details_text = f"""
**المدينة:** {alert.get('city', 'غير محدد')}
**نوع العقار:** {signal.get('property_type', 'غير محدد')}
**انخفاض المعروض:** {drop_pct:.1f}%
**الأحياء المختفية:** {districts_text}
**نسبة اختفاء الأحياء:** {district_loss_ratio:.1f}%
**العدد السابق:** {prev_count} | **الحالي:** {curr_count}
**نافذة الفرصة:** {signal.get('window_hours', 72)} ساعة

🔥 هذا ليس تصحيح سعر، بل **شراء صامت**.
القرار: المراقبة الدقيقة – الفرص التالية أقل عددًا وأقوى أثرًا.
        """
        
        details = {
            "city": alert.get("city", "غير محدد"),
            "property_type": signal.get("property_type", "غير محدد"),
            "supply_drop": drop_pct,
            "districts_lost": districts_text,
            "district_loss_ratio": district_loss_ratio,
            "previous_count": prev_count,
            "current_count": curr_count,
            "window": signal.get("window_hours", 72)
        }
        
    else:  # GOLDEN_OPPORTUNITY
        discount = signal.get("discount_percent", 0)
        current_price = signal.get('current_price', 0)
        if current_price:
            try:
                price_str = f"{int(current_price):,}"
            except:
                price_str = str(current_price)
        else:
            price_str = "غير متاح"
        
        icon = "💰"
        title = alert.get("title", f"💰 فرصة في {alert.get('city')}")
        description = alert.get("description", "")
        
        details_text = f"""
**المدينة:** {alert.get('city', 'غير محدد')} | **الحي:** {alert.get('district', 'غير محدد')}
**الخصم:** {discount:.1f}% | **السعر:** {price_str} ريال
**نافذة الفرصة:** {signal.get('window_hours', 48)} ساعة
        """
        
        details = {
            "city": alert.get("city", "غير محدد"),
            "district": alert.get("district", "غير محدد"),
            "discount": discount,
            "price": price_str,
            "window": signal.get("window_hours", 48),
            "property_type": signal.get("property_type", "غير محدد"),
            "expected_return": signal.get("expected_return", "غير متاح")
        }
    
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
        "title": title,
        "description": description,
        "details": details,
        "details_text": details_text,
        "confidence": confidence,
        "time": alert.get("generated_at", "وقت غير محدد"),
        "type": alert_type
    }

def print_alerts_summary():
    """طباعة ملخص التنبيهات (للتجربة في الطرفية)"""
    alerts = get_today_alerts()
    stats = get_alerts_stats()
    
    print(f"\n{'='*60}")
    print(f"📋 ملخص التنبيهات - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print(f"📊 إجمالي التنبيهات: {stats['total']}")
    
    # توزيع حسب النوع
    print(f"\n📌 توزيع التنبيهات حسب النوع:")
    for alert_type, count in stats["by_type"].items():
        icon = "🔥" if alert_type == "SUPPLY_ABSORPTION" else "💰"
        print(f"  {icon} {alert_type}: {count}")
    
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
            alert_type = alert.get("type", "GOLDEN_OPPORTUNITY")
            icon = "🔥" if alert_type == "SUPPLY_ABSORPTION" else "💰"
            confidence = alert.get("confidence", "MEDIUM")
            conf_icon = "🔴" if confidence == "HIGH" else "🟡" if confidence == "MEDIUM" else "🟢"
            
            if alert_type == "SUPPLY_ABSORPTION":
                drop = alert.get("signal", {}).get("supply_drop_percent", 0)
                districts = alert.get("signal", {}).get("districts_lost", [])
                districts_text = ", ".join(districts[:2]) if districts else "عدة أحياء"
                print(f"  {i+1}. {icon} {conf_icon} {alert['city']} - {districts_text}: اختفاء {drop:.1f}% ({confidence})")
            else:
                discount = alert.get("signal", {}).get("discount_percent", 0)
                print(f"  {i+1}. {icon} {conf_icon} {alert['city']} - {alert.get('district', 'غير محدد')}: خصم {discount:.1f}% ({confidence})")

# ==============================
# 8️⃣ بيانات تجريبية للاختبار (اختياري)
# ==============================

def generate_test_alerts():
    """توليد تنبيهات تجريبية لاختبار المنصة"""
    test_alerts = []
    
    # تنبيهات تجريبية لجميع المدن
    for city in CITIES:
        for i, prop_type in enumerate(PROPERTY_TYPES):
            # تنبيه خصم سعري
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
                "source": "TEST_DATA",
                "property_type": prop_type
            })
            
            # تنبيه اختفاء معروض تجريبي
            drop_pct = 10 + i * 10  # 10%, 20%, 30%
            if drop_pct >= 30:
                confidence = "HIGH"
            elif drop_pct >= 20:
                confidence = "MEDIUM"
            else:
                confidence = "LOW"
            
            # ترقية الثقة في حالة اختفاء 3 أحياء
            districts_lost = [f"حي تجريبي {j+1}" for j in range(i+2)]
            if len(districts_lost) >= 3:
                if confidence == "MEDIUM":
                    confidence = "HIGH"
                elif confidence == "LOW":
                    confidence = "MEDIUM"
                
            test_alerts.append({
                "type": "SUPPLY_ABSORPTION",
                "city": city,
                "district": ", ".join(districts_lost[:3]),
                "title": f"🔥 اختفاء معروض في {city}",
                "description": f"انخفض عدد عقارات {prop_type} المعروضة بنسبة {drop_pct}% من {len(districts_lost)} أحياء",
                "signal": {
                    "supply_drop_percent": drop_pct,
                    "previous_count": 100 + i * 20,
                    "current_count": 80 + i * 10,
                    "districts_lost": districts_lost,
                    "district_loss_ratio": (len(districts_lost) / 5) * 100,
                    "window_hours": 72,
                    "property_type": prop_type
                },
                "confidence": confidence,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "source": "TEST_DATA",
                "property_type": prop_type
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
    print(f"  • توزيع الأنواع: {stats['by_type']}")
    
    print("\n✅ انتهى الاختبار")
