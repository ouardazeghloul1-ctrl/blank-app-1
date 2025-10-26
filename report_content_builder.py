from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
import arabic_reshaper
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
import pandas as pd

# تسجيل خط عربي
font_path = "Amiri-Regular.ttf"
pdfmetrics.registerFont(TTFont("Arabic", font_path))

def arabic_text(text):
    """تهيئة النص العربي للعرض في PDF"""
    return get_display(arabic_reshaper.reshape(str(text)))

# ==================== إنشاء التقرير النهائي ====================
def generate_report(user_info, market_data, real_data, ai_recommendations=None, package_level="فضية"):
    """
    user_info: dict يحتوي على keys: user_type, city, property_type, area
    market_data: dict يحتوي على مؤشرات السوق
    real_data: pd.DataFrame يحتوي على العقارات (السعر، المنطقة، العائد المتوقّع)
    ai_recommendations: dict اختياري يحتوي على التوصيات الذكية
    package_level: "فضية" / "ذهبية" / "ماسية"
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # -------------------- صفحة الغلاف --------------------
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.rect(0, 0, width, height, fill=1)

    c.setFillColorRGB(0.83, 0.7, 0.27)
    c.setFont("Arabic", 32)
    c.drawCentredString(width/2, height - 3*cm, arabic_text("تقرير Warda Intelligence الفاخر"))

    c.setFont("Arabic", 20)
    c.drawCentredString(width/2, height - 4.2*cm, arabic_text("التحليل الاستثماري الذهبي"))

    c.setFont("Arabic", 13)
    text = f"""
تقرير استثماري مقدم إلى {user_info['user_type']}
المدينة: {user_info['city']}
نوع العقار: {user_info['property_type']}
المساحة: {user_info['area']} م²
عدد العقارات المحللة: {len(real_data)}
الباقة: {package_level}
تاريخ إعداد التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    y = height - 7*cm
    for line in text.split("\n"):
        c.drawCentredString(width/2, y, arabic_text(line))
        y -= 0.9*cm

    c.showPage()

    # -------------------- الملخص التنفيذي --------------------
    c.setFont("Arabic", 22)
    c.drawString(2*cm, height - 2.5*cm, arabic_text("الملخص التنفيذي"))

    c.setFont("Arabic", 14)
    summary = f"""
يوفر هذا التقرير تحليلاً دقيقًا لسوق العقارات في مدينة {user_info['city']}
استناداً إلى بيانات حقيقية تم جمعها من {len(real_data)} عقار فعلي.

العائد التأجيري المتوقع: {market_data.get('العائد_التأجيري', 0):.1f}%
معدل النمو الشهري: {market_data.get('معدل_النمو_الشهري', 0):.1f}%
"""
    y = height - 4.5*cm
    for line in summary.split("\n"):
        c.drawString(2*cm, y, arabic_text(line))
        y -= 1*cm

    c.showPage()

    # ==================== الرسوم البيانية الخمسة ====================
    charts = create_analysis_charts(real_data, market_data, user_info, ai_recommendations)

    for chart in charts:
        chart.savefig(buffer, format='png', bbox_inches='tight')
        plt.close(chart)
        # إدراج الرسم في PDF
        c.drawImage(buffer, 2*cm, 5*cm, width=16*cm, height=20*cm)
        c.showPage()
        buffer.seek(0)
        buffer.truncate(0)

    # -------------------- صفحة التوصيات الذكية --------------------
    if ai_recommendations and package_level in ["ذهبية", "ماسية"]:
        c.setFont("Arabic", 22)
        c.drawString(2*cm, height - 2.5*cm, arabic_text("توصيات الذكاء الاصطناعي"))

        c.setFont("Arabic", 14)
        ai_text = f"""
ملف المخاطر: {ai_recommendations.get('ملف_المخاطر', '-') }
الاستراتيجية المقترحة: {ai_recommendations.get('استراتيجية_الاستثمار', '-') }
التوقيت المثالي: {ai_recommendations.get('التوقيت_المثالي', '-') }
مستوى الثقة: {ai_recommendations.get('مؤشرات_الثقة', {}).get('مستوى_الثقة', '-') }
"""
        y = height - 4.5*cm
        for line in ai_text.split("\n"):
            c.drawString(2*cm, y, arabic_text(line))
            y -= 1*cm
        c.showPage()

    c.save()
    buffer.seek(0)
    return buffer

