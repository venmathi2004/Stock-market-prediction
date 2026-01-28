# app.py
import os  # ✅ VERY IMPORTANT (ERROR FIX)
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from predict_utils import (
    fetch_latest_data,
    preprocess_input,
    predict_multi_day
)

# ---------------- APP INIT ----------------
app = Flask(__name__)
CORS(app)

# ---------------- ROUTES ----------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stock-prices")
def stock_prices():
    return render_template("stock-prices.html")

@app.route("/prediction")
def prediction_page():
    return render_template("prediction.html")

# ---------------- API ----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        stock = data.get("stock", "AAPL")
        days = int(data.get("days", 5))

        df = fetch_latest_data(stock)
        input_seq = preprocess_input(df)
        predictions = predict_multi_day(input_seq, days)

        return jsonify({
            "stock": stock,
            "days": days,
            "predictions": predictions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- MAIN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
