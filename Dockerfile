FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install uv && uv pip install . --system --no-cache-dir

CMD ["sh", "-c", "while ! nc -z db 5432; do sleep 1; done && python -m anthill.main"]