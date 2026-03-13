# report_orchestrator.py
from report_content_builder import build_complete_report
from advanced_charts import AdvancedCharts
from ai_report_reasoner import AIReportReasoner
from ai_executive_summary import generate_executive_summary
from market_data_core import get_market_data
from investment_scorecard import calculate_investment_score
from scorecard_visualizer import build_scorecard_text
from data_repair_engine import repair_market_data

from district_metrics_engine import (
    prepare_district_data,
    calculate_basic_district_metrics,
    calculate_dpi_score
)

from district_narrative_engine import generate_district_narrative
from district_ranking_engine import rank_districts, get_top_districts

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
    """
    if df is None or df.empty:
        return df
    
    df = df.copy()
    
    # خريطة تحويل الأعمدة العربية إلى الإنجليزية
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
            if col == "district":
                df[col] = "غير محدد"
            elif col == "date":
                df[col] = pd.NA
    
    # ✅ التعديل 1: إصلاح الأعمدة الرقمية والتواريخ
    # تحويل الأعمدة الرقمية
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
    if "area" in df.columns:
        df["area"] = pd.to_numeric(df["area"], errors="coerce")
    
    # إصلاح القيم الناقصة
    if "price" in df.columns:
        median_price = df["price"].median()
        if pd.isna(median_price):
            median_price = 500000
        df["price"] = df["price"].fillna(median_price)
    
    if "area" in df.columns:
        median_area = df["area"].median()
        if pd.isna(median_area):
            median_area = 120
        df["area"] = df["area"].fillna(median_area)
        # ✅ التعديل 2: منع القيم الصفرية أو السالبة للمساحة (يمنع Infinity)
        df.loc[df["area"] <= 0, "area"] = median_area
    
    # ✅ التعديل 3: إصلاح التواريخ بطريقة متوافقة مع الإصدارات الحديثة
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        # استخدام ffill() بدلاً من fillna(method="ffill") (الأسلوب الحديث)
        df["date"] = df["date"].ffill()
        # إذا بقي أي NaN، استخدم التاريخ الأكثر تكراراً
        if df["date"].isna().any():
            most_common_date = df["date"].mode()[0] if not df["date"].mode().empty else pd.Timestamp.now()
            df["date"] = df["date"].fillna(most_common_date)
    
    return df

def blocks_to_text(report):
    sections = []

    for chapter in report.get("chapters", []):
        # استخراج عنوان الفصل
        for block in chapter.get("blocks", []):
            if block.get("type") == "chapter_title":
                title = block.get("content", "").strip()
                if title:
                    sections.append(title)
                    sections.append("")
                break

        # تجميع الفقرات
        for block in chapter.get("blocks", []):
            block_type = block.get("type")
            content = block.get("content", "")
            tag = block.get("tag", "")

            if block_type == "chapter_title":
                continue

            if block_type == "chart":
                sections.append(tag)
                sections.append("")
                continue

            if block_type == "chart_caption" and content:
                sections.append(content.strip())
                sections.append("")
                continue

            if block_type in ("text", "rich_text") and content:
                paragraph = "\n".join(
                    line.rstrip() for line in content.splitlines()
                ).strip()
                
                if paragraph:
                    sections.append(paragraph)
                    sections.append("")

    return "\n\n".join(sections).strip()

def inject_ai_by_anchor(content_text, anchor, title, ai_content):
    """حقن محتوى الذكاء الاصطناعي"""
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

    # تنويه البيانات
    content_text += "\n\n"
    content_text += "📌 تنويه مهم حول البيانات:\n"
    content_text += (
        "تم إنشاء هذا التقرير اعتمادًا على بيانات سوقية متاحة وقت إعداد التقرير، "
        "تم تحليلها وفق نماذج كمية ومعايير سوقية معتمدة. "
        "تعكس المؤشرات اتجاهات السوق في لحظة التحليل، "
        "وقد تختلف النتائج مستقبلًا تبعًا لتغيرات العرض والطلب.\n\n"
    )

    # تحميل البيانات
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
    
    # إصلاح البيانات الناقصة
    if df is not None and not df.empty:
        df = repair_market_data(df)
        print("🛠️ تم إصلاح البيانات الناقصة بنجاح")
    
    # التحقق من البيانات
    if df is not None and not df.empty:
        # تصفية حسب النوع التفصيلي
        property_subtype = user_info.get("property_subtype")
        if property_subtype and "property_subtype" in df.columns:
            print(f"🎯 تصفية حسب النوع التفصيلي: {property_subtype}")
            before_filter = len(df)
            df = df[df["property_subtype"] == property_subtype]
            print(f"   ✅ بعد التصفية: {len(df)} صفقة")
            
            if len(df) > 0:
                content_text = content_text.replace(
                    f"تقرير سوق {user_info.get('city', '')}",
                    f"تقرير سوق {property_subtype} في {user_info.get('city', '')}"
                )
        
        # توحيد الأعمدة (يتضمن الآن التعديلات 1, 2, 3)
        df = unify_columns_for_charts(df)
        
        # ✅ التعديل 3 (الجديد): إضافة price_per_sqm مع حماية إضافية
        df["price_per_sqm"] = df["price"] / df["area"].replace(0, 1)
        print(f"📊 تم إضافة price_per_sqm للتحليلات")
        
        print(f"📊 الأعمدة بعد التوحيد: {list(df.columns)}")
        print(f"📊 إجمالي الصفقات بعد الإصلاح: {len(df)}")
    else:
        print("⚠️ DataFrame فارغ - استخدام بيانات افتراضية")
        df = pd.DataFrame()

    # حساب ترتيب الأحياء
    district_ranking = None
    top_districts = None
    try:
        if df is not None and not df.empty and ("district_clean" in df.columns or "district" in df.columns):
            district_column = "district_clean" if "district_clean" in df.columns else "district"
            print(f"🏆 حساب ترتيب الأحياء باستخدام: {district_column}")
            
            # ✅ التعديل 4: استخدام نسخة من dataframe لمنع SettingWithCopyWarning
            district_ranking = rank_districts(df.copy())
            if district_ranking is not None and not district_ranking.empty:
                # ✅ التعديل 1 (الجديد): استخدام copy() هنا أيضاً
                top_districts = get_top_districts(df.copy(), top_n=5)
                
                if top_districts is not None and not top_districts.empty:
                    display_district_col = "district_clean" if "district_clean" in top_districts.columns else "district" if "district" in top_districts.columns else None
                    
                    if display_district_col and "dpi" in top_districts.columns:
                        top_districts_text = f"\n\n🏆 أفضل الأحياء للاستثمار في {user_info.get('city', 'الرياض')}:\n"
                        
                        for i, (_, row) in enumerate(top_districts.head(5).iterrows(), start=1):
                            district_name = row.get(display_district_col, "غير محدد")
                            dpi_score = row.get("dpi", 0)
                            top_districts_text += f"  {i}. {district_name} (DPI: {dpi_score:.0f})\n"
                        
                        top_districts_text += "\n*DPI: مؤشر قوة الحي - كلما ارتفع كلما كان الحي أقوى استثمارياً*\n"
                        
                        content_text = content_text.replace(
                            "📌 تنويه مهم حول البيانات:",
                            f"{top_districts_text}\n\n📌 تنويه مهم حول البيانات:"
                        )
    except Exception as e:
        print("⚠️ فشل حساب ترتيب الأحياء:", e)

    # حساب Investment Scorecard
    investment_scores = {}
    scorecard_text = ""
    try:
        if df is not None and not df.empty:
            print("💹 حساب Investment Scorecard...")
            investment_scores = calculate_investment_score(df)
            scorecard_text = build_scorecard_text(investment_scores)
            print("   ✅ تم توليد Scorecard")
        else:
            investment_scores = {
                "investment_score": 50,
                "liquidity_score": 50,
                "price_score": 50,
                "growth_score": 50,
                "risk_score": 50
            }
            scorecard_text = build_scorecard_text(investment_scores)
    except Exception as e:
        print("⚠️ فشل حساب Scorecard:", e)
        investment_scores = {
            "investment_score": 50,
            "liquidity_score": 50,
            "price_score": 50,
            "growth_score": 50,
            "risk_score": 50
        }
        scorecard_text = build_scorecard_text(investment_scores)

    # تحليل الحي
    district_analysis_text = ""
    try:
        selected_district = user_info.get("district")
        selected_city = user_info.get("city")
        if selected_district and selected_city and df is not None and not df.empty:
            print(f"📍 تحليل الحي: {selected_district}")
            
            df_prepared = df.copy()
            
            if "transaction_date" not in df_prepared.columns and "date" in df_prepared.columns:
                df_prepared["transaction_date"] = df_prepared["date"]
            
            df_prepared = prepare_district_data(df_prepared)
            
            district_metrics = calculate_basic_district_metrics(
                df_prepared, 
                selected_city, 
                selected_district
            )
            
            # ✅ التعديل 2 (من الدالة الأصلية): منع انهيار تحليل الحي
            if not district_metrics:
                district_metrics = {
                    "district_name": selected_district,
                    "city_name": selected_city,
                    "district_avg_price": df_prepared["price"].mean() if "price" in df_prepared.columns else 0,
                    "city_avg_price": df_prepared["price"].mean() if "price" in df_prepared.columns else 0,
                    "transactions_count": len(df_prepared)
                }
            
            # تحسين DPI
            if district_metrics and isinstance(district_metrics, dict):
                dpi_score = calculate_dpi_score(district_metrics)
            else:
                dpi_score = 50
            
            district_analysis_text = generate_district_narrative(
                user_info=user_info,
                district_metrics=district_metrics,
                nearby_districts=[],
                dpi_score=dpi_score,
                market_data={},
                real_data=df_prepared
            )
            print("✅ تم توليد تحليل الحي")
    except Exception as e:
        print("⚠️ فشل تحليل الحي:", e)

    # توليد رؤى الذكاء الاصطناعي
    ai_reasoner = AIReportReasoner()
    
    # بناء market_data
    if df is not None and not df.empty:
        if "date" in df.columns and "price" in df.columns:
            try:
                # ✅ التعديل 2 (الجديد): نسخ العمودين فقط بدلاً من نسخ الـ DataFrame كاملاً
                tmp = df[["date", "price"]].dropna().copy()
                
                # ✅ التعديل 1 (الصغير): استخدام dt.to_period مباشرة دون إعادة to_datetime
                # لأن date تم تحويلها مسبقاً في unify_columns_for_charts
                tmp["month"] = tmp["date"].dt.to_period("M")
                monthly_avg = (
                    tmp.groupby("month")["price"]
                    .mean()
                    .sort_index()
                )
                
                if len(monthly_avg) >= 2:
                    growth_series = monthly_avg.pct_change().dropna()
                    growth_series = growth_series[
                        (growth_series > -2) & (growth_series < 2)
                    ]
                    growth_value = (
                        growth_series.median() if not growth_series.empty else 0.01
                    )
                else:
                    growth_value = 0.01
            except Exception as e:
                print("⚠️ خطأ في حساب النمو:", e)
                growth_value = 0.01
        else:
            growth_value = 0.01
        
        growth_rate = round(float(growth_value * 100), 2)
        
        # ✅ تحسين مؤشر السيولة ليكون أكثر واقعية مع 44k صفقة
        # استخدام معامل 500 بدلاً من 20 لجعل المؤشر يتدرج بشكل أفضل
        # 44,000 / 500 = 88 (أقل من 100) -> يعطي مجالاً للنمو
        liquidity_base = len(df) / 500
        liquidity_score = int(min(100, max(30, liquidity_base)))
        
        market_data = {
            "مؤشر_السيولة": liquidity_score,
            "معدل_النمو_الشهري": growth_rate
        }
        print(f"📊 مؤشر السيولة المحسوب: {market_data['مؤشر_السيولة']} (بناءً على {len(df)} صفقة)")
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

    # حقن رؤى الذكاء الاصطناعي
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

    # توليد الخلاصة التنفيذية
    package_level = user_info.get("package") or user_info.get("chosen_pkg") or "مجانية"
    
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
        package=package_key
    )

    # ✅ التعديل 3 (من الدالة السابقة): إصلاح المساحة قبل الرسومات
    if df is not None and not df.empty and "area" in df.columns:
        median_area = df["area"].median()
        if pd.isna(median_area):
            median_area = 120
        df.loc[df["area"] <= 0, "area"] = median_area
        # تحديث price_per_sqm بعد إصلاح المساحة مع حماية إضافية
        df["price_per_sqm"] = df["price"] / df["area"].replace(0, 1)
        print("🛠️ تم إصلاح المساحة الصفرية قبل الرسومات وتحديث price_per_sqm")

    # توليد الرسومات
    print("🚀 بدء توليد الرسومات...")
    if df is not None and not df.empty:
        charts = charts_engine.generate_all_charts(df)
        print(f"📊 عدد الرسومات المولدة: {len(charts)}")
        
        try:
            selected_district = user_info.get("district")
            if selected_district:
                district_charts = charts_engine.generate_all_district_charts(
                    df, 
                    selected_district
                )
                charts["district_analysis"] = district_charts
                print(f"📊 رسومات الحي المولدة: {len(district_charts)}")
        except Exception as e:
            print("⚠️ فشل توليد رسومات الحي:", e)
    else:
        charts = {}

    # إضافة Scorecard
    content_text += "\n\n" + scorecard_text
    
    # إضافة تحليل الحي إلى التقرير النصي
    if district_analysis_text:
        content_text += "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        content_text += "🏙️ التحليل العميق للحي\n"
        content_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        content_text += district_analysis_text

    return {
        "meta": {
            "package": prepared["package"],
            "generated_at": datetime.now().isoformat()
        },
        "content_text": content_text,
        "executive_decision": executive_decision,
        "charts": charts,
        "district_ranking": district_ranking,
        "top_districts": top_districts,
        "investment_scorecard": investment_scores,
        "district_analysis": district_analysis_text
    }
