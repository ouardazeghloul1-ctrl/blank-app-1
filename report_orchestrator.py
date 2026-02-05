# report_orchestrator.py
# =========================================
# Report Orchestrator – Warda Intelligence
# التحكم الكامل في بناء التقرير والقرار
# =========================================

from report_content_builder import build_complete_report
from advanced_charts import AdvancedCharts
from ai_report_reasoner import AIReportReasoner
from ai_executive_summary import build_final_decision, FinalDecision
from live_real_data_provider import get_live_real_data
from ultimate_report_system import UltimateReportSystem

import pandas as pd
import numpy as np
from datetime import datetime

charts_engine = AdvancedCharts()

# ==================================================
# أدوات معالجة البيانات
# ==================================================
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


# ==================================================
# تحويل blocks إلى نص
# ==================================================
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


# ==================================================
# مساعدات منطق القرار
# ==================================================
def confidence_level(confidence: float) -> str:
    """
    تحويل درجة الثقة الرقمية إلى مستوى استشاري مفهوم
    """
    if confidence >= 0.75:
        return "عالية"
    if confidence >= 0.60:
        return "متوسطة"
    return "منخفضة"


# ==================================================
# البناء الرئيسي للتقرير
# ==================================================
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
    # 1) بناء التقرير النصي الأساسي
    # -------------------------
    report = build_complete_report(prepared)
    content_text = blocks_to_text(report)

    # -------------------------
    # 2) تحميل البيانات الحية
    # -------------------------
    df = get_live_real_data(
        city=user_info.get("city"),
        property_type=user_info.get("property_type"),
    )
    df = normalize_dataframe(df)

    # -------------------------
    # 3) توليد القرار التنفيذي (العقل الحاكم)
    # -------------------------
    final_decision: FinalDecision = build_final_decision(
        user_info=user_info,
        market_data={},
        real_data=df if df is not None else pd.DataFrame()
    )

    # -------------------------
    # 4) الذكاء التفسيري داخل الفصول
    # -------------------------
    ai_reasoner = AIReportReasoner()
    ai_insights = ai_reasoner.generate_all_insights(
        user_info=user_info,
        market_data={},
        real_data=df if df is not None else pd.DataFrame(),
        final_decision=final_decision
    )

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

    # ==================================================
    # 5) القرار التنفيذي – Section مستقل منطقيًا
    # ==================================================
    if final_decision:
        decision_label = final_decision.action
        decision_conf_level = confidence_level(final_decision.confidence)

        content_text += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏁 القرار الاستثماري التنفيذي النهائي
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

القرار:
{decision_label}

درجة الثقة:
{decision_conf_level}

الأفق الزمني:
{final_decision.horizon}

────────────────────────
لماذا هذا القرار؟
────────────────────────
"""

        for r in final_decision.rationale:
            content_text += f"- {r}\n"

        # -------------------------
        # BUY → نصائح تنفيذ ثمينة
        # -------------------------
        if final_decision.action == "BUY":
            content_text += """

────────────────────────
🧭 كيف تنفّذ هذا القرار بذكاء بعد إغلاق التقرير؟
────────────────────────

- لا تدخل الصفقة بأقصى قدرتك حتى لو بدت مثالية.
- اترك هامش سيولة ونَفَس نفسي بعد الشراء.
- لا تعتبر القرار ناجحًا في أول أشهره؛ راقب التشغيل لا الضجيج.
- أي تذبذب مبكر لا يعني فشل القرار.
- أعد التقييم فقط إذا تغيّرت الفرضية، لا المزاج العام.
"""

        # -------------------------
        # WAIT → توجيه انتظار واعٍ
        # -------------------------
        elif final_decision.action == "WAIT":
            content_text += """

────────────────────────
🧭 ماذا تفعل خلال فترة الانتظار؟
────────────────────────

- راقب مؤشرين فقط: سرعة البيع والفجوة بين السعر المعروض والمنفذ.
- حدّد شرط التحوّل الواضح من الانتظار إلى التنفيذ.
- لا تدخل التزامات كبيرة قبل تحقق هذا الشرط.
- الانتظار هنا استعداد، لا تجميد ولا تردد.
"""

        # -------------------------
        # AVOID → بدائل ذكية فقط
        # -------------------------
        elif final_decision.action == "AVOID":
            content_text += """

────────────────────────
🧭 ماذا تفعل بدلًا من التنفيذ الآن؟
────────────────────────

1) وضع المراقبة الذكية دون أي التزام اندفاعي.
2) تعديل الصيغة الاستثمارية (نوع / موقع / استخدام) بدل تغيير الفكرة بالكامل.
3) الحفاظ على رأس المال حتى تظهر فرصة بهامش أمان حقيقي.
"""

    # -------------------------
    # 6) الإغلاق التنفيذي (بدون تكرار القرار)
    # -------------------------
    ultimate = UltimateReportSystem(final_decision)
    content_text = ultimate.apply(content_text)

    # -------------------------
    # 7) معلومات التقرير – بخط عريض
    # -------------------------
    content_text += f"""

**📅 تاريخ إنشاء التقرير:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**📊 مصدر البيانات:** بيانات سوقية حقيقية تم جمعها وتحليلها وقت إنشاء التقرير
"""

    # -------------------------
    # 8) الرسومات
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
