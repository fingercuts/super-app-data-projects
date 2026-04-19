FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source and data maps
COPY scripts/ /app/scripts/
COPY tests/ /app/tests/
COPY .env.example /app/.env

# Ensure dirs exist
RUN mkdir -p logs data/sample data/sample/dlq

# Command to generate all
# In an Airflow context, we might override this with a specific script block
CMD ["python", "scripts/generate_all.py"]
