# FHIR Frontend

This folder contains the Next.js frontend for the FHIR Interoperability Diabetes Dashboard. It provides the clinician and patient-facing UI for viewing unified chart data, importing external records, documenting clinical notes, and presenting diabetes education content.

## What It Does

- Presents a login-driven clinician and patient experience
- Shows a clinician patient directory with internal and external record states
- Renders patient chart summaries, medication profiles, conditions, HbA1c trends, and safety alerts
- Supports clinical note entry through the dashboard
- Provides patient-facing learning cards for diabetes education
- Calls the Flask backend with JWT bearer tokens stored client-side for the demo workflow

## Main Technologies

- Next.js App Router
- React and TypeScript
- Tailwind CSS
- Recharts for clinical trend visualization
- Axios for API calls

## Project Structure

```text
app/           # Pages and global styles
components/    # Dashboard, chart, notes, sidebar, and learning UI
services/      # API client for backend calls
utils/         # FHIR-to-UI mapping helpers
public/        # Static assets
```

## Local Run

Install dependencies and start the development server:

```bash
npm install
npm run dev
```

The app expects a backend API URL in local environment configuration, for example:

```bash
NEXT_PUBLIC_FHIR_BASE_URL=http://127.0.0.1:5000
```

No live credentials are documented in this portfolio copy.
