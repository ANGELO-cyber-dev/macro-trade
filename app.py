from flask import Flask, render_template, request, redirect, url_for
import os
import requests

app = Flask(__name__)
app.secret_key = "macro_trade_secure_key"

FINNHUB_KEY = os.environ.get("FINNHUB_API_KEY", "")

community_posts = [
    {
        "id": 1,
        "author": "ANGELOFX",
        "pair": "XAU/USD",
        "bias": "Bullish",
        "entry": "2510.00",
        "target": "2550.00",
        "content": "Central bank accumulation is driving structural breakouts on the daily timeframe.",
        "timestamp": "2 hours ago"
    }
]

def calculate_macro_score():
    return 78

def get_finnhub_price(symbol, fallback):
    if not FINNHUB_KEY:
        return fallback
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}"
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            data = res.json()
            price = data.get("c")
            if price and price > 0:
                return f"{price:,.4f}" if price < 10 else f"{price:,.2f}"
    except Exception:
        pass
    return fallback

@app.route("/")
def index():
    try:
        eur_price = get_finnhub_price("OANDA:EUR_USD", "1.1045")
        gbp_price = get_finnhub_price("OANDA:GBP_USD", "1.3120")
        jpy_price = get_finnhub_price("USD_JPY", "146.85")
        chf_price = get_finnhub_price("OANDA:USD_CHF", "0.8850")
        cad_price = get_finnhub_price("OANDA:USD_CAD", "1.3540")
        gold_price = get_finnhub_price("OANDA:XAU_USD", "2,520.40")
        btc_price = get_finnhub_price("BINANCE:BTCUSDT", "59,400.00")
    except Exception:
        eur_price, gbp_price, jpy_price, chf_price, cad_price, gold_price, btc_price = "1.1045", "1.3120", "146.85", "0.8850", "1.3540", "2,520.40", "59,400.00"

    live_assets = [
        {"ticker": "EUR/USD", "name": "Euro / US Dollar", "price": eur_price, "change": "+0.15%"},
        {"ticker": "GBP/USD", "name": "British Pound / US Dollar", "price": gbp_price, "change": "+0.22%"},
        {"ticker": "USD/JPY", "name": "USD Dollar / Japanese Yen", "price": jpy_price, "change": "-0.18%"},
        {"ticker": "USD/CHF", "name": "USD Dollar / Swiss Franc", "price": chf_price, "change": "+0.05%"},
        {"ticker": "USD/CAD", "name": "USD Dollar / Canadian Dollar", "price": cad_price, "change": "-0.12%"},
        {"ticker": "AUD/USD", "name": "Australian Dollar / US Dollar", "price": "0.6720", "change": "+0.31%"},
        {"ticker": "NZD/USD", "name": "New Zealand Dollar / US Dollar", "price": "0.6150", "change": "+0.19%"},
        {"ticker": "XAU/USD", "name": "Spot Gold", "price": gold_price, "change": "+0.45%"},
        {"ticker": "XAG/USD", "name": "Spot Silver", "price": "29.15", "change": "+0.60%"},
        {"ticker": "BTC/USD", "name": "Bitcoin / US Dollar", "price": btc_price, "change": "+1.25%"},
        {"ticker": "US30", "name": "Wall Street 30 Index", "price": "41,150.00", "change": "+0.35%"},
        {"ticker": "NAS100", "name": "Nasdaq 100 Index", "price": "19,820.00", "change": "+0.78%"}
    ]

    return render_template("index.html", macro_score=calculate_macro_score(), active_page="market", assets=live_assets)

@app.route("/indicators")
def indicators():
    macro_indicators = [
        {"id": "CPIAUCSL", "name": "Consumer Price Index (All Urban)", "category": "Inflation", "freq": "Monthly"},
        {"id": "UNRATE", "name": "Civilian Total Unemployment Rate", "category": "Labor Market", "freq": "Monthly"},
        {"id": "GDP", "name": "US Gross Domestic Product", "category": "Growth", "freq": "Quarterly"},
        {"id": "FEDFUNDS", "name": "Federal Funds Effective Rate", "category": "Interest Rates", "freq": "Monthly"},
        {"id": "DGS10", "name": "10-Yr Treasury Constant Maturity Rate", "category": "Interest Rates", "freq": "Daily"},
        {"id": "M2SL", "name": "M2 Money Supply", "category": "Liquidity", "freq": "Monthly"}
    ]
    return render_template("indicators.html", macro_score=calculate_macro_score(), active_page="indicators", indicators=macro_indicators)

@app.route("/signals")
def signals():
    complete_signals = [
        {"type": "LONG SETUP", "badge_class": "success", "pair": "EUR/USD (Euro Major)", "title": "ECB Divergence & Support Test", "desc": "Eurozone trade surplus and resilient services PMI underpin structural bids.", "confidence": "82%", "timeframe": "Intraday"},
        {"type": "SHORT SETUP", "badge_class": "danger", "pair": "GBP/USD (Cable)", "title": "UK Fiscal Headwinds Resistance", "desc": "Stalling wage growth and softer retail metrics weigh on the Sterling.", "confidence": "79%", "timeframe": "Swing"},
        {"type": "LONG SETUP", "badge_class": "success", "pair": "USD/JPY (Ninja)", "title": "BoJ Rate Stance Carry Continuation", "desc": "Yield differentials favor long USD carry trades on pullbacks.", "confidence": "85%", "timeframe": "Position"},
        {"type": "LONG SETUP", "badge_class": "success", "pair": "AUD/USD (Aussie)", "title": "Commodity Super-Cycle Bounce", "desc": "Industrial metal demand recovery supports high-beta Oceania currency.", "confidence": "77%", "timeframe": "Multi-Day"},
        {"type": "LONG SETUP", "badge_class": "success", "pair": "XAU/USD (Gold)", "title": "Gold Safe-Haven Breakout", "desc": "Central bank reserve accumulation and sticky US inflation drive bullion higher.", "confidence": "84%", "timeframe": "Swing"},
        {"type": "LONG SETUP", "badge_class": "success", "pair": "BTC/USD (Crypto)", "title": "Bitcoin Institutional Accumulation", "desc": "Strong ETF net inflows and macro liquidity expansion support bullish continuation.", "confidence": "81%", "timeframe": "Multi-Day"}
    ]
    return render_template("signals.html", macro_score=calculate_macro_score(), active_page="signals", signals=complete_signals)

@app.route("/sizer")
def sizer():
    return render_template("sizer.html", macro_score=calculate_macro_score(), active_page="sizer")

@app.route("/tracker")
def tracker():
    return render_template("tracker.html", macro_score=calculate_macro_score(), active_page="tracker")

@app.route("/community", methods=["GET", "POST"])
def community():
    try:
        if request.method == "POST":
            author = request.form.get("author", "Anonymous Trader")
            pair = request.form.get("pair", "EUR/USD")
            bias = request.form.get("bias", "Bullish")
            entry = request.form.get("entry", "0.0000")
            target = request.form.get("target", "0.0000")
            content = request.form.get("content", "")
            if content:
                community_posts.insert(0, {
                    "id": len(community_posts) + 1,
                    "author": author,
                    "pair": pair,
                    "bias": bias,
                    "entry": entry,
                    "target": target,
                    "content": content,
                    "timestamp": "Just now"
                })
            return redirect(url_for("community"))
    except Exception:
        pass
    
    return render_template("community.html", macro_score=calculate_macro_score(), active_page="community", posts=community_posts)

@app.route("/comn")
def comn_alias():
    return redirect(url_for("community"))

@app.errorhandler(500)
def internal_error(e):
    return redirect(url_for("index"))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
