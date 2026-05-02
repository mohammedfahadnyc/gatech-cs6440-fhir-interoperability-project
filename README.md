# Georgia Tech CS6440 FHIR Interoperability Portfolio

This repository is a portfolio collection for Georgia Tech CS6440: Introduction to Health Informatics. It combines a full-stack FHIR interoperability practicum project with the supporting course lab work on FHIR resources, SMART on FHIR, clinical data extraction, and health data engineering. Includes EPIC integration for patient authorization and revoking access to their EHR data.

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

<img width="1259" height="696" alt="4" src="https://github.com/user-attachments/assets/49ed6163-5a51-4ba5-9b90-647eb6354aec" />
<img width="1216" height="696" alt="3" src="https://github.com/user-attachments/assets/00f336ca-f210-452a-b5fe-b90d2e5d249f" />
<img width="1216" height="696" alt="2" src="https://github.com/user-attachments/assets/65ecec54-01cd-43cf-a2db-ccc6f4e4204c" />
<img width="1259" height="696" alt="1" src="https://github.com/user-attachments/assets/0208bc5a-05fa-4026-99b9-2414d27baf6f" />


