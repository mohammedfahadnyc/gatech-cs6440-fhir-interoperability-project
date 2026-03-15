# Frontend API Guide

This document describes the backend endpoints for UI developers, including required headers, arguments, request bodies, and example responses.

Base URL:

```text
http://127.0.0.1:5000
```

## Quick Start From Repo Root

Install dependencies, seed the database, and run the backend:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
docker compose up -d postgres
backend/.venv/bin/python backend/run.py
```

Then use:

- Base URL: `http://127.0.0.1:5000`
- Default clinician login: `doctor1@clinic.com` / `password123`

Notes:

- If `AUTO_SEED=true`, the backend seeds an empty database automatically on startup
- If you stay on the SQLite `DATABASE_URL`, you can skip `docker compose up -d postgres`

## Auth Model

The backend uses JWT bearer tokens.

After login, include this header on protected routes:

```text
Authorization: Bearer <token>
```

Roles:

- `clinician`: can access all patients
- `admin`: can access all patients
- `patient`: can only access their own patient record and chart

## 1. Login

Endpoint:

```text
POST /auth/login
```

Request body:

```json
{
  "email": "doctor1@clinic.com",
  "password": "password123"
}
```

Arguments:

- `email` string, required
- `password` string, required

Example `fetch`:

```js
const response = await fetch("http://127.0.0.1:5000/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "doctor1@clinic.com",
    password: "password123",
  }),
});

const data = await response.json();
```

Success response:

```json
{
  "token": "jwt-token",
  "user": {
    "id": 1,
    "email": "doctor1@clinic.com",
    "role": "clinician",
    "patient_id": null,
    "created_at": "2026-03-14T12:00:00+00:00"
  }
}
```

## 2. Get All Patients

Endpoint:

```text
GET /patients
```

Access:

- `clinician`
- `admin`

Headers:

```text
Authorization: Bearer <token>
```

Example `fetch`:

```js
const response = await fetch("http://127.0.0.1:5000/patients", {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

const patients = await response.json();
```

Response:

```json
[
  {
    "id": 1,
    "name": "George Burdell",
    "dob": "1978-04-12",
    "gender": "male",
    "created_at": "2026-03-14T12:00:00+00:00"
  }
]
```

## 3. Get One Patient

Endpoint:

```text
GET /patients/:id
```

Access:

- `clinician`
- `admin`
- `patient` only for their own patient id

Path params:

- `id` integer, required

Example:

```js
const response = await fetch(`http://127.0.0.1:5000/patients/${patientId}`, {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
```

Response:

```json
{
  "id": 1,
  "name": "George Burdell",
  "dob": "1978-04-12",
  "gender": "male",
  "created_at": "2026-03-14T12:00:00+00:00"
}
```

## 4. Get Patient Chart

Endpoint:

```text
GET /patients/:id/chart
```

Access:

- `clinician`
- `admin`
- `patient` only for their own chart

Path params:

- `id` integer, required

Frontend purpose:

- Main doctor dashboard view
- Main patient dashboard view
- Chart timeline widgets
- medication list
- condition summary
- note history

Example `fetch`:

```js
const response = await fetch(`http://127.0.0.1:5000/patients/${patientId}/chart`, {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

const chart = await response.json();
```

Response shape:

```json
{
  "patient": {
    "id": 1,
    "name": "George Burdell",
    "dob": "1978-04-12",
    "gender": "male",
    "created_at": "2026-03-14T12:00:00+00:00"
  },
  "observations": [
    {
      "resourceType": "Observation",
      "code": {
        "text": "HbA1c"
      },
      "valueQuantity": {
        "value": 7.4,
        "unit": "%"
      },
      "effectiveDateTime": "2026-01-01"
    }
  ],
  "medications": [
    {
      "resourceType": "MedicationStatement",
      "medicationCodeableConcept": {
        "text": "Metformin"
      },
      "effectiveDateTime": "2026-01-01"
    }
  ],
  "conditions": [
    {
      "resourceType": "Condition",
      "code": {
        "text": "Type 2 Diabetes Mellitus"
      },
      "recordedDate": "2026-01-01"
    }
  ],
  "notes": [
    {
      "resourceType": "DocumentReference",
      "description": "Clinical note",
      "author": [
        {
          "display": "doctor1@clinic.com"
        }
      ],
      "date": "2026-01-01T12:00:00+00:00"
    }
  ]
}
```

Important frontend note:

- `notes[].content[0].attachment.data` is base64-encoded text

## 5. Create Clinical Note

Endpoint:

```text
POST /patients/:id/notes
```

Access:

- `clinician`
- `admin`

Path params:

- `id` integer, required

Request body:

```json
{
  "note": "Patient reports improved glucose control over the last month."
}
```

Arguments:

- `note` string, required

Example `fetch`:

```js
const response = await fetch(`http://127.0.0.1:5000/patients/${patientId}/notes`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  },
  body: JSON.stringify({
    note: "Patient reports improved glucose control over the last month.",
  }),
});

