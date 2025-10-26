from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
import arabic_reshaper
from io import BytesIO
from datetime import datetime

# تسجيل خط عربي
font_path = "Amiri-Regular.ttf"  # تأكدي أن الخط موجود
pdfmetrics.registerFont(TTFont("Arabic", font_path))

def A(text):
    """تهيئة العربية"""
    return get_display(arabic_reshaper.reshape(str(text)))

def generate_report(user_info, market_data, real_data, ai_recommendations, package_level):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # -------------------- صفحة الغلاف --------------------
    c.setFillColorRGB(0.1,0.1,0.1)
    c.rect(0,0,width,height,fill=1)
    c.setFillColorRGB(0.83,0.7,0.27)
    c.setFont("Arabic", 32)
    c.drawCentredString(width/2, height - 3*cm, A("تقرير Warda Intelligence الفاخر"))
    c.showPage()

    # -------------------- صفحة الملخص التنفيذي --------------------
    c.setFont("Arabic", 22)
    c.drawString(2*cm, height - 2.5*cm, A("الملخص التنفيذي"))
    c.setFont("Arabic", 14)
    c.drawString(2*cm, height - 4*cm, A(f"العائد التأجيري المتوقع: {market_data['العائد_التأجيري']:.1f}%"))
    c.showPage()

    # -------------------- توصيات الذكاء الاصطناعي --------------------
    if ai_recommendations and package_level in ["ذهبية","ماسية"]:
        c.setFont("Arabic", 22)
        c.drawString(2*cm, height - 2.5*cm, A("تحليل الذكاء الاصطناعي"))
        c.showPage()

    c.save()
    buffer.seek(0)
    return buffer
