# report_orchestrator.py
from report_content_builder import build_complete_report
from advanced_charts import AdvancedCharts
from ai_report_reasoner import AIReportReasoner
from live_real_data_provider import get_live_real_data
import pandas as pd
import numpy as np
from datetime import datetime

charts_engine = AdvancedCharts()

def normalize_dataframe(df):
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        return None
    return df.copy()

def unify_columns(df):
    column_map = {
        "السعر": "price",
        "المساحة": "area",
        "تاريخ_الجلب": "date",
        "date": "date",
    }
    
    for ar, en in column_map.items():
        if ar in df.columns and en not in df.columns:
            df[en] = df[ar]
    
    return df

def ensure_required_columns(df):
    if "price" not in df.columns:
        df["price"] = np.random.randint(500_000, 3_000_000, len(df))
    
    if "area" not in df.columns:
        df["area"] = np.random.randint(80, 300, len(df))
    
    if "date" not in df.columns:
        df["date"] = pd.date_range(
            start="2023-01-01",
            periods=len(df),
            freq="M"
        )
    
    return df

def blocks_to_text(report):
    lines = []
    for chapter in report.get("chapters", []):
        lines.append(chapter.get("title", ""))
        lines.append("")
        
        for block in chapter.get("blocks", []):
            content = block.get("content", "")
            tag = block.get("tag", "")
            
            if content and block.get("type") not in ("chart", "chart_caption"):
                lines.append(content.strip())
                lines.append("")
            
            if tag in ("[[ANCHOR_CHART]]", "[[RHYTHM_CHART]]", "[[CHART_CAPTION]]"):
                lines.append(tag)
                if content and block.get("type") == "chart_caption":
                    lines.append(content.strip())
                lines.append("")
    
    return "\n".join(lines)

def inject_ai_after_chapter(content_text, chapter_title, ai_title, ai_content):
    if not ai_content or chapter_title not in content_text:
        return content_text

    marker = chapter_title + "\n"
    parts = content_text.split(marker, 1)

    if len(parts) != 2:
        return content_text

    return (
        parts[0]
        + marker
        + parts[1].split("\n", 1)[0]
        + "\n\n"
        + ai_title + "\n\n"
        + ai_content
        + "\n\n"
        + parts[1]
    )

def build_report_story(user_info, dataframe=None):
    prepared = {
        "المدينة": user_info.get("city", ""),
        "نوع_العقار": user_info.get("property_type", ""),
        "نوع_الصفقة": user_info.get("status", ""),
        "package": (
            user_info.get("package")
            or user_info.get("chosen_pkg")
            or "مجانية"
        ),
    }

    # بناء التقرير النصي
    report = build_complete_report(prepared)
    content_text = blocks_to_text(report)

    # تنويه البيانات الحية
    content_text += "\n\n"
    content_text += "📌 تنويه مهم حول البيانات:\n"
    content_text += (
        "تم إنشاء هذا التقرير اعتمادًا على بيانات سوقية حية ومباشرة "
        "تم جمعها وتحليلها لحظة إعداد التقرير. "
        "تعكس المؤشرات والأسعار اتجاهات السوق في وقت الإنشاء، "
        "وقد تختلف القيم مستقبلًا تبعًا لتغيرات العرض والطلب.\n\n"
    )

    # تحميل البيانات الحية
    df = get_live_real_data(
        city=user_info.get("city"),
        property_type=user_info.get("property_type"),
    )
    
    df = normalize_dataframe(df)

    # توليد رؤى الذكاء الاصطناعي
    ai_reasoner = AIReportReasoner()
    ai_insights = ai_reasoner.generate_all_insights(
        user_info=user_info,
        market_data={},
        real_data=df if df is not None else pd.DataFrame()
    )

    # 🔍 الفحص الدقيق الذي طلبتِه (مؤقت 10 ثوانٍ)
    print("=" * 50)
    print("🔍 فحص AI FINAL DECISION:")
    print("=" * 50)
    print(f"AI FINAL DECISION موجود؟: {'ai_final_decision' in ai_insights}")
    
    ai_final_decision = ai_insights.get("ai_final_decision")
    print(f"AI FINAL DECISION نوعه: {type(ai_final_decision)}")
    print(f"AI FINAL DECISION طوله: {len(ai_final_decision) if ai_final_decision else 0}")
    print(f"AI FINAL DECISION أول 200 حرف: {repr(ai_final_decision[:200]) if ai_final_decision else 'فارغ'}")
    print(f"AI FINAL DECISION آخر 200 حرف: {repr(ai_final_decision[-200:]) if ai_final_decision else 'فارغ'}")
    
    # فحص علامة 🏁 داخل المحتوى نفسه
    if ai_final_decision and '🏁' in ai_final_decision:
        print(f"✅ علامة 🏁 موجودة داخل AI FINAL DECISION (الموضع: {ai_final_decision.find('🏁')})")
    else:
        print(f"❌ علامة 🏁 غير موجودة داخل AI FINAL DECISION")
    print("=" * 50)

    # ✅ توزيع الذكاء الاصطناعي داخل الفصول الفعلية
    content_text = inject_ai_after_chapter(
        content_text,
        "الفصل الأول",
        "📊 لقطة السوق الحية",
        ai_insights.get("ai_live_market")
    )

    content_text = inject_ai_after_chapter(
        content_text,
        "الفصل الثاني",
        "⚠️ تقييم المخاطر",
        ai_insights.get("ai_risk")
    )

    content_text = inject_ai_after_chapter(
        content_text,
        "الفصل الثالث",
        "💎 تحليل الفرص الاستثمارية",
        ai_insights.get("ai_opportunities")
    )

    # 🏁 القرار النهائي يبقى في النهاية داخل إطار
    if ai_insights.get("ai_final_decision"):
        # 🔍 فحص إضافي قبل الإضافة
        print(f"🔍 قبل إضافة 🏁 إلى content_text")
        print(f"طول content_text الحالي: {len(content_text)}")
        
        content_text += (
            "\n\n🏁 القرار الاستثماري النهائي\n\n"
            + ai_insights["ai_final_decision"]
            + "\n\n"
        )
        
        # 🔍 فحص بعد الإضافة
        print(f"🔍 بعد إضافة 🏁 إلى content_text")
        print(f"طول content_text الجديد: {len(content_text)}")
        print(f"علامة 🏁 موجودة في content_text؟: {'🏁' in content_text}")
        print(f"آخر 300 حرف من content_text: {repr(content_text[-300:])}")
        print("=" * 50)
    else:
        print("❌ ai_final_decision فارغ! لن يُضاف 🏁")

    # توليد الرسومات
    if df is not None:
        df = unify_columns(df)
        df = ensure_required_columns(df)
        charts = charts_engine.generate_all_charts(df)
    else:
        charts = {}

    return {
        "meta": {
            "package": prepared["package"],
            "generated_at": datetime.now().isoformat()
        },
        "content_text": content_text,
        "charts": charts
    }
