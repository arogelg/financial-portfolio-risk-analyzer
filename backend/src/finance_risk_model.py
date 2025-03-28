# -*- coding: utf-8 -*-
"""finance_risk_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1npPohAqv7vbBJjs4A3vcwNMtHK8akIpy
"""

"""
finance_risk_model.py
----------------------------------
Modular risk modeling and ML classification for stock risk analysis.
- Pull data (Yahoo API now, DB integration later)
- Engineer features
- Train ML model (classification)
- Predict on recent data
- Return risk score + classification
Author: Andres Alvarez
Date: 2025-03
"""

# === Imports ===
import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from main import Stock, Session
from sqlalchemy.orm import Session as DBSession
import pandas as pd

# ============================================
# SECTION 1: Data Retrieval (Using database)
# ============================================

#Uses yahoo finance (to test only, uses 6months)
'''
def fetch_stock_data_yf(ticker: str, period: str = "6mo") -> pd.DataFrame:
    """
    Fetch historical data for the given ticker from Yahoo Finance.
    Later: replace this with a version that queries your DB.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)

    if hist.empty:
        raise ValueError(f"No data found for {ticker}")

    df = hist[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df.reset_index(inplace=True)
    df.rename(columns={'Date': 'date'}, inplace=True)
    return df
    '''

def fetch_stock_data_from_db(db: Session, ticker: str, days: int = 180) -> pd.DataFrame:
    """
    Pull historical stock data from PostgreSQL database for a given ticker.
    Returns a clean pandas DataFrame.
    """
    query = (
        db.query(Stock)
        .filter(Stock.symbol == ticker)
        .order_by(Stock.date.desc())
        .limit(days)
    )

    records = query.all()

    if not records:
        raise ValueError(f"No data found for {ticker} in DB.")

    # Convert to DataFrame
    data = [{
        'date': r.date,
        'open': float(r.open_price),
        'high': float(r.high_price),
        'low': float(r.low_price),
        'close': float(r.close_price),
        'volume': int(r.volume)
    } for r in records]

    # Reverse to chronological order (since we ordered desc)
    return pd.DataFrame(data[::-1])

# ============================================
# SECTION 2: Feature Engineering
# ============================================

def calculate_var(returns: pd.Series, confidence_level=0.05) -> float:
    """
    Historical VaR using percentile (95% by default).
    Represents the worst expected return on a normal day.
    """
    return np.percentile(returns, 100 * confidence_level)

def generate_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate risk features including VaR, volatility, and momentum.
    """
    df['returns'] = df['Close'].pct_change()
    df['volatility_5d'] = df['returns'].rolling(5).std()
    df['momentum_5d'] = df['Close'] / df['Close'].shift(5) - 1
    df['VaR_95'] = df['returns'].rolling(20).apply(calculate_var)  # 20-day rolling VaR

    # Define risk as "1" if next day return < VaR threshold (i.e., worse than expected loss)
    df['target'] = (df['returns'].shift(-1) < df['VaR_95']).astype(int)

    return df.dropna()

def map_risk_class(pred: int, confidence: float) -> str:
    """
    Translate model prediction into a human-readable risk label.
    """
    if pred == 0 and confidence >= 0.8:
        return "Low Risk – Stable outlook"
    elif pred == 0:
        return "Moderate Risk – Some volatility expected"
    elif pred == 1 and confidence < 0.75:
        return "Elevated Risk – Potential downside"
    else:
        return "High Risk – Significant downside risk likely"

# ============================================
# SECTION 3: Train Model and Predict Risk
# ============================================

def train_and_evaluate_model(df: pd.DataFrame) -> Dict:
    """
    Train the ML model and return predictions + interpretations.
    """
    features = ['volatility_5d', 'momentum_5d', 'VaR_95']
    X = df[features]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = (y_pred == y_test).mean()

    # Predict on most recent observation
    latest = X.iloc[-1:]
    predicted_risk = model.predict(latest)[0]
    confidence = model.predict_proba(latest)[0].max()
    risk_label = map_risk_class(predicted_risk, confidence)

    return {
        "model_accuracy": round(float(accuracy), 4),
        "predicted_risk_level": risk_label,
        "confidence_score": round(float(confidence), 4)
    }

# ============================================
# SECTION 4: Main Analysis Function
# Called from FastAPI
# ============================================

def analyze_stock_risk_db(ticker: str) -> Dict:
    """
    Pulls stock data from the database, runs ML model, returns risk classification.
    """
    try:
        db = DBSession()
        df = fetch_stock_data_from_db(db, ticker)
        df = generate_features(df)
        results = train_and_evaluate_model(df)
        db.close()

        results.update({
            "ticker": ticker,
            "latest_close": round(df['close'].iloc[-1], 2),
            "latest_VaR_95": round(df['VaR_95'].iloc[-1], 4),
            "latest_volatility": round(df['volatility_5d'].iloc[-1], 4)
        })

        return results

    except Exception as e:
        return {"ticker": ticker, "error": str(e)}

#analyze_stock_risk('AAPL')
