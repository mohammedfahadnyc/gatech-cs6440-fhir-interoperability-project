# FHIR Diabetes Interoperability Bridge

This project is a Flask backend for a diabetes-focused interoperability demo. It takes simple EMR-style payloads, converts them into FHIR resources, stores the clinical data as JSON, and exposes a UI-friendly chart API for frontend dashboards.

## Quick Start

Make sure Docker Desktop or Docker Engine is running first.

First-time setup from the repo root:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
docker compose up -d postgres
backend/.venv/bin/python backend/run.py
```

Before first run, review `backend/.env` and set `DATABASE_URL` if you want a different PostgreSQL instance.

Subsequent runs from the repo root:

```bash
./backend/scripts/start_dev.sh
```

This starts PostgreSQL and then runs the API at `http://127.0.0.1:5000`.
Swagger UI is available at `http://127.0.0.1:5000/apidocs/`.

## What Is Built

- JWT authentication with clinician, patient, and admin roles
- RBAC enforcement so patients can only access their own chart
- FHIR resource storage in `fhir_resources` using JSON/JSONB-compatible models
- Supported FHIR resources for the MVP:
  - `Patient`
  - `Observation`
  - `MedicationStatement`
  - `Condition`
  - `DocumentReference`
- Chart aggregation endpoint returning:
  - `patient`
  - `observations`
  - `medications`
  - `conditions`
  - `notes`
- EMR import endpoint that converts simple JSON into FHIR resources automatically
- current-user endpoint for frontend role/patient resolution
- patient summary endpoint for lightweight dashboard stats
- FHIR Bundle export endpoint for standards-compliant interoperability output
- Seed script that creates:
  - 2 clinician users
  - 5 patient users
  - diabetes conditions
  - HbA1c observation history
  - medication history
  - doctor notes
- Postman collection for manual API testing
- Persistent PostgreSQL via Docker with auto-seeding on first startup

## Project Layout

```text
backend/
  app/
    config.py
    __init__.py
    db/
    middleware/
    models/
    routes/
    services/
  postman/
  scripts/
  requirements.txt
  run.py
```

## Documentation

- Run guide: [backend/RUNNING.md](backend/RUNNING.md)
- Frontend API guide: [backend/FRONTEND_API.md](backend/FRONTEND_API.md)
- Postman collection: [backend/postman/fhir_diabetes_collection.json](backend/postman/fhir_diabetes_collection.json)

## Repo Root Usage

All documented commands in this repository are written to be run from the repo root.

## Database

The backend now uses PostgreSQL as the single supported local database.

Copy `backend/.env.example` to `backend/.env`, then start PostgreSQL with Docker before running the app.

To publish the current database contents for future fresh clones:

```bash
./backend/scripts/export_db_snapshot.sh
```

That updates `backend/db/init/001_snapshot.sql`. Commit that file when you want the latest database snapshot to be restored on brand-new environments.

## Developer Workflow

Use this flow when you want to clone the repo, run the app, add data, and publish the latest database state for future fresh clones.

Clone and start the project:

```bash
git clone https://github.gatech.edu/mfahad7/fhir-backend.git
cd fhir-backend
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
docker compose up -d postgres
backend/.venv/bin/python backend/run.py
```

What happens next:

- If the PostgreSQL database is empty, the app seeds it automatically
- You can then add more data through the API, through seed logic, or directly in PostgreSQL
- That data stays persisted in your local Docker Postgres volume

When you want to publish the current database state into GitHub for future fresh clones:

```bash
./backend/scripts/export_db_snapshot.sh
git add backend/db/init/001_snapshot.sql
git commit -m "Update database snapshot"
git push
```

Important:

- Your live local Postgres data is not pushed automatically
- The export command updates the tracked SQL snapshot file
- Future fresh clones can initialize from that committed snapshot


Quick Demo:

https://github.gatech.edu/user-attachments/assets/151479ff-50c7-43c7-800d-07c785f9fa29

##

