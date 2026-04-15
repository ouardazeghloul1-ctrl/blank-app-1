# report_pdf_generator.py
from io import BytesIO
import os
import tempfile
import re
import unicodedata
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
        # ✅ إزالة الأقواس المعكوسة نهائيًا
        text = text.replace("(", "")
        text = text.replace(")", "")
        text = text.replace("% ", "%")
        text = text.replace(" %", "%")
        text = re.sub(r'(-?\d+(\.\d+)?)\s*%', r'\1%', text)

        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
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
        print("Chart export error:", e)
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
            print("Map: missing district coordinates")
            return None
        
        # ✅ التعديل الاحترافي: التعامل مع حالة عدم وجود مشاريع
        if projects_df is None:
            print("Map: no projects data, creating empty DataFrame")
            projects_df = pd.DataFrame()
        
        # =========================================================
        # ✅ التعديل 1: إعادة تسمية عمود اسم المشروع إذا كان بالصيغة العربية
        # =========================================================
        if not projects_df.empty and "اسم_المشروع" not in projects_df.columns:
            if "اسم المشروع بالعربية" in projects_df.columns:
                projects_df = projects_df.rename(columns={"اسم المشروع بالعربية": "اسم_المشروع"})
                print("✅ Map: تم إعادة تسمية العمود 'اسم المشروع بالعربية' → 'اسم_المشروع'")
        
        required_columns = ["خط_العرض", "خط_الطول", "اسم_المشروع"]
        for col in required_columns:
            if not projects_df.empty and col not in projects_df.columns:
                print(f"Map: missing column '{col}' in projects_df")
                return None
        
        # =========================
        # ✅ تحويل الإحداثيات إلى أرقام (حل نهائي)
        # =========================
        if not projects_df.empty:
            projects_df["خط_العرض"] = pd.to_numeric(projects_df["خط_العرض"], errors="coerce")
            projects_df["خط_الطول"] = pd.to_numeric(projects_df["خط_الطول"], errors="coerce")
            
            # إزالة الصفوف غير الصالحة
            projects_df = projects_df.dropna(subset=["خط_العرض", "خط_الطول"])
        
        print("DEBUG dtype latitude:", projects_df["خط_العرض"].dtype if not projects_df.empty else "empty")
        print("DEBUG dtype longitude:", projects_df["خط_الطول"].dtype if not projects_df.empty else "empty")
        print(f"DEBUG district_lat type: {type(district_lat)}, value: {district_lat}")
        print(f"DEBUG district_lon type: {type(district_lon)}, value: {district_lon}")
        
        # تحويل إحداثيات الحي إلى float أيضاً
        district_lat = float(district_lat)
        district_lon = float(district_lon)
        
        # =========================================================
        # ✅ التعديل النهائي: احترام نطاق البحث الذي يختاره المستخدم
        # =========================================================
        # نضمن فقط حدًا أدنى منطقيًا (1 كم) لمنع الأخطاء
        radius_km = max(float(impact_radius_km), 1)
        radius_deg = radius_km / 111
        
        print(f"DEBUG radius_km: {radius_km}")
        print(f"DEBUG radius_deg: {radius_deg}")
        print(f"DEBUG district_lat: {district_lat}, district_lon: {district_lon}")
        
        # فلترة المشاريع القريبة (إذا كان هناك مشاريع)
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
        
        print(f"Map: found {len(nearby_projects)} nearby projects within {radius_km} km")
        
        fig = go.Figure()
        
        # دبوس الحي (يتم رسمه دائماً)
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
        
        # دبابيس المشاريع (إذا وجدت)
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
        
        # =========================================================
        # ✅ التعديل 3: تغيير mapbox_style من open-street-map إلى carto-positron
        # =========================================================
        title_text = f"موقع حي {district_name}"
        if not nearby_projects.empty:
            title_text += f" والمشاريع القريبة (نطاق {radius_km} كم)"
        
        fig.update_layout(
            mapbox_style="carto-positron",  # حل مشكلة Access blocked – Referrer is required
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
        print(f"Map error: {e}")
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
        raise FileNotFoundError("Amiri font not found")

    pdfmetrics.registerFont(TTFont("Amiri", font_path))

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
        # ✅ التعديل النهائي: إزالة OFFSET نهائيًا (لم نعد نستخدم فصلين إضافيين)
        CHAPTER_CHART_MAP = {
            4: 4,
            7: 5,
            11: 6,
            16: 7,
            21: 8
        }

    # =========================
    # COVER
    # =========================
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph(ar("تقرير وردة للذكاء العقاري"), title))
    
    if user_info:
        district = user_info.get("district_name", "")
        city = user_info.get("city_name", "")
        # ✅ التعديل: تنظيف property_type لمنع None أو فراغ
        property_type = str(user_info.get("property_type", "عقار")).strip()
        if not property_type:
            property_type = "عقار"
        
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
        property_type = str(user_info.get("property_type", "عقار")).strip()
        if not property_type:
            property_type = "عقار"
        
        price = user_info.get("district_avg_price", "—")
        city_price = user_info.get("city_avg_price", "—")
        transactions = user_info.get("transactions_count", "—")
        dpi = user_info.get("dpi_score", "—")
        
        # ✅ تنسيق السعر بشكل صحيح مع الفواصل
        def format_number_with_commas(value):
            if value == "—":
                return "—"
            try:
                num = float(value)
                if abs(num - round(num)) < 0.01:
                    return f"{int(round(num)):,}"
                else:
                    return f"{num:,.2f}"
            except (ValueError, TypeError):
                return str(value)
        
        price_formatted = format_number_with_commas(price)
        city_price_formatted = format_number_with_commas(city_price)
        transactions_formatted = format_number_with_commas(transactions)
        
        if report_kind == "city":
            table_data = [
                [ar("المؤشر"), ar("القيمة")],
                [ar("المدينة"), ar(city)],
                [ar("نوع العقار"), ar(property_type)],
                [ar("متوسط سعر المتر"), ar(f"{price_formatted} ريال") if price != "—" else ar("—")],
                [ar("عدد صفقات الحي"), ar(f"{transactions_formatted} صفقة") if transactions != "—" else ar("—")],
                [ar("مؤشر قوة السوق"), ar(f"{dpi} / 100") if dpi != "—" else ar("—")]
            ]
        else:
            table_data = [
                [ar("المؤشر"), ar("القيمة")],
                [ar("المدينة"), ar(city)],
                [ar("الحي"), ar(district)],
                [ar("نوع العقار"), ar(property_type)],
                [ar("متوسط سعر المتر"), ar(f"{price_formatted} ريال") if price != "—" else ar("—")],
                [ar("متوسط المدينة"), ar(f"{city_price_formatted} ريال") if city_price != "—" else ar("—")],
                [ar("عدد صفقات الحي"), ar(f"{transactions_formatted} صفقة") if transactions != "—" else ar("—")],
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
        
        # ✅ إضافة سطر توضيحي احترافي في الغلاف
        story.append(Spacer(1, 0.4 * cm))
        story.append(Paragraph(
            ar("تم تحليل صفقات نوع العقار المختار فقط داخل الحي."),
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
                key = line.repl
