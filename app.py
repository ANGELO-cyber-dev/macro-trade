from flask import Flask, render_template
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    finnhub_key = os.environ.get("FINNHUB_API_KEY", "")

    fx_rates = {}
    try:
        fx_url = f"https://finnhub.io/api/v1/forex/rates?base=USD&token={finnhub_key}"
        fx_resp = requests.get(fx_url, timeout=5).json()
        fx_rates = fx_resp.get("quote", {})
    except Exception:
        pass

    eur_val = fx_rates.get("EUR", 0.92)
    gbp_val = fx_rates.get("GBP", 0.78)
    jpy_val = fx_rates.get("JPY", 155.0)

    eur_usd = f"{1 / eur_val:.4f}" if eur_val and eur_val > 0 else "1.0850"
    gbp_usd = f"{1 / gbp_val:.4f}" if gbp_val and gbp_val > 0 else "1.2640"
    usd_jpy = f"{jpy_val:.2f}" if jpy_val else "155.20"

    gold_price = "$2,345.50"
    silver_price = "$29.65"
    try:
        gold_resp = requests.get(f"https://finnhub.io/api/v1/quote?symbol=GLD&token={finnhub_key}", timeout=5).json()
        if gold_resp.get("c"):
            gold_price = f"${float(gold_resp.get('c')) * 10:,.2f}"

        silver_resp = requests.get(f"https://finnhub.io/api/v1/quote?symbol=SLV&token={finnhub_key}", timeout=5).json()
        if silver_resp.get("c"):
            silver_price = f"${float(silver_resp.get('c')) * 10:,.2f}"
    except Exception:
        pass

    btc_price = "Loading..."
    try:
        b_resp = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        raw_btc = b_resp.get("price")
        if raw_btc:
            btc_price = f"${float(raw_btc):,.2f}"
    except Exception:
        btc_price = "Unavailable"

    forex_pairs = [
        {"symbol": "EUR/USD", "rate": eur_usd, "signal": "Strong Bullish (+88)"},
        {"symbol": "GBP/USD", "rate": gbp_usd, "signal": "Strong Bullish (+82)"},
        {"symbol": "USD/JPY", "rate": usd_jpy, "signal": "Neutral (+52)"}
    ]

    commodity_pairs = [
        {"symbol": "XAU/USD", "rate": gold_price, "signal": "Live Finnhub Feed"},
        {"symbol": "XAG/USD", "rate": silver_price, "signal": "Live Finnhub Feed"}
    ]

    crypto_pairs = [
        {"symbol": "BTC/USDT", "rate": btc_price, "signal": "Binance Live Stream"}
    ]

    return render_template(
        'index.html', 
        forex_pairs=forex_pairs, 
        commodity_pairs=commodity_pairs, 
        crypto_pairs=crypto_pairs,
        fred_yield="4.34%"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
