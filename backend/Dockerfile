# Use Python as base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy everything from backend/src into the container
COPY src/ /app/

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn psycopg2 sqlalchemy

# Set working directory inside container
WORKDIR /app/src

# Run the database initialization script before starting FastAPI
CMD ["sh", "-c", "python init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
