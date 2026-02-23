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
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

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

# مسار ملف التخزين الدائم
ALERTS_FILE = Path("alerts/alerts_db.json")

# أنواع التنبيهات
ALERT_TYPES = {
    "GOLDEN_OPPORTUNITY": "💰 فرصة ذهبية - خصم قوي عن السوق",
    "MARKET_SHIFT": "📊 تحول سعري غير طبيعي",
    "RISK_WARNING": "⚠️ خطر خفي يظهر",
    "SUPPLY_ABSORPTION": "🔥 اختفاء المعروض - السوق يشتري بصمت",
    "LIQUIDITY_INFLOW": "💧 دخول سيولة ذكية - السوق يتحرك قبل السعر",
    "BUYER_BEHAVIOR_SHIFT": "🧠 تغير سلوك الشراء - من يشتري ماذا وأين"
}

# ==============================
# دالة موحدة لحساب مستوى الثقة
# ==============================

def compute_confidence(score, rules=None):
    """
    توحيد مستوى الثقة لجميع التنبيهات
    score: رقم صحيح (0 → n)
    rules: dict اختياري لتخصيص العتبات
    """
    rules = rules or {"HIGH": 3, "MEDIUM": 2}

    if score >= rules["HIGH"]:
        return "HIGH"
    elif score >= rules["MEDIUM"]:
        return "MEDIUM"
    else:
        return "LOW"

# ==============================
# دالة إنشاء بصمة فريدة للتنبيه (لمنع التكرار)
# ==============================

def alert_fingerprint(alert):
    """إنشاء بصمة فريدة للتنبيه بناءً على النوع والمدينة والحي ووقت الحدث"""
    key = f"{alert.get('type')}-{alert.get('city')}-{alert.get('district', '')}-{alert.get('property_type', '')}"
    # استخدام تاريخ التنبيه نفسه، وليس وقت التنفيذ
    date_str = alert.get("generated_at", datetime.now().strftime("%Y-%m-%d"))[:10]
    return hashlib.md5(f"{key}-{date_str}".encode()).hexdigest()

# ==============================
# دالة بناء رسالة بشرية (بدون HTML أو كود)
# ==============================

