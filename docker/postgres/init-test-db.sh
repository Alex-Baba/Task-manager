#!/usr/bin/env bash
set -e

if [ -z "$POSTGRES_TEST_DB" ]; then
  echo "POSTGRES_TEST_DB is not set; skipping test database creation."
  exit 0
fi

database_exists=$(
  psql \
    -v ON_ERROR_STOP=1 \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" \
    -tAc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_TEST_DB'"
)

if [ "$database_exists" = "1" ]; then
  echo "Test database '$POSTGRES_TEST_DB' already exists."
else
  echo "Creating test database '$POSTGRES_TEST_DB'."
  createdb --username "$POSTGRES_USER" "$POSTGRES_TEST_DB"
fi
