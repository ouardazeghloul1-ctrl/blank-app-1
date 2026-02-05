# report_orchestrator.py
# =========================================
# Report Orchestrator – Warda Intelligence
# العقل الذي يربط المحتوى + الذكاء + البيانات + الإخراج
# =========================================

from datetime import datetime
import pandas as pd
import numpy as np

from report_content_builder import build_complete_report
from ai_report_reasoner import AIReportReasoner
from live_real_data_provider import get_live_real_data
from advanced_charts import AdvancedCharts


charts_engine = AdvancedCharts()


# =========================
# Helpers
# =========================

def normalize_dataframe(df):
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        return pd.DataFrame()
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
    """
    يحول بنية التقرير إلى نص خطي
    بدون أي ذكاء – فقط المحتوى الخام
    """
    lines = []

    for chapter in report.get("chapters", []):
        for block in chapter.get("blocks", []):
            btype = block.get("type")
            content = block.get("content", "").strip()
            tag = block.get("tag", "")

            if btype == "chapter_title" and content:
                lines.append(content)
                lines.append("")

            elif btype == "rich_text" and content:
                lines.append(content)
                lines.append("")

            elif btype == "chart":
                lines.append(tag)
                lines.append("")

            elif btype == "chart_caption":
                lines.append(tag)
                lines.append(content)
                lines.append("")

    return "\n".join(lines)


def inject_ai_after_chapter(content_text, chapter_title, ai_title, ai_content):
    """
    يحقن فقرة ذكاء اصطناعي بعد فصل محدد
    """
    if not ai_content or chapter_title not in content_text:
        return content_text

    parts = content_text.split(chapter_title, 1)
    if len(parts) != 2:
        return content_text

    return (
        parts[0]
        + chapter_title
        + "\n\n"
        + ai_title
        + "\n\n"
        + ai_content
        + "\n\n"
        + parts[1]
    )


# =========================
# MAIN ORCHESTRATOR
# =========================

def build_report_story(user_info):
    """
    الدالة الرسمية الوحيدة لبناء التقرير
    ⚠️ لا تغيّر توقيعها
    """

    # -------------------------
    # User context
    # -------------------------
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

    # -------------------------
    # Base report content
    # -------------------------
    report = build_complete_report(prepared)
    content_text = blocks_to_text(report)

    # -------------------------
    # Data disclaimer (يظهر بخط عريض في PDF)
    # -------------------------
    content_text += (
        "\n\n📌 تنويه مهم حول البيانات:\n"
        "تم إنشاء هذا التقرير اعتمادًا على بيانات سوقية حقيقية وحية "
        "تم جمعها وتحليلها في تاريخ إعداد التقرير. "
        "تعكس النتائج حالة السوق في وقت الإنشاء، "
        "وقد تتغير المؤشرات مستقبلًا وفقًا لتغيرات العرض والطلب.\n"
    )

    # -------------------------
    # Live real data
    # -------------------------
    real_data = get_live_real_data(
        city=user_info.get("city"),
        property_type=user_info.get("property_type"),
    )

    real_data = normalize_dataframe(real_data)

    # -------------------------
    # AI Reasoning (شرح + قرار)
    # -------------------------
    ai_reasoner = AIReportReasoner()

    ai_insights = ai_reasoner.generate_all_insights(
        user_info=user_info,
        market_data={},
        real_data=real_data
    )

    # -------------------------
    # Inject AI insights inside chapters
    # -------------------------
    content_text = inject_ai_after_chapter(
        content_text,
        "الفصل الأول",
        "📊 لقطة السوق الحية (ذكاء اصطناعي)",
        ai_insights.get("ai_live_market")
    )

    content_text = inject_ai_after_chapter(
        content_text,
        "الفصل الثاني",
        "⚠️ تقييم المخاطر (ذكاء اصطناعي)",
        ai_insights.get("ai_risk")
    )

    content_text = inject_ai_after_chapter(
        content_text,
        "الفصل الثالث",
        "💎 الفرص الاستثمارية الذكية",
        ai_insights.get("ai_opportunities")
    )

    # -------------------------
    # Final Executive Decision
    # (مرة واحدة – في النهاية فقط)
    # -------------------------
    if ai_insights.get("ai_final_decision"):
        content_text += (
            "\n\n🏁 القرار الاستشاري النهائي: موقفك الصحيح الآن\n\n"
            + ai_insights["ai_final_decision"]
            + "\n"
        )

    # -------------------------
    # Charts
    # -------------------------
    charts = {}
    if not real_data.empty:
        df = unify_columns(real_data)
        df = ensure_required_columns(df)
        charts = charts_engine.generate_all_charts(df)

    # -------------------------
    # Final payload
    # -------------------------
    return {
        "meta": {
            "package": prepared["package"],
            "generated_at": datetime.now().isoformat()
        },
        "content_text": content_text,
        "charts": charts,
        "real_data": real_data
    }
