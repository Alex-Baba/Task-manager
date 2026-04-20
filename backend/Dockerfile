FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Wrapper entrypoint (LF) that fixes CRLF on bind-mounted scripts before executing.

RUN printf '%s\n' \
    '#!/bin/sh' \
    'set -e' \
    '' \
    'if [ -f /app/docker-entrypoint.sh ]; then' \
    "  sed -i 's/\\r$//' /app/docker-entrypoint.sh" \
    'fi' \
    '' \
    'exec /bin/sh /app/docker-entrypoint.sh "$@"' \
    > /usr/local/bin/app-entrypoint \
    && chmod +x /usr/local/bin/app-entrypoint \
    && useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Run migrations in entrypoint then start Uvicorn
ENTRYPOINT ["/usr/local/bin/app-entrypoint"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]