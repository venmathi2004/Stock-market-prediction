# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import tensorflow as tf
import json
# from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from predict_utils import fetch_latest_data, preprocess_input, predict_multi_day

app = Flask(__name__)
CORS(app)

# ✅ Home page with named endpoint
@app.route("/", endpoint="index")
def home():
    return render_template("index.html")

# Stock Prices page
@app.route("/stock-prices")
def stock_prices():
    return render_template("stock-prices.html")

# Prediction page
@app.route("/prediction", endpoint="prediction_page")
def prediction_page():
    return render_template ("prediction.html")
# Prediction API
@app.route("/predict", methods=['POST'])
def predict():
    try:
        data = request.get_json()
        stock = data.get("stock", "AAPL, GOOG, AMZN, TSLA, MSFT")
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
