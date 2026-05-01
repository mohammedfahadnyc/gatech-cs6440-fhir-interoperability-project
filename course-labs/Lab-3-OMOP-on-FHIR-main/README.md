# Lab 3 – OMOP on FHIR
@Mohammed Fahad
## Project Overview

This lab explored how clinical FHIR resources are translated into the OMOP Common Data Model using the OMOPonFHIR server. The goal was to understand how standardized healthcare data is normalized, stored, and returned through a mapping layer between two different healthcare standards.

The environment was deployed locally using Docker and PostgreSQL, and FHIR resources were posted to the OMOPonFHIR server to observe how they are written into OMOP tables.

---

## Deployment

The OMOPonFHIR server and OMOP database were launched using Docker Compose. Vocabulary files from OHDSI Athena were loaded to support concept mapping. Once deployed, the FHIR UI was accessed at:

http://localhost:8080

Resources were posted through the UI and retrieved to inspect server behavior and database changes.

---

## Key Observations

### Patient Resource

After posting a Patient resource, the server added a standardized U.S. Core Race extension when the resource was retrieved. The race coding returned was automatically generated to represent unknown race, demonstrating how OMOPonFHIR enforces standardized representations even when data is incomplete.

---

### Observation Mapping

Three Observation resources were mapped to OMOP tables based on their classification:

- observation_1 → measurement table
- observation_2 → measurement table
- observation_3 → observation table

A fourth observation replaced `valueCodeableConcept` with `valueString` when returned from the server, showing how values are simplified to match OMOP storage constraints.

---

### Medication Mapping

MedicationStatement resources were stored in the `drug_exposure` table. This confirms that medication-related events are normalized into OMOP’s pharmacological schema.

---

## Data Model Exercises

Python exercises demonstrated direct interaction with OMOP schema rows:

- Extracting measurement values
- Building a patient full name
- Retrieving gender via dynamic column lookup

These reinforced understanding of schema indexing and tuple-based access.

---

## Conclusion

OMOPonFHIR acts as a translation layer that normalizes FHIR data into a research-ready schema. The lab highlights the complexity of healthcare interoperability and the importance of standardized mappings when working across clinical systems.



About the Project: 

# CS 6440 Lab 3 - OMOP-on-FHIR

This lab is based on the OMOP on FHIR Demo main repository found at https://github.com/SmartChartSuite/OMOP-on-FHIR-Demo. It has been slightly
modified for student use, with additional lab focused code added in the `/student` folder. The files in the `/resources` folder are generic FHIR
resources but also intended for students to use with this lab.

## Quick Start for OMOP-on-FHIR
For help with this demo, please reach out to Elizabeth.Shivers@gtri.gatech.edu.

### Step 1 - Download Athena Vocab
Go to https://athena.ohdsi.org/search-terms/start. Go to Download.

Select the following Vocabularies to Download:
* LOINC
* SNOMED
* RxNorm
* Gender (OMOP Gender)
* Race (Race and Ethnicity Code Set (USBC))

### Step 2 - Add Vocab to Build Path
Extract the .CSV files from the zip provided by Athena. Place the CSVs in the /vocab directory (which should be available when you clone with a place holder file inside it).

### Step 3 - Run Docker
With Docker Desktop/Engine running, execute the following command:
`docker compose up`

## Troubleshooting
If you run into an error, cancel your running container with CTRL+C in the terminal. Then be sure to remove the partially configured container with `docker compose down` before running the `up` command again.

## Health Check Script
The OMOP CDM database image used includes a health check script which allows the OMOP on FHIR container to wait until the `f_person` tables are available prior to starting. This shows up as an expected "error" in the logs, as follows:

```
2023-06-30 16:58:46.481 UTC [91] ERROR:  relation "f_person" does not exist at character 15
2023-06-30 16:58:46.481 UTC [91] STATEMENT:  SELECT * FROM f_person;
```
This message can be disregarded.

Please note this script may not work consistently in all environments, and has been observed to not always function as expected in Non-WSL Windows deployments, starting the OMOP on FHIR container prior to the required dependencies being setup. In such a case, you may have to stop the containers *after the database has been loaded fully* and rerun them per the troubleshooting section of this file. (It should pick up with the database fully loaded and should not impact the operation of the containers.)