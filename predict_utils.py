# utils/predict_utils.py

import requests
import pandas as pd
import numpy as np
import joblib
from keras.models import load_model

API_KEY = "1eb83bbe8a084c8aabd415467aeb0b7f"  # 🔁 Replace this

scaler = joblib.load("scaler.pkl")
model = load_model("model.h5")

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def compute_macd(series, slow=26, fast=12):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    return ema_fast - ema_slow

def fetch_latest_data(ticker="AAPL, GOOG, AMZN, TSLA, MSFT", days=5):
    url = f"https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize={days+30}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if 'values' not in data:
        raise ValueError(f"API Error: {data.get('message', 'Invalid response')}")

    df = pd.DataFrame(data['values'])
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime')
    df.set_index('datetime', inplace=True)

    df = df[['close', 'volume']].astype(float)
    df.rename(columns={'close': 'Close', 'volume': 'Volume'}, inplace=True)

    df['RSI'] = compute_rsi(df['Close'])
    df['MACD'] = compute_macd(df['Close'])

    df.dropna(inplace=True)
    if len(df) < days:
        raise ValueError(f"Not enough data for prediction (got {len(df)} rows).")

    return df.tail(days)

def preprocess_input(df):
    scaled = scaler.transform(df)
    return scaled.reshape(1, df.shape[0], df.shape[1])  # (1, 120, 4)

def predict_multi_day(input_seq, n_days):
    predictions_scaled = []
    seq = input_seq.copy()

    for _ in range(n_days):
        pred = model.predict(seq, verbose=0)[0][0]
        predictions_scaled.append(pred)
        last_features = seq[0, -1, 1:]
        new_point = np.concatenate([[pred], last_features])
        seq = np.append(seq[:, 1:, :], [[new_point]], axis=1)

    dummy = np.zeros((n_days, 3))
    full = np.concatenate([np.array(predictions_scaled).reshape(-1, 1), dummy], axis=1)
    return scaler.inverse_transform(full)[:, 0].round(2).tolist()
