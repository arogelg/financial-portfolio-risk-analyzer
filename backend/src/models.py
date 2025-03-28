from sqlalchemy import Column, Integer, String, Numeric, Date, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# In here add the columns that the model needs
class Stock(Base):
    __tablename__ = 'stocks'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)
    date = Column(Date)
    open_price = Column(Numeric)
    high_price = Column(Numeric)
    low_price = Column(Numeric)
    close_price = Column(Numeric)
    volume = Column(BigInteger)