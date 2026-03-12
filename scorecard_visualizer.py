# scorecard_visualizer.py

def render_score_bar(score, max_blocks=10):
    """
    تحويل الرقم إلى شريط بصري
    مثال:
    70 → ███████░░░
    """
    filled = int((score / 100) * max_blocks)
    empty = max_blocks - filled

    return "█" * filled + "░" * empty


def build_scorecard_text(scorecard):
    """
    إنشاء الصفحة البصرية لـ Investment Scorecard
    """

    if not scorecard:
        return "لا توجد بيانات لحساب Investment Score."

    investment_score = scorecard.get("investment_score", 50)
    liquidity = scorecard.get("liquidity_score", 50)
    price = scorecard.get("price_score", 50)
    growth = scorecard.get("growth_score", 50)
    risk = scorecard.get("risk_score", 50)

    score_text = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Investment Scorecard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

النتيجة الاستثمارية الكلية

⭐ Investment Score: {investment_score} / 100


مؤشرات التحليل

السيولة السوقية
{render_score_bar(liquidity)}  ({liquidity})

موقع السعر في السوق
{render_score_bar(price)}  ({price})

إشارة النمو
{render_score_bar(growth)}  ({growth})

مستوى المخاطر
{render_score_bar(100-risk)}  ({risk})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return score_text.strip()
