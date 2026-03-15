#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
OUTPUT_FILE="$ROOT_DIR/backend/db/init/001_snapshot.sql"
CONTAINER_NAME="fhir-bridge-postgres"
TMP_FILE="$(mktemp)"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required to export the database snapshot."
  exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
  echo "Postgres container '$CONTAINER_NAME' is not running."
  echo "Start it with: docker compose up -d postgres"
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT_FILE")"

docker exec "$CONTAINER_NAME" \
  pg_dump -U fhir -d fhir_bridge --clean --if-exists --inserts --no-owner --no-privileges \
  > "$TMP_FILE"

mv "$TMP_FILE" "$OUTPUT_FILE"

echo "Database snapshot exported to $OUTPUT_FILE"
echo "Commit this file if you want fresh clones to start from the latest published dataset."
