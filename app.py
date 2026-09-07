from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

community_posts = [
    {
        "id": 1,
        "author": "ANGELOFX",
        "pair": "GBP/USD",
        "bias": "Bullish",
        "entry": "1.2650",
        "target": "1.2800",
        "content": "Bouncing off the 4H macro support zone with strong bullish divergence on RSI.",
        "timestamp": "2 hours ago"
    },
    {
        "id": 2,
        "author": "LagosTrader",
        "pair": "EUR/USD",
        "bias": "Bearish",
        "entry": "1.0850",
        "target": "1.0750",
        "content": "Rejection at daily resistance following strong US NFP employment data release.",
        "timestamp": "4 hours ago"
    }
]

def calculate_macro_score():
    return random.randint(68, 85)

@app.route("/")
def index():
    return render_template("index.html", macro_score=calculate_macro_score(), active_page="market")

@app.route("/indicators")
def indicators():
    return render_template("indicators.html", macro_score=calculate_macro_score(), active_page="indicators")

@app.route("/signals")
def signals():
    return render_template("signals.html", macro_score=calculate_macro_score(), active_page="signals")

@app.route("/sizer")
def sizer():
    return render_template("sizer.html", macro_score=calculate_macro_score(), active_page="sizer")

@app.route("/tracker")
def tracker():
    return render_template("tracker.html", macro_score=calculate_macro_score(), active_page="tracker")

@app.route("/community")
def community():
    return render_template("community.html", macro_score=calculate_macro_score(), active_page="community", posts=community_posts)

@app.route("/post_setup", methods=["POST"])
def post_setup():
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
