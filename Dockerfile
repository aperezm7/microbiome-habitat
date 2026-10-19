FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src:/app \
    HABITAT_ROOT=/app \
    HABITAT_DATA_DIR=/data \
    HABITAT_SOURCE=fixture \
    PORT=8000

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY services ./services
COPY challenges ./challenges
COPY fixtures ./fixtures

RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["python", "-m", "services.gateway"]
