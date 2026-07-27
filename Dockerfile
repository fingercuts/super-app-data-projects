# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Set up a virtual environment to isolate dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# STAGE 2: Runner (Production)
# ==========================================
FROM python:3.12-slim AS runner

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create a non-root user for security
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser

# Copy source files
COPY --chown=appuser:appgroup scripts/ /app/scripts/
COPY --chown=appuser:appgroup tests/ /app/tests/
COPY --chown=appuser:appgroup api/ /app/api/
COPY --chown=appuser:appgroup dashboard/ /app/dashboard/
COPY --chown=appuser:appgroup .env.example /app/.env

# Ensure output dirs exist
RUN mkdir -p logs data/sample data/sample/dlq data/raw data/production && \
    chown -R appuser:appgroup logs data

# Switch to non-root user
USER appuser

# Default: generate sample data
CMD ["python", "scripts/generate_entities.py"]
