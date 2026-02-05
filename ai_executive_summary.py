# ai_executive_summary.py
# =========================================
# Executive Decision Engine – Warda Intelligence
# =========================================

from dataclasses import dataclass
from typing import List


@dataclass
class FinalDecision:
    action: str                 # BUY / WAIT / AVOID
    confidence: float            # 0.0 – 1.0
    horizon: str                 # "3–5 years"
    rationale: List[str]
    risks: List[str]
    change_triggers: List[str]


def build_final_decision(user_info, signals):
    """
    يبني القرار التنفيذي النهائي بمنطق مؤسسي
    """

    score = signals.get("score", 0.0)

    # -------------------------
    # منطق القرار
    # -------------------------
    if score >= 0.75:
        action = "BUY"
        confidence = min(0.95, score)
        horizon = "5–7 سنوات"
    elif score >= 0.55:
        action = "WAIT"
        confidence = score
        horizon = "3–5 سنوات"
    else:
        action = "AVOID"
        confidence = max(0.65, score)
        horizon = "غير مناسب حاليًا"

    return FinalDecision(
        action=action,
        confidence=round(confidence, 2),
        horizon=horizon,
        rationale=signals.get("rationale", []),
        risks=signals.get("risks", []),
        change_triggers=signals.get("triggers", []),
    )


def render_final_decision(decision: FinalDecision) -> str:
    """
    إخراج القرار بصيغة فاخرة جاهزة للتقرير
    """

    box_top = "═" * 60

    decision_text = f"""
{box_top}
🏁 القرار الاستثماري التنفيذي النهائي
{box_top}

🔹 القرار:
**{decision.action}**

🔹 درجة الثقة:
**{int(decision.confidence * 100)}%**

🔹 الأفق الزمني:
**{decision.horizon}**

────────────────────────
🔍 لماذا هذا القرار؟
────────────────────────
"""

    for r in decision.rationale:
        decision_text += f"• {r}\n"

    decision_text += "\n────────────────────────\n⚠️ المخاطر التي نراقبها\n────────────────────────\n"
    for r in decision.risks:
        decision_text += f"• {r}\n"

    decision_text += "\n────────────────────────\n🔄 متى نغيّر هذا القرار؟\n────────────────────────\n"
    for t in decision.change_triggers:
        decision_text += f"• {t}\n"

    return decision_text.strip()
