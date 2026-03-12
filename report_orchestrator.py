# report_orchestrator.py
from report_content_builder import build_complete_report
from advanced_charts import AdvancedCharts
from ai_report_reasoner import AIReportReasoner
from ai_executive_summary import generate_executive_summary
from market_data_core import get_market_data
from investment_scorecard import calculate_investment_score  # ✅ إضافة Scorecard الاستثماري
from scorecard_visualizer import build_scorecard_text  # ✅ إضافة المُنسق البصري للـ Scorecard

from district_metrics_engine import (
    prepare_district_data,
    calculate_basic_district_metrics,
    calculate_dpi_score
)

from district_narrative_engine import generate_district_narrative
from district_ranking_engine import rank_districts, get_top_districts  # ✅ نظام ترتيب الأحياء

import pandas as pd
import numpy as np
from datetime import datetime

charts_engine = AdvancedCharts()

def normalize_dataframe(df):
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        return None
    return df.copy()

def unify_columns_for_charts(df):
    """
    توحيد أعمدة البيانات لتتوافق مع Data Contract الخاص بـ AdvancedCharts
    AdvancedCharts يتوقع: price | area | district | date
    
    ⚠️ ملاحظة معمارية:
    هذا التوحيد طبقة حماية قبل orchestration
    التوحيد النهائي الصارم يتم داخل AdvancedCharts
    """
    if df is None or df.empty:
        return df
    
    df = df.copy()
    
    # خريطة تحويل الأعمدة العربية إلى الإنجليزية - محدثة حسب التعديلات النهائية
    column_map = {
        "السعر": "price",
        "المساحة": "area", 
        "الحي": "district",
        "الحي / المدينة": "district"
    }
    
    # تحويل الأعمدة العربية إلى الإنجليزية
    for ar_col, en_col in column_map.items():
        if ar_col in df.columns and en_col not in df.columns:
            df[en_col] = df[ar_col]
    
    # التأكد من وجود الأعمدة المطلوبة
    required_cols = ["price", "area", "district", "date"]
    for col in required_cols:
        if col not in df.columns:
            # إذا كان العمود مفقوداً، نضيفه بقيمة افتراضية
            if col == "district":
                df[col] = "غير محدد"
            elif col == "date":
                # ✅ استخدام pd.NA بدلاً من None (يتجاهل بشكل نظيف في العمليات)
                df[col] = pd.NA
    
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

def build_report_story(user_info, provided_dataframe=None):
    """
    بناء قصة التقرير الكاملة
    
    Args:
        user_info: معلومات المستخدم (المدينة، نوع العقار، النوع التفصيلي، الباقة)
        مثال:
        {
            "city": "الرياض",
            "property_type": "سكني",
            "property_subtype": "شقة",  # ✅ النوع التفصيلي (شقة، فيلا، قصر/عقار كبير)
            "district": "الملقا",  # ✅ الحي المحدد للتحليل
            "package": "ذهبية"
        }
    
    Returns:
        dict: يحتوي على meta, content_text, executive_decision, charts, district_ranking, top_districts, investment_scorecard
    """
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

    # تنويه البيانات - صادق قانونياً واستثمارياً ✅
    content_text += "\n\n"
    content_text += "📌 تنويه مهم حول البيانات:\n"
    content_text += (
        "تم إنشاء هذا التقرير اعتمادًا على بيانات سوقية متاحة وقت إعداد التقرير، "
        "تم تحليلها وفق نماذج كمية ومعايير سوقية معتمدة. "
        "تعكس المؤشرات اتجاهات السوق في لحظة التحليل، "
        "وقد تختلف النتائج مستقبلًا تبعًا لتغيرات العرض والطلب.\n\n"
    )

    # تحميل البيانات الحية - استخدام الـ DataFrame المُمرر إذا وُجد، وإلا جلب من المصدر الحي
    if provided_dataframe is not None:
        df = provided_dataframe
        print("📊 استخدام DataFrame مُمرر خارجياً")
    else:
        try:
            df = get_market_data(
                city=user_info.get("city"),
                property_type=user_info.get("property_type"),
            )
            print("📊 جلب بيانات حقيقية من market_data_core")
        except Exception as e:
            raise RuntimeError(f"فشل توليد التقرير بسبب البيانات: {e}")
    
    df = normalize_dataframe(df)
    
    # ✅ التحقق من أن DataFrame ليس فارغاً قبل المعالجة
    if df is not None and not df.empty:
        # =========================================
        # 🎯 Smart Property Subtype Filter
        # =========================================
        # ✅ تحسين: الفلتر قبل توحيد الأعمدة للحفاظ على property_subtype
        property_subtype = user_info.get("property_subtype")
        if property_subtype and "property_subtype" in df.columns:
            print(f"🎯 تصفية حسب النوع التفصيلي: {property_subtype}")
            before_filter = len(df)
            df = df[df["property_subtype"] == property_subtype]
            print(f"   ✅ بعد التصفية: {len(df)} صفقة (تمت إزالة {before_filter - len(df)} صفقة)")
            
            # تحديث عنوان التقرير ليعكس النوع التفصيلي
            if len(df) > 0:
                content_text = content_text.replace(
                    f"تقرير سوق {user_info.get('city', '')}",
                    f"تقرير سوق {property_subtype} في {user_info.get('city', '')}"
                )
        
        # ✅ توحيد الأعمدة لمحرك الرسومات بعد التصفية
        df = unify_columns_for_charts(df)
        print(f"📊 الأعمدة بعد التوحيد: {list(df.columns)}")
    else:
        print("⚠️ DataFrame فارغ أو غير موجود - سيتم استخدام بيانات افتراضية")
        df = pd.DataFrame()  # DataFrame فارغ للمعالجة اللاحقة

    # =====================================
    # حساب ترتيب الأحياء الاستثمارية 🏆
    # =====================================
    district_ranking = None
    top_districts = None
    try:
        if df is not None and not df.empty and "district_clean" in df.columns:
            print("🏆 جاري حساب ترتيب الأحياء الاستثمارية...")
            district_ranking = rank_districts(df)
            if district_ranking is not None and not district_ranking.empty:
                top_districts = get_top_districts(df, top_n=5)
                print("🏆 أفضل الأحياء استثمارياً:")
                if top_districts is not None and not top_districts.empty:
                    display_cols = [col for col in ["district_clean", "dpi"] if col in top_districts.columns]
                    if display_cols:
                        print(top_districts[display_cols].head())
                    
                    # إضافة فقرة متميزة عن أفضل الأحياء إلى التقرير
                    if len(display_cols) >= 2:
                        top_districts_text = "\n\n🏆 أفضل الأحياء للاستثمار:\n"
                        
                        # ✅ تحسين: استخدام عداد منفصل للترقيم الصحيح 1,2,3 بدلاً من idx
                        for i, (_, row) in enumerate(top_districts.head(5).iterrows(), start=1):
                            district_name = row.get("district_clean", "غير محدد")
                            dpi_score = row.get("dpi", 0)
                            top_districts_text += f"  {i}. {district_name} (DPI: {dpi_score:.0f})\n"
                        
                        # إضافة تفسير DPI
                        top_districts_text += "\n*DPI: مؤشر قوة الحي (District Power Index) - كلما ارتفع كلما كان الحي أقوى استثمارياً*\n"
                        
                        # حقن الفقرة في التقرير (بعد التنويه)
                        content_text = content_text.replace(
                            "📌 تنويه مهم حول البيانات:",
                            f"🏆 أفضل الأحياء للاستثمار في {user_info.get('city', 'الرياض')}\n{top_districts_text}\n\n📌 تنويه مهم حول البيانات:"
                        )
    except Exception as e:
        print("⚠️ فشل حساب ترتيب الأحياء:", e)
        import traceback
        traceback.print_exc()

    # =====================================
    # 💹 حساب Investment Scorecard (بعد التصحيح)
    # =====================================
    investment_scores = {}
    scorecard_text = ""  # تهيئة متغير النص البصري
    try:
        if df is not None and not df.empty:
            print("💹 جاري حساب Investment Scorecard...")
            investment_scores = calculate_investment_score(df)
            print(f"   ✅ Investment Score: {investment_scores.get('investment_score', 'N/A')}")
            print(f"   ✅ Liquidity Score: {investment_scores.get('liquidity_score', 'N/A')}")
            print(f"   ✅ Price Score: {investment_scores.get('price_score', 'N/A')}")
            print(f"   ✅ Growth Score: {investment_scores.get('growth_score', 'N/A')}")
            print(f"   ✅ Risk Score: {investment_scores.get('risk_score', 'N/A')}")
            
            # 🎨 توليد النص البصري للـ Scorecard
            scorecard_text = build_scorecard_text(investment_scores)
            print("   ✅ تم توليد النص البصري للـ Scorecard")
        else:
            # قيم افتراضية متوافقة مع هيكل الدالة الأصلية
            investment_scores = {
                "investment_score": 50,
                "liquidity_score": 50,
                "price_score": 50,
                "growth_score": 50,
                "risk_score": 50
            }
            # توليد Scorecard من القيم الافتراضية
            scorecard_text = build_scorecard_text(investment_scores)
            print("⚠️ استخدام قيم افتراضية لـ Investment Scorecard")
    except Exception as e:
        print("⚠️ فشل حساب Investment Scorecard:", e)
        import traceback
        traceback.print_exc()
        # قيم افتراضية في حالة الفشل (متوافقة مع هيكل الدالة)
        investment_scores = {
            "investment_score": 50,
            "liquidity_score": 50,
            "price_score": 50,
            "growth_score": 50,
            "risk_score": 50
        }
        scorecard_text = build_scorecard_text(investment_scores)

    # توليد رؤى الذكاء الاصطناعي
    ai_reasoner = AIReportReasoner()
    
    # ✅ بناء market_data من البيانات الحية - مع حساب النمو المحسّن والمستقر
    if df is not None and not df.empty:
        # ============================
        # حساب معدل النمو الشهري - نسخة مستقرة احترافياً
        # ============================
        if "date" in df.columns and "price" in df.columns:
            try:
                tmp = df.copy()
                # ✅ إزالة القيم الفارغة قبل حساب الشهر (تحسين احترافي)
                tmp = tmp.dropna(subset=["date", "price"])
                
                tmp["month"] = tmp["date"].astype(str).str[:7]
                monthly_avg = (
                    tmp.groupby("month")["price"]
                    .mean()
                    .sort_index()
                )
                
                if len(monthly_avg) >= 2:
                    growth_series = monthly_avg.pct_change().dropna()
                    # إزالة القيم الشاذة (±200%)
                    growth_series = growth_series[
                        (growth_series > -2) & (growth_series < 2)
                    ]
                    growth_value = (
                        growth_series.median() if not growth_series.empty else 0.01
                    )
                else:
                    growth_value = 0.01
            except Exception:
                growth_value = 0.01
        else:
            growth_value = 0.01
        
        growth_rate = round(float(growth_value * 100), 2)
        
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
        market_data=market_data,
        real_data=df if df is not None else pd.DataFrame()
    )

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

    # توليد الخلاصة التنفيذية بشكل مستقل
    package_level = user_info.get("package") or user_info.get("chosen_pkg") or "مجانية"
    
    # تحويل اسم الباقة العربي إلى المفتاح الإنجليزي
    package_key_map = {
        "مجانية": "free",
        "فضية": "silver",
        "ذهبية": "gold",
        "ماسية": "diamond",
        "ماسية متميزة": "diamond_plus"
    }
    
    package_key = package_key_map.get(package_level, "free")

    executive_decision = generate_executive_summary(
        user_info=user_info,
        market_data=market_data,
        real_data=df if df is not None else pd.DataFrame(),
        package=package_key  # ✅ تمرير package إجباريًا
    )

    # =============================================
    # 🎨 توليد الرسومات (السوق العام + رسومات الأحياء)
    # =============================================
    print("🚀 DEBUG: بدء توليد الرسومات...")
    if df is not None and not df.empty:
        # رسومات السوق العامة
        charts = charts_engine.generate_all_charts(df)
        print(f"📊 DEBUG: عدد الرسومات المولدة: {len(charts)}")
        
        # =====================================
        # 🏙️ رسومات الحي (بعد التصحيح)
        # =====================================
        try:
            selected_district = user_info.get("district")
            if selected_district:
                district_charts = charts_engine.generate_all_district_charts(
                    df, 
                    selected_district
                )
                charts["district_analysis"] = district_charts
                print(f"📊 DEBUG: رسومات الحي المولدة: {len(district_charts)}")
        except Exception as e:
            print("⚠️ فشل توليد رسومات الحي:", e)
            import traceback
            traceback.print_exc()
        
        print(f"📊 DEBUG: إجمالي فصول الرسومات: {len(charts)}")
    else:
        print("❌ DEBUG: df فارغ قبل توليد الرسومات")
        charts = {}

    # =============================================
    # 📝 إضافة Scorecard البصري إلى التقرير النصي
    # =============================================
    content_text += "\n\n" + scorecard_text
    print("📝 تم إضافة Scorecard البصري إلى التقرير")

    return {
        "meta": {
            "package": prepared["package"],
            "generated_at": datetime.now().isoformat()
        },
        "content_text": content_text,
        "executive_decision": executive_decision,  # ⭐ عنصر مستقل
        "charts": charts,
        # ⭐ إضافات نظام ترتيب الأحياء
        "district_ranking": district_ranking,
        "top_districts": top_districts,
        # ⭐ إضافة Investment Scorecard (بعد التصحيح)
        "investment_scorecard": investment_scores
    }
