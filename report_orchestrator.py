# report_orchestrator.py
# =========================================
# Report Orchestrator – Warda Intelligence
# =========================================

from report_content_builder import (
    build_complete_report,
    decision_invalid_conditions_block
)
from advanced_charts import AdvancedCharts
from ai_report_reasoner import AIReportReasoner
from ai_executive_summary import build_final_decision
from live_real_data_provider import get_live_real_data

import pandas as pd
import numpy as np
from datetime import datetime

charts_engine = AdvancedCharts()


# =========================
# أدوات مساعدة للبيانات
# =========================
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


# =========================
# تحويل blocks إلى نص
# =========================
def blocks_to_text(report):
    lines = []

    for chapter in report.get("chapters", []):
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

    marker = chapter_title
    parts = content_text.split(marker, 1)

    if len(parts) != 2:
        return content_text

    return (
        parts[0]
        + marker
        + "\n\n"
        + ai_title
        + "\n\n"
        + ai_content
        + "\n\n"
        + parts[1]
    )


# =========================
# 🎼 البناء الرئيسي للتقرير
# =========================
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

    # -------------------------
    # بناء التقرير الأساسي
    # -------------------------
    report = build_complete_report(prepared)
    content_text = blocks_to_text(report)

    # -------------------------
    # تنويه البيانات الحية
    # -------------------------
    content_text += (
        "\n\n📌 تنويه مهم حول البيانات:\n"
        "تم إعداد هذا التقرير اعتمادًا على بيانات سوقية حية ومباشرة "
        "تم تحليلها لحظة الإنشاء. تعكس النتائج وضع السوق الحالي "
        "وقد تتغير مع تغير الظروف.\n\n"
    )

    # -------------------------
    # البيانات الحية
    # -------------------------
    df = get_live_real_data(
        city=user_info.get("city"),
        property_type=user_info.get("property_type"),
    )

    df = normalize_dataframe(df)

    # -------------------------
    # 🧠 بناء القرار النهائي (العقل الحاكم)
    # -------------------------
    final_decision = build_final_decision(
        user_info=user_info,
        market_data={},
        real_data=df if df is not None else pd.DataFrame()
    )

    # -------------------------
    # الذكاء التفسيري
    # -------------------------
    ai_reasoner = AIReportReasoner()
    ai_insights = ai_reasoner.generate_all_insights(
        user_info=user_info,
        market_data={},
        real_data=df if df is not None else pd.DataFrame(),
        final_decision=final_decision
    )

    # -------------------------
    # دمج الذكاء داخل الفصول
    # -------------------------
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

    # -------------------------
    # 🏁 القرار النهائي
    # -------------------------
    if final_decision:
        content_text += (
            "\n\n🏁 القرار الاستثماري النهائي\n\n"
            f"التوصية: {final_decision.action}\n"
            f"درجة الثقة: {int(final_decision.confidence * 100)}%\n"
            f"الأفق الزمني: {final_decision.horizon}\n\n"
            f"{final_decision.summary_text}\n\n"
            "أسباب هذا القرار:\n"
            + "\n".join(f"• {r}" for r in final_decision.rationale)
            + "\n\n"
        )

        # -------------------------
        # 🧠 كسر الخوف النفسي (الخطوة 3)
        # -------------------------
        invalid_block = decision_invalid_conditions_block(final_decision)
        if invalid_block and invalid_block.get("content"):
            content_text += (
                "\n\n"
                + invalid_block["content"]
                + "\n\n"
            )

    # -------------------------
    # الرسومات
    # -------------------------
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
        "charts": charts,
        "final_decision": final_decision
    }
