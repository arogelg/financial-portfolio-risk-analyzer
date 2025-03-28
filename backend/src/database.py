import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@db:5432/risk_analyzer_DB")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)