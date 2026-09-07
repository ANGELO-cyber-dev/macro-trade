from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf

app = Flask(__name__)

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

@app.route("/")
def index():
    tickers = {
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "USDJPY=X",
        "USD/CHF": "USDCHF=X",
        "USD/CAD": "USDCAD=X",
        "XAU/USD": "GC=F",
        "XAG/USD": "SI=F",
        "BTC/USD": "BTC-USD",
        "US30": "^DJI",
        "NAS100": "^NDX"
    }
    
    names = {
        "EUR/USD": "Euro / US Dollar",
        "GBP/USD": "British Pound / US Dollar",
        "USD/JPY": "US Dollar / Japanese Yen",
        "USD/CHF": "US Dollar / Swiss Franc",
        "USD/CAD": "US Dollar / Canadian Dollar",
        "XAU/USD": "Spot Gold",
        "XAG/USD": "Spot Silver",
        "BTC/USD": "Bitcoin / US Dollar",
        "US30": "Wall Street 30 Index",
        "NAS100": "Nasdaq 100 Index"
    }

    live_assets = []
    for ticker_key, symbol in tickers.items():
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period="2d")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                change_pct = ((current_price - prev_close) / prev_close) * 100
                change_str = f"+{change_pct:.2f}%" if change_pct >= 0 else f"{change_pct:.2f}%"
                
                if ticker_key in ["US30", "NAS100", "BTC/USD", "XAU/USD", "XAG/USD"]:
                    price_str = f"{current_price:,.2f}"
                else:
                    price_str = f"{current_price:.4f}"
            else:
                price_str, change_str = "N/A", "0.00%"
        except Exception:
            price_str, change_str = "1.0000", "+0.00%"
            
        live_assets.append({
            "ticker": ticker_key,
            "name": names[ticker_key],
            "price": price_str,
            "change": change_str
        })

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
    if request.method == "POST":
        author = request.form.get("author", "Anonymous Trader")
        pair = request.form.get("pair", "EUR/USD")
        bias = request.form.get("bias", "Bullish")
        entry = request.form.get("entry", "0.0000")
        target = request.form.get("target", "0.0000")
        content = request.form.get("content", "")
        if content:
            community_posts.insert(0, {"id": len(community_posts) + 1, "author": author, "pair": pair, "bias": bias, "entry": entry, "target": target, "content": content, "timestamp": "Just now"})
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
