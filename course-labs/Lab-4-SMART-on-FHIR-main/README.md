# Lab 4 - SMART on FHIR Medication App

This project implements a SMART on FHIR application that manages patient medications using a live FHIR server. The app runs inside the SMART sandbox and demonstrates secure, scoped access to patient data.

Features

Search all MedicationRequest resources for the active patient

Update medication status (e.g., active → stopped)

Create new medication orders

Enforce correct SMART authorization scopes

The app uses the SMART Client.js library and follows FHIR R4 standards.

SMART Scopes Used
launch profile openid online_access
patient/Patient.read
patient/Observation.read
patient/MedicationRequest.*


These scopes allow safe read/write access to medication data while preserving patient security.

Tech Stack

Angular

TypeScript

SMART on FHIR

FHIR R4

OAuth 2.0

SMART Client.js

Running the App
npm install
ng serve


Then launch via:

https://launch.smarthealthit.org/

Set app URL:

http://localhost:4200/launch/

Result

The application successfully:

loads patient context

retrieves medication requests

updates medication status

creates new medication orders

passes all automated tests
Please see Canvas for instructions.

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.