# report_orchestrator.py
# =================================================
# REPORT ORCHESTRATOR – FINAL CLEAN ARCHITECTURE
# =================================================

from report_content_builder import build_complete_report
from ai_report_reasoner import AIReportReasoner


# =================================================
# PACKAGE CAPABILITIES (قرار نهائي)
# =================================================
PACKAGE_CAPABILITIES = {
    "free": {
        "ai_insight": False,
        "final_decision": False,
    },
    "silver": {
        "ai_insight": False,
        "final_decision": False,
    },
    "gold": {
        "ai_insight": True,
        "final_decision": False,
    },
    "diamond": {
        "ai_insight": True,
        "final_decision": False,
    },
    "diamond_plus": {
        "ai_insight": True,
        "final_decision": True,   # 🟣 حصري
    },
}


# =================================================
# MAIN ENTRY
# =================================================
def build_report_story(user_info, real_data):
    """
    المخرج الوحيد:
    {
        "blocks": [...],
        "charts": {...}
    }
    """

    # -----------------------------
    # 1️⃣ تحديد الباقة
    # -----------------------------
    raw_pkg = user_info.get("package", "free")
    package = normalize_package(raw_pkg)
    capabilities = PACKAGE_CAPABILITIES[package]

    # -----------------------------
    # 2️⃣ بناء المحتوى النصي الثابت
    # -----------------------------
    report_structure = build_complete_report(user_info)

    # -----------------------------
    # 3️⃣ تشغيل الذكاء الاصطناعي (مرة واحدة)
    # -----------------------------
    ai_reasoner = AIReportReasoner()
    ai_outputs = ai_reasoner.generate_all_insights(
        user_info=user_info,
        market_data={},      # السوق لا يهم هنا
        real_data=real_data
    )

    # -----------------------------
    # 4️⃣ تحويل كل شيء إلى Blocks
    # -----------------------------
    blocks = []
    charts_by_chapter = {}

    for chapter in report_structure["chapters"]:
        ch_num = chapter["chapter_number"]
        charts_by_chapter[f"chapter_{ch_num}"] = []

        # عنوان الفصل
        blocks.append({
            "type": "chapter_title",
            "chapter": ch_num,
            "content": f"الفصل {ch_num}"
        })

        for block in chapter["blocks"]:

            # ===== نص عادي =====
            if block["type"] == "rich_text":
                blocks.append({
                    "type": "text",
                    "chapter": ch_num,
                    "content": block["content"]
                })

            # ===== رسم =====
            elif block["type"] == "chart":
                blocks.append({
                    "type": "chart",
                    "chapter": ch_num
                })

            # ===== شرح رسم =====
            elif block["type"] == "chart_caption":
                blocks.append({
                    "type": "chart_caption",
                    "chapter": ch_num,
                    "content": block["content"]
                })

        # ===== AI INSIGHT (للفصول الأولى فقط) =====
        if capabilities["ai_insight"] and ch_num in (1, 2, 3):
            insight_key = {
                1: "ai_live_market",
                2: "ai_risk",
                3: "ai_opportunities",
            }.get(ch_num)

            ai_text = ai_outputs.get(insight_key, "")
            if ai_text:
                blocks.append({
                    "type": "ai_insight",
                    "chapter": ch_num,
                    "content": ai_text
                })

    # =================================================
    # 🟣 FINAL DECISION – فقط للماسية المتميزة
    # =================================================
    if capabilities["final_decision"]:
        final_text = ai_outputs.get("ai_final_decision", "")
        if final_text:
            blocks.append({
                "type": "final_decision",
                "chapter": "final",
                "title": "🧠 الخلاصة الاستشارية النهائية",
                "content": final_text
            })

    return {
        "blocks": blocks,
        "charts": charts_by_chapter
    }


# =================================================
# HELPERS
# =================================================
def normalize_package(pkg):
    mapping = {
        "مجانية": "free",
        "فضية": "silver",
        "ذهبية": "gold",
        "ماسية": "diamond",
        "ماسية متميزة": "diamond_plus",
        "free": "free",
        "silver": "silver",
        "gold": "gold",
        "diamond": "diamond",
        "diamond_plus": "diamond_plus",
    }
    return mapping.get(pkg, "free")
