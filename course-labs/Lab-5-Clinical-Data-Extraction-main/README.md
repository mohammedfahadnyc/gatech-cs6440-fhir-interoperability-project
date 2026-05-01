# CS-6440 Lab 5 — Clinical Data Extraction (FHIR RAG QA)

## 📌 Project Overview

This project demonstrates a **Retrieval-Augmented Generation (RAG)** workflow for answering clinical questions using **FHIR healthcare data**.

The lab simulates a real-world AI workflow:

1. Extract clinical notes from FHIR bundles.
2. Convert notes into searchable embeddings.
3. Store them inside a vector database.
4. Retrieve relevant context for a question.
5. Use an LLM (Flan-T5) to generate answers.
6. Compare answers against reference answers.
7. Compute NLP evaluation metrics.
8. Prepare structured results for grading.

The goal is not model training — it is understanding the **end-to-end pipeline** of healthcare data → retrieval → LLM reasoning → evaluation.

---

## 🧠 Core Concepts Used

### 1. FHIR Bundles

FHIR (Fast Healthcare Interoperability Resources) is a healthcare data standard.

Each patient JSON file contains multiple resources:

* Patient
* Observations
* DocumentReference (clinical notes)
* DiagnosticReport
* Medications, etc.

In this lab we mainly extract:

```
DocumentReference → clinical notes
```

---

### 2. Clinical Note Extraction

Clinical notes inside FHIR are stored as:

```
base64 encoded text
```

The lab requires:

* Decoding base64 content
* Extracting note text
* Formatting notes into readable files

Output:

```
clinical_notes_output.txt
```

---

### 3. Vector Database (RAG)

The extracted notes are:

1. Split into chunks
2. Converted into embeddings
3. Stored in a Chroma vector database

Embedding model used:

```
nomic-ai/nomic-embed-text-v1
```

This allows semantic search over clinical notes.

---

### 4. Question Answering (LLM)

The pipeline:

```
Question
   ↓
Vector DB Retrieval
   ↓
Relevant Context
   ↓
Flan-T5 Model
   ↓
Generated Answer
```

Model used:

```
Google Flan-T5
```

The model answers 10 healthcare questions per patient.

---

### 5. Evaluation Metrics

Generated answers are compared against reference answers (OpenAI outputs).

Metrics computed:

* BLEU
* ROUGE
* METEOR
* BERTScore

Results are saved as:

```
submission/experimentX/experiment_result.json
```

---

## 🧩 Project Pipeline (High Level)

```
FHIR Bundle (.json)
        ↓
Extract Notes
        ↓
Decode Base64
        ↓
clinical_notes_output.txt
        ↓
Vector Embeddings
        ↓
Chroma Vector DB
        ↓
Retrieve Context
        ↓
Flan-T5 Answer Generation
        ↓
Evaluation Metrics
        ↓
Submission JSON
```

---

## 📂 Important Files

### Main Files

| File                         | Purpose                |
| ---------------------------- | ---------------------- |
| `experiments.ipynb`          | Main notebook pipeline |
| `experiments.py`             | Core lab logic         |
| `experiments.json`           | Configuration file     |
| `fhir_bundles/patient*.json` | Input patient data     |

---

### Generated Files

| File                                            | Purpose                 |
| ----------------------------------------------- | ----------------------- |
| `clinical_notes_output.txt`                     | Extracted notes         |
| `patientX_result.json`                          | QA output per patient   |
| `submission/experimentX/experiment_result.json` | Final evaluated results |

---

## 🔧 Required Coding Changes (Lab Tasks)

Only two TODOs were required inside `experiments.py`:

### 1. Base64 Decode

Function:

```python
decode_base64()
```

Purpose:

* Convert encoded clinical note → readable text.

---

### 2. Extract Notes

Function:

```python
extract_notes()
```

Purpose:

* Call decode function.
* Pull clinical note text from FHIR.

---

## ▶️ Execution Flow (Colab)

### Step 1 — Setup

* Install requirements
* Load notebook config

### Step 2 — Select Patient Bundle

Example:

```python
bundle_name = "fhir_bundles/patient1.json"
```

---

### Step 3 — Extract Clinical Notes

```python
main_read_fhir_bundle(config)
```

---

### Step 4 — Load Vector DB + Model

```python
main_vector_db_and_genai_model_config(config)
```

---

### Step 5 — Generate Answers

```python
main_question_answering(config, "No")
```

---

### Step 6 — Evaluate Metrics

Run NLP evaluation cell.

This creates:

```
submission/experimentX/experiment_result.json
```

---

### Step 7 — Repeat for ALL Patients

Required experiments:

```
patient1 → experiment1
patient2 → experiment2
...
patient9 → experiment9
```

---

### Step 8 — Verify Experiments

Notebook checks required experiments exist.

---

## ⚠️ Lessons Learned.
* Vector DB + model loading is expensive; avoid rerunning unnecessarily.

---

## 🧭 What This Project Teaches

This lab demonstrates a real production AI pattern:

```
Unstructured Data → Retrieval → LLM Reasoning → Evaluation
```

Skills gained:

* Working with healthcare FHIR data
* Base64 decoding in clinical datasets
* Vector databases (Chroma)
* Embeddings
* Retrieval-Augmented Generation (RAG)
* NLP metric evaluation

---


Key idea:

> The LLM is NOT answering from memory — it answers using retrieved context from clinical notes.

The intelligence pipeline is:

```
Data → Retrieval → Context → Generation
```

That is the foundation of modern enterprise AI systems.

---

## 👤 Author

Mohammed Fahad
Georgia Tech — CS-6440
Clinical Data Extraction Lab




# **Learning Objective**

- **Course Overview**:
  - Understand how to use AI models to answer clinical questions from FHIR-based patient data.

- **Objectives**:
  - Extract important clinical information (e.g., allergies, medications) from patient records.
  - Apply AI to analyze and answer specific healthcare-related questions.
  - Evaluate the accuracy of AI-generated answers by comparing them with expert-provided responses.
 
- **Patient Data**:
We have provided 9 patient bundles in this notebook. These bundles contain the necessary FHIR resources needed for the experiment.

- **Key Questions**:
Using the provided data, load it into the vector database and conduct the experiments to answer the following questions accurately:

What allergies does the patient have? Answer correctly.
What medications is the patient currently taking? Answer correctly.
What immunizations has the patient received? Answer correctly.
What is the patient's primary diagnosis? Answer correctly.
What procedures were conducted on the patient? Answer correctly.
What treatments have been administered during the recent visit? Answer correctly.
What is the patient's history of present illness? Answer correctly.
What are the patient's vital info? Answer correctly.
What findings are mentioned in the patient's assessment and plan? Answer correctly.
What follow-up care is planned for the patient? Answer correctly.

# Addtional References

# Understanding Vector Databases and Their Role in GenAI Applications

## Vector Database Basics

Vector databases are specialized data storage systems designed to handle high-dimensional vector data efficiently. Unlike traditional databases that store structured data in rows and columns or flexible documents, vector databases are optimized for storing and querying data represented as numerical vectors. These vectors often originate from embedding techniques that convert complex data types—like text, images, or audio—into numerical formats that capture their semantic meaning.

## How Vector Databases Differ from SQL and NoSQL Databases

### Data Storage and Structure

- **SQL Databases**: Use structured schemas with predefined tables and relationships. Data is stored in rows and columns, making them ideal for applications requiring complex queries and transactions.

- **NoSQL Databases**: Offer flexible schemas to store unstructured or semi-structured data. They include various types like key-value stores, document databases, and graph databases, each optimized for specific data models.

- **Vector Databases**: Specifically designed to store and manage vector embeddings. They focus on efficient similarity search and nearest neighbor queries in high-dimensional spaces.

### Query Capabilities

- **SQL**: Utilize Structured Query Language for complex queries involving joins, aggregations, and transactions.

- **NoSQL**: Provide query mechanisms tailored to the specific data model, often sacrificing complex querying capabilities for scalability and speed.

- **Vector Databases**: Enable similarity searches using distance metrics like cosine similarity or Euclidean distance to find vectors closest to a query vector.

## Importance of Vector Databases for GenAI Applications

### Overcoming Context Window Limitations in LLMs

Large Language Models (LLMs) like GPT-4 have a fixed context window, limiting the amount of information they can process at once. Vector databases help overcome this limitation by enabling the retrieval of relevant information from large datasets in a way that fits within the context window. By fetching only the most pertinent data based on similarity to the input query, they ensure that the LLM operates efficiently without exceeding its capacity.

### Providing Broader Short-Term Memory and In-Context Learning

Vector databases act as an extended memory for GenAI applications. They store vast amounts of embedded knowledge that can be quickly queried and fed into the LLM. This approach enhances in-context learning by providing the model with additional relevant information, leading to more accurate and contextually appropriate responses.

## What is Retrieval-Augmented Generation (RAG)?

Retrieval-Augmented Generation (RAG) is a pattern that combines the strengths of LLMs with external data sources to produce more informed and accurate outputs. The process involves:

1. **Retrieval**: Extracting relevant information from a database (like a vector database) based on the input query.

2. **Augmentation**: Supplying this retrieved data to the LLM as additional context.

3. **Generation**: The LLM generates a response that is informed by both the initial input and the augmented data.

### How RAG Patterns Are Evolving

- **Graph RAG**: An advanced variation that incorporates graph databases to capture and utilize the relationships between different data points. This method enriches the retrieval process by considering the connections and dependencies within the data, leading to more nuanced and insightful responses.

- **Enhanced Retrieval Techniques**: Combining vector similarity with other retrieval methods to improve the relevance and accuracy of the information supplied to the LLM.

- **Domain-Specific Adaptations**: Tailoring RAG architectures to specific fields (like healthcare) to handle specialized terminology and data structures more effectively.

## Conclusion

Understanding vector databases and RAG patterns is crucial for developing advanced GenAI applications, especially in fields like health informatics. These technologies address the limitations of LLMs by extending their effective context and enabling access to pertinent information stored externally. As you work on your lab and future projects, consider how leveraging vector databases and exploring evolving RAG patterns can enhance your data analysis capabilities and lead to deeper insights.



