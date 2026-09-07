from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory store for community posts to ensure persistence during session
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
    },
    {
        "id": 2,
        "author": "MacroTrader_NG",
        "pair": "EUR/USD",
        "bias": "Bullish",
        "entry": "1.1020",
        "target": "1.1150",
        "content": "Narrower US-Eurozone GDP differentials supporting medium-term support.",
        "timestamp": "4 hours ago"
    }
]

def calculate_macro_score():
    return 78

@app.route("/")
def index():
    live_assets = [
        {"ticker": "EUR/USD", "name": "Euro / US Dollar", "price": "1.1045", "change": "+0.15%"},
        {"ticker": "GBP/USD", "name": "British Pound / US Dollar", "price": "1.3120", "change": "+0.22%"},
        {"ticker": "USD/JPY", "name": "US Dollar / Japanese Yen", "price": "146.85", "change": "-0.18%"},
        {"ticker": "USD/CHF", "name": "US Dollar / Swiss Franc", "price": "0.8850", "change": "+0.05%"},
        {"ticker": "USD/CAD", "name": "US Dollar / Canadian Dollar", "price": "1.3540", "change": "-0.12%"},
        {"ticker": "XAU/USD", "name": "Spot Gold", "price": "2,520.40", "change": "+0.45%"},
        {"ticker": "XAG/USD", "name": "Spot Silver", "price": "29.15", "change": "+0.60%"},
        {"ticker": "BTC/USD", "name": "Bitcoin / US Dollar", "price": "59,400.00", "change": "+1.25%"},
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
        {
            "type": "LONG SETUP",
            "badge_class": "success",
            "pair": "XAU/USD (Gold)",
            "title": "Gold Safe-Haven Breakout",
            "desc": "Central bank reserve accumulation and sticky US inflation drive bullion higher.",
            "confidence": "84%",
            "timeframe": "Swing / Multi-Week"
        },
        {
            "type": "LONG SETUP",
            "badge_class": "success",
            "pair": "XAG/USD (Silver)",
            "title": "Industrial & Precious Demand",
            "desc": "Green energy manufacturing requirements coupled with gold parity momentum.",
            "confidence": "80%",
            "timeframe": "Swing"
        },
        {
            "type": "LONG SETUP",
            "badge_class": "success",
            "pair": "BTC/USD (Crypto)",
            "title": "Bitcoin Institutional Accumulation",
            "desc": "Strong ETF net inflows and macro liquidity expansion support bullish continuation.",
            "confidence": "81%",
            "timeframe": "Multi-Day"
        },
        {
            "type": "LONG SETUP",
            "badge_class": "success",
            "pair": "EUR/USD",
            "title": "Euro Area Consolidation",
            "desc": "Narrower US-Eurozone GDP differentials supporting medium-term structural support.",
            "confidence": "77%",
            "timeframe": "Swing"
        },
        {
            "type": "LONG SETUP",
            "badge_class": "success",
            "pair": "GBP/USD",
            "title": "Cable Resiliency Test",
            "desc": "Higher-timeframe technical support holds firm ahead of UK fiscal data releases.",
            "confidence": "76%",
            "timeframe": "Multi-Day"
        },
        {
            "type": "SHORT SETUP",
            "badge_class": "danger",
            "pair": "USD/JPY",
            "title": "Intervention Risk Watch",
            "desc": "Wide interest rate differentials balanced against potential Bank of Japan rate shifts.",
            "confidence": "72%",
            "timeframe": "Intraday / Swing"
        },
        {
            "type": "SHORT SETUP",
            "badge_class": "danger",
            "pair": "USD/CAD",
            "title": "Oil-Led Pullback",
            "desc": "Stable crude oil futures and sticky inflation metrics sustain Loonie upside.",
            "confidence": "75%",
            "timeframe": "Multi-Day"
        },
        {
            "type": "NEUTRAL / RANGE",
            "badge_class": "secondary",
            "pair": "USD/CHF",
            "title": "Consolidation",
            "desc": "Safe-haven stabilization amidst steady Swiss National Bank monetary policy.",
            "confidence": "68%",
            "timeframe": "Range Bound"
        },
        {
            "type": "LONG SETUP",
            "badge_class": "success",
            "pair": "NZD/USD",
            "title": "Dairy & Rate Support",
            "desc": "Dairy export pricing recovery and steady RBNZ hawkish stance drive Kiwi gains.",
            "confidence": "78%",
            "timeframe": "Swing / Multi-Week"
        },
        {
            "type": "LONG SETUP",
            "badge_class": "success",
            "pair": "US30 (Wall Street 30)",
            "title": "Blue-Chip Industrial Momentum",
            "desc": "Corporate earnings resilience and soft-landing narrative boost equity indices.",
            "confidence": "82%",
            "timeframe": "Multi-Day"
        },
        {
            "type": "LONG SETUP",
            "badge_class": "success",
            "pair": "NAS100 (Nasdaq)",
            "title": "Tech Sector Liquidity Flow",
            "desc": "AI infrastructure spending and growth stock cash flows drive upper channel expansion.",
            "confidence": "85%",
            "timeframe": "Swing"
        }
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
        
    return render_template("community.html", macro_score=calculate_macro_score(), active_page="community", posts=community_posts)

@app.route("/comn")
def comn_alias():
    return redirect(url_for("community"))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
