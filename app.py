from flask import Flask, render_template, request, redirect, url_for
import os
import requests

app = Flask(__name__)
app.secret_key = "macro_trade_secure_key"

TWELVE_KEY = os.environ.get("TWELVE_API_KEY", "8af3a193bbdc405fbae305f525b9543d")

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

def get_twelve_price(symbol, fallback):
    if not TWELVE_KEY:
        return fallback
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_KEY}"
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            data = res.json()
            if "price" in data:
                price = float(data["price"])
                return f"{price:,.4f}" if price < 10 else f"{price:,.2f}"
    except Exception:
        pass
    return fallback

@app.route("/")
def index():
    try:
        eur_usd = get_twelve_price("EUR/USD", "1.1045")
        gbp_usd = get_twelve_price("GBP/USD", "1.3120")
        usd_jpy = get_twelve_price("USD/JPY", "146.85")
        usd_chf = get_twelve_price("USD/CHF", "0.8850")
        usd_cad = get_twelve_price("USD/CAD", "1.3540")
        aud_usd = get_twelve_price("AUD/USD", "0.6720")
        nzd_usd = get_twelve_price("NZD/USD", "0.6150")
        eur_gbp = get_twelve_price("EUR/GBP", "0.8520")
        eur_jpy = get_twelve_price("EUR/JPY", "158.40")
        gbp_jpy = get_twelve_price("GBP/JPY", "192.50")
        xau_usd = get_twelve_price("XAU/USD", "2,520.40")
        xag_usd = get_twelve_price("XAG/USD", "29.15")
        btc_usd = get_twelve_price("BTC/USD", "59,400.00")
        eth_usd = get_twelve_price("ETH/USD", "2,650.00")
    except Exception:
        eur_usd, gbp_usd, usd_jpy, usd_chf, usd_cad, aud_usd, nzd_usd = "1.1045", "1.3120", "146.85", "0.8850", "1.3540", "0.6720", "0.6150"
        eur_gbp, eur_jpy, gbp_jpy, xau_usd, xag_usd, btc_usd, eth_usd = "0.8520", "158.40", "192.50", "2,520.40", "29.15", "59,400.00", "2,650.00"

    live_assets = [
        {"ticker": "EUR/USD", "name": "Euro / US Dollar", "price": eur_usd, "change": "+0.15%"},
        {"ticker": "GBP/USD", "name": "British Pound / US Dollar", "price": gbp_usd, "change": "+0.22%"},
        {"ticker": "USD/JPY", "name": "USD Dollar / Japanese Yen", "price": usd_jpy, "change": "-0.18%"},
        {"ticker": "USD/CHF", "name": "USD Dollar / Swiss Franc", "price": usd_chf, "change": "+0.05%"},
        {"ticker": "USD/CAD", "name": "USD Dollar / Canadian Dollar", "price": usd_cad, "change": "-0.12%"},
        {"ticker": "AUD/USD", "name": "Australian Dollar / US Dollar", "price": aud_usd, "change": "+0.31%"},
        {"ticker": "NZD/USD", "name": "New Zealand Dollar / US Dollar", "price": nzd_usd, "change": "+0.19%"},
        {"ticker": "EUR/GBP", "name": "Euro / British Pound", "price": eur_gbp, "change": "-0.08%"},
        {"ticker": "EUR/JPY", "name": "Euro / Japanese Yen", "price": eur_jpy, "change": "+0.12%"},
        {"ticker": "GBP/JPY", "name": "British Pound / Japanese Yen", "price": gbp_jpy, "change": "+0.25%"},
        {"ticker": "XAU/USD", "name": "Spot Gold", "price": xau_usd, "change": "+0.45%"},
        {"ticker": "XAG/USD", "name": "Spot Silver", "price": xag_usd, "change": "+0.60%"},
        {"ticker": "BTC/USD", "name": "Bitcoin / US Dollar", "price": btc_usd, "change": "+1.25%"},
        {"ticker": "ETH/USD", "name": "Ethereum / US Dollar", "price": eth_usd, "change": "+1.80%"},
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
