from flask import Flask, render_template
import os
import requests
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def index():
    finnhub_key = os.environ.get("FINNHUB_API_KEY", "Daetc89r01qqo7nu2ucgdaetc89r01qqo7nu2ud0")

    # 1. Fetch live rates for all major Forex pairs via Frankfurter API
    eur_usd, gbp_usd, usd_jpy, aud_usd, usd_cad, usd_chf, nzd_usd = "1.0850", "1.2640", "155.20", "0.6550", "1.3650", "0.8900", "0.6100"
    try:
        fx_resp = requests.get("https://api.frankfurter.app/latest?from=USD", timeout=5).json()
        rates = fx_resp.get("rates", {})
        if "EUR" in rates: eur_usd = f"{1 / rates['EUR']:.4f}"
        if "GBP" in rates: gbp_usd = f"{1 / rates['GBP']:.4f}"
        if "JPY" in rates: usd_jpy = f"{rates['JPY']:.2f}"
        if "AUD" in rates: aud_usd = f"{1 / rates['AUD']:.4f}"
        if "CAD" in rates: usd_cad = f"{rates['CAD']:.4f}"
        if "CHF" in rates: usd_chf = f"{rates['CHF']:.4f}"
        if "NZD" in rates: nzd_usd = f"{1 / rates['NZD']:.4f}"
    except Exception:
        pass

    # 2. Fetch live Gold & Silver via yfinance
    gold_price = "$4,430.00"
    silver_price = "$66.15"
    try:
        g_data = yf.Ticker("GC=F").history(period="1d")
        if not g_data.empty and g_data['Close'].iloc[-1] > 100:
            gold_price = f"${g_data['Close'].iloc[-1]:,.2f}"
            
        s_data = yf.Ticker("SI=F").history(period="1d")
        if not s_data.empty and s_data['Close'].iloc[-1] > 1:
            silver_price = f"${s_data['Close'].iloc[-1]:,.2f}"
    except Exception:
        pass

    # 3. Fetch live BTC via Binance Public API
    btc_price = "Loading..."
    try:
        b_resp = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        raw_btc = b_resp.get("price")
        if raw_btc:
            btc_price = f"${float(raw_btc):,.2f}"
    except Exception:
        btc_price = "Unavailable"

    # 4. Fetch live Economic Calendar from Finnhub API
    news_items = []
    try:
        cal_url = f"https://finnhub.io/api/v1/calendar/economic?token={finnhub_key}"
        cal_resp = requests.get(cal_url, timeout=5).json()
        economic_events = cal_resp.get("economicCalendar", [])[:6]
        for event in economic_events:
            news_items.append({
                "time": f"{event.get('country', 'USD')} - {event.get('time', 'Scheduled')}",
                "title": event.get('event', 'Macro Event'),
                "impact": f"Impact: {event.get('impact', 'Normal')} | Forecast: {event.get('estimate', 'N/A')}"
            })
    except Exception:
        pass

    if not news_items:
        news_items = [
            {"time": "Global - Live", "title": "Syncing Economic Calendar Feed...", "impact": "Impact: Normal | Forecast: N/A"}
        ]

    forex_pairs = [
        {"symbol": "EUR/USD", "rate": eur_usd, "signal": "Bullish Bias (ECB Hawkish / Fed Hold)"},
        {"symbol": "GBP/USD", "rate": gbp_usd, "signal": "Neutral-Bullish (UK Growth Resilient)"},
        {"symbol": "USD/JPY", "rate": usd_jpy, "signal": "Bearish USD (Yields Capped)"},
        {"symbol": "AUD/USD", "rate": aud_usd, "signal": "Bullish (Commodity Linked Momentum)"},
        {"symbol": "USD/CAD", "rate": usd_cad, "signal": "Neutral (Oil & BOC Divergence)"},
        {"symbol": "USD/CHF", "rate": usd_chf, "signal": "Balanced Safe Haven Flows"},
        {"symbol": "NZD/USD", "rate": nzd_usd, "signal": "Bullish (Dairy & RBNZ Policy)"}
    ]

    commodity_pairs = [
        {"symbol": "XAU/USD", "rate": gold_price, "signal": "Strong Bullish (Inflation Hedge)"},
        {"symbol": "XAG/USD", "rate": silver_price, "signal": "Bullish (Industrial Demand)"}
    ]

    crypto_pairs = [
        {"symbol": "BTC/USDT", "rate": btc_price, "signal": "Risk-On Liquidity Stream"}
    ]

    fred_snapshot = [
        {"title": "CPI", "value": "2.9%", "desc": "Consumer inflation", "trend": "+0.2%"},
        {"title": "Fed Rate", "value": "5.25%", "desc": "Federal funds rate", "trend": "Hold"},
        {"title": "2Y Treasury", "value": "4.34%", "desc": "US 2-year yield", "trend": "-0.04"},
        {"title": "NFP Jobs", "value": "142K", "desc": "Monthly payroll change", "trend": "Beaten"},
        {"title": "Unemployment", "value": "4.2%", "desc": "US unemployment rate", "trend": "+0.1%"}
    ]

    return render_template(
        'index.html', 
        forex_pairs=forex_pairs, 
        commodity_pairs=commodity_pairs, 
        crypto_pairs=crypto_pairs,
        news_items=news_items,
        fred_snapshot=fred_snapshot,
        fred_yield="4.34%",
        macro_title="Liquidity Expansion & Risk-On Flow",
        policy_stance="Neutral / Rate Cuts Anticipated"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
