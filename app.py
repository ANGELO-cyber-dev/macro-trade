from flask import Flask, render_template
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # 1. Fetch live Forex rates
    fx_url = "https://open.er-api.com/v6/latest/USD"
    try:
        fx_resp = requests.get(fx_url, timeout=5)
        fx_data = fx_resp.json()
        rates = fx_data.get("rates", {})
    except Exception:
        rates = {}

    eur_rate = rates.get("EUR", 0)
    gbp_rate = rates.get("GBP", 0)
    jpy_rate = rates.get("JPY", 0)

    # Calculate mock bid/ask style active rates from fetched base data
    active_pairs = [
        {"symbol": "EUR/USD", "rate": f"{1 / eur_rate:.4f}" if eur_rate else "1.0850", "signal": "Strong Bullish (+88)"},
        {"symbol": "GBP/USD", "rate": f"{1 / gbp_rate:.4f}" if gbp_rate else "1.2640", "signal": "Strong Bullish (+82)"},
        {"symbol": "USD/JPY", "rate": f"{jpy_rate:.2f}" if jpy_rate else "155.20", "signal": "Neutral (+52)"},
        {"symbol": "XAU/USD", "rate": "$2,345.50", "signal": "Strong Bullish (+91)"},
        {"symbol": "XAG/USD", "rate": "$29.65", "signal": "Strong Bullish (+82)"}
    ]

    # 2. Fetch official 2Y Yield from FRED (using public series DGS2)
    fred_api_key = os.environ.get("FRED_API_KEY", "abcdef1234567890abcdef1234567890") # Replace or add key in Render env vars if needed
    fred_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=DGS2&api_key={fred_api_key}&file_type=json"
    
    yield_val = "4.34%"
    try:
        fred_resp = requests.get(fred_url, timeout=5)
        fred_data = fred_resp.json()
        observations = fred_data.get("observations", [])
        # Get the latest valid observation value
        for obs in reversed(observations):
            if obs.get("value") != ".":
                yield_val = f"{obs.get('value')}%"
                break
    except Exception:
        pass

    return render_template('index.html', currency_pairs=active_pairs, fred_yield=yield_val)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
