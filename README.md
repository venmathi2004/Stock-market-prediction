# 📊 Stock Market Prediction using Deep Learning (CNN + LSTM)


This project is a **real-time stock prediction system** that forecasts the future prices of **Multiple Stocks** using a hybrid **CNN + LSTM** deep learning model.  
It combines historical stock data with technical indicators like **RSI** and **MACD**, fetched using the **Twelve Data API**.  
The backend is powered by **Flask**, and predictions are exposed through a RESTful API.

---

## 📌 Project Overview

This system performs the following tasks:

1. **Fetches latest historical stock data** (Open, Close price & High, Low Volume) from Twelve Data API.
2. **Computes technical indicators**: RSI (momentum) and MACD (trend).
3. **Preprocesses data** using a saved `MinMaxScaler`.
4. **Makes future predictions** using a CNN+LSTM `.h5` model trained on Multiple Stocks data.
5. **Returns prediction as JSON** to be displayed on a web frontend.

---

## 🧱 Project Structure

```
.
├── app.py                  # Main Flask application
├── predict_utils.py        # Utilities for fetching, processing, and predicting data
├── model.h5     # Trained CNN+LSTM model
├── scaler.pkl   # MinMaxScaler used to preprocess inputs
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```

---

## ⚙️ Setup & Run Instructions

### ✅ Step 1: Clone or Download the Project

Place all files into a single folder on your system.

### ✅ Step 2: Create a Virtual Environment (Optional but recommended)

```bash
python -m venv venv
venv\\Scripts\\activate  # On Windows
```

### ✅ Step 3: Install Required Libraries

```bash
pip install -r requirements.txt
```

### ✅ Step 4: Run the Flask App

```bash
python app.py
```

### ✅ Step 5: Open Web Browser

Go to:
```
http://127.0.0.1:5000/prediction
```

Enter:
- Stock Name: `AAPL, GOOG, AMZN, TSLA, MSFT, `
- Days: e.g., `5`

Click "Predict" to view future price predictions.

---

## 📡 API Usage

### Endpoint: `/predict` (POST)

**Request:**
```json
{
  "stock": "AAPL, GOOG, AMZN, TSLA, MSFT",
  "days": 5
}
```

**Response:**
```json
{
  "stock": "AAPL, GOOG, AMZN, TSLA, MSFT",
  "days": 5,
  "predictions": [1012.45, 1014.78, 1016.92, ...]
}
```

---

## 🧠 Model Details

- Model Type: Hybrid of **CNN + LSTM**
- Trained on: **Multiple Stocks** historical data
- Features:
  - Close Price
  - Volume
  - RSI
  - MACD
- Scaled using `MinMaxScaler`

---

## 📈 Data Source

- API: [Twelve Data](https://twelvedata.com)
- API Endpoint used:
  ```
  https://api.twelvedata.com/time_series?symbol=MOTORS.NSE&interval=1day&outputsize=120&apikey=1eb83bbe8a084c8aabd415467aeb0b7f
  ```

---

## 👤 Author

**Venmathi Raj**  
Final Year Deep Learning Project – Stock Market Prediction using CNN+LSTM
