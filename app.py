from datetime import datetime
from flask import Flask, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from database import SessionLocal, init_db
from models import Instrument, MarketQuote
import requests

app = Flask(__name__)
init_db()

# Direct Yahoo Finance API mapping
TICKER_MAP = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "GOLD": "GC=F",
    "OIL": "CL=F",
    "BTC": "BTC-USD",
    "SPX": "^GSPC",
}

def background_live_sync():
    """Lightweight background task to poll live market quotes via API."""
    db = SessionLocal()
    print(f"[{datetime.utcnow().isoformat()}] Fetching live feeds via direct API...")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for internal_ticker, yf_symbol in TICKER_MAP.items():
        instrument = db.query(Instrument).filter_by(ticker=internal_ticker).first()
        if not instrument:
            continue
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yf_symbol}?interval=1d&range=1d"
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                continue
                
            data = response.json()
            result = data["chart"]["result"][0]
            meta = result["meta"]
            
            price = float(meta["regularMarketPrice"])
            previous_close = float(meta.get("chartPreviousClose", price))
            change = ((price - previous_close) / previous_close) * 100 if previous_close > 0 else 0.0

            quote = db.query(MarketQuote).filter_by(instrument_id=instrument.id).first()
            if quote:
                quote.price = price
                quote.change_24h = change
                quote.updated_at = datetime.utcnow()
            else:
                db.add(MarketQuote(
                    instrument_id=instrument.id,
                    price=price,
                    change_24h=change,
                    source="YahooAPI"
                ))
            db.commit()
            print(f"Updated {internal_ticker}: {price} ({change:+.2f}%)")
        except Exception as e:
            db.rollback()
            print(f"Sync error for {internal_ticker}: {e}")
            
    db.close()

# Start background scheduler running every 5 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=background_live_sync, trigger="interval", minutes=5)
scheduler.start()

@app.route("/")
def index():
    db = SessionLocal()
    quotes = db.query(MarketQuote).all()
    db.close()
    return render_template("index.html", quotes=quotes)

@app.route("/api/v1/quotes")
def api_quotes():
    db = SessionLocal()
    quotes = db.query(MarketQuote).all()
    data = [{
        "ticker": q.instrument.ticker,
        "price": float(q.price),
        "change_24h": q.change_24h,
        "updated_at": q.updated_at.isoformat()
    } for q in quotes]
    db.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
