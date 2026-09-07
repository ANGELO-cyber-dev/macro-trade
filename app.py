from datetime import datetime
from flask import Flask, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import joinedload
from database import SessionLocal, init_db
from models import Instrument, MarketQuote, MacroIndicator, AssetClass
from scoring import calculate_macro_score
import requests

app = Flask(__name__)
init_db()

def seed_production_data():
    db = SessionLocal()
    if db.query(Instrument.id).first() is not None:
        db.close()
        return

    instruments = [
        Instrument(ticker="EUR/USD", name="Euro / US Dollar", asset_class=AssetClass.FX),
        Instrument(ticker="GBP/USD", name="British Pound / US Dollar", asset_class=AssetClass.FX),
        Instrument(ticker="USD/JPY", name="US Dollar / Japanese Yen", asset_class=AssetClass.FX),
        Instrument(ticker="GOLD", name="Gold Futures", asset_class=AssetClass.COMMODITIES),
        Instrument(ticker="OIL", name="Crude Oil Futures", asset_class=AssetClass.COMMODITIES),
        Instrument(ticker="BTC", name="Bitcoin", asset_class=AssetClass.CRYPTO),
        Instrument(ticker="SPX", name="S&P 500 Index", asset_class=AssetClass.INDICES),
    ]
    
    macro_indicators = [
        MacroIndicator(series_id="CPIAUCSL", name="Consumer Price Index (CPI)", category="Inflation", frequency="Monthly"),
        MacroIndicator(series_id="PAYEMS", name="Nonfarm Payrolls (NFP)", category="Labor", frequency="Monthly"),
        MacroIndicator(series_id="UNRATE", name="Unemployment Rate", category="Labor", frequency="Monthly"),
        MacroIndicator(series_id="GDP", name="Gross Domestic Product", category="Growth", frequency="Quarterly"),
        MacroIndicator(series_id="M2SL", name="M2 Money Supply", category="Liquidity", frequency="Monthly")
    ]
    
    db.add_all(instruments)
    db.add_all(macro_indicators)
    db.commit()
    db.close()

seed_production_data()

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
    db = SessionLocal()
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
            meta = data["chart"]["result"][0]["meta"]
            price = float(meta["regularMarketPrice"])
            previous_close = float(meta.get("chartPreviousClose", price))
            change = ((price - previous_close) / previous_close) * 100 if previous_close > 0 else 0.0

            quote = db.query(MarketQuote).filter_by(instrument_id=instrument.id).first()
            if quote:
                quote.price = price
                quote.change_24h = change
                quote.updated_at = datetime.utcnow()
            else:
                db.add(MarketQuote(instrument_id=instrument.id, price=price, change_24h=change, source="YahooAPI"))
            db.commit()
        except Exception:
            db.rollback()
    db.close()

background_live_sync()

scheduler = BackgroundScheduler()
scheduler.add_job(func=background_live_sync, trigger="interval", minutes=5)
scheduler.start()

@app.route("/")
def index():
    db = SessionLocal()
    quotes = db.query(MarketQuote).options(joinedload(MarketQuote.instrument)).all()
    
    # Generate mock macro scoring breakdown for demonstration of the transparent engine
    sample_macro_score = calculate_macro_score(inflation_val=0.3, labor_val=0.2, growth_val=0.1, liquidity_val=0.4)
    
    db.close()
    return render_template("index.html", quotes=quotes, macro_score=sample_macro_score)

@app.route("/api/v1/scoring")
def api_scoring():
    # Transparent API endpoint exposing macro score metrics
    score_data = calculate_macro_score(inflation_val=0.3, labor_val=0.2, growth_val=0.1, liquidity_val=0.4)
    return jsonify(score_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
