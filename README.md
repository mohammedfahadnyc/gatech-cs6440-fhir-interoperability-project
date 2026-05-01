# Georgia Tech CS6440 FHIR Interoperability Portfolio

This repository is a portfolio-style collection for Georgia Tech CS6440: Introduction to Health Informatics. It combines a full-stack FHIR interoperability practicum project with the supporting course lab work on FHIR resources, SMART on FHIR, clinical data extraction, and health data engineering.

## Repository Layout

```text
.
|-- fhir-interoperability-platform/
|   |-- fhir-frontend/
|   |-- fhir-backend/
|   `-- README.md
`-- course-labs/
```

## FHIR Interoperability Platform

`fhir-interoperability-platform/` contains a full-stack diabetes care dashboard built as a proof-of-concept for multi-EHR interoperability. The project demonstrates how a clinic-facing application can normalize data from different EHR-style sources into a standards-based FHIR layer, then present a unified longitudinal chart for clinicians and a focused self-management portal for patients.

The platform includes:

- a Next.js frontend for clinician and patient workflows
- a Flask backend API with JWT authentication and role-based access control
- PostgreSQL-backed FHIR resource storage
- FHIR resource normalization for patients, observations, medications, conditions, and notes
- internal patient data flows, external import flows, and sandbox-style authorization hooks
- diabetes-focused charting, clinical documentation, safety alerts, and education content

Sensitive live credentials, submission access details, and personally identifying demo walkthrough details are intentionally omitted from the portfolio documentation.

## Course Labs

`course-labs/` contains the broader CS6440 lab sequence. The labs explore core health informatics concepts including FHIR resource manipulation, OMOP-on-FHIR mapping, SMART on FHIR applications, clinical NLP/RAG workflows, and FHIR-based machine learning feature engineering.

## Theme

The common thread across the repository is healthcare interoperability: translating fragmented clinical data into standards-based representations that can support safer workflows, more useful dashboards, and better downstream analytics.
