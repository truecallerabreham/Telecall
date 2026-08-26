FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for caching
COPY pyproject.toml ./
RUN pip install --no-cache-dir uv && uv sync --no-dev

# Copy source code
COPY src/ ./src/
COPY scripts/ ./scripts/

# Expose port for FastAPI
EXPOSE 8000

# Run the FastAPI server
CMD ["uv", "run", "uvicorn", "telecomcall.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
