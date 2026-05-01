# Running The Backend

## Prerequisites

- Python 3.9+
- Docker Desktop or Docker Engine
- PostgreSQL via the included Docker Compose service

## Setup

From `fhir-interoperability-platform/fhir-backend`:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
docker compose up -d postgres
backend/.venv/bin/python backend/run.py
```

For day-to-day local development, use:

```bash
./backend/scripts/start_dev.sh
```

## API URLs

```text
API:        http://127.0.0.1:5000
Swagger:    http://127.0.0.1:5000/apidocs/
Health:     http://127.0.0.1:5000/health
```

## Seed Data

When `AUTO_SEED=true`, the app seeds an empty local database with synthetic development users, synthetic patients, diabetes-oriented chart data, medications, observations, conditions, and notes.

This portfolio copy does not publish live demo credentials. If you need local demo accounts, inspect or customize the local seed script and keep any credentials private.

## External Authorization Flow

The backend includes a sandbox-style external authorization path for demonstrating how an external EHR authorization callback can unlock an import workflow. Configure sandbox client values in `backend/.env`; do not commit real client secrets.

## Health Check

```bash
curl http://127.0.0.1:5000/health
```

Expected response:

```json
{
  "status": "ok"
}
```
