FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Update OS to pull security fixes, then install ffmpeg only
RUN apt-get update \
 && apt-get -y dist-upgrade \
 && apt-get install -y --no-install-recommends ffmpeg \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create non-root user and writable data dir
RUN useradd -m -u 10001 app \
 && mkdir -p /data/uploads /data/outputs \
 && chown -R app:app /app /data
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=20s CMD wget -qO- http://127.0.0.1:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host","0.0.0.0","--port","8000","--workers","1"]
