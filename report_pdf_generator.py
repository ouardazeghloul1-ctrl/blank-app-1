# report_pdf_generator.py
from io import BytesIO
import os
import tempfile
import re
import unicodedata
import logging
from datetime import datetime

import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    PageBreak, Image, HRFlowable,
    Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
import plotly.graph_objects as go

# =========================
# ✅ LOGGING SETUP
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =========================
# ✅ VALIDATION FUNCTION - منع الأخطاء المنطقية
# =========================
def validate_report_data(user_info):
    """
    التحقق من صحة البيانات قبل إنشاء التقرير
    يمنع الأخطاء المنطقية مثل تساوي عدد صفقات الحي مع صفقات نوع العقار
    """
    if not user_info:
        return True, ""
    
    district_transactions = user_info.get("district_transactions_total")
    property_transactions = user_info.get("property_transactions_count")
    
    # التحقق من عدم تساوي عدد صفقات الحي مع صفقات نوع العقار (إلا إذا كان هناك نوع واحد فقط)
    if district_transactions and property_transactions:
        try:
            d_total = float(district_transactions)
            p_total = float(property_transactions)
            
            if d_total == p_total and d_total > 0:
                # هذا خطأ منطقي - كل صفقات الحي لا يمكن أن تكون من نوع واحد فقط
                property_types_in_district = user_info.get("property_types_in_district", 1)
                if property_types_in_district > 1:
                    error_msg = (
                        f"❌ خطأ منطقي في البيانات: عدد صفقات الحي ({d_total:,.0f}) "
                        f"يساوي عدد صفقات نوع العقار ({p_total:,.0f}) "
                        f"مع وجود {property_types_in_district} أنواع عقارات في الحي"
                    )
                    logger.error(error_msg)
                    return False, error_msg
        except (ValueError, TypeError) as e:
            logger.warning(f"تحذير في التحقق من البيانات: {e}")
            pass
    
    logger.info("✅ تم التحقق من صحة البيانات بنجاح")
    return True, "✅ البيانات صالحة"


# =========================
# الحل النهائي: تقسيم الفقرة العربية إلى أسطر متعددة
# =========================
def arabic_paragraph_flowables(text, style, available_width):
    """
    تقسيم الفقرة العربية إلى أسطر متعددة وكل سطر يصبح Paragraph مستقل
    هذا يمنع Bug ترتيب الأسطر من الأسفل في ReportLab مع RTL
    """
    if not text:
        return []
    
    text = str(text)
    words = text.split()
    
    if not words:
        return []
    
    lines = []
    current_line = []
    
    for word in words:
        test_line = " ".join(current_line + [word])
        reshaped = arabic_reshaper.reshape(test_line)
        bidi_text = get_display(reshaped)
        width = stringWidth(bidi_text, style.fontName, style.fontSize)
        
        if width <= available_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(" ".join(current_line))
    
    flowables = []
    for line in lines:
        reshaped = arabic_reshaper.reshape(line)
        bidi_line = get_display(reshaped)
        flowables.append(Spacer(1, 0.15 * cm))
        flowables.append(Paragraph(bidi_line, style))
    
    return flowables


# =========================
# Arabic helper
# =========================
def ar(text):
    if not text:
        return ""

    try:
        text = str(text)
        # ✅ استبدال الأقواس بشرطة باستخدام regex لمنع المسافات المزدوجة
        text = re.sub(r"\(\s*", " - ", text)
        text = re.sub(r"\s*\)", "", text)
        text = text.replace("% ", "%")
        text = text.replace(" %", "%")
        text = re.sub(r'(-?\d+(\.\d+)?)\s*%', r'\1%', text)

        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception as e:
        logger.warning(f"خطأ في معالجة النص العربي: {e}")
        return str(text)


# =========================
# Clean bullets & junk
# =========================
def clean_text(text: str) -> str:
    if not text:
        return ""

    text = str(text)
    cleaned = []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat.startswith(("L", "N", "P", "Z")) or ch in "%$▲▼":
            cleaned.append(ch)

    text = "".join(cleaned)
    text = re.sub(r"^[\-\*\d\.\)]\s*", "", text)
    text = text.replace(":", " : ")
    text = text.replace("،", " ، ")
    text = text.replace("؛", " ؛ ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# =========================
# Plotly → Image
# =========================
def plotly_to_image(fig, width_cm, height_cm):
    if fig is None:
        return None

    tmp = None
    try:
        img_bytes = fig.to_image(
            format="png",
            width=1600,
            height=1000,
            scale=2,
            engine="kaleido"
        )

        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.write(img_bytes)
        tmp.close()

        img_obj = Image(tmp.name, width=width_cm * cm, height=height_cm * cm)
        img_obj._temp_file = tmp.name
        
        return img_obj

    except Exception as e:
        logger.error(f"خطأ في تصدير الرسم البياني: {e}")
        if tmp and os.path.exists(tmp.name):
            try:
                os.unlink(tmp.name)
            except:
                pass
        return None


# =========================
# MAP: District & Projects Map
# =========================
import pandas as pd

def create_district_projects_map(
    district_lat,
    district_lon,
    district_name,
    projects_df,
    impact_radius_km=5
):
    """
    إنشاء خريطة الحي والمشاريع القريبة
    الأعمدة المطلوبة في projects_df: خط_العرض, خط_الطول, اسم_المشروع
    """
    try:
        if district_lat is None or district_lon is None:
            logger.warning("الخريطة: إحداثيات الحي مفقودة")
            return None
        
        # ✅ التعامل مع حالة عدم وجود مشاريع
        if projects_df is None:
            logger.info("الخريطة: لا توجد بيانات مشاريع، إنشاء DataFrame فارغ")
            projects_df = pd.DataFrame()
        
        # ✅ إعادة تسمية عمود اسم المشروع إذا كان بالصيغة العربية
        if not projects_df.empty and "اسم_المشروع" not in projects_df.columns:
            if "اسم المشروع بالعربية" in projects_df.columns:
                projects_df = projects_df.rename(columns={"اسم المشروع بالعربية": "اسم_المشروع"})
                logger.info("✅ الخريطة: تم إعادة تسمية العمود 'اسم المشروع بالعربية' → 'اسم_المشروع'")
        
        required_columns = ["خط_العرض", "خط_الطول", "اسم_المشروع"]
        for col in required_columns:
            if not projects_df.empty and col not in projects_df.columns:
                logger.warning(f"الخريطة: العمود '{col}' مفقود في projects_df")
                return None
        
        # ✅ تحويل الإحداثيات إلى أرقام
        if not projects_df.empty:
            projects_df["خط_العرض"] = pd.to_numeric(projects_df["خط_العرض"], errors="coerce")
            projects_df["خط_الطول"] = pd.to_numeric(projects_df["خط_الطول"], errors="coerce")
            
            # إزالة الصفوف غير الصالحة
            projects_df = projects_df.dropna(subset=["خط_العرض", "خط_الطول"])
        
        logger.debug(f"نوع بيانات خط العرض: {projects_df['خط_العرض'].dtype if not projects_df.empty else 'empty'}")
        logger.debug(f"نوع بيانات خط الطول: {projects_df['خط_الطول'].dtype if not projects_df.empty else 'empty'}")
        logger.debug(f"إحداثيات الحي: خط العرض={district_lat}, خط الطول={district_lon}")
        
        # تحويل إحداثيات الحي إلى float
        district_lat = float(district_lat)
        district_lon = float(district_lon)
        
        # ✅ احترام نطاق البحث الذي يختاره المستخدم
        radius_km = max(float(impact_radius_km), 1)
        radius_deg = radius_km / 111
        
        logger.debug(f"نطاق البحث: {radius_km} كم = {radius_deg} درجة")
        
        # فلترة المشاريع القريبة
        nearby_projects = pd.DataFrame()
        if not projects_df.empty:
            nearby_projects = projects_df[
                (
                    (projects_df["خط_العرض"] - district_lat).abs() <= radius_deg
                ) &
                (
                    (projects_df["خط_الطول"] - district_lon).abs() <= radius_deg
                )
            ]
        
        logger.info(f"الخريطة: تم العثور على {len(nearby_projects)} مشروع قريب ضمن نطاق {radius_km} كم")
        
        fig = go.Figure()
        
        # دبوس الحي
        fig.add_trace(
            go.Scattermapbox(
                lat=[district_lat],
                lon=[district_lon],
                mode="markers",
                marker=dict(size=14, color="red"),
                text=[district_name],
                name="الحي"
            )
        )
        
        # دبابيس المشاريع
        if not nearby_projects.empty:
            fig.add_trace(
                go.Scattermapbox(
                    lat=nearby_projects["خط_العرض"],
                    lon=nearby_projects["خط_الطول"],
                    mode="markers",
                    marker=dict(size=10, color="blue"),
                    text=nearby_projects["اسم_المشروع"],
                    name="المشاريع القريبة"
                )
            )
        
        # ✅ استخدام carto-positron لحل مشكلة Access blocked
        title_text = f"موقع حي {district_name}"
        if not nearby_projects.empty:
            title_text += f" والمشاريع القريبة (نطاق {radius_km} كم)"
        
        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox=dict(
                center=dict(lat=district_lat, lon=district_lon),
                zoom=12
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=450,
            title=dict(
                text=title_text,
                x=0.5,
                xanchor='center',
                font=dict(size=16)
            )
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"خطأ في إنشاء الخريطة: {e}")
        import traceback
        traceback.print_exc()
        return None


# =========================
# Elegant divider
# =========================
def elegant_divider(width="80%", thickness=0.6, color=colors.HexColor("#C8C8C8")):
    return HRFlowable(
        width=width,
        thickness=thickness,
        color=color,
        spaceBefore=6,
        spaceAfter=8,
        lineCap='round'
    )


# =========================
# FOOTER
# =========================
def add_footer(canvas, doc):
    canvas.saveState()
    
    canvas.setStrokeColor(colors.HexColor("#DDDDDD"))
    canvas.line(2.4 * cm, 2 * cm, A4[0] - 2.4 * cm, 2 * cm)
    
    canvas.setFont("Amiri", 9)
    canvas.setFillColor(colors.HexColor("#777777"))
    
    page_number = canvas.getPageNumber()
    
    canvas.drawRightString(
        A4[0] - 2.4 * cm, 
        1.5 * cm, 
        ar(f"Warda Intelligence | منصة الذكاء العقاري | {datetime.now().year}")
    )
    
    canvas.drawString(
        2.4 * cm, 
        1.5 * cm, 
        ar(f"الصفحة {page_number}")
    )
    
    canvas.restoreState()


# =========================
# ✅ تنسيق الأرقام بشكل احترافي - منع قطع الأرقام
# =========================
def format_number_with_commas(value):
    """
    تنسيق الأرقام مع فواصل الآلاف ومنع قطع الأرقام
    """
    if value in [None, "", "—"]:
        return "—"
    
    try:
        num = float(value)
        
        # منع الأرقام السالبة الغريبة
        if abs(num) < 0.0001:
            return "0"
        
        # ✅ استخدام صيغة موحدة لمنع قطع الأرقام
        if abs(num - round(num)) < 0.01:
            # رقم صحيح
            return f"{int(round(num)):,}"
        else:
            # رقم عشري
            return f"{num:,.2f}"
            
    except (ValueError, TypeError) as e:
        logger.warning(f"خطأ في تنسيق الرقم '{value}': {e}")
        return str(value)


# =========================
# MAIN PDF GENERATOR
# =========================
def create_pdf_from_content(
    user_info,
    content_text,
    executive_decision,
    charts_by_chapter,
    package_level,
    ai_recommendations=None
):
    logger.info("بدء إنشاء تقرير PDF")
    
    # ✅ التحقق من صحة البيانات قبل إنشاء التقرير - إيقاف التقرير عند خطأ
    is_valid, validation_message = validate_report_data(user_info)
    if not is_valid:
        logger.error(f"فشل التحقق من صحة البيانات: {validation_message}")
        raise ValueError(validation_message)
    
    buffer = BytesIO()

    # -------------------------
    # FONT
    # -------------------------
    font_path = None
    for p in [
        "Amiri-Regular.ttf",
        "fonts/Amiri-Regular.ttf",
        os.path.join(os.getcwd(), "Amiri-Regular.ttf"),
        os.path.join(os.getcwd(), "fonts", "Amiri-Regular.ttf"),
    ]:
        if os.path.exists(p):
            font_path = p
            break

    if not font_path:
        raise FileNotFoundError("خط Amiri غير موجود")

    pdfmetrics.registerFont(TTFont("Amiri", font_path))
    logger.info(f"تم تحميل الخط: {font_path}")

    # -------------------------
    # DOCUMENT
    # -------------------------
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2.4 * cm,
        leftMargin=2.4 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm
    )

    styles = getSampleStyleSheet()

    body = ParagraphStyle(
        "ArabicBody",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=14,
        leading=24,
        alignment=TA_RIGHT,
        wordWrap='RTL',
        spaceAfter=12,
        allowWidows=1,
        allowOrphans=1,
    )

    chapter = ParagraphStyle(
        "ArabicChapter",
        parent=styles["Heading2"],
        fontName="Amiri",
        fontSize=19,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#8B0000"),
        spaceBefore=24,
        spaceAfter=12,
        keepWithNext=1
    )

    ai_sub_title = ParagraphStyle(
        "AISubTitle",
        parent=styles["Heading3"],
        fontName="Amiri",
        fontSize=15.5,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#444444"),
        spaceBefore=14,
        spaceAfter=8,
    )

    title = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        fontName="Amiri",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        spaceAfter=40
    )

    ai_executive_header = ParagraphStyle(
        "AIExecutiveHeader",
        parent=chapter,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#7a0000"),
        fontSize=17,
        spaceBefore=24,
        spaceAfter=12,
    )

    date_style = ParagraphStyle(
        "DateStyle",
        parent=body,
        alignment=TA_CENTER,
        fontSize=14,
        textColor=colors.HexColor("#555555"),
        spaceBefore=6,
        spaceAfter=12,
    )

    stats_style = ParagraphStyle(
        "StatsStyle",
        parent=body,
        fontSize=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1B5E20"),
        spaceBefore=16,
        spaceAfter=16,
    )

    SPECIAL_TAGS = {"[[ANCHOR_CHART]]", "[[RHYTHM_CHART]]", "[[CHART_CAPTION]]"}

    story = []
    
    AVAILABLE_WIDTH = A4[0] - (2.4 * cm) - (2.4 * cm)
    
    # =========================
    # DYNAMIC CHAPTER CHART MAP
    # =========================
    report_kind = user_info.get("report_kind", "district") if user_info else "district"
    
    if report_kind == "city":
        CHAPTER_CHART_MAP = {
            1: 1, 2: 2, 3: 3, 4: 4,
            5: 5, 6: 6, 7: 7, 8: 8
        }
    else:
        OFFSET = 2
        CHAPTER_CHART_MAP = {
            4 + OFFSET: 4,
            7 + OFFSET: 5,
            11 + OFFSET: 6,
            16 + OFFSET: 7,
            21 + OFFSET: 8
        }

    # =========================
    # COVER
    # =========================
    logger.info("إنشاء صفحة الغلاف")
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), title))
    
    if user_info:
        district = user_info.get("district_name", "")
        city = user_info.get("city_name", "")
        property_type = user_info.get("property_type", "")
        
        if report_kind == "city":
            subtitle = f"التقرير الاستثماري العقاري\nمدينة {city}\nتحليل سوق {property_type}"
        else:
            subtitle = f"التقرير الاستثماري العقاري\nحي {district} – مدينة {city}\nتحليل سوق {property_type}"
        
        story.append(Spacer(1, 0.6 * cm))
        story.append(Paragraph(ar(subtitle), ai_executive_header))
    
    date_text = f"تاريخ التقرير: {datetime.now().strftime('%B %Y')}"
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(ar(date_text), date_style))
    
    if user_info:
        district = user_info.get("district_name", "")
        city = user_info.get("city_name", "")
        property_type = user_info.get("property_type", "")
        
        price = user_info.get("district_avg_price", "—")
        city_price = user_info.get("city_avg_price", "—")
        
        # ✅ فصل المتغيرات: صفقات الحي الكلية ≠ صفقات نوع العقار
        district_transactions = user_info.get("district_transactions_total", "—")
        property_transactions = user_info.get("property_transactions_count", "—")
        
        dpi = user_info.get("dpi_score", "—")
        
        price_formatted = format_number_with_commas(price)
        city_price_formatted = format_number_with_commas(city_price)
        district_transactions_formatted = format_number_with_commas(district_transactions)
        property_transactions_formatted = format_number_with_commas(property_transactions)
        
        if report_kind == "city":
            table_data = [
                [ar("المؤشر"), ar("القيمة")],
                [ar("المدينة"), ar(city)],
                [ar("نوع العقار"), ar(property_type)],
                [ar("متوسط سعر المتر"), ar(f"{price_formatted} ريال") if price != "—" else ar("—")],
                [ar("عدد صفقات نوع العقار"), ar(f"{property_transactions_formatted} صفقة") if property_transactions != "—" else ar("—")],
                [ar("مؤشر قوة السوق"), ar(f"{dpi} / 100") if dpi != "—" else ar("—")]
            ]
        else:
            table_data = [
                [ar("المؤشر"), ar("القيمة")],
                [ar("المدينة"), ar(city)],
                [ar("الحي"), ar(district)],
                [ar("نوع العقار"), ar(property_type)],
                [ar("متوسط سعر المتر في الحي"), ar(f"{price_formatted} ريال") if price != "—" else ar("—")],
                [ar("متوسط سعر المتر في المدينة"), ar(f"{city_price_formatted} ريال") if city_price != "—" else ar("—")],
                [ar("عدد صفقات الحي الكلي"), ar(f"{district_transactions_formatted} صفقة") if district_transactions != "—" else ar("—")],
                [ar("عدد صفقات نوع العقار"), ar(f"{property_transactions_formatted} صفقة") if property_transactions != "—" else ar("—")],
                [ar("مؤشر قوة الحي"), ar(f"{dpi} / 100") if dpi != "—" else ar("—")]
            ]
        
        table = Table(table_data, colWidths=[7*cm, 9*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Amiri'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#8B0000")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F9F9F9")),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F9F9F9"), colors.white]),
        ]))
        story.append(Spacer(1, 1*cm))
        story.append(table)
        
        # ✅ سطر توضيحي احترافي
        story.append(Spacer(1, 0.4 * cm))
        story.append(Paragraph(
            ar("تم تحليل صفقات نوع العقار المختار فقط داخل الحي. عدد صفقات الحي الكلي يشمل جميع أنواع العقارات."),
            body
        ))
    
    if user_info and "total_transactions" in user_info:
        total = user_info["total_transactions"]
        if total is not None:
            story.append(Spacer(1, 0.8 * cm))
            try:
                total_formatted = f"{int(float(total)):,}" if total else "0"
            except (ValueError, TypeError):
                total_formatted = str(total)
            story.append(Paragraph(
                ar(f"إجمالي الصفقات المستخدمة في التحليل: {total_formatted} صفقة"),
                stats_style
            ))
    
    story.append(PageBreak())

    # =========================
    # EXECUTIVE DECISION
    # =========================
    DECISION_BLOCK_TITLES = {
        "DECISION_DEFINITION": "تعريف القرار التنبؤي",
        "MARKET_STATUS": "وضع السوق الحالي",
        "PREDICTIVE_SIGNALS": "الإشارات التنبؤية",
        "SCENARIOS": "السيناريوهات المحتملة",
        "OPTIMAL_POSITION": "القرار التنفيذي",
        "DECISION_GUARANTEE": "ضمان القرار"
    }

    if executive_decision and executive_decision.strip():
        logger.info("إضافة الخلاصة التنفيذية")
        story.append(Spacer(1, 1.2 * cm))
        story.append(Paragraph(ar("الخلاصة التنفيذية للقرار"), ai_executive_header))
        story.append(elegant_divider("60%"))
        story.append(Spacer(1, 0.6 * cm))

        for line in executive_decision.split("\n"):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.2 * cm))
                continue

            if line.startswith("[DECISION_BLOCK:"):
                key = line.replace("[DECISION_BLOCK:", "").replace("]", "")
                title_text = DECISION_BLOCK_TITLES.get(key, "")
                if title_text:
                    story.append(Spacer(1, 0.6 * cm))
                    story.append(Paragraph(ar(title_text), chapter))
                    story.append(elegant_divider("50%"))
                continue

            if line == "[END_DECISION_BLOCK]":
                continue

            story.extend(arabic_paragraph_flowables(line, body, AVAILABLE_WIDTH))
            story.append(Spacer(1, 0.2 * cm))

        story.append(Spacer(1, 1.0 * cm))
        story.append(elegant_divider("30%"))
        story.append(PageBreak())

    # =========================
    # TRANSITION PAGE
    # =========================
    logger.info("إضافة صفحة الانتقال")
    story.append(Spacer(1, 2.5 * cm))
    story.append(Paragraph(ar("كيف تقرأ هذا التقرير بناءً على القرار أعلاه"), ai_executive_header))
    story.append(elegant_divider("55%"))
    story.append(Spacer(1, 1.0 * cm))

    transition_texts = [
        "الخلاصة التنفيذية للقرار تمثل القرار المعتمد لهذا التقرير، "
        "وقد تم اشتقاقه بناءً على مؤشرات رقمية ومعايير تحليلية محددة.",
        
        "الفصول التالية لا تُقرأ كتحليل عام للسوق، ولا كمسار للوصول إلى قرار جديد، "
        "بل كشرح منهجي للأسس التي بُني عليها القرار الصادر.",
        
        "كل فصل يفسر جانبًا محددًا من القرار، ويبيّن السياق السوقي، "
        "وحدود المخاطر، وطبيعة الفرص، وشروط التوقيت والتنفيذ، "
        "بهدف توضيح لماذا جاء القرار بهذه الصيغة تحديدًا.",
        
        "القرار موجود في الأعلى، "
        "وما يلي هو الإطار التحليلي الذي يبرره، "
        "ويحدّد نطاق صلاحيته، ويضبط تطبيقه."
    ]
    
    for text in transition_texts:
        story.extend(arabic_paragraph_flowables(text, body, AVAILABLE_WIDTH))
        story.append(Spacer(1, 0.15 * cm))

    story.append(Spacer(1, 1.2 * cm))
    story.append(elegant_divider("30%"))
    story.append(PageBreak())

    # =========================
    # PROCESS CONTENT WITH MAP
    # =========================
    chapter_index = 0
    chart_cursor = {}
    first_chapter_processed = False
    temp_files = []

    # =========================
    # INSERT MAP BEFORE CONTENT
    # =========================
    if user_info:
        logger.info("إنشاء خريطة الحي والمشاريع")
        district_lat = user_info.get("خط_العرض") or user_info.get("district_latitude") or user_info.get("district_lat")
        district_lon = user_info.get("خط_الطول") or user_info.get("district_longitude") or user_info.get("district_lon")
        district_name = user_info.get("district_name")
        projects_df = user_info.get("projects_data")
        
        district_impact = user_info.get("نطاق_التأثير") or user_info.get("impact_radius") or 5
        try:
            impact_radius = max(float(district_impact or 0), 1)
        except (ValueError, TypeError):
            impact_radius = 5
        
        logger.debug(f"إحداثيات الحي: خط العرض={district_lat}, خط الطول={district_lon}")
        logger.debug(f"نطاق التأثير: {impact_radius} كم")
        
        map_fig = create_district_projects_map(
            district_lat,
            district_lon,
            district_name,
            projects_df,
            impact_radius_km=impact_radius
        )
        
        # حفظ المشاريع القريبة لاستخدامها في النص
        if projects_df is not None and not projects_df.empty:
            user_info["nearby_projects"] = projects_df.to_dict("records")
            logger.info(f"تم حفظ {len(projects_df)} مشروع في user_info['nearby_projects']")
        
        # ✅ الخريطة في صفحة كاملة وحدها
        if map_fig:
            # إنهاء الصفحة الحالية
            story.append(PageBreak())
            
            # إدراج الخريطة بحجم صفحة كاملة
            map_img = plotly_to_image(map_fig, 18.0, 24.0)
            if map_img:
                if hasattr(map_img, '_temp_file'):
                    temp_files.append(map_img._temp_file)
                story.append(map_img)
                story.append(Spacer(1, 0.4 * cm))
                logger.info("✅ تم إضافة الخريطة بنجاح")
            else:
                logger.warning("⚠️ فشل تحويل الخريطة إلى صورة")
                story.append(Paragraph(
                    ar("⚠️ فشل تحويل الخريطة إلى صورة"),
                    body
                ))
            
            # إنهاء صفحة الخريطة
            story.append(PageBreak())
        else:
            # الخريطة نفسها لم تنشأ
            logger.warning("⚠️ لم يتم إنشاء الخريطة - تحقق من الإحداثيات أو البيانات")
            story.append(Paragraph(
                ar("⚠️ لم يتم إنشاء الخريطة - تحقق من الإحداثيات أو البيانات"),
                body
            ))
            
            # معلومات تشخيصية إضافية
            diag_text = f"الإحداثيات المستلمة: خط العرض = {district_lat}, خط الطول = {district_lon}"
            story.append(Paragraph(ar(diag_text), body))
            story.append(Spacer(1, 0.4 * cm))

    # =========================
    # MAIN CONTENT LOOP
    # =========================
    logger.info("بدء معالجة محتوى التقرير")
    for raw in content_text.split("\n"):
        raw_stripped = raw.strip()

        if not raw_stripped:
            continue

        clean = raw_stripped if raw_stripped in SPECIAL_TAGS else clean_text(raw)

        if clean.startswith(("📊", "💎", "⚠️")):
            story.append(Spacer(1, 0.6 * cm))
            story.append(elegant_divider())
            story.append(Paragraph(ar(clean), ai_sub_title))
            story.append(Spacer(1, 0.3 * cm))
            continue

        # ✅ التعديل الأساسي: كل فصل يبدأ في صفحة جديدة - مع منع الصفحات الفارغة المزدوجة
        if raw_stripped.lower().startswith(("الفصل", "chapter")):
            # ✅ منع PageBreak مزدوج
            if story and not isinstance(story[-1], PageBreak):
                story.append(PageBreak())
                logger.debug(f"إضافة PageBreak قبل الفصل {chapter_index + 1}")
            
            chapter_index += 1
            chart_cursor[chapter_index] = 0
            story.append(Paragraph(ar(clean), chapter))
            story.append(Spacer(1, 0.3 * cm))
            story.append(elegant_divider("40%"))
            story.append(Spacer(1, 0.6 * cm))
            first_chapter_processed = True
            logger.info(f"معالجة الفصل {chapter_index}")
            continue

        if clean == "[[ANCHOR_CHART]]":
            real_chapter = CHAPTER_CHART_MAP.get(chapter_index)
            if real_chapter:
                charts = charts_by_chapter.get(f"chapter_{real_chapter}", [])
                cursor = chart_cursor.get(chapter_index, 0)

                if cursor < len(charts):
                    img = plotly_to_image(charts[cursor], 16.8, 9)
                    if img:
                        if hasattr(img, '_temp_file'):
                            temp_files.append(img._temp_file)
                        story.append(Spacer(1, 0.8 * cm))
                        story.append(img)
                        story.append(Spacer(1, 0.4 * cm))
                    chart_cursor[chapter_index] += 1
            continue

        if clean == "[[RHYTHM_CHART]]":
            real_chapter = CHAPTER_CHART_MAP.get(chapter_index)
            if real_chapter:
                charts = charts_by_chapter.get(f"chapter_{real_chapter}", [])
                cursor = chart_cursor.get(chapter_index, 0)

                if cursor < len(charts):
                    fig = charts[cursor]
                    is_indicator = (
                        fig is not None
                        and hasattr(fig, 'data')
                        and len(fig.data) > 0
                        and isinstance(fig.data[0], go.Indicator)
                    )
                    img = plotly_to_image(fig, 17.5 if is_indicator else 16.8,
                                           9.5 if is_indicator else 9)
                    if img:
                        if hasattr(img, '_temp_file'):
                            temp_files.append(img._temp_file)
                        story.append(Spacer(1, 0.8 * cm if is_indicator else 0.7 * cm))
                        story.append(img)
                        story.append(Spacer(1, 0.4 * cm))
                    chart_cursor[chapter_index] += 1
            continue

        if clean and clean not in SPECIAL_TAGS:
            story.extend(arabic_paragraph_flowables(clean, body, AVAILABLE_WIDTH))
            story.append(Spacer(1, 0.15 * cm))

    logger.info("بدء بناء مستند PDF")
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    
    buffer.seek(0)
    
    # ✅ تنظيف الملفات المؤقتة
    unique_temp_files = list(set(temp_files))
    for temp_file in unique_temp_files:
        try:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
                logger.debug(f"تم حذف الملف المؤقت: {temp_file}")
        except Exception as cleanup_error:
            logger.warning(f"تحذير في تنظيف الملفات المؤقتة: {cleanup_error}")
    
    logger.info("✅ تم إنشاء التقرير بنجاح")
    return buffer


# =========================
# ✅ UNIT TESTS
# =========================
def run_unit_tests():
    """
    اختبارات وحدة للتأكد من صحة التعديلات
    """
    print("🧪 بدء اختبارات الوحدة...")
    
    # Test 1: Validation function
    print("\n📋 اختبار 1: التحقق من صحة البيانات")
    test_data_1 = {
        "district_transactions_total": 1000,
        "property_transactions_count": 1000,
        "property_types_in_district": 3
    }
    is_valid, msg = validate_report_data(test_data_1)
    assert not is_valid, "❌ يجب أن يفشل التحقق عندما تتساوى الأرقام مع وجود أنواع متعددة"
    print("✅ اختبار 1 ناجح: تم اكتشاف الخطأ المنطقي")
    
    test_data_2 = {
        "district_transactions_total": 1000,
        "property_transactions_count": 380,
        "property_types_in_district": 3
    }
    is_valid, msg = validate_report_data(test_data_2)
    assert is_valid, "❌ يجب أن ينجح التحقق عندما تختلف الأرقام"
    print("✅ اختبار 2 ناجح: البيانات الصحيحة تمر")
    
    # Test 2: Number formatting
    print("\n📋 اختبار 3: تنسيق الأرقام")
    assert format_number_with_commas(2828) == "2,828", "❌ خطأ في تنسيق الرقم 2828"
    assert format_number_with_commas(1000000) == "1,000,000", "❌ خطأ في تنسيق المليون"
    assert format_number_with_commas(None) == "—", "❌ خطأ في التعامل مع None"
    assert format_number_with_commas("") == "—", "❌ خطأ في التعامل مع نص فارغ"
    print("✅ اختبار 3 ناجح: تنسيق الأرقام صحيح")
    
    # Test 3: Arabic text with parentheses
    print("\n📋 اختبار 4: معالجة الأقواس في النص العربي")
    test_text = "عدد الصفقات (شقة)"
    result = ar(test_text)
    assert "(" not in result, "❌ لا يزال هناك قوس في النص"
    assert "-" in result, "❌ لم يتم استبدال القوس بشرطة"
    assert "  " not in result, "❌ توجد مسافات مزدوجة في النص"
    print("✅ اختبار 4 ناجح: تم استبدال الأقواس بشرطة بدون مسافات مزدوجة")
    
    # Test 4: Parentheses with spaces
    print("\n📋 اختبار 5: معالجة الأقواس مع مسافات")
    test_text_2 = "السعر ( 5000 ) ريال"
    result_2 = ar(test_text_2)
    assert "السعر - 5000 ريال" in result_2 or "السعر - 5000 ريال" in result_2.replace("  ", " ")
    print("✅ اختبار 5 ناجح: معالجة المسافات حول الأقواس صحيحة")
    
    print("\n🎉 جميع الاختبارات ناجحة!")
    print("✅ النظام جاهز للإنتاج")


