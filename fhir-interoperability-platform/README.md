# FHIR Interoperability Diabetes Dashboard

This project is a full-stack proof-of-concept for a diabetes clinic that needs a unified view of patient records spread across multiple EHR-style systems. It combines a clinician dashboard, patient portal, FHIR-normalizing backend, and database-backed chart API into one interoperable mini-EMR experience.

## Problem

Diabetes care depends on longitudinal visibility into lab trends, medications, diagnoses, and clinical notes. In real clinical environments, that data is often fragmented across different EHR systems and organizational boundaries. This project explores how a lightweight middleware layer can normalize those records into FHIR resources and present them through practical clinician and patient workflows.

## Solution

The application is organized as two cooperating services:

```text
fhir-frontend/   # Next.js clinician/patient dashboard
fhir-backend/    # Flask API, FHIR normalization, auth, RBAC, PostgreSQL
```

The backend ingests internal and external-style chart data, converts it into FHIR-inspired resources, stores it in PostgreSQL, and exposes dashboard-friendly APIs. The frontend uses those APIs to display patient directories, chart summaries, HbA1c trends, medication profiles, clinical notes, safety alerts, authorization flows, and patient education content.

## Core Capabilities

- Clinician and patient role-based workflows
- Unified patient chart view across internal and imported records
- Diabetes-focused lab trend visualization
- Medication, condition, note, and safety-alert presentation
- Clinical note creation for provider documentation
- Patient learning portal for diabetes education
- External-source import workflow with sandbox-style authorization support
- FHIR Bundle export and FHIR resource persistence

## Technology

- Frontend: Next.js, React, TypeScript, Tailwind CSS, Recharts
- Backend: Python, Flask, SQLAlchemy, JWT, Swagger/OpenAPI
- Data: PostgreSQL, JSON/JSONB-style FHIR resource storage
- Interoperability: HL7 FHIR R4-inspired resources and SMART-on-FHIR-style authorization patterns

## Privacy Note

This portfolio copy avoids publishing live access credentials, contributor contact details, or real patient information. Demo records are synthetic/local-development records only.
