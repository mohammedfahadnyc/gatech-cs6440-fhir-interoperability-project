# FHIR Backend

This folder contains the Flask backend for the FHIR Interoperability Diabetes Dashboard. It provides authentication, role-based access control, FHIR-style resource normalization, PostgreSQL persistence, and chart APIs consumed by the frontend dashboard.

## What It Does

- Authenticates clinician, patient, and admin-style users with JWTs
- Enforces role-based access so patient users can only access their own chart
- Stores normalized clinical data as FHIR-style resources
- Supports patient, observation, medication, condition, and clinical-note resources
- Aggregates resources into UI-friendly chart and summary endpoints
- Supports internal chart data and external-source import workflows
- Includes sandbox-style authorization hooks for external EHR integration demos
- Exposes Swagger/OpenAPI documentation for local development

## Main Technologies

- Python and Flask
- SQLAlchemy
- PostgreSQL
- JWT authentication
- FHIR R4-inspired JSON resources
- Docker Compose for local database startup

## Local Run

From this folder:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
docker compose up -d postgres
backend/.venv/bin/python backend/run.py
```

The API starts at:

```text
http://127.0.0.1:5000
```

Swagger UI is available at:

```text
http://127.0.0.1:5000/apidocs/
```

## Documentation

- `backend/RUNNING.md`: local setup and run notes
- `backend/FRONTEND_API.md`: frontend integration overview
- `backend/.env.example`: non-secret local configuration template

## Privacy Note

This portfolio version intentionally omits live credentials and removes database snapshots/Postman payloads that contained demo account data. Local seed data is synthetic and intended only for development.
