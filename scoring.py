def calculate_macro_score(inflation_val, labor_val, growth_val, liquidity_val):
    """
    Computes a transparent macro bias score (-100 to +100) 
    and returns component breakdown for institutional explainability.
    """
    # Normalized component weights (Total = 1.0)
    w_inflation = 0.30
    w_labor = 0.25
    w_growth = 0.25
    w_liquidity = 0.20

    # Simplified scoring logic mapping indicators to a normalized scale (-1 to 1)
    # In production, these compare actuals vs consensus or trend baselines.
    inf_score = max(min(-inflation_val * 10, 1.0), -1.0) # High inflation hurts risk/bonds, helps commodities
    lab_score = max(min(labor_val * 5, 1.0), -1.0)       # Strong labor supports growth/currency
    gro_score = max(min(growth_val * 10, 1.0), -1.0)     # Positive GDP growth supports equities
    liq_score = max(min(liquidity_val * 8, 1.0), -1.0)   # Expanding liquidity supports risk assets/crypto

    composite = (
        (inf_score * w_inflation) +
        (lab_score * w_labor) +
        (gro_score * w_growth) +
        (liq_score * w_liquidity)
    ) * 100

    bias = "BULLISH" if composite > 15 else ("BEARISH" if composite < -15 else "NEUTRAL")

    return {
        "composite_score": round(composite, 2),
        "bias": bias,
        "components": {
            "inflation_impact": round(inf_score * 100, 1),
            "labor_market": round(lab_score * 100, 1),
            "economic_growth": round(gro_score * 100, 1),
            "liquidity_conditions": round(liq_score * 100, 1)
        }
    }
