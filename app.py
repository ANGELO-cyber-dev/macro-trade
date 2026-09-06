from flask import Flask, jsonify, render_template, request
import requests
import csv
from datetime import datetime

app = Flask(__name__)

FRED_API_KEY = "6e86d61a91271a60ef92da75259fb7b3"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/macro")
def get_macro():
    indicators = {
        "CPI (Inflation)": "CPIAUCSL",
        "NFP (Payrolls)": "PAYEMS",
        "Interest Rate": "FEDFUNDS",
        "JOLTS Openings": "JTSJOL"
    }
    data = {}
    vals = {}
    for name, series_id in indicators.items():
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json&sort_order=desc&limit=2"
        try:
            res = requests.get(url).json()
            obs_list = res["observations"]
            latest = float(obs_list[0]["value"])
            prev = float(obs_list[1]["value"])
            date = obs_list[0]["date"]
            
            trend = "Bullish for USD" if latest > prev else "Bearish for USD"
            if name == "Interest Rate":
                trend = "High Yield Support" if latest > 3.0 else "Low Yield Environment"

            data[name] = {"value": latest, "date": date, "trend": trend}
        except Exception:
            data[name] = {"value": "N/A", "date": "N/A", "trend": "Neutral"}
            
    return jsonify(data)

@app.route("/api/analyze", methods=["POST"])
def analyze_trades():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    try:
        decoded_file = file.stream.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        total_trades = 0
        winning_trades = 0
        total_hold_winner = 0
        total_hold_loser = 0
        losing_trades = 0
        symbol_profits = {}
        
        for row in reader:
            try:
                profit = float(row.get('Profit', 0))
                symbol = row.get('Symbol', 'UNKNOWN')
                open_time = datetime.strptime(row['Open Time'], '%Y-%m-%d %H:%M:%S')
                close_time = datetime.strptime(row['Close Time'], '%Y-%m-%d %H:%M:%S')
                
                hold_duration = (close_time - open_time).total_seconds() / 3600
                
                total_trades += 1
                symbol_profits[symbol] = symbol_profits.get(symbol, 0) + profit
                
                if profit > 0:
                    winning_trades += 1
                    total_hold_winner += hold_duration
                else:
                    losing_trades += 1
                    total_hold_loser += hold_duration
            except Exception:
                continue
                
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        avg_hold_winner = total_hold_winner / winning_trades if winning_trades > 0 else 0
        avg_hold_loser = total_hold_loser / losing_trades if losing_trades > 0 else 0
        
        best_symbol = max(symbol_profits, key=symbol_profits.get) if symbol_profits else "N/A"
        worst_symbol = min(symbol_profits, key=symbol_profits.get) if symbol_profits else "N/A"
        
        return jsonify({
            "total_trades": total_trades,
            "win_rate": round(win_rate, 2),
            "avg_hold_winner_hours": round(avg_hold_winner, 2),
            "avg_hold_loser_hours": round(avg_hold_loser, 2),
            "best_symbol": best_symbol,
            "worst_symbol": worst_symbol
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
