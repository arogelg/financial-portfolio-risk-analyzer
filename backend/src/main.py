import yfinance as yf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List
from .finance_risk_model import analyze_stock_risk_db
from .database import Stock, Session, Base, engine  # Use what you've already defined

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# Fetch stock data and insert into the database
def fetch_and_store_stock_data(symbol: str):
    stock = yf.Ticker(symbol)
    stock_data = stock.history(period="6mo")
    
    # If no data is found, return an error
    if stock_data.empty:
        return None

    # Extract stock data for insertion into the database
    stock_info = stock_data.reset_index()
    stock_info = stock_info[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    
    # Create a new session to interact with the DB
    session = Session()

    for _, row in stock_info.iterrows():
        new_stock = Stock(
            symbol=symbol,
            date=row['Date'],
            open_price=row['Open'],
            high_price=row['High'],
            low_price=row['Low'],
            close_price=row['Close'],
            volume=row['Volume']
        )
        session.add(new_stock)

    session.commit()
    session.close()

    return {"message": f"Data for {symbol} stored successfully!"}

# API endpoint to receive multiple stock symbols and store data
@app.post("/api/store-stocks")
async def store_stocks(symbols: List[str]):
    print("Received ticker symbols:", symbols)
    if not symbols:
        raise HTTPException(status_code=400, detail="A list of stock symbols is required!")
    
    results = []

    for symbol in symbols:
        result = fetch_and_store_stock_data(symbol)
        if result is None:
            results.append({"symbol": symbol, "error": f"No data found for {symbol}"})
        else:
            analysis = analyze_stock_risk_db(symbol)
            results.append({"symbol": symbol, "message": result['message'], "analysis": analysis})

    print("Storing results:", results)
    return {"results": results}

# API endpoint to clear the database
@app.post("/api/clear-stocks")
async def clear_stocks():
    # Create a session to interact with the DB
    session = Session()
    
    # Delete all records from the stocks table
    session.query(Stock).delete()
    session.commit()
    session.close()

    return {"message": "All stock data has been cleared from the database!"}

@app.get("/api/history/{ticker}")
def get_price_history(ticker: str):
    db = Session()
    try:
        records = (
            db.query(Stock)
            .filter(Stock.symbol == ticker)
            .order_by(Stock.date.desc())
            .limit(30)
            .all()
        )
        history = [{"date": r.date.strftime("%Y-%m-%d"), "close": float(r.close_price)} for r in reversed(records)]
        return history
    finally:
        db.close()

