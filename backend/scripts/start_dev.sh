#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required. Please start Docker Desktop or Docker Engine first."
  exit 1
fi

if [ ! -f "backend/.env" ]; then
  echo "backend/.env not found. Create it first with:"
  echo "cp backend/.env.example backend/.env"
  exit 1
fi

if [ ! -x "backend/.venv/bin/python" ]; then
  echo "backend virtualenv not found. Create it first with:"
  echo "python3 -m venv backend/.venv"
  echo "backend/.venv/bin/pip install -r backend/requirements.txt"
  exit 1
fi

docker compose up -d postgres
exec backend/.venv/bin/python backend/run.py
