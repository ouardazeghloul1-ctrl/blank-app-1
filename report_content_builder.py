# report_content_builder.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
import arabic_reshaper
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

# تسجيل خط عربي
font_path = "Amiri-Regular.ttf"  # تأكدي أن الخط موجود في نفس المسار
pdfmetrics.registerFont(TTFont("Arabic", font_path))

def arabic_text(text):
    """تهيئة النص العربي للعرض"""
    return get_display(arabic_reshaper.reshape(str(text)))

# ========================== دالة توليد التقرير ==========================
def generate_report(user_info, market_data, real_data, ai_recommendations=None, package_level="فضية"):
    buffer = BytesIO()  # هذه المهمة الأساسية لتوليد PDF في الذاكرة
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
يوفر هذا التقرير تحليلاً عميقًا لسوق العقارات في مدينة {user_info['city']} 
استناداً إلى بيانات حقيقية تم جمعها من {len(real_data)} عقار فعلي.

العائد التأجيري المتوقع: {market_data['العائد_التأجيري']:.1f}%
معدل النمو الشهري: {market_data['معدل_النمو_الشهري']:.1f}%
"""
    y = height - 4.5*cm
    for line in summary.split("\n"):
        c.drawString(2*cm, y, arabic_text(line))
        y -= 1*cm

    c.showPage()

    # -------------------- توصيات الذكاء الاصطناعي --------------------
    if ai_recommendations and package_level in ["ذهبية", "ماسية"]:
        c.setFont("Arabic", 22)
        c.drawString(2*cm, height - 2.5*cm, arabic_text("تحليل الذكاء الاصطناعي"))

        c.setFont("Arabic", 14)
        ai_text = f"""
ملف المخاطر: {ai_recommendations['ملف_المخاطر']}
الاستراتيجية المقترحة: {ai_recommendations['استراتيجية_الاستثمار']}
التوقيت المثالي: {ai_recommendations['التوقيت_المثالي']}
مستوى الثقة: {ai_recommendations['مؤشرات_الثقة']['مستوى_الثقة']}
"""
        y = height - 4.5*cm
        for line in ai_text.split("\n"):
            c.drawString(2*cm, y, arabic_text(line))
            y -= 1*cm

        c.showPage()

    c.save()
    buffer.seek(0)
    return buffer  # هذه تعود مباشرة للـ Streamlit

# ========================== الرسوم البيانية ==========================
def create_analysis_charts(market_data, real_data, user_info):
    charts = []

    # تنظيف الأسعار
    if real_data is not None and not real_data.empty:
        real_data = real_data.copy()
        real_data["السعر"] = pd.to_numeric(real_data["السعر"], errors="coerce")
        real_data = real_data.dropna(subset=["السعر"])
    else:
        real_data = pd.DataFrame()

    charts.append(create_price_distribution_chart(real_data, user_info))
    charts.append(create_area_analysis_chart(real_data, user_info))
    charts.append(create_forecast_chart(market_data, user_info))

    return charts

def create_price_distribution_chart(real_data, user_info):
    fig, ax = plt.subplots(figsize=(10,6), facecolor='white')
    if real_data.empty:
        ax.text(0.5, 0.5, "لا توجد بيانات كافية للعرض", ha='center', va='center', fontsize=14, color='#d4af37')
        ax.axis('off')
        return fig

    prices = real_data['السعر'] / 1000
    ax.hist(prices, bins=15, color='gold', alpha=0.7, edgecolor='#d4af37')
    ax.set_xlabel(arabic_text('السعر (ألف ريال)'))
    ax.set_ylabel(arabic_text('عدد العقارات'))
    ax.set_title(arabic_text(f'توزيع أسعار {user_info["property_type"]} - {user_info["city"]}'))
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

def create_area_analysis_chart(real_data, user_info):
    fig, ax = plt.subplots(figsize=(10,6), facecolor='white')
    if real_data.empty:
        ax.text(0.5, 0.5, "لا توجد بيانات كافية للعرض", ha='center', va='center', fontsize=14, color='#d4af37')
        ax.axis('off')
        return fig

    area_prices = real_data.groupby('المنطقة')['السعر'].mean().nlargest(8) / 1000
    bars = ax.bar(range(len(area_prices)), area_prices.values, color='#d4af37', alpha=0.8)
    ax.set_xlabel(arabic_text('المناطق'))
    ax.set_ylabel(arabic_text('متوسط السعر (ألف ريال)'))
    ax.set_title(arabic_text('أعلى المناطق سعراً'))
    ax.set_xticks(range(len(area_prices)))
    ax.set_xticklabels([arabic_text(idx) for idx in area_prices.index], rotation=45, ha='right')

    for bar, price in zip(bars, area_prices.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f'{price:,.0f}', ha='center', fontsize=10)

    plt.tight_layout()
    return fig

def create_forecast_chart(market_data, user_info):
    fig, ax = plt.subplots(figsize=(10,6), facecolor='white')
    months = [arabic_text('الحالي'), arabic_text('3 أشهر'), arabic_text('6 أشهر'), arabic_text('سنة')]
    growth_rates = [0, 3, 6, 12]

    current_price = market_data.get('السعر_الحالي', 1000)
    growth_rate = market_data.get('معدل_النمو_الشهري', 0)

    future_prices = [current_price * (1 + growth_rate * rate / 100) for rate in growth_rates]
    ax.plot(months, future_prices, marker='o', linewidth=3, markersize=8, color='#d4af37', markerfacecolor='gold')
    ax.set_xlabel(arabic_text('الفترة الزمنية'))
    ax.set_ylabel(arabic_text('السعر المتوقع (ريال/م²)'))
    ax.set_title(arabic_text('التوقعات المستقبلية للأسعار'))
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig
