# report_pdf_generator.py
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from report_content_builder import build_report_content  # نص التقرير (HTML/plain)
import arabic_reshaper
from bidi.algorithm import get_display

def arabic_text(text):
    return get_display(arabic_reshaper.reshape(str(text)))

def create_pdf_from_content(user_info, market_data, df, content_text, package_level, ai_recommendations=None):
    """
    content_text: نص التقرير الكامل (string) من build_report_content
    يعيد BytesIO جاهز للتحميل.
    """
    buffer = BytesIO()
    with PdfPages(buffer) as pdf:
        # صفحة الغلاف بسيطة ونظيفة
        fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
        plt.axis('off')
        plt.text(0.5, 0.85, arabic_text("تقرير Warda Intelligence"), fontsize=24, ha='center', weight='bold')
        plt.text(0.5, 0.8, arabic_text("التحليل الاستثماري الاحترافي"), fontsize=14, ha='center')
        meta = f"المدينة: {user_info.get('city','-')}  |  نوع العقار: {user_info.get('property_type','-')}  |  الباقة: {package_level}  |  تاريخ: {datetime.now().strftime('%Y-%m-%d')}"
        plt.text(0.5, 0.72, arabic_text(meta), fontsize=10, ha='center')
        plt.text(0.5, 0.45, arabic_text("ملخص التقرير:"), fontsize=12, ha='center', weight='bold')
        plt.text(0.5, 0.35, arabic_text(content_text[:1200] + ("..." if len(content_text) > 1200 else "")), fontsize=10, ha='center', wrap=True)
        pdf.savefig(fig)
        plt.close(fig)

        # صفحة: الملخص التنفيذي (نص كامل مقسّم)
        fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
        plt.axis('off')
        plt.text(0.5, 0.95, arabic_text("الملخص التنفيذي"), fontsize=18, ha='center', weight='bold')
        # نعرض جزء من النص بشكل منسق
        wrapped = content_text.replace('\n', '\n\n')
        plt.text(0.05, 0.88, arabic_text(wrapped[:3500]), fontsize=11, ha='right', va='top', wrap=True)
        pdf.savefig(fig)
        plt.close(fig)

        # إضافة رسوم بيانية من df: (5 صفحات) — كل صفحة رسم أو جدول ملخّص
        # 1) توزيع الأسعار
        try:
            fig, ax = plt.subplots(figsize=(8.27, 5))
            prices = df['السعر'].dropna() / 1000.0
            ax.hist(prices, bins=15)
            ax.set_title(arabic_text("توزيع الأسعار (بالآلاف)"))
            ax.set_xlabel(arabic_text("السعر (ألف ريال)"))
            ax.set_ylabel(arabic_text("عدد الإعلانات"))
            pdf.savefig(fig)
            plt.close(fig)
        except Exception:
            pass

        # 2) نمو الأسعار - مبني على market_data إن وُجد
        try:
            fig, ax = plt.subplots(figsize=(8.27, 5))
            months = ['حالي', '1 شهر', '3 أشهر', '6 أشهر', 'سنة']
            growth_rate = market_data.get('معدل_النمو_الشهري', 0)
            current = market_data.get('السعر_الحالي', df['السعر'].mean() if not df.empty else 0)
            rates = [current * (1 + growth_rate * i/100) for i in [0,1,3,6,12]]
            ax.plot(months, rates, marker='o')
            ax.set_title(arabic_text("توقع تطور الأسعار"))
            pdf.savefig(fig)
            plt.close(fig)
        except Exception:
            pass

        # 3) توزيع الأسعار حسب المناطق (bar)
        try:
            fig, ax = plt.subplots(figsize=(8.27,5))
            area_avg = df.groupby('المنطقة')['السعر'].mean().nlargest(8) / 1000.0
            area_avg.plot(kind='bar', ax=ax)
            ax.set_title(arabic_text("متوسط السعر حسب المنطقة (أعلى 8)"))
            pdf.savefig(fig)
            plt.close(fig)
        except Exception:
            pass

        # 4) عائد الإيجار مقابل السعر (scatter) إن وُجد العمود
        try:
            fig, ax = plt.subplots(figsize=(8.27,5))
            if 'العائد_المتوقع' in df.columns:
                ax.scatter(df['السعر'], df['العائد_المتوقع'])
                ax.set_title(arabic_text("عائد الإيجار مقابل السعر"))
                pdf.savefig(fig)
            plt.close(fig)
        except Exception:
            pass

        # 5) أفضل 5 فرص من ai_recommendations إن وُجدت
        try:
            fig, ax = plt.subplots(figsize=(8.27,5))
            if ai_recommendations and "أفضل_الفرص" in ai_recommendations:
                top5 = ai_recommendations["أفضل_الفرص"]
                names = [p['name'] for p in top5][:5]
                scores = [p['score'] for p in top5][:5]
                ax.bar(names, scores)
                ax.set_title(arabic_text("أفضل 5 فرص حسب الذكاء الاصطناعي"))
                pdf.savefig(fig)
            plt.close(fig)
        except Exception:
            pass

        # صفحة: توصيات (مخصصة حسب الباقة)
        fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
        plt.axis('off')
        plt.text(0.5, 0.95, arabic_text("التوصيات النهائية"), fontsize=18, ha='center', weight='bold')
        # نأخذ نهاية النص (أجزاء التوصية) 
        tail = content_text[-1500:] if len(content_text) > 1500 else content_text
        plt.text(0.05, 0.9, arabic_text(tail), fontsize=11, ha='right', va='top', wrap=True)
        pdf.savefig(fig)
        plt.close(fig)

    buffer.seek(0)
    return buffer
