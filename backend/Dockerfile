FROM python:3.9-slim

WORKDIR /app

# First we install the Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then we copy our backend code
COPY src/ ./src/

# Well use port 8000
EXPOSE 8000

# Finally we run FastAPI with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
