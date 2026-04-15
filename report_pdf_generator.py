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
        # ✅ التعديل 2: إصلاح الأرقام - إضافة مسافة نهاية لمنع انكسار الأرقام  
        width = stringWidth(bidi_text + " ", style.fontName, style.fontSize)  
          
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
# Arabic helper - استبدال الأقواس بشرطة (حل نهائي لمشكلة RTL)  
# =========================  
def ar(text):  
    if not text:  
        return ""  
  
    try:  
        text = str(text)  
        # ✅ استبدال الأقواس بشرطة (بدل محاولة إصلاحها المعقدة)  
        text = text.replace("(", " - ")  
        text = text.replace(")", "")  
        text = text.replace(" - ", " - ")  # تحسين احترافي لمنع المسافات الزائدة  
        # ✅ تنظيف المسافات  
        text = re.sub(r"\s+", " ", text)  
        # ✅ إصلاح علامة النسبة المئوية  
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
    # DOCUMENT - هوامش متساوية لاتجاه RTL  
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
        splitLongWords=False,  # ✅ منع انكسار السطر داخل الأرقام  
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
        keepWithNext=1,  
        splitLongWords=False,  
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
        splitLongWords=False,  
    )  
  
    title = ParagraphStyle(  
        "ArabicTitle",  
        parent=styles["Title"],  
        fontName="Amiri",  
        fontSize=22,  
        alignment=TA_CENTER,  
        textColor=colors.HexColor("#7a0000"),  
        spaceAfter=40,  
        splitLongWords=False,  
    )  
  
    ai_executive_header = ParagraphStyle(  
        "AIExecutiveHeader",  
        parent=chapter,  
        alignment=TA_CENTER,  
        textColor=colors.HexColor("#7a0000"),  
        fontSize=17,  
        spaceBefore=24,  
        spaceAfter=12,  
        splitLongWords=False,  
    )  
  
    date_style = ParagraphStyle(  
        "DateStyle",  
        parent=body,  
        alignment=TA_CENTER,  
        fontSize=14,  
        textColor=colors.HexColor("#555555"),  
        spaceBefore=6,  
        spaceAfter=12,  
        splitLongWords=False,  
    )  
  
    stats_style = ParagraphStyle(  
        "StatsStyle",  
        parent=body,  
        fontSize=16,  
        alignment=TA_CENTER,  
        textColor=colors.HexColor("#1B5E20"),  
        spaceBefore=16,  
        spaceAfter=16,  
        splitLongWords=False,  
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
          
        # ✅ تنسيق السعر بشكل صحيح مع الفواصل - إصلاح الأرقام المكسورة  
        def format_number_with_commas(value):  
            if value == "—" or value is None:  
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
                [ar("عدد صفقات نوع العقار"), ar(f"{transactions_formatted} صفقة") if transactions != "—" else ar("—")],  
                [ar("مؤشر قوة السوق - DPI"), ar(f"{dpi} / 100") if dpi != "—" else ar("—")]  
            ]  
              
            # ✅ إضافة إجمالي صفقات الحي  
            total_transactions = user_info.get("total_transactions")  
            if total_transactions is not None and total_transactions != "—":  
                total_formatted = format_number_with_commas(total_transactions)  
                table_data.append([ar("إجمالي صفقات المدينة"), ar(f"{total_formatted} صفقة")])  
        else:  
            table_data = [  
                [ar("المؤشر"), ar("القيمة")],  
                [ar("المدينة"), ar(city)],  
                [ar("الحي"), ar(district)],  
                [ar("نوع العقار"), ar(property_type)],  
                [ar("متوسط سعر المتر"), ar(f"{price_formatted} ريال") if price != "—" else ar("—")],  
                [ar("متوسط المدينة"), ar(f"{city_price_formatted} ريال") if city_price != "—" else ar("—")],  
                [ar("عدد صفقات نوع العقار"), ar(f"{transactions_formatted} صفقة") if transactions != "—" else ar("—")],  
                [ar("مؤشر قوة الحي - DPI"), ar(f"{dpi} / 100") if dpi != "—" else ar("—")]  
            ]  
              
            # ✅ إضافة إجمالي صفقات الحي  
            total_transactions = user_info.get("total_transactions")  
            if total_transactions is not None and total_transactions != "—":  
                total_formatted = format_number_with_commas(total_transactions)  
                table_data.append([ar("إجمالي صفقات الحي"), ar(f"{total_formatted} صفقة")])  
          
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
        district_lat = user_info.get("خط_العرض") or user_info.get("district_latitude") or user_info.get("district_lat")  
        district_lon = user_info.get("خط_الطول") or user_info.get("district_longitude") or user_info.get("district_lon")  
        district_name = user_info.get("district_name")  
        projects_df = user_info.get("projects_data")  
          
        district_impact = user_info.get("نطاق_التأثير") or user_info.get("impact_radius") or 5  
        try:  
            impact_radius = max(float(district_impact or 0), 1)  
        except (ValueError, TypeError):  
            impact_radius = 5  
          
        print(f"DEBUG: district_lat={district_lat}, district_lon={district_lon}")  
        print(f"DEBUG: impact_radius={impact_radius}")  
          
        map_fig = create_district_projects_map(  
            district_lat,  
            district_lon,  
            district_name,  
            projects_df,  
            impact_radius_km=impact_radius  
        )  
          
        # ✅ هذا هو التعديل الحاسم: حفظ المشاريع القريبة لاستخدامها في النص  
        if projects_df is not None and not projects_df.empty:  
            user_info["nearby_projects"] = projects_df.to_dict("records")  
            print(f"DEBUG: تم حفظ {len(projects_df)} مشروع في user_info['nearby_projects']")  
          
        # =========================================================  
        # ✅ الخريطة في صفحة كاملة وحدها  
        # =========================================================  
        if map_fig:  
            # إدراج الخريطة بحجم صفحة كاملة  
            map_img = plotly_to_image(map_fig, 18.0, 24.0)  
            if map_img:  
                if hasattr(map_img, '_temp_file'):  
                    temp_files.append(map_img._temp_file)  
                story.append(map_img)  
                story.append(Spacer(1, 0.4 * cm))  
            else:  
                story.append(Paragraph(  
                    ar("⚠️ فشل تحويل الخريطة إلى صورة"),  
                    body  
                ))  
              
            # ✅ التعديل 3: حذف الصفحة الفارغة - إضافة PageBreak فقط إذا كان هناك محتوى بعدها  
            if content_text.strip():  
                story.append(PageBreak())  
        else:  
            # الخريطة نفسها لم تنشأ (map_fig = None)  
            story.append(Paragraph(  
                ar("⚠️ لم يتم إنشاء الخريطة - تحقق من الإحداثيات أو البيانات"),  
                body  
            ))  
              
            # معلومات تشخيصية إضافية  
            diag_text = f"الإحداثيات المستلمة: خط العرض = {district_lat}, خط الطول = {district_lon}"  
            story.append(Paragraph(ar(diag_text), body))  
            story.append(Spacer(1, 0.4 * cm))  
              
            # ✅ التعديل 3: حذف الصفحة الفارغة - إضافة PageBreak فقط إذا كان هناك محتوى بعدها  
            if content_text.strip():  
                story.append(PageBreak())  
  
    # =========================  
    # MAIN CONTENT LOOP  
    # =========================  
    for raw in content_text.split("\n"):  
        raw_stripped = raw.strip()  
  
        if not raw_stripped:  
            continue  
  
        # ✅ التعديل 1: إصلاح الأقواس - تمرير النص عبر ar() بعد clean_text  
        clean = raw_stripped if raw_stripped in SPECIAL_TAGS else ar(clean_text(raw))  
  
        if clean.startswith(("📊", "💎", "⚠️")):  
            story.append(Spacer(1, 0.6 * cm))  
            story.append(elegant_divider())  
            story.append(Paragraph(ar(clean), ai_sub_title))  
            story.append(Spacer(1, 0.3 * cm))  
            continue  
  
        if raw_stripped.startswith("الفصل"):  
            # ✅ إصلاح الصفحة الفارغة: أول فصل يبدأ مباشرة بدون صفحة فارغة  
            if first_chapter_processed:  
                story.append(PageBreak())  
            first_chapter_processed = True  
            chapter_index += 1  
            chart_cursor[chapter_index] = 0  
            story.append(Paragraph(ar(clean), chapter))  
            story.append(Spacer(1, 0.3 * cm))  
            story.append(elegant_divider("40%"))  
            story.append(Spacer(1, 0.6 * cm))  
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
  
    # ✅ منع الصفحة الفارغة الأخيرة  
    while story and isinstance(story[-1], PageBreak):  
        story.pop()  
  
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)  
      
    buffer.seek(0)  
      
    # ✅ تنظيف الملفات المؤقتة مع حماية إضافية  
    unique_temp_files = list(set(temp_files))  
    for temp_file in unique_temp_files:  
        try:  
            if temp_file and os.path.exists(temp_file):  
                os.remove(temp_file)  
        except Exception as cleanup_error:  
            print("Temp cleanup warning:", cleanup_error)  
      
    return buffer
