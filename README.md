# FHIR Diabetes Interoperability Bridge

This project is a Flask backend for a diabetes-focused interoperability demo. It takes simple EMR-style payloads, converts them into FHIR resources, stores the clinical data as JSON, and exposes a UI-friendly chart API for frontend dashboards.

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
- Seed script that creates:
  - 2 clinician users
  - 5 patient users
  - diabetes conditions
  - HbA1c observation history
  - medication history
  - doctor notes
- Postman collection for manual API testing
- SQLite fallback for zero-setup local testing
- Persistent PostgreSQL option via Docker with auto-seeding on first startup

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

## Database Modes

The backend supports both:

- SQLite fallback for simple local testing
- Persistent PostgreSQL through Docker for a production-like local setup

Copy `backend/.env.example` to `backend/.env`, then keep the `DATABASE_URL` you want and comment out the other.
