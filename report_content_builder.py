from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display

# ---------------------- إعدادات أساسية ----------------------
PACKAGES = {
    "مجانية": {"pages": 15},
    "فضية": {"pages": 35},
    "ذهبية": {"pages": 60},
    "ماسية": {"pages": 90}
}

def arabic_text(text):
    """تهيئة النص العربي للعرض"""
    return get_display(arabic_reshaper.reshape(str(text)))

# ---------------------- الغلاف ----------------------
def create_cover_page(user_info):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.5, 0.85, arabic_text("تقرير Warda Intelligence"), fontsize=28, ha='center', weight='bold', color='black')
    plt.text(0.5, 0.78, arabic_text("التحليل الاستثماري الاحترافي"), fontsize=20, ha='center', style='italic', color='black')
    
    intro_text = f"""
تقرير استثماري مقدم إلى {user_info['user_type']}
المدينة: {user_info['city']}
نوع العقار: {user_info['property_type']}
المساحة: {user_info['area']} م²
تاريخ إعداد التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    plt.text(0.5, 0.55, arabic_text(intro_text), fontsize=12, ha='center', va='center', color='black',
             bbox=dict(boxstyle="round,pad=1", facecolor="#f0f0f0", edgecolor='black', linewidth=1))
    return fig

# ---------------------- الملخص التنفيذي ----------------------
def create_executive_summary(user_info, market_data, real_data):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.5, 0.9, arabic_text("الملخص التنفيذي"), fontsize=22, ha='center', weight='bold', color='black')

    summary_text = f"""
يوفر هذا التقرير تحليلاً عميقًا لسوق العقارات في {user_info['city']} 
استناداً إلى بيانات حقيقية تم جمعها من {len(real_data)} عقار فعلي.
العائد التأجيري المتوقع: {market_data.get('العائد_التأجيري', 0):.1f}%
معدل النمو الشهري: {market_data.get('معدل_النمو_الشهري', 0):.1f}%
"""
    plt.text(0.5, 0.55, arabic_text(summary_text), fontsize=14, ha='center', va='center', color='black')
    return fig

# ---------------------- مؤشرات الأداء ----------------------
def create_performance_metrics(user_info, market_data, real_data):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.5, 0.9, arabic_text("مؤشرات الأداء الرئيسية"), fontsize=22, ha='center', weight='bold', color='black')
    
    metrics_text = f"""
عدد العقارات المحللة: {len(real_data)}
الأسعار الفعلية المتوسطة: {market_data.get('متوسط_السعر', 0):,.0f} ريال
"""
    plt.text(0.5, 0.55, arabic_text(metrics_text), fontsize=14, ha='center', va='center', color='black')
    return fig

# ---------------------- تحليل البيانات ----------------------
def create_analysis_charts(market_data, real_data, user_info):
    charts = []
    # رسم بياني نمو الأسعار
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.5, 0.9, arabic_text("نمو الأسعار الشهرية"), fontsize=20, ha='center', weight='bold', color='black')
    plt.text(0.5, 0.55, arabic_text("مخطط توضيحي لنمو الأسعار لكل شهر خلال العام"), fontsize=14, ha='center', color='black')
    charts.append(fig)
    
    # رسم بياني مقارنة المشاريع
    fig2 = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.5, 0.9, arabic_text("مقارنة المشاريع المنافسة"), fontsize=20, ha='center', weight='bold', color='black')
    plt.text(0.5, 0.55, arabic_text("مخطط يوضح أسعار المنافسين للمقارنة"), fontsize=14, ha='center', color='black')
    charts.append(fig2)
    
    return charts

# ---------------------- التحليل المالي ----------------------
def create_financial_analysis(user_info, market_data):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.5, 0.9, arabic_text("التحليل المالي"), fontsize=22, ha='center', weight='bold', color='black')
    financial_text = f"""
العائد المتوقع: {market_data.get('العائد_التأجيري', 0):.1f}%
معدل النمو: {market_data.get('معدل_النمو_الشهري', 0):.1f}%
"""
    plt.text(0.5, 0.55, arabic_text(financial_text), fontsize=14, ha='center', color='black')
    return fig

# ---------------------- توصيات استراتيجية ----------------------
def create_strategic_recommendations(user_info, market_data):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.5, 0.9, arabic_text("التوصيات الاستراتيجية"), fontsize=22, ha='center', weight='bold', color='black')
    rec_text = arabic_text("نصائح استثمارية مخصصة حسب باقتك ومستوى التحليل.")
    plt.text(0.5, 0.55, rec_text, fontsize=14, ha='center', color='black')
    return fig

# ---------------------- الذكاء الاصطناعي ----------------------
def create_ai_analysis_page(user_info, ai_recommendations):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.5, 0.9, arabic_text("تحليل الذكاء الاصطناعي"), fontsize=22, ha='center', weight='bold', color='black')
    ai_text = f"""
ملف المخاطر: {ai_recommendations.get('ملف_المخاطر', '-') }
الاستراتيجية: {ai_recommendations.get('استراتيجية_الاستثمار', '-') }
التوقيت المثالي: {ai_recommendations.get('التوقيت_المثالي', '-') }
مستوى الثقة: {ai_recommendations.get('مستوى_الثقة', '-') }
"""
    plt.text(0.5, 0.55, arabic_text(ai_text), fontsize=14, ha='center', color='black')
    return fig

# ---------------------- الصفحات التفصيلية ----------------------
def create_detailed_analysis_page(user_info, market_data, real_data, page_num, total_pages, package_level):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    plt.axis('off')
    plt.text(0.5, 0.9, arabic_text(f"صفحة {page_num} من {total_pages}"), fontsize=18, ha='center', color='black')
    content_text = arabic_text("تفاصيل متقدمة حسب باقتك وتحليل السوق")
    plt.text(0.5, 0.55, content_text, fontsize=14, ha='center', color='black')
    return fig

# ---------------------- دالة إنشاء PDF نهائي ----------------------
def create_professional_pdf(user_info, market_data, real_data, package_level, ai_recommendations=None):
    buffer = BytesIO()
    with PdfPages(buffer) as pdf:
        total_pages = PACKAGES[package_level]['pages']
        
        # صفحة الغلاف
        pdf.savefig(create_cover_page(user_info))
        plt.close('all')
        
        # الملخص التنفيذي
        pdf.savefig(create_executive_summary(user_info, market_data, real_data))
        plt.close('all')
        
        # مؤشرات الأداء
        pdf.savefig(create_performance_metrics(user_info, market_data, real_data))
        plt.close('all')
        
        # الرسوم البيانية والتحليل
        if package_level in ["فضية", "ذهبية", "ماسية"]:
            charts = create_analysis_charts(market_data, real_data, user_info)
            for chart in charts:
                pdf.savefig(chart)
                plt.close('all')
        
        # التحليل المالي
        pdf.savefig(create_financial_analysis(user_info, market_data))
        plt.close('all')
        
        # التوصيات
        pdf.savefig(create_strategic_recommendations(user_info, market_data))
        plt.close('all')
        
        # الذكاء الاصطناعي
        if package_level in ["ذهبية", "ماسية"] and ai_recommendations:
            pdf.savefig(create_ai_analysis_page(user_info, ai_recommendations))
            plt.close('all')
        
        # الصفحات التفصيلية
        start_page = 11 if package_level in ["ذهبية", "ماسية"] and ai_recommendations else 10
        for page_num in range(start_page, total_pages + 1):
            pdf.savefig(create_detailed_analysis_page(user_info, market_data, real_data, page_num, total_pages, package_level))
            plt.close('all')
    
    buffer.seek(0)
    return buffer
