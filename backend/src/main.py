import yfinance as yf
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List

# Initialize FastAPI app
app = FastAPI()

# PostgreSQL database connection string
DATABASE_URL = "postgresql://arogelg:7150Vavagvba@db:5432/risk_analyzer_DB"

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Define the Stock model
class Stock(Base):
    __tablename__ = 'stocks'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)
    name = Column(String(100))
    date = Column(Date)
    open_price = Column(Numeric)
    high_price = Column(Numeric)
    low_price = Column(Numeric)
    close_price = Column(Numeric)
    volume = Column(BigInteger)

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
    if not symbols:
        raise HTTPException(status_code=400, detail="A list of stock symbols is required!")
    
    results = []
    
    # Fetch and store data for each symbol
    for symbol in symbols:
        result = fetch_and_store_stock_data(symbol)
        if result is None:
            results.append({"symbol": symbol, "error": f"No data found for {symbol}"})
        else:
            results.append({"symbol": symbol, "message": result['message']})
    
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