# ==================== إنشاء الرسوم البيانية الخمسة ====================
def create_analysis_charts(real_data, market_data, user_info, ai_recommendations=None):
    charts = []

    # تنظيف البيانات
    if real_data is None or real_data.empty:
        fig, ax = plt.subplots(figsize=(10,6))
        ax.text(0.5,0.5,"لا توجد بيانات كافية للعرض", ha='center', va='center', fontsize=14)
        ax.axis('off')
        charts.append(fig)
        return charts

    real_data = real_data.copy()
    real_data["السعر"] = pd.to_numeric(real_data["السعر"], errors="coerce")
    real_data = real_data.dropna(subset=["السعر"])

    # --------- الرسم 1: مقارنة الأسعار ----------
    fig, ax = plt.subplots(figsize=(10,6))
    ax.hist(real_data['السعر']/1000, bins=15, color='gold', alpha=0.7)
    ax.set_xlabel(arabic_text("السعر (ألف ريال)"))
    ax.set_ylabel(arabic_text("عدد العقارات"))
    ax.set_title(arabic_text(f"توزيع أسعار {user_info['property_type']} في {user_info['city']}"))
    charts.append(fig)

    # --------- الرسم 2: تطور الأسعار خلال 6 أشهر ----------
    fig, ax = plt.subplots(figsize=(10,6))
    months = ['حالي', '1 شهر', '3 أشهر', '6 أشهر']
    growth_rate = market_data.get('معدل_النمو_الشهري', 0)
    current_price = market_data.get('السعر_الحالي', real_data['السعر'].mean())
    future_prices = [current_price*(1 + growth_rate*i/100) for i in [0,1,3,6]]
    ax.plot(months, future_prices, marker='o', color='gold', linewidth=2)
    ax.set_xlabel(arabic_text("الفترة الزمنية"))
    ax.set_ylabel(arabic_text("السعر المتوقع"))
    ax.set_title(arabic_text("تطور الأسعار المتوقع"))
    charts.append(fig)

    # --------- الرسم 3: توزيع الأسعار حسب المنطقة ----------
    fig, ax = plt.subplots(figsize=(10,6))
    area_prices = real_data.groupby('المنطقة')['السعر'].mean().nlargest(8)/1000
    bars = ax.bar(range(len(area_prices)), area_prices.values, color='gold', alpha=0.7)
    ax.set_xticks(range(len(area_prices)))
    ax.set_xticklabels([arabic_text(idx) for idx in area_prices.index], rotation=45)
    ax.set_ylabel(arabic_text("متوسط السعر (ألف ريال)"))
    ax.set_title(arabic_text("أعلى المناطق سعراً"))
    charts.append(fig)

    # --------- الرسم 4: عائد الإيجار مقابل السعر ----------
    fig, ax = plt.subplots(figsize=(10,6))
    ax.scatter(real_data['السعر'], real_data['العائد_المتوقع'], color='green', alpha=0.7)
    ax.set_xlabel(arabic_text("السعر"))
    ax.set_ylabel(arabic_text("العائد المتوقع (%)"))
    ax.set_title(arabic_text("عائد الإيجار مقابل السعر"))
    charts.append(fig)

    # --------- الرسم 5: أفضل 5 فرص استثمارية ----------
    fig, ax = plt.subplots(figsize=(10,6))
    if ai_recommendations and "أفضل_الفرص" in ai_recommendations:
        top5 = ai_recommendations["أفضل_الفرص"]
        ax.bar(range(len(top5)), [x['score'] for x in top5], color='purple', alpha=0.7)
        ax.set_xticks(range(len(top5)))
        ax.set_xticklabels([arabic_text(x['name']) for x in top5], rotation=45)
        ax.set_ylabel(arabic_text("درجة الفرصة"))
        ax.set_title(arabic_text("أفضل 5 فرص عقارية حسب الذكاء الاصطناعي"))
    else:
        ax.text(0.5,0.5,"لا توجد فرص لتقييمها", ha='center', va='center', fontsize=14)
        ax.axis('off')
    charts.append(fig)

    return charts
