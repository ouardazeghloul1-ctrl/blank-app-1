# report_orchestrator.py

from report_content_builder import build_complete_report
from ai_executive_summary import generate_executive_summary
from ai_report_reasoner import AIReportReasoner
from live_real_data_provider import get_live_real_data
from datetime import datetime
import pandas as pd


def build_report_story(user_info):
    prepared = {
        "المدينة": user_info.get("city", ""),
        "نوع_العقار": user_info.get("property_type", ""),
        "نوع_الصفقة": user_info.get("status", ""),
        "package": user_info.get("package", "مجانية"),
    }

    report = build_complete_report(prepared)
    content_text = ""

    for chapter in report["chapters"]:
        for block in chapter["blocks"]:
            if block.get("content"):
                content_text += block["content"] + "\n\n"

    # 🔴 تنويه البيانات – بخط عريض
    content_text += (
        "\n\n📌 **تنويه مهم حول البيانات:**\n"
        "**تم إنشاء هذا التقرير اعتمادًا على بيانات سوقية حية ومباشرة "
        "تم جمعها وتحليلها لحظة إعداد التقرير.**\n\n"
    )

    df = get_live_real_data(
        city=user_info.get("city"),
        property_type=user_info.get("property_type"),
    )

    df = df if isinstance(df, pd.DataFrame) else pd.DataFrame()

    # 🧠 القرار التنفيذي – المصدر الوحيد
    executive = generate_executive_summary(user_info, {}, df)

    decision_type = executive["decision_type"]
    decision_text = executive["decision_text"]
    confidence = executive["confidence_level"]

    # 🏁 إدخال القرار مرة واحدة فقط
    content_text += "\n\n🏁 القرار الاستثماري النهائي\n\n"
    content_text += decision_text + "\n\n"

    # 🎯 ماذا يفعل المستثمر بعد التقرير
    if decision_type == "BUY":
        content_text += (
            "📌 ماذا تفعل بعد هذا القرار؟\n"
            "• التزم بنطاق سعري منضبط\n"
            "• راقب السيولة لا الأخبار\n"
            "• لا توسّع قبل تثبيت العائد\n\n"
        )

    elif decision_type == "WAIT":
        content_text += (
            "📌 ماذا تراقب خلال فترة الانتظار؟\n"
            "• تحسّن السيولة\n"
            "• تقلّص الفجوة السعرية\n"
            "• تغيّر سلوك الطلب\n\n"
        )

    elif decision_type == "AVOID":
        content_text += (
            "📌 بدائل ذكية حاليًا:\n"
            "• الحفاظ على رأس المال\n"
            "• مراقبة فرص أقل مخاطرة\n"
            "• عدم الالتزام طويل الأجل الآن\n\n"
        )

    return {
        "meta": {
            "decision": decision_type,
            "confidence": confidence,
            "generated_at": datetime.now().isoformat(),
        },
        "content_text": content_text,
    }