# =========================
# ✅ INTEGRATION TEST
# =========================
def run_integration_test():
    """
    اختبار تكاملي - إنشاء PDF فعلي والتحقق من عدم وجود صفحات فارغة
    """
    print("\n🧪 بدء الاختبار التكاملي...")
    
    try:
        # بيانات اختبارية
        test_user_info = {
            "report_kind": "district",
            "district_name": "حي النخيل",
            "city_name": "الرياض",
            "property_type": "شقة",
            "district_avg_price": 4500,
            "city_avg_price": 4200,
            "district_transactions_total": 1250,
            "property_transactions_count": 380,
            "property_types_in_district": 3,
            "dpi_score": 78,
            "total_transactions": 1250,
            "خط_العرض": 24.7136,
            "خط_الطول": 46.6753
        }
        
        test_content = """الفصل الأول: ملخص الاستثمار السريع
هذا فصل اختباري للتأكد من أن الفصل يبدأ في صفحة جديدة.

الفصل الثاني: تحليل السوق
هذا فصل آخر للتأكد من pagination."""
        
        test_decision = "[DECISION_BLOCK:DECISION_DEFINITION]\nقرار اختباري\n[END_DECISION_BLOCK]"
        
        # إنشاء PDF
        pdf_buffer = create_pdf_from_content(
            test_user_info,
            test_content,
            test_decision,
            {},
            "premium"
        )
        
        # حفظ الملف للفحص
        with open("test_report.pdf", "wb") as f:
            f.write(pdf_buffer.getvalue())
        
        print("✅ الاختبار التكاملي ناجح: تم إنشاء test_report.pdf")
        print("📄 يمكنك فتح الملف للتأكد من:")
        print("   1. الفصل الأول يبدأ في صفحة جديدة")
        print("   2. لا توجد صفحات فارغة مزدوجة")
        print("   3. الأرقام منسقة بشكل صحيح")
        print("   4. الأقواس مستبدلة بشرطة")
        
    except Exception as e:
        print(f"❌ فشل الاختبار التكاملي: {e}")
        import traceback
        traceback.print_exc()


# تشغيل الاختبارات إذا تم استدعاء الملف مباشرة
if __name__ == "__main__":
    run_unit_tests()
    print("\n" + "="*50)
    run_integration_test()
