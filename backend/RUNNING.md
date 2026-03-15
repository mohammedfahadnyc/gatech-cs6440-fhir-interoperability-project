# Running The Project

## Prerequisites

- Python 3.9+
- `pip`

Optional:

- PostgreSQL if you want to use a real Postgres database instead of the default SQLite fallback

## Install

From the repo root:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
```

## Configure The Database

The app supports two database modes from the same codebase.

Option 1: SQLite fallback

- Works with no Docker
- Good for quick local testing
- Data persists in `backend/instance/`

Option 2: Persistent PostgreSQL

- Uses Docker
- Keeps data in a Docker volume
- Auto-seeds only on the first empty startup

Edit `backend/.env` and keep only one `DATABASE_URL` active.

Default `backend/.env.example` includes both options:

```bash
DATABASE_URL=sqlite:///fhir_diabetes_bridge.db
# DATABASE_URL=postgresql://fhir:fhir@localhost:5432/fhir_bridge
```

For PostgreSQL, start the database from the repo root:

```bash
docker compose up -d postgres
```

Optional local secrets:

```bash
export SECRET_KEY=replace-me
export JWT_SECRET_KEY=replace-me-too
```

## Seed Data

For a manual reset-and-reseed, run:

```bash
backend/.venv/bin/python backend/scripts/seed_data.py
```

Normally you do not need to run the seed script when `AUTO_SEED=true`.

- On app startup, the backend checks whether the database is empty
- If it is empty, it inserts the default seeded dataset
- If data already exists, nothing is overwritten

This seeded dataset includes:

- 2 clinician users
- 5 patient users
- FHIR patient resources
- HbA1c observations
- medication statements
- diabetes conditions
- doctor notes

## Single Command To Run The App

Use this from the repo root:

```bash
backend/.venv/bin/python backend/run.py
```

The API starts on:

```text
http://127.0.0.1:5000
```

## Typical Local Flow

1. Install dependencies.
2. Copy the env file.
3. Optionally start PostgreSQL with Docker.
4. Run the app.
5. Import the Postman collection or connect the frontend.

Commands:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
docker compose up -d postgres
backend/.venv/bin/python backend/run.py
```

SQLite-only quick run:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
backend/.venv/bin/python backend/run.py
```

## Seeded Login Accounts

Clinicians:

- `doctor1@clinic.com` / `password123`
- `doctor2@clinic.com` / `password123`

Patients:

- `george.burdell@patient.com` / `password123`
- `maria.lopez@patient.com` / `password123`
- `david.chen@patient.com` / `password123`
- `sarah.kim@patient.com` / `password123`
- `john.patel@patient.com` / `password123`

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
