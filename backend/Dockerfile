FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY database/ ./database/

RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 5678

CMD ["gunicorn", "--bind", "0.0.0.0:5678", "run:app"]