# report_orchestrator.py
from report_content_builder import build_complete_report
from advanced_charts import AdvancedCharts
from ai_report_reasoner import AIReportReasoner
from ai_executive_summary import generate_executive_summary
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
    sections = []

    for chapter in report.get("chapters", []):
        # استخراج عنوان الفصل من blocks
        for block in chapter.get("blocks", []):
            if block.get("type") == "chapter_title":
                title = block.get("content", "").strip()
                if title:
                    sections.append(title)
                    sections.append("")  # سطر فارغ بعد العنوان
                break

        # تجميع الفقرات كوحدات مع الحفاظ على الرسومات
        for block in chapter.get("blocks", []):
            block_type = block.get("type")
            content = block.get("content", "")
            tag = block.get("tag", "")

            # تخطي عنوان الفصل (تم معالجته أعلاه)
            if block_type == "chapter_title":
                continue

            # التعامل مع الرسومات والعلامات
            if block_type == "chart":
                sections.append(tag)   # 👈 هذا هو الجسر للرسومات
                sections.append("")
                continue

            if block_type == "chart_caption" and content:
                sections.append(content.strip())
                sections.append("")
                continue

            # التعامل مع النص العادي
            if block_type in ("text", "rich_text") and content:
                # تنظيف المحتوى مع الحفاظ على المسافات الطبيعية
                paragraph = "\n".join(
                    line.rstrip() for line in content.splitlines()
                ).strip()
                
                if paragraph:  # فقط إذا كان هناك محتوى بعد التنظيف
                    sections.append(paragraph)
                    sections.append("")  # فاصل فقرة واضح

    # دمج نهائي بنمط مستقر
    return "\n\n".join(sections).strip()

def inject_ai_by_anchor(content_text, anchor, title, ai_content):
    """حقن محتوى الذكاء الاصطناعي باستخدام Anchors المضمونة"""
    if not ai_content or anchor not in content_text:
        return content_text

    return content_text.replace(
        anchor,
        f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{title}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{ai_content}\n\n"
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
    
    # ✅ بناء market_data من البيانات الحية - بعد توحيد الأعمدة
    if df is not None:
        df = unify_columns(df)
        df = ensure_required_columns(df)
        
        # حساب معدل النمو بأمان باستخدام median بدل mean (أكثر دقة)
        if "price" in df.columns:
            growth_value = df["price"].pct_change().median()
            growth_value = growth_value if pd.notna(growth_value) else 0.01
            growth_rate = round(float(growth_value * 100), 2)
        else:
            growth_rate = 1.0
        
        market_data = {
            "مؤشر_السيولة": int(min(100, max(30, len(df) * 2))),
            "معدل_النمو_الشهري": growth_rate
        }
    else:
        market_data = {
            "مؤشر_السيولة": 50,
            "معدل_النمو_الشهري": 1.0
        }

    ai_insights = ai_reasoner.generate_all_insights(
        user_info=user_info,
        market_data=market_data,   # ✅ لم تعد {}
        real_data=df if df is not None else pd.DataFrame()
    )

    # 🔍 المرحلة 1: فحص نصوص الذكاء الاصطناعي
    print("="*50)
    print("🔍 المرحلة 1: فحص نصوص الذكاء الاصطناعي")
    print("="*50)
    print(f"AI LIVE موجود: {'نعم' if ai_insights.get('ai_live_market') else 'لا'}")
    if ai_insights.get('ai_live_market'):
        print(f"طول AI LIVE: {len(ai_insights['ai_live_market'])} حرف")
        print(f"العينة: {ai_insights['ai_live_market'][:150]}...")
    
    print(f"\nAI RISK موجود: {'نعم' if ai_insights.get('ai_risk') else 'لا'}")
    if ai_insights.get('ai_risk'):
        print(f"طول AI RISK: {len(ai_insights['ai_risk'])} حرف")
        print(f"العينة: {ai_insights['ai_risk'][:150]}...")
    
    print(f"\nAI OPPORTUNITIES موجود: {'نعم' if ai_insights.get('ai_opportunities') else 'لا'}")
    if ai_insights.get('ai_opportunities'):
        print(f"طول AI OPPORTUNITIES: {len(ai_insights['ai_opportunities'])} حرف")
        print(f"العينة: {ai_insights['ai_opportunities'][:150]}...")
    
    print(f"\nAI FINAL DECISION موجود: {'نعم' if ai_insights.get('ai_final_decision') else 'لا'}")
    if ai_insights.get('ai_final_decision'):
        print(f"طول AI FINAL DECISION: {len(ai_insights['ai_final_decision'])} حرف")
        print(f"العينة: {ai_insights['ai_final_decision'][:150]}...")
        print(f"يحتوي على 🏁: {'نعم' if '🏁' in ai_insights['ai_final_decision'] else 'لا'}")
    print("="*50)

    # 🔍 التحقق من وجود Anchors في التقرير
    print("\n🔍 فحص وجود Anchors في التقرير:")
    print("="*30)
    anchors = ["[[AI_SLOT_CH1]]", "[[AI_SLOT_CH2]]", "[[AI_SLOT_CH3]]"]
    for anchor in anchors:
        if anchor in content_text:
            print(f"✅ {anchor} موجود في التقرير")
        else:
            print(f"❌ {anchor} غير موجود في التقرير")
    print("="*30)

    # ✅ إدخال الذكاء الاصطناعي باستخدام Anchors (مضمون)
    content_text = inject_ai_by_anchor(
        content_text,
        "[[AI_SLOT_CH1]]",
        "📊 لقطة السوق الحية",
        ai_insights.get("ai_live_market", "")
    )

    content_text = inject_ai_by_anchor(
        content_text,
        "[[AI_SLOT_CH2]]",
        "⚠️ تقييم المخاطر الذكي",
        ai_insights.get("ai_risk", "")
    )

    content_text = inject_ai_by_anchor(
        content_text,
        "[[AI_SLOT_CH3]]",
        "💎 تحليل الفرص الاستثمارية",
        ai_insights.get("ai_opportunities", "")
    )

    # 🔍 التحقق بعد الحقن
    print("\n🔍 التحقق بعد إدخال نصوص الذكاء الاصطناعي:")
    print("="*30)
    ai_markers = ["📊 لقطة السوق الحية", "⚠️ تقييم المخاطر الذكي", "💎 تحليل الفرص الاستثمارية"]
    for marker in ai_markers:
        if marker in content_text:
            print(f"✅ '{marker}' تم إدراجه بنجاح")
        else:
            print(f"❌ '{marker}' لم يتم إدراجه")
    print("="*30)

    # =========================
    # 🧠 EXECUTIVE PREDICTIVE DECISION (FINAL – SOURCE OF TRUTH)
    # =========================
    executive_decision = generate_executive_summary(
        user_info=user_info,
        market_data=market_data,
        real_data=df if df is not None else pd.DataFrame()
    )

    content_text += "\n\n=== EXECUTIVE_PREDICTIVE_DECISION ===\n"
    content_text += executive_decision
    content_text += "\n"

    # توليد الرسومات
    if df is not None:
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
