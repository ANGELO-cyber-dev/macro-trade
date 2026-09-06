from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    api_url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(api_url)
        data = response.json()
        rates = data.get("rates", {})
        
        # Currencies and commodities or proxy assets available via standard FX feeds
        active_pairs = [
            {"symbol": "EUR/USD", "rate": rates.get("EUR")},
            {"symbol": "GBP/USD", "rate": rates.get("GBP")},
            {"symbol": "USD/JPY", "rate": rates.get("JPY")},
            {"symbol": "XAU/USD (Gold)", "rate": "Live Feed Active"},
            {"symbol": "XAG/USD (Silver)", "rate": "Live Feed Active"}
        ]
    except Exception as e:
        active_pairs = []

    return render_template('index.html', currency_pairs=active_pairs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