const data = await response.json();
```

Success response:

```json
{
  "id": 44,
  "patient_id": 1,
  "resource_type": "DocumentReference",
  "payload_json": {
    "resourceType": "DocumentReference"
  },
  "source_system": "manual_note",
  "created_at": "2026-03-14T12:00:00+00:00"
}
```

## 6. Import EMR Payload

Endpoint:

```text
POST /emr/import
```

Access:

- `clinician`
- `admin`

Request body:

```json
{
  "name": "George Burdell",
  "patient_id": 1,
  "a1c": 7.4,
  "medications": ["Metformin"],
  "diagnosis": "Type 2 Diabetes Mellitus",
  "note": "Imported follow-up note from simulated Athena feed",
  "source_system": "Athena"
}
```

Arguments:

- `name` string, required
- `patient_id` integer, optional
- `dob` string in ISO date format, optional when creating a new patient
- `gender` string, optional when creating a new patient
- `a1c` number, optional
- `medications` array of strings, optional
- `diagnosis` string, optional
- `note` string, optional
- `source_system` string, optional
- `observed_on` ISO date string, optional
- `diagnosed_on` ISO date string, optional

Behavior:

- If `patient_id` is provided and found, resources are added to that patient
- If `patient_id` is missing, a new patient is created
- The payload is converted into FHIR resources before storage

Example `fetch`:

```js
const response = await fetch("http://127.0.0.1:5000/emr/import", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  },
  body: JSON.stringify({
    name: "George Burdell",
    patient_id: 1,
    a1c: 7.4,
    medications: ["Metformin"],
    diagnosis: "Type 2 Diabetes Mellitus",
    note: "Imported follow-up note from simulated Athena feed",
    source_system: "Athena",
  }),
});

const data = await response.json();
```

Success response:

```json
{
  "message": "EMR payload imported successfully",
  "patient": {
    "id": 1,
    "name": "George Burdell",
    "dob": "1978-04-12",
    "gender": "male",
    "created_at": "2026-03-14T12:00:00+00:00"
  },
  "resource_count": 4
}
```

## Error Responses

Common errors:

```json
{
  "error": "Invalid credentials"
}
```

```json
{
  "error": "Forbidden"
}
```

```json
{
  "error": "Email and password are required"
}
```

```json
{
  "error": "Note text is required"
}
```

## Frontend Integration Notes

- Store the JWT token after login
- Pass the token in the `Authorization` header for every protected route
- The main dashboard should primarily use `GET /patients/:id/chart`
- Clinician dashboards can use `GET /patients` to populate a patient list
- Patient dashboards should use the logged-in user’s `patient_id` from the login response
- Notes are stored as FHIR `DocumentReference`
- Imported EMR data is normalized into FHIR resources before persistence
