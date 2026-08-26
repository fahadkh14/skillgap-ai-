# Build context is the repository root (see docker-compose.yml) so that
# database/seed.py can be included in the image for optional seeding.

FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies needed for building some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY database/ ./database/

# Create a non-root user and switch to it
RUN useradd --create-home --shell /bin/bash appuser \
    && mkdir -p /tmp/skillgap_uploads \
    && chown -R appuser:appuser /app /tmp/skillgap_uploads

USER appuser

EXPOSE 5678

CMD ["gunicorn", "--bind", "0.0.0.0:5678", "--workers", "3", "--timeout", "60", "run:app"]
