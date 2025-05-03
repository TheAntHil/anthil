FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock /app/
RUN pip install uv==0.7.2 \
 && uv export -o requirements.txt --no-header --no-hashes \
 && pip install -r requirements.txt --no-cache-dir -U \
 && pip uninstall -y uv

COPY alembic.ini /app/
COPY migrations /app/migrations
COPY anthill /app/anthill


CMD ["python", "-m", "anthill"]