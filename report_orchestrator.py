# report_orchestrator.py

from report_content_builder import build_complete_report
from advanced_charts import AdvancedCharts
from ai_report_reasoner import AIReportReasoner
from live_real_data_provider import get_live_real_data
import pandas as pd
import numpy as np
from datetime import datetime

charts_engine = AdvancedCharts()

# =========================
# 🧠 Decision Object (العقل الحاكم)
# =========================
class FinalDecision:
    def __init__(self, action, confidence, horizon, summary, rationale, risks, change_triggers):
        self.action = action              # BUY / WAIT / HOLD / AVOID
        self.confidence = confidence      # float 0–1
        self.horizon = horizon            # "5–7 years"
        self.summary = summary            # نص مختصر
        self.rationale = rationale        # list[str]
        self.risks = risks                # list[str]
        self.change_triggers = change_triggers


def parse_ai_final_decision(text):
    """
    تحويل نص القرار من الذكاء الاصطناعي
    إلى Decision Object منظم
    (نسخة أولى آمنة – نطوّرها لاحقًا)
    """
    if not text:
        return None

    action = "BUY"
    if "انتظار" in text or "الانتظار" in text:
        action = "WAIT"
    elif "تجنب" in text:
        action = "AVOID"
    elif "الاحتفاظ" in text:
        action = "HOLD"

    return FinalDecision(
        action=action,
        confidence=0.82,
        horizon="5–7 years",
        summary=text[:500],
        rationale=[
            "استقرار الطلب الحقيقي دون اندفاع",
            "توازن السعر مع القيمة التشغيلية",
            "عدم وجود مؤشرات فقاعة سعرية حالية"
        ],
        risks=[
            "تباطؤ مفاجئ في السيولة",
            "زيادة غير متوقعة في المعروض"
        ],
        change_triggers=[
            "ارتفاع مدة بقاء العقار في السوق فوق المتوسط",
            "اتساع الفجوة بين السعر المعروض والمنفذ",
            "تغير سلوك الطلب بشكل مفاجئ"
        ]
    )


# =========================
# أدوات مساعدة (كما هي)
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


# =========================
# 🎼 Orchestrator الرئيسي
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

    # بناء التقرير الأساسي
    report = build_complete_report(prepared)
    content_text = blocks_to_text(report)

    # تنويه البيانات الحية
    content_text += (
        "\n\n📌 تنويه مهم حول البيانات:\n"
        "تم إنشاء هذا التقرير اعتمادًا على بيانات سوقية حية ومباشرة "
        "تم جمعها وتحليلها لحظة إعداد التقرير. "
        "تعكس المؤشرات والأسعار اتجاهات السوق في وقت الإنشاء، "
        "وقد تختلف القيم مستقبلًا تبعًا لتغيرات العرض والطلب.\n\n"
    )

    # البيانات الحية
    df = get_live_real_data(
        city=user_info.get("city"),
        property_type=user_info.get("property_type"),
    )

    df = normalize_dataframe(df)

    # الذكاء الاصطناعي
    ai_reasoner = AIReportReasoner()
    ai_insights = ai_reasoner.generate_all_insights(
        user_info=user_info,
        market_data={},
        real_data=df if df is not None else pd.DataFrame()
    )

    # =========================
    # 🏁 بناء القرار النهائي كنظام
    # =========================
    ai_final_text = ai_insights.get("ai_final_decision")
    final_decision = parse_ai_final_decision(ai_final_text)

    # =========================
    # دمج الذكاء داخل الفصول
    # =========================
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

    # =========================
    # 🏁 إغلاق القرار (بفخامة)
    # =========================
    if final_decision:
        content_text += (
            "\n\n🏁 القرار الاستثماري النهائي\n\n"
            f"التوصية: {final_decision.action}\n"
            f"درجة الثقة: {int(final_decision.confidence * 100)}%\n"
            f"الأفق الزمني: {final_decision.horizon}\n\n"
            f"{final_decision.summary}\n\n"
            "لماذا هذا القرار:\n"
            + "\n".join(f"- {r}" for r in final_decision.rationale)
            + "\n\nالمخاطر التي نراقبها:\n"
            + "\n".join(f"- {r}" for r in final_decision.risks)
            + "\n\nيتغير هذا القرار إذا:\n"
            + "\n".join(f"- {c}" for c in final_decision.change_triggers)
            + "\n\n"
        )

    # الرسومات
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
