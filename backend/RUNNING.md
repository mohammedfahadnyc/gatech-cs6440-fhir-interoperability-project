# Running The Project

## Prerequisites

- Python 3.9+
- `pip`

Optional:

- Docker Desktop or Docker Engine

## Install

From the repo root:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
```

Make sure Docker Desktop or Docker Engine is already running.

## Configure The Database

The app uses PostgreSQL as the single supported local database.

`backend/.env.example` includes the default local connection:

```bash
DATABASE_URL=postgresql://fhir:fhir@localhost:5432/fhir_bridge
```

Start PostgreSQL from the repo root:

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

Useful API routes after startup:

- `POST /auth/login`
- `GET /auth/me`
- `GET /patients`
- `GET /patients/<id>`
- `GET /patients/<id>/summary`
- `GET /patients/<id>/chart`
- `GET /patients/<id>/fhir`
- `POST /patients/<id>/notes`
- `POST /emr/import`

## Single Command To Run The App

Use this from the repo root:

```bash
backend/.venv/bin/python backend/run.py
```

For normal day-to-day development after setup, use:

```bash
./backend/scripts/start_dev.sh
```

That starts PostgreSQL and then launches the Flask app.

The API starts on:

```text
http://127.0.0.1:5000
```

Swagger UI:

```text
http://127.0.0.1:5000/apidocs/
```

## Typical Local Flow

1. Install dependencies.
2. Copy the env file.
3. Start PostgreSQL with Docker.
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

## Publish A Database Snapshot

If you add or change data and want future fresh clones to start from that exact database state, export a new snapshot:

```bash
./backend/scripts/export_db_snapshot.sh
```

This writes:

```text
backend/db/init/001_snapshot.sql
```

Then commit and push that file.

Important:

- This does not change an already-existing local Docker volume
- PostgreSQL only imports `backend/db/init/001_snapshot.sql` when the Docker volume is brand new
- If you want to reinitialize from the latest snapshot, reset the Postgres volume and start the container again

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

## Demo Flow

The default seed path now creates:

- internal patients with existing chart data
- external demo patients that start empty

External demo patients:

- Alex Morgan
- Chris Walker
- Nina Patel
- Daniel Kim

External patient flow:

1. `POST /patients/<id>/authorize`
2. `POST /patients/<id>/import`
3. `GET /patients/<id>/chart`
4. `DELETE /patients/<id>/data`

Epic sandbox note:

- `nina.patel@patient.com` is the only local patient currently wired to the real Epic sandbox authorize flow
- call `POST /patients/<id>/authorize` with `{"source":"epic"}` to get an `authorization_url`
- open that URL in a browser to complete Epic login
- after the callback succeeds, the existing mock import flow still works unchanged

Epic local env values:

```bash
EPIC_ENABLED=true
EPIC_CLIENT_ID=
EPIC_CLIENT_SECRET=
EPIC_REDIRECT_URI=http://127.0.0.1:5000/auth/epic/callback
EPIC_FHIR_BASE_URL=https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4
EPIC_AUTH_BASE_URL=https://fhir.epic.com/interconnect-fhir-oauth/
EPIC_DEMO_PATIENT_EMAIL=nina.patel@patient.com
```

Useful commands:

```bash
backend/.venv/bin/python backend/scripts/migrate_patient_origin.py
backend/.venv/bin/python backend/scripts/seed_demo_patients.py
backend/.venv/bin/python backend/scripts/demo_flow_test.py
```
