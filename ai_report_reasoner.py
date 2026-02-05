from ai_executive_summary import build_final_decision, render_final_decision

# داخل generate_all_insights بعد حساب المؤشرات

signals = {
    "score": market_insights.get("decision_score", 0.6),
    "rationale": [
        "السوق لا يُظهر ضغط طلب كافٍ لدعم الدخول الآن",
        "الفجوة السعرية لا تعكس فرصة تشغيلية حقيقية",
    ],
    "risks": [
        "استمرار ضعف السيولة",
        "زيادة معروض غير مستوعب",
    ],
    "triggers": [
        "تحسن سرعة البيع",
        "تراجع الفجوة بين السعر المعروض والمنفذ",
    ],
}

final_decision_obj = build_final_decision(user_info, signals)
final_decision_text = render_final_decision(final_decision_obj)

return {
    "ai_live_market": ...,
    "ai_opportunities": ...,
    "ai_risk": ...,
    "ai_final_decision": final_decision_text,
}