def build_human_message(alert):
    """تحويل التنبيه إلى رسالة مفهومة للبشر (بدون HTML أو أكواد)"""
    t = alert.get("type")
    city = alert.get("city")
    conf = alert.get("confidence")
    signal = alert.get("signal", {})
    window = signal.get("window_hours", 24)
    priority = alert.get("priority", "MID")

    priority_text = {
        "GOLD": "🔴 ذهبية",
        "MID": "🟡 متوسطة",
        "LOW": "🟢 خفيفة"
    }.get(priority, "")

    if t == "BUYER_BEHAVIOR_SHIFT":
        signals = signal.get("signals", [])
        main = signals[0] if signals else "تغير غير معتاد في سلوك المشترين"
        return f"📍 {city}: خلال آخر {window} ساعة لوحظ {main}. (قوة الإشارة: {conf} | {priority_text})"

    if t == "SUPPLY_ABSORPTION":
        drop = signal.get("supply_drop_percent", 0)
        districts = signal.get("districts_lost", [])
        districts_text = f" في {', '.join(districts[:2])}" if districts else ""
        return f"📍 {city}{districts_text}: خلال آخر {window} ساعة انخفض المعروض بنسبة {drop:.1f}%. السوق يشتري بصمت. ({priority_text})"

    if t == "LIQUIDITY_INFLOW":
        liq = signal.get("liquidity_change_percent", 0)
        active = signal.get("active_districts", [])
        active_text = f" في {', '.join(active[:2])}" if active else ""
        return f"📍 {city}{active_text}: خلال آخر {window} ساعة دخلت سيولة ذكية (+{liq:.1f}%) بدون ارتفاع في السعر. ({priority_text})"

    if t == "GOLDEN_OPPORTUNITY":
        d = signal.get("discount_percent", 0)
        dist = alert.get("district", "")
        prop_type = signal.get("property_type", "عقار")
        exclusive = "📢 خبر حصري – " if alert.get("is_exclusive") else ""
        return f"{exclusive}💰 فرصة {priority_text} في {city} ({dist}): {prop_type} بخصم {d:.1f}% عن السوق. (نافذة الفرصة: {window} ساعة)"

    return f"📍 {city}: حركة سوق غير اعتيادية خلال آخر {window} ساعة."

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
    ✅ لا يتم حفظ نفس التنبيه أكثر من مرة باستخدام fingerprint
    """
    alerts = load_alerts()

    # إضافة بصمة فريدة للتنبيه (تعتمد على generated_at)
    alert["fingerprint"] = alert_fingerprint(alert)
    
    # 🔥 منع التكرار: نفس البصمة خلال نفس اليوم
    for existing in alerts:
        if existing.get("fingerprint") == alert["fingerprint"]:
            print(f"⚠️ تنبيه مكرر تجاهل: {alert.get('type')} - {alert.get('city')} - {alert.get('district', '')}")
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

def get_alerts_history(days=7, city=None, alert_type=None):
    """
    جلب التنبيهات من الأيام السابقة (للتاريخ والتحليل)
    days: عدد الأيام الماضية (افتراضي: 7 أيام)
    city: فلترة حسب المدينة (اختياري)
    alert_type: فلترة حسب نوع التنبيه (اختياري)
    """
    cutoff = datetime.now() - timedelta(days=days)
    
    all_alerts = load_alerts()
    history_alerts = []
    
    for alert in all_alerts:
        try:
            # تحويل النص إلى كائن datetime للمقارنة الدقيقة
            alert_time = datetime.strptime(alert.get("generated_at", "2000-01-01 00:00"), "%Y-%m-%d %H:%M")
            if alert_time >= cutoff:
                history_alerts.append(alert)
        except:
            # إذا فشل التحويل، نتجاهل هذا التنبيه
            continue
    
    # تصفية حسب المدينة إذا طلبت
    if city:
        history_alerts = [a for a in history_alerts if a.get("city") == city]
    
    # تصفية حسب نوع التنبيه إذا طلب
    if alert_type:
        history_alerts = [a for a in history_alerts if a.get("type") == alert_type]
    
    return history_alerts

def get_latest_alert_by_city(city, alert_type=None):
    """
    جلب آخر تنبيه لمدينة محددة
    city: اسم المدينة
    alert_type: نوع التنبيه المطلوب (اختياري)
    """
    all_alerts = load_alerts()
    
    # تصفية حسب المدينة
    city_alerts = [a for a in all_alerts if a.get("city") == city]
    
    # تصفية حسب النوع إذا طلب
    if alert_type:
        city_alerts = [a for a in city_alerts if a.get("type") == alert_type]
    
    if not city_alerts:
        return None
    
    # ترتيب تنازلي حسب الوقت وأخذ الأحدث
    city_alerts.sort(key=lambda x: x.get("generated_at", ""), reverse=True)
    return city_alerts[0]

def get_latest_alerts_summary():
    """
    الحصول على ملخص آخر التنبيهات لكل مدينة
    يعرض أحدث تنبيه من كل نوع لكل مدينة
    """
    summary = {}
    
    for city in CITIES:
        city_summary = {}
        for alert_type in ALERT_TYPES.keys():
            latest = get_latest_alert_by_city(city, alert_type)
            if latest:
                city_summary[alert_type] = {
                    "message": build_human_message(latest),
                    "time": latest.get("generated_at"),
                    "confidence": latest.get("confidence"),
                    "priority": latest.get("priority"),
                    "is_exclusive": latest.get("is_exclusive", True)
                }
        if city_summary:
            summary[city] = city_summary
    
    return summary

def clear_old_alerts(days=365):
    """حذف التنبيهات الأقدم من عدد محدد من الأيام (افتراضي: سنة كاملة)"""
    alerts = load_alerts()
    cutoff = datetime.now() - timedelta(days=days)
    
    new_alerts = []
    for alert in alerts:
        try:
            alert_time = datetime.strptime(alert.get("generated_at", "2000-01-01 00:00"), "%Y-%m-%d %H:%M")
            if alert_time >= cutoff:
                new_alerts.append(alert)
        except:
            # إذا فشل التحويل، نحتفظ بالتنبيه
            new_alerts.append(alert)
    
    if len(new_alerts) != len(alerts):
        ALERTS_FILE.write_text(
            json.dumps(new_alerts, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"🧹 تم حذف {len(alerts) - len(new_alerts)} تنبيه قديم (أقدم من {days} يوم)")
    
    return new_alerts

# ==============================
# 3️⃣ محرك التنبيهات (Alert Engine)
# ==============================

from smart_opportunities import SmartOpportunityFinder

class AlertEngine:
    """محرك استخراج الفرص الذهبية من البيانات الحقيقية"""
    
    def __init__(self):
        self.opportunity_finder = SmartOpportunityFinder()
    
    # 🛑 حارس زمني: يمنع التنبيهات إذا الفرق بين اللقطتين أقل من 3 ساعات
    def is_valid_time_gap(self, prev_df, curr_df, min_minutes=180):
        """
        التحقق من أن الفرق الزمني بين اللقطتين كافٍ لإصدار تنبيه
        min_minutes: الحد الأدنى بالدقائق (افتراضي: 180 دقيقة = 3 ساعات)
        """
        try:
            # محاولة قراءة وقت اللقطة من العمود المخصص
            if "__snapshot_time__" in prev_df.columns and "__snapshot_time__" in curr_df.columns:
                t1 = pd.to_datetime(prev_df["__snapshot_time__"].iloc[0])
                t2 = pd.to_datetime(curr_df["__snapshot_time__"].iloc[0])
                diff_minutes = (t2 - t1).total_seconds() / 60
                return diff_minutes >= min_minutes
        except:
            pass
        
        # إذا لم نتمكن من قراءة الوقت، نسمح بالتحليل (للأمان)
        return True

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
            
            # 🛑 حارس زمني: لا نحلل فروقات تافهة (أقل من 3 ساعات)
            if not self.is_valid_time_gap(previous_df, current_df):
                print(f"⏱️ {city} | {property_type}: فرق زمني ضعيف – تجاهل التنبيهات")
                return []
            
            real_data = current_df

            # ==============================
            # متغيرات مشتركة (مرة واحدة فقط)
            # ==============================
            prev_count = len(previous_df)
            curr_count = len(current_df)

            # تحليل الأحياء (للتنبيهات التي تحتاجه)
            prev_districts = set(previous_df.get("الحي", [])) if "الحي" in previous_df.columns else set()
            curr_districts = set(current_df.get("الحي", [])) if "الحي" in current_df.columns else set()

            alerts = []

            # ==============================
            # 🔥 تنبيه اختفاء المعروض (Supply Absorption)
            # ==============================

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
            if supply_change_pct >= 10 and district_loss_ratio >= 15:
                # حساب score رقمي بدلاً من تصنيف مباشر
                confidence_score = 0

                # قوة انخفاض المعروض
                if supply_change_pct >= 30:
                    confidence_score += 3
                elif supply_change_pct >= 20:
                    confidence_score += 2
                elif supply_change_pct >= 10:
                    confidence_score += 1

                # دعم إضافي إذا اختفت أحياء كثيرة
                if len(districts_lost) >= 3:
                    confidence_score += 1

                # حساب مستوى الثقة عبر الدالة الموحدة
                confidence = compute_confidence(confidence_score)
                
                # تصنيف تجاري
                priority = "GOLD" if confidence == "HIGH" else "MID" if confidence == "MEDIUM" else "LOW"
                
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
                        "window_hours": 24,
                        "property_type": property_type
                    },
                    "confidence": confidence,
                    "priority": priority,
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "source": "MarketMemory",
                    "property_type": property_type,
                    "is_exclusive": True
                }

                alerts.append(alert)
                save_alert(alert)

                print(
                    f"🔥 {city} | {property_type}: اختفاء معروض "
                    f"{supply_change_pct:.1f}% من {len(districts_lost)} أحياء ({confidence}) [{priority}]"
                )

            # ==============================
            # 💧 تنبيه دخول السيولة (Liquidity Inflow)
            # ==============================

            # حساب تغير الحجم
            if prev_count > 0:
                liquidity_change_pct = ((curr_count - prev_count) / prev_count) * 100
            else:
                liquidity_change_pct = 0

            # حساب تغير السعر (مع التحقق من وجود العمود)
            if ("سعر_المتر" in previous_df.columns and "سعر_المتر" in current_df.columns 
                and len(previous_df["سعر_المتر"].dropna()) > 0 and len(current_df["سعر_المتر"].dropna()) > 0):
                prev_price = previous_df["سعر_المتر"].mean()
                curr_price = current_df["سعر_المتر"].mean()
                price_change_pct = ((curr_price - prev_price) / prev_price) * 100 if prev_price else 0
            else:
                price_change_pct = 0
                print(f"ℹ️ {city} | {property_type}: لا توجد بيانات سعر كافية، التنبيه سيعتمد على الحجم فقط")

            # تحليل الأحياء المتداولة
            active_districts = curr_districts - prev_districts

            # شروط إطلاق التنبيه
            if liquidity_change_pct >= 15 and -2 <= price_change_pct <= 1:
                # حساب score رقمي بدلاً من تصنيف مباشر
                confidence_score = 0

                # قوة زيادة السيولة
                if liquidity_change_pct >= 30:
                    confidence_score += 3
                elif liquidity_change_pct >= 20:
                    confidence_score += 2
                elif liquidity_change_pct >= 15:
                    confidence_score += 1

                # دعم إضافي إذا ظهرت أحياء جديدة
                if len(active_districts) >= 2:
                    confidence_score += 1

                # حساب مستوى الثقة عبر الدالة الموحدة
                confidence = compute_confidence(confidence_score)
                
                # تصنيف تجاري
                priority = "GOLD" if confidence == "HIGH" else "MID" if confidence == "MEDIUM" else "LOW"

                alert = {
                    "type": "LIQUIDITY_INFLOW",
                    "city": city,
                    "district": ", ".join(list(active_districts)[:3]) or "عدة أحياء",
                    "title": f"💧 دخول سيولة ذكية في {city}",
                    "description": (
                        f"ارتفع حجم التداول لعقارات {property_type} بنسبة "
                        f"{liquidity_change_pct:.1f}% بينما بقي السعر شبه ثابت "
                        f"({price_change_pct:.1f}%)."
                    ),
                    "signal": {
                        "liquidity_change_percent": round(liquidity_change_pct, 1),
                        "price_change_percent": round(price_change_pct, 2),
                        "active_districts": list(active_districts)[:5],
                        "previous_count": prev_count,
                        "current_count": curr_count,
                        "window_hours": 24,
                        "property_type": property_type
                    },
                    "confidence": confidence,
                    "priority": priority,
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "source": "MarketMemory",
                    "property_type": property_type,
                    "is_exclusive": True
                }

                alerts.append(alert)
                save_alert(alert)

                print(
                    f"💧 {city} | {property_type}: دخول سيولة "
                    f"{liquidity_change_pct:.1f}% ({confidence}) [{priority}]"
                )

            # ==============================
            # 🧠 تنبيه تغير سلوك الشراء (Buyer Behavior Shift)
            # ==============================

            behavior_signals = []
            confidence_score = 0

            # ---- 1. تغير نوع العقار المهيمن ----
            def dominant_type(df):
                return df["نوع_العقار"].value_counts(normalize=True).to_dict() if "نوع_العقار" in df.columns else {}

            prev_types = dominant_type(previous_df)
            curr_types = dominant_type(current_df)

            for t, pct in curr_types.items():
                prev_pct = prev_types.get(t, 0)
                if pct - prev_pct >= 0.20:
                    behavior_signals.append(f"تحول قوي نحو {t}")
                    confidence_score += 1

            # ---- 2. انتقال الشراء بين الشرائح السعرية ----
            if "سعر_المتر" in previous_df.columns and "سعر_المتر" in current_df.columns:
                prev_prices = previous_df["سعر_المتر"].dropna()
                curr_prices = current_df["سعر_المتر"].dropna()

                if len(prev_prices) > 10 and len(curr_prices) > 10:
                    p_low, p_high = prev_prices.quantile([0.33, 0.66])
                    prev_segment = pd.cut(prev_prices, [-1, p_low, p_high, 1e9], labels=["منخفض", "متوسط", "مرتفع"])
                    curr_segment = pd.cut(curr_prices, [-1, p_low, p_high, 1e9], labels=["منخفض", "متوسط", "مرتفع"])

                    prev_dist = prev_segment.value_counts(normalize=True)
                    curr_dist = curr_segment.value_counts(normalize=True)

                    for seg in curr_dist.index:
                        if curr_dist[seg] - prev_dist.get(seg, 0) >= 0.15:
                            behavior_signals.append(f"انتقال الشراء نحو الشريحة {seg}")
                            confidence_score += 1

            # ---- 3. تركّز الشراء في أحياء محددة ----
            dominant_districts = []
            if "الحي" in current_df.columns:
                district_dist = current_df["الحي"].value_counts(normalize=True)
                dominant_districts = district_dist[district_dist >= 0.15].index.tolist()

                if len(dominant_districts) >= 3:
                    behavior_signals.append("تركيز الشراء في أحياء محددة")
                    confidence_score += 1

            # ---- 4. سلوك الصفقة (حجم الصفقة) ----
            # نراقب هل السوق يتجه لصفقات أصغر (أفراد) أو أكبر (مستثمرين)
            
            def avg_transaction_size(df):
                if "المساحة" in df.columns and df["المساحة"].dropna().any():
                    return df["المساحة"].mean()
                elif "السعر" in df.columns and df["السعر"].dropna().any():
                    return df["السعر"].mean()
                return None

            prev_tx_size = avg_transaction_size(previous_df)
            curr_tx_size = avg_transaction_size(current_df)

            if prev_tx_size and curr_tx_size:
                change_pct = ((curr_tx_size - prev_tx_size) / prev_tx_size) * 100

                # انتقال نحو صفقات أصغر (شراء أفراد / سرعة دوران)
                if change_pct <= -15:
                    behavior_signals.append("انتقال السوق نحو صفقات أصغر وأسرع")
                    confidence_score += 1

                # انتقال نحو صفقات أكبر (شراء استثماري ثقيل)
                elif change_pct >= 15:
                    behavior_signals.append("اتجاه السوق نحو صفقات أكبر واستثمار طويل")
                    confidence_score += 1

            # ---- إطلاق التنبيه باستخدام دالة الثقة الموحدة ----
            if confidence_score >= 1:
                confidence = compute_confidence(confidence_score)
                
                # تصنيف تجاري
                priority = "GOLD" if confidence == "HIGH" else "MID" if confidence == "MEDIUM" else "LOW"

                alert = {
                    "type": "BUYER_BEHAVIOR_SHIFT",
                    "city": city,
                    "district": ", ".join(dominant_districts[:3]) if dominant_districts else "عدة أحياء",
                    "title": f"🧠 تغير سلوك الشراء في {city}",
                    "description": " | ".join(behavior_signals),
                    "signal": {
                        "signals": behavior_signals,
                        "window_hours": 24,
                        "property_type": property_type
                    },
                    "confidence": confidence,
                    "priority": priority,
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "source": "MarketMemory",
                    "property_type": property_type,
                    "is_exclusive": True
                }

                alerts.append(alert)
                save_alert(alert)

                print(f"🧠 {city} | {property_type}: تغير سلوك الشراء ({confidence}) [{priority}]")

            # ==============================
            # 💰 تنبيهات الخصم السعري (GOLDEN_OPPORTUNITY) – موحّد بالـ score
            # ==============================

            # إشارات سياقية من نفس الجولة (تعزيز ذكي)
            context_bias = {
                "SUPPLY_ABSORPTION": any(a.get("type") == "SUPPLY_ABSORPTION" for a in alerts),
                "LIQUIDITY_INFLOW": any(a.get("type") == "LIQUIDITY_INFLOW" for a in alerts),
            }

            undervalued = self.opportunity_finder.find_undervalued_properties(
                real_data, city
            )

            if not undervalued:
                print(f"⚠️ {city}: لا توجد عقارات مخفضة")
                return alerts

            for prop in undervalued:
                # ---- قراءة الخصم بأمان ----
                discount_raw = prop.get("الخصم", "0").replace("%", "")
                try:
                    discount = float(discount_raw)
                except:
                    discount = 0.0

                # فلتر الظهور
                if discount < MIN_DISCOUNT_PERCENT:
                    continue

                # ---- حساب score ----
                confidence_score = 0

                # (1) الخصم – الأساس
                if discount >= 20:
                    confidence_score += 3
                elif discount >= 12:
                    confidence_score += 2
                elif discount >= 5:
                    confidence_score += 1

                # (2) تعزيز سياقي إذا السوق يدعم
                if context_bias["SUPPLY_ABSORPTION"]:
                    confidence_score += 1
                if context_bias["LIQUIDITY_INFLOW"]:
                    confidence_score += 1

                # حساب مستوى الثقة الموحد
                confidence = compute_confidence(confidence_score)
                
                # تصنيف تجاري
                priority = "GOLD" if confidence == "HIGH" else "MID" if confidence == "MEDIUM" else "LOW"

                # ---- أمان الحقول ----
                current_price = prop.get("السعر_الحالي") or prop.get("السعر") or 0
                avg_price = (
                    prop.get("متوسط_المنطقة")
                    or prop.get("متوسط_السعر")
                    or (current_price * 1.1 if current_price else 0)
                )
                district = prop.get("المنطقة") or prop.get("الحي") or "غير محدد"
                expected_return = prop.get("العائد_المتوقع", "غير متاح")

                alert = {
                    "type": "GOLDEN_OPPORTUNITY",
                    "city": city,
                    "district": district,
                    "title": f"💰 فرصة {('قوية' if confidence=='HIGH' else 'متوسطة' if confidence=='MEDIUM' else 'خفيفة')} في {city}",
                    "description": f"عقار {property_type} في {district} بخصم {discount:.1f}% عن متوسط المنطقة",
                    "signal": {
                        "discount_percent": round(discount, 1),
                        "current_price": current_price,
                        "avg_area_price": avg_price,
                        "expected_return": expected_return,
                        "window_hours": 24,
                        "property_type": property_type,
                        "context_bias": context_bias,
                        "score": confidence_score
                    },
                    "confidence": confidence,
                    "priority": priority,
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "source": "AlertEngine",
                    "property_type": property_type,
                    "is_exclusive": True
                }

                alerts.append(alert)
                save_alert(alert)

                print(f"💰 {city} | {property_type}: فرصة {confidence} بخصم {discount:.1f}% (score={confidence_score}) [{priority}]")

            return alerts
            
        except Exception as e:
            print(f"❌ خطأ في {city}: {str(e)}")
            return []

# ==============================
# دالة لحظية للتنبيهات (تستخدم مباشرة بعد حفظ snapshot)
# ==============================

def check_and_emit_alert(city, property_type):
    """
    دالة لحظية لتوليد التنبيهات مباشرة بعد حفظ snapshot جديد
    هذه هي الدالة الموصى باستخدامها للتنبيهات الفورية
    """
    engine = AlertEngine()
    alerts = engine.generate_city_alerts(city, property_type)
    
    # إذا كان هناك تنبيهات جديدة، يمكن إرسال إشعار فوري هنا
    if alerts:
        print(f"📢 تنبيه جديد الآن في {city}: {len(alerts)} تنبيه")
        for alert in alerts:
            print(f"  → {build_human_message(alert)}")
    
    return alerts

# ==============================
# 4️⃣ تجميع كل المدن (وظيفة إدارية للاستخدام الدفعي)
# ==============================

def generate_all_alerts():
    """
    ⚠️ وظيفة إدارية فقط - تجمع كل التنبيهات من جميع المدن دفعة واحدة
    تستخدم للصيانة أو التهيئة الأولية، وليس للاستخدام اليومي
    """
    print("⚠️ تحذير: generate_all_alerts هي وظيفة إدارية ثقيلة، يفضل استخدام check_and_emit_alert للتنبيهات اللحظية")
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
# 5️⃣ واجهة الاستخدام (API) - للاستخدام من الملفات الأخرى
# ==============================

def get_today_alerts(force_refresh=False):
    """
    ✅ المصدر الرئيسي للتنبيهات في الواجهة
    يقرأ من الملف مباشرة للحصول على آخر التنبيهات المحفوظة
    
    المعاملات:
        force_refresh: إذا كان True، يولد تنبيهات جديدة قبل العرض
    """
    if force_refresh:
        # تحديث إجباري: يولد تنبيهات جديدة ويحفظها
        print("🔄 تحديث إجباري للتنبيهات...")
        generate_all_alerts()
    
    # قراءة التنبيهات من الملف مباشرة
    return get_today_stored_alerts()

def refresh_alerts():
    """
    تحديث إجباري للتنبيهات (للاستخدام اليدوي)
    """
    print("🔄 تحديث يدوي للتنبيهات...")
    return generate_all_alerts()

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
        "by_priority": {
            "GOLD": 0,
            "MID": 0,
            "LOW": 0
        },
        "by_type": {}
    }
    
    for alert in alerts:
        city = alert.get("city", "أخرى")
        confidence = alert.get("confidence", "MEDIUM")
        priority = alert.get("priority", "MID")
        alert_type = alert.get("type", "OTHER")
        
        stats["by_city"][city] = stats["by_city"].get(city, 0) + 1
        stats["by_confidence"][confidence] = stats["by_confidence"].get(confidence, 0) + 1
        stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
        stats["by_type"][alert_type] = stats["by_type"].get(alert_type, 0) + 1
    
    return stats

# ==============================
# 6️⃣ أدوات التنسيق والعرض (مستقلة عن Streamlit)
# ==============================

def format_alert_for_display(alert):
    """
    تنسيق التنبيه ليظهر بشكل جميل في الواجهة
    (هذه دالة مستقلة، يمكن استخدامها مع أي واجهة)
    """
    signal = alert.get("signal", {})
    alert_type = alert.get("type", "GOLDEN_OPPORTUNITY")
    priority = alert.get("priority", "MID")
    
    # تنسيق حسب نوع التنبيه
    if alert_type == "SUPPLY_ABSORPTION":
        drop_pct = signal.get("supply_drop_percent", 0)
        
        icon = "🔥"
        title = alert.get("title", f"🔥 اختفاء معروض في {alert.get('city')}")
        
        details = {
            "city": alert.get("city", "غير محدد"),
            "property_type": signal.get("property_type", "غير محدد"),
            "supply_drop": drop_pct,
            "districts_lost": alert.get("district", "عدة أحياء"),
            "district_loss_ratio": signal.get("district_loss_ratio", 0),
            "previous_count": signal.get("previous_count", 0),
            "current_count": signal.get("current_count", 0),
            "window": signal.get("window_hours", 24),
            "is_exclusive": alert.get("is_exclusive", True),
            "priority": priority
        }
        
    elif alert_type == "LIQUIDITY_INFLOW":
        icon = "💧"
        title = alert.get("title", f"💧 دخول سيولة في {alert.get('city')}")
        
        details = {
            "city": alert.get("city", "غير محدد"),
            "property_type": signal.get("property_type", "غير محدد"),
            "liquidity_change": signal.get("liquidity_change_percent", 0),
            "price_change": signal.get("price_change_percent", 0),
            "active_districts": alert.get("district", "عدة أحياء"),
            "previous_count": signal.get("previous_count", 0),
            "current_count": signal.get("current_count", 0),
            "window": signal.get("window_hours", 24),
            "is_exclusive": alert.get("is_exclusive", True),
            "priority": priority
        }

    elif alert_type == "BUYER_BEHAVIOR_SHIFT":
        icon = "🧠"
        title = alert.get("title", f"🧠 تغير سلوك الشراء في {alert.get('city')}")
        signals_list = signal.get("signals", [])
        
        details = {
            "city": alert.get("city", "غير محدد"),
            "property_type": signal.get("property_type", "غير محدد"),
            "signals": signals_list,
            "window": signal.get("window_hours", 24),
            "is_exclusive": alert.get("is_exclusive", True),
            "priority": priority
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
        
        details = {
            "city": alert.get("city", "غير محدد"),
            "district": alert.get("district", "غير محدد"),
            "discount": discount,
            "price": price_str,
            "window": signal.get("window_hours", 24),
            "property_type": signal.get("property_type", "غير محدد"),
            "expected_return": signal.get("expected_return", "غير متاح"),
            "context_bias": signal.get("context_bias", {}),
            "is_exclusive": alert.get("is_exclusive", True),
            "priority": priority
        }
    
    # إضافة رمز حسب مستوى الثقة
    confidence = alert.get("confidence", "MEDIUM")
    if confidence == "HIGH":
        confidence_icon = "🔴"
    elif confidence == "MEDIUM":
        confidence_icon = "🟡"
    else:
        confidence_icon = "🟢"
    
    # إضافة رمز حسب الأولوية التجارية
    priority_icon = {
        "GOLD": "💎",
        "MID": "⚡",
        "LOW": "📌"
    }.get(priority, "")
    
    return {
        "icon": icon,
        "confidence_icon": confidence_icon,
        "priority_icon": priority_icon,
        "title": title,
        "message": build_human_message(alert),  # ✅ رسالة بشرية نظيفة
        "details": details,
        "confidence": confidence,
        "priority": priority,
        "time": alert.get("generated_at", "وقت غير محدد"),
        "type": alert_type,
        "is_exclusive": alert.get("is_exclusive", True)
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
        if alert_type == "SUPPLY_ABSORPTION":
            icon = "🔥"
        elif alert_type == "LIQUIDITY_INFLOW":
            icon = "💧"
        elif alert_type == "BUYER_BEHAVIOR_SHIFT":
            icon = "🧠"
        else:
            icon = "💰"
        print(f"  {icon} {alert_type}: {count}")
    
    # توزيع حسب مستوى الثقة
    print(f"\n🔴 توزيع التنبيهات حسب القوة:")
    for conf, count in stats["by_confidence"].items():
        icon = "🔴" if conf == "HIGH" else "🟡" if conf == "MEDIUM" else "🟢"
        print(f"  {icon} {conf}: {count}")
    
    # توزيع حسب الأولوية التجارية
    print(f"\n💎 توزيع التنبيهات حسب الأولوية:")
    for priority, count in stats["by_priority"].items():
        icon = "💎" if priority == "GOLD" else "⚡" if priority == "MID" else "📌"
        print(f"  {icon} {priority}: {count}")
    
    # توزيع حسب المدينة
    print(f"\n📍 التوزيع حسب المدينة:")
    for city, count in stats["by_city"].items():
        print(f"  • {city}: {count} تنبيه")
    
    # عرض أول 5 تنبيهات
    if alerts:
        print(f"\n📌 أبرز التنبيهات:")
        for i, alert in enumerate(alerts[:5]):
            exclusive = "📢 " if alert.get("is_exclusive") else ""
            priority_icon = "💎" if alert.get("priority") == "GOLD" else "⚡" if alert.get("priority") == "MID" else "📌"
            print(f"  {i+1}. {priority_icon} {exclusive}{build_human_message(alert)}")

# ==============================
# 7️⃣ اختبار سريع (يشتغل فقط إذا شغلت الملف مباشرة)
# ==============================

if __name__ == "__main__":
    print("\n🧪 تشغيل اختبار نظام التنبيهات...")
    
    # تنظيف التنبيهات القديمة (سنة كاملة)
    clear_old_alerts(days=365)
    
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
    print(f"  • توزيع الأولويات: {stats['by_priority']}")
    
    # عرض نموذج لرسالة بشرية
    if alerts:
        print(f"\n📝 نموذج رسالة بشرية:")
        exclusive = "📢 " if alerts[0].get("is_exclusive") else ""
        priority_icon = "💎" if alerts[0].get("priority") == "GOLD" else "⚡" if alerts[0].get("priority") == "MID" else "📌"
        print(f"  {priority_icon} {exclusive}{build_human_message(alerts[0])}")
    
    # اختبار التاريخ
    print(f"\n📜 اختبار جلب آخر 7 أيام:")
    history = get_alerts_history(days=7)
    print(f"  ✅ عدد التنبيهات في آخر 7 أيام: {len(history)}")
    
    # اختبار آخر تنبيه لكل مدينة
    print(f"\n📍 اختبار آخر تنبيه لكل مدينة:")
    latest_summary = get_latest_alerts_summary()
    for city, alerts in latest_summary.items():
        print(f"  {city}:")
        for alert_type, info in alerts.items():
            priority_icon = "💎" if info.get("priority") == "GOLD" else "⚡" if info.get("priority") == "MID" else "📌"
            print(f"    • {priority_icon} {info['message']}")
    
    print("\n✅ انتهى الاختبار")
