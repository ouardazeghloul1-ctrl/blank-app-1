# investment_scorecard.py

import pandas as pd


def calculate_investment_score(df, district=None):
    """
    حساب Investment Score للحي أو للسوق العام
    يعتمد على:
    - Liquidity
    - Price Position
    - Market Growth
    - Risk
    """

    if df is None or df.empty:
        return {
            "investment_score": 50,
            "liquidity_score": 50,
            "price_score": 50,
            "growth_score": 50,
            "risk_score": 50
        }

    data = df.copy()

    # -----------------------------
    # Liquidity Score
    # -----------------------------
    transactions = len(data)

    if transactions >= 50:
        liquidity_score = 90
    elif transactions >= 30:
        liquidity_score = 75
    elif transactions >= 15:
        liquidity_score = 60
    elif transactions >= 8:
        liquidity_score = 45
    else:
        liquidity_score = 30

    # -----------------------------
    # Price Score
    # -----------------------------
    if "price" in data.columns and "area" in data.columns:

        # ✅ تعديل: منع القسمة على صفر
        valid = data[(data["area"].notna()) & (data["area"] > 0)]

        if not valid.empty:
            price_per_sqm = (valid["price"] / valid["area"]).mean()
        else:
            price_per_sqm = 0

    else:
        price_per_sqm = 0

    if price_per_sqm < 6000:
        price_score = 85
    elif price_per_sqm < 9000:
        price_score = 70
    elif price_per_sqm < 12000:
        price_score = 60
    else:
        price_score = 45

    # -----------------------------
    # Growth Score
    # -----------------------------
    if "date" in data.columns and "price" in data.columns:

        tmp = data.copy()
        tmp = tmp.dropna(subset=["date", "price"])

        if not tmp.empty:

            tmp["month"] = tmp["date"].astype(str).str[:7]

            monthly = (
                tmp.groupby("month")["price"]
                .mean()
                .sort_index()
            )

            if len(monthly) >= 2:

                growth = monthly.pct_change().median()

                if growth > 0.03:
                    growth_score = 85
                elif growth > 0.01:
                    growth_score = 70
                elif growth > -0.01:
                    growth_score = 55
                else:
                    growth_score = 40
            else:
                growth_score = 50
        else:
            growth_score = 50

    else:
        growth_score = 50

    # -----------------------------
    # Risk Score
    # -----------------------------
    if liquidity_score >= 70:
        risk_score = 30
    elif liquidity_score >= 50:
        risk_score = 45
    else:
        risk_score = 65

    # -----------------------------
    # Final Investment Score
    # -----------------------------
    investment_score = (
        liquidity_score * 0.30
        + price_score * 0.25
        + growth_score * 0.25
        + (100 - risk_score) * 0.20
    )

    investment_score = round(investment_score, 1)

    return {
        "investment_score": investment_score,
        "liquidity_score": liquidity_score,
        "price_score": price_score,
        "growth_score": growth_score,
        "risk_score": risk_score
    }
