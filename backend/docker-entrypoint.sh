#!/bin/sh
set -e

# Simple entrypoint: run alembic migrations if DATABASE_URL is set, then exec the CMD
if [ -n "$DATABASE_URL" ]; then
	echo "DATABASE_URL detected — running alembic migrations (if any)..."
	# brief pause to allow linked DB container to start
	sleep 5
	if command -v alembic >/dev/null 2>&1; then
		alembic upgrade head || echo "alembic upgrade head failed"
	else
		echo "alembic not installed; skipping migrations"
	fi
fi

exec "$@"
