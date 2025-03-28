from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://arogelg:7150Vavagvba@db:5432/risk_analyzer_DB"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

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