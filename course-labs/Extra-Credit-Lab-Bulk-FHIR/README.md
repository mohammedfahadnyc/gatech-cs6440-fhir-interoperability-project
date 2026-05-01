# Extra Credit Lab — Bulk FHIR (Conceptual README)

## Overview

This extra credit lab explores **FHIR Bulk Export** and basic analytics using healthcare data.

Unlike earlier labs that focused on machine learning pipelines, this lab is primarily about:

* understanding bulk healthcare data exports
* performing simple data analysis
* working with NDJSON formatted FHIR resources
* extracting insights from condition data

The main idea is:

```id="0z2u8s"
Bulk FHIR Data → Pandas Analysis → Counts, Trends, Prediction
```

---

## What is Bulk FHIR?

FHIR normally allows querying resources one-by-one through an API.

**Bulk FHIR** is designed for large-scale export.

Instead of API calls, a FHIR server exports:

```id="o4hmpy"
NDJSON files (newline-delimited JSON)
```

Each line is a full FHIR resource:

```json id="nzstlw"
{"resourceType":"Condition", ...}
{"resourceType":"Condition", ...}
```

This format allows fast downloads and large-scale analytics.

---

## Why Bulk FHIR Exists

Healthcare systems need to:

* export millions of records
* perform analytics offline
* run research studies
* build machine learning datasets

Bulk export provides:

* scalable data transfer
* standardized structure
* easier analysis pipelines

---

## Lab Objective

You are helping a health system analyze its patient population.

The data already exists in a FHIR server.

Your job:

```id="3flpnw"
Analyze condition data to answer population-level questions.
```

---

## Project Structure

Only one file was modified:

```id="2rzy8l"
src/bulk_fhir/eda.py
```

This file contains four analytical functions:

1. Count all prediabetes cases
2. Count cases within a time range
3. Predict future cumulative cases
4. Identify top procedures (manual lookup)

---

## Data Source

The dataset is loaded using:

```python id="z6q1iq"
get_bulk_data()
```

This returns a Pandas DataFrame containing **FHIR Condition resources**.

Important columns:

| Column       | Meaning                             |
| ------------ | ----------------------------------- |
| code         | Nested FHIR condition code (SNOMED) |
| recordedDate | When the condition was recorded     |

---

## SNOMED Code Used

Prediabetes is identified by:

```id="jf3wjs"
15777000
```

(Deprecated SNOMED code, but included in dataset.)

The code is nested inside:

```id="yome6r"
Condition.code.coding[].code
```

---

## Q1 — Count All Prediabetes Conditions

### Goal

Find how many records represent prediabetes.

### Logic

1. Iterate through `df["code"]`
2. Extract nested `coding` list
3. Check for SNOMED code `15777000`
4. Count matches

### Concept

This mimics real healthcare analytics:

```id="kuzhx8"
Filter large datasets by standardized clinical codes.
```

---

## Q2 — Count Prediabetes Within a Time Range

### Goal

Count prediabetes cases between two years (example: 1982–1990).

### Logic

1. Reuse SNOMED filtering from Q1
2. Read year from:

```id="du5f0m"
recordedDate
```

3. Extract year using string slicing.
4. Count only entries inside range.

### Concept

This shows:

```id="za4sfh"
Temporal filtering in healthcare analytics.
```

Example real-world uses:

* disease trend analysis
* policy evaluation
* epidemiology studies

---

## Q3 — Predict Future Cumulative Prediabetes Cases

### Goal

Estimate cumulative number of cases for a future year.

This uses **simple linear regression**.

---

### Step 1 — Gather yearly occurrences

Extract year of each prediabetes condition.

Example:

```id="hcsqaw"
1982, 1983, 1983, 1984...
```

---

### Step 2 — Build cumulative counts

Count per year:

```id="nqqh41"
1982 → 1
1983 → 2
1984 → 1
```

Convert to cumulative totals:

