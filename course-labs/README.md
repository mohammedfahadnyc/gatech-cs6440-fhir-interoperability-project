# Georgia Tech CS 6440 — Healthcare Interoperability & Clinical AI Portfolio 
This repository showcases a series of applied healthcare engineering projects focused on interoperability, clinical data systems, and AI pipelines built on the FHIR (Fast Healthcare Interoperability Resources) standard.

The work demonstrates end-to-end experience across:

• clinical data APIs  
• healthcare data normalization  
• research database mapping  
• SMART-on-FHIR app development  
• large language model pipelines  
• machine learning feature engineering  

Each project mirrors real-world workflows used in modern electronic health record (EHR) systems, healthcare research platforms, and AI-driven clinical decision tools.

The labs progress from raw FHIR resource handling → standardized research schemas → secure app integration → clinical NLP → machine learning inference.

This repository serves as a practical portfolio of healthcare software engineering and clinical AI workflows.

This contains a sequence of hands-on labs exploring modern healthcare interoperability, data engineering, and machine learning using the FHIR (Fast Healthcare Interoperability Resources) standard.

Each lab builds practical experience with real healthcare data systems, from API-level integration to ML feature engineering.

---

## Lab Overview

### Lab 2 — FHIR Resource Manipulation

Focused on programmatic interaction with FHIR resources using Java and HAPI FHIR.  
Implemented handlers to navigate bundles, modify patient data, and construct standardized resources.

Key skills:
- FHIR resource modeling
- Java healthcare APIs
- Bundle navigation
- Resource transformation

---

### Lab 3 — OMOP on FHIR

Deployed an OMOPonFHIR server using Docker and PostgreSQL to observe how clinical FHIR data is normalized into the OMOP Common Data Model.

Posted synthetic patient data and analyzed how different FHIR resources are mapped into research tables such as measurement, observation, and drug_exposure.

Key skills:
- Healthcare data mapping
- OMOP Common Data Model
- Docker infrastructure
- Clinical database inspection
- Python schema interaction

---

### Lab 4 — SMART on FHIR Application

Developed a SMART on FHIR web app using Angular and TypeScript to perform secure FHIR queries inside a simulated EHR environment.

Implemented medication search, update, and creation workflows using SMART client APIs.

Key skills:
- SMART on FHIR authentication
- OAuth healthcare workflows
- Angular front-end integration
- Client-side FHIR CRUD operations

---

### Lab 5 — Clinical Data Extraction with LLMs

Used Retrieval-Augmented Generation (RAG) to answer clinical questions from FHIR bundles using a vector database and a language model.

Extracted notes from synthetic patient bundles and evaluated LLM responses against ground-truth answers.

Key skills:
- Clinical NLP pipelines
- Vector databases
- FHIR document processing
- AI-assisted question answering

---

### Lab 6 — Data Engineering & Machine Learning with FHIR

Transformed bulk FHIR exports into tabular machine learning features using pandas and PyTorch.

Implemented feature engineering, normalization, and inference with a pre-trained neural network to predict stroke risk.

Key skills:
- FHIR data engineering
- ML feature construction
- pandas pipelines
- PyTorch inference
- healthcare predictive modeling

---

## Technologies Used

- FHIR (HL7 standard)
- HAPI FHIR
- OMOP Common Data Model
- Docker & PostgreSQL
- Angular / TypeScript
- Python / pandas / PyTorch
- Vector databases
- Large Language Models

---

## Purpose of This Repository

This project demonstrates practical skills in:

- healthcare interoperability
- clinical data transformation
- modern FHIR-based application development
- ML pipelines using real healthcare data structures

The labs simulate workflows used in production EHR systems, research databases, and AI-assisted clinical tools.

---

## Disclaimer

All patient data used in these labs is synthetic and generated for educational purposes only.
