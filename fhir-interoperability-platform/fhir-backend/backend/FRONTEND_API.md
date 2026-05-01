# Frontend API Guide

This backend exposes JWT-protected endpoints for the FHIR dashboard frontend. The frontend logs in, stores the returned token for the demo session, and sends it as a bearer token on protected API calls.

Base URL for local development:

```text
http://127.0.0.1:5000
```

## Auth Model

After login, include:

```text
Authorization: Bearer <token>
```

Roles:

- `clinician`: can access patient directory and patient charts
- `admin`: can access patient directory and patient charts
- `patient`: can access only the linked patient chart

## Key Endpoints

```text
POST   /auth/login
GET    /auth/me
GET    /patients
GET    /patients/:id
GET    /patients/:id/summary
GET    /patients/:id/chart
GET    /patients/:id/fhir
POST   /patients/:id/notes
POST   /patients/:id/authorize
POST   /patients/:id/import
DELETE /patients/:id/data
POST   /emr/import
GET    /health
```

## Login Request Shape

```json
{
  "email": "<local-demo-user>",
  "password": "<local-demo-password>"
}
```

## Chart Response Shape

The chart endpoint returns a dashboard-friendly aggregation:

```json
{
  "patient": {},
  "observations": [],
  "medications": [],
  "conditions": [],
  "notes": []
}
```

## External Import Flow

External-source demos use this general flow:

1. `POST /patients/:id/authorize`
2. Complete sandbox authorization when required.
3. `POST /patients/:id/import`
4. `GET /patients/:id/chart`
5. Optionally `DELETE /patients/:id/data` to reset local imported demo data.

No live credentials are documented in this portfolio copy.