```id="5or870"
1982 → 1
1983 → 3
1984 → 4
```

Cumulative curves always increase or plateau.

---

### Step 3 — Linear Regression

We model:

```id="cmvuyj"
Y = bX + a
```

Where:

* X = year
* Y = cumulative count

Using NumPy:

```python id="mjlwm6"
np.polyfit(X, y, 1)
```

This returns slope and intercept.

---

### Step 4 — Predict

Plug in year:

```id="k312em"
prediction = b * year + a
```

This gives a simple trend-based forecast.

---

### Why Simple Regression?

The lab intentionally avoids advanced ML.

Goal:

```id="8c9n7s"
Learn trend analysis from healthcare data.
```

---

## Q4 — Top 3 Procedures (Manual)

This part uses the SMART Bulk Export Tool.

No coding required.

Steps:

1. Export procedure resources
2. Inspect NDJSON
3. Count procedure names
4. Return top three as tuple

Example:

```python id="ohdfm8"
("procedure1", "procedure2", "procedure3")
```

---

## Skills Practiced

This lab focuses on **data analysis fundamentals**:

* reading standardized healthcare data
* nested JSON processing
* filtering by clinical codes
* time-based analysis
* cumulative statistics
* basic forecasting

---

## How This Fits Into Real Healthcare Analytics

This workflow mirrors real-world tasks:

```id="kgzr02"
FHIR Bulk Export
        ↓
DataFrame Analysis
        ↓
Population Metrics
        ↓
Trend Prediction
```

Common use cases:

* chronic disease tracking
* healthcare planning
* public health analysis
* hospital reporting dashboards

---

## Relationship to Previous Labs

### Lab 6

Focused on:

```id="9tdi3p"
Feature engineering → ML inference
```

### Extra Credit Lab

Focused on:

```id="efr67y"
Population analytics → trend prediction
```

Together they represent two sides of healthcare AI:

| Area                | Purpose                       |
| ------------------- | ----------------------------- |
| Feature Engineering | Individual patient prediction |
| Bulk Analytics      | Population-level insights     |

---

## Key Takeaway

The most important lesson:

> Healthcare AI is not just about models — it starts with structured data analysis.

Before machine learning, analysts must:

* understand the data
* filter correctly
* aggregate meaningfully
* detect trends

---

## Running Tests

```bash id="tvqzvc"
pytest -v
```

Expected output:

```id="r77srm"
5 passed
```

---

## Final Submission

Submit ONLY:

```id="ykrt63"
eda.py
```

No zip or additional files required.

---

## Final Reflection

This lab demonstrates how standardized healthcare data enables scalable analytics workflows.

Even simple operations like filtering by SNOMED codes or counting yearly occurrences reflect real tasks performed by healthcare data scientists and analysts every day.



# Extra Credit 2 Lab : Working with Bulk-FHIR

Extra credit lab for CS6440

## Install
Using a virtual environment for this lab is highly recommended. You may create the environment through your method of choice, though please note instructions given here are generic. Creating the environment through VS Code is often the simplest solution.

### Example CLI Based Configuration
For an example using the Python CLI directly, assuming you have Python installed you can run:
```
python -m venv bulk_fhir
source ~/bulk_fhir/bin/activate
```
Change "python" to "python3" as needed, this depends on your environment. Then to install this lab's dependencies:

```
pip install -r requirements.lock
```

If you would like jupyternotebook, matplotlib, and pytest installed as well, you may use the alternative:
```
pip install -r requirements-dev.lock
```

## Instructions
All of the code that you will fill out is in `src/bulk_fhir/eda.py`. There are 4 methods that have TODOs. Do your best to answer them, and make sure that the base tests pass. Testing instructions below.

## Running Tests
To run tests, you require pytest. If you don't have pytest you can install the whole dev suite as mentioned in install above or just run:
```
pip install pytest
```

To execute pytest, you just need to run:
```
pytest
```


