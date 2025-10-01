# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install curl for downloading supercronic
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright and Chromium runtime dependencies (no Xvfb; headless)
RUN pip install --no-cache-dir playwright && \
    playwright install chromium && \
    playwright install-deps chromium && \
    rm -rf /root/.cache/pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install supercronic (tiny cron runner)
ARG SUPERCRONIC_VERSION=0.2.29
RUN curl -fsSLo /usr/local/bin/supercronic https://github.com/aptible/supercronic/releases/download/v${SUPERCRONIC_VERSION}/supercronic-linux-amd64 && \
    chmod +x /usr/local/bin/supercronic

# Copy app
COPY allow.py /app/allow.py

# Lightweight entrypoint supporting one-shot and cron modes
RUN printf '%s\n' \
  '#!/bin/sh' \
  'set -e' \
  '' \
  'if [ -n "${CRON_EXPR:-}" ]; then' \
  '  echo "$CRON_EXPR python /app/allow.py" | exec /usr/local/bin/supercronic /dev/stdin' \
  'else' \
  '  exec python /app/allow.py' \
  'fi' \
  > /entrypoint.sh && chmod +x /entrypoint.sh

ENV RENEW_URL="" \
    PASSWORD="" \
    CRON_EXPR=""

ENTRYPOINT ["/entrypoint.sh"]
