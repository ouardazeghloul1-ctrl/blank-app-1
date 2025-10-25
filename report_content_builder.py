from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
import arabic_reshaper
import os
from datetime import datetime

# تسجيل خط عربي
font_path = "Amiri-Regular.ttf"  # إذا عندك خط ثاني غيّري الاسم فقط
pdfmetrics.registerFont(TTFont("Arabic", font_path))

def A(text):
    """ تهيئة العربية """
    return get_display(arabic_reshaper.reshape(str(text)))

def generate_report(user_info, market_data, real_data, ai_recommendations, package_level):
    pdf_path = "real_estate_report.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    
    # -------------------- صفحة الغلاف --------------------
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.rect(0, 0, width, height, fill=1)

    c.setFillColorRGB(0.83, 0.7, 0.27)
    c.setFont("Arabic", 32)
    c.drawCentredString(width/2, height - 3*cm, A("تقرير Warda Intelligence الفاخر"))

    c.setFont("Arabic", 20)
    c.drawCentredString(width/2, height - 4.2*cm, A("التحليل الاستثماري الذهبي"))

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
        c.drawCentredString(width/2, y, A(line))
        y -= 0.9*cm

    c.showPage()

    # -------------------- صفحة الملخص التنفيذي --------------------
    c.setFont("Arabic", 22)
    c.drawString(2*cm, height - 2.5*cm, A("الملخص التنفيذي"))

    c.setFont("Arabic", 14)
    summary = f"""
يوفر هذا التقرير تحليلاً عميقًا لسوق العقارات في مدينة {user_info['city']} 
استناداً إلى بيانات حقيقية تم جمعها من {len(real_data)} عقار فعلي.

العائد التأجيري المتوقع: {market_data['العائد_التأجيري']:.1f}%
معدل النمو الشهري: {market_data['معدل_النمو_الشهري']:.1f}%
"""
    y = height - 4.5*cm
    for line in summary.split("\n"):
        c.drawString(2*cm, y, A(line))
        y -= 1*cm
    
    c.showPage()

    # -------------------- توصيات الذكاء الاصطناعي (إن وجدت) --------------------
    if ai_recommendations and package_level in ["ذهبية", "ماسية"]:
        c.setFont("Arabic", 22)
        c.drawString(2*cm, height - 2.5*cm, A("تحليل الذكاء الاصطناعي"))

        c.setFont("Arabic", 14)
        ai_text = f"""
ملف المخاطر: {ai_recommendations['ملف_المخاطر']}
الاستراتيجية المقترحة: {ai_recommendations['استراتيجية_الاستثمار']}
التوقيت المثالي: {ai_recommendations['التوقيت_المثالي']}
مستوى الثقة: {ai_recommendations['مؤشرات_الثقة']['مستوى_الثقة']}
"""
        y = height - 4.5*cm
        for line in ai_text.split("\n"):
            c.drawString(2*cm, y, A(line))
            y -= 1*cm

        c.showPage()

    c.save()
    return pdf_path
