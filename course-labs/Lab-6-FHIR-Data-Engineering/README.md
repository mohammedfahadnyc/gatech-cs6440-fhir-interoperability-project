# Lab 6 — Data Engineering & ML Inference with FHIR
@Mohammed Fahad
## Overview

This lab demonstrates how healthcare data represented in **FHIR (Fast Healthcare Interoperability Resources)** can be transformed into machine-learning-ready features and used for neural network inference.

The primary goal is **not** to train a machine learning model, but to understand the **data engineering pipeline** required to make healthcare data usable for ML systems.

The workflow simulates a realistic healthcare AI pipeline:

```
Raw FHIR Data (NDJSON)
        ↓
ETL / Feature Engineering
        ↓
Structured Tabular Features
        ↓
PyTorch Tensor Conversion
        ↓
Pretrained Neural Network Inference
        ↓
Stroke Risk Prediction
```

---

## Learning Objectives

This lab focuses on four core ideas:

1. Understanding FHIR as a structured healthcare data model.
2. Converting raw healthcare JSON data into ML features.
3. Applying common data engineering techniques:

   * feature creation
   * one-hot encoding
   * aggregation
   * imputation
   * normalization
4. Running inference using a pretrained neural network with PyTorch.

---

## Project Context — Why This Lab Exists

In real-world machine learning systems:

* **Most effort is spent preparing data**, not building models.
* Healthcare data is highly structured but complex.
* FHIR is becoming the standard way hospitals exchange data.

This lab models a common production scenario:

> You are given standardized clinical data and must transform it into usable numerical features for an existing model.

---

## What is FHIR?

FHIR (Fast Healthcare Interoperability Resources) is a healthcare data standard designed to make medical data consistent and interoperable.

Examples of FHIR resources:

| Resource    | Meaning                        |
| ----------- | ------------------------------ |
| Patient     | Demographics and personal info |
| Observation | Lab measurements or vitals     |
| Medication  | Prescriptions                  |
| Encounter   | Clinical visits                |

This lab uses:

* **Patient resources**
* **Observation resources**

---

## Input Data Format

The dataset is provided as **NDJSON** (newline-delimited JSON).

Each line represents one FHIR resource:

```json
{"resourceType":"Patient", ...}
{"resourceType":"Patient", ...}
```

This format is commonly used in real **bulk FHIR exports**.

---

## Architecture of the Lab

### High-Level Pipeline

```
Patient.ndjson       Observation.ndjson
       ↓                     ↓
   Patients ETL         Observations ETL
       ↓                     ↓
        -------- Feature Merge -------
                     ↓
              Feature DataFrame
                     ↓
             Tensor Conversion
                     ↓
             Neural Network Model
                     ↓
               Stroke Prediction
```

---

## Part 1 — ETL (Feature Engineering)

### 1. Patients Pipeline (`patients.py`)

This module generates demographic features.

#### Age Calculation

The raw FHIR patient record contains:

```
birthDate = YYYY-MM-DD
```

Machine learning models cannot directly use dates.

The pipeline converts:

```
birthDate → age (integer)
```

Age becomes a numeric feature used by the model.

---

#### Marital Status One-Hot Encoding

FHIR represents marital status as structured text:

```python
{"text": "Married"}
```

Neural networks require numerical input.

One-hot encoding transforms categories into binary columns:

| marital status | encoded columns |
| -------------- | --------------- |
| Married        | 0 1 0 0         |
| Divorced       | 1 0 0 0         |
| Widowed        | 0 0 1 0         |
| Never Married  | 0 0 0 1         |

This avoids introducing artificial numeric ordering between categories.

---

### 2. Observations Pipeline (`observations.py`)

This module extracts lab measurements.

#### LOINC Codes

Clinical observations are identified using universal codes:

| Measurement   | LOINC Code |
| ------------- | ---------- |
| Glucose       | 2339-0     |
| Triglycerides | 2571-8     |

Filtering by LOINC ensures consistent feature extraction.

---

#### Aggregation

Patients may have multiple observations:

```
Patient A glucose:
100, 110, 95
```

The pipeline groups by patient and computes:

```
mean value per patient
```

This ensures one feature row per patient.

---

#### Missing Data Imputation

Some patients lack measurements.

Many ML models cannot handle missing values, so missing data is replaced with:

```
column mean value
```

This is called **mean imputation**.

---

#### Z-Score Normalization

To improve neural network performance, features are standardized:

```
(x − mean) / standard_deviation
```

Benefits:

* equal feature scale
* faster model convergence
* improved numerical stability

Values are rounded to 3 decimal places for consistency.

---

## Part 2 — Neural Network Inference

### Tensor Conversion (`inference.py`)

Neural networks accept tensors, not DataFrames.

The processed features are converted into:

```
torch.Tensor
shape = (n_samples, n_features)
```

Feature order matters and must match the model’s expectation.

---

### Running Inference

The pretrained model produces:

1. **Probabilities** — likelihood of stroke risk
2. **Predictions** — binary classification

Output format:

```python
{
  "probabilities": np.ndarray,
  "predictions": np.ndarray
}
```

---

## Features Used by the Model

Final feature set:

* age
* married_Divorced
* married_Married
* married_Widowed
* married_Never Married
* glucose
* triglycerides

Each row represents one patient.

---

## What This Lab Simulates in Real Life

This workflow mirrors production healthcare AI systems:

```
EMR / FHIR Data
       ↓
Feature Engineering Pipeline
       ↓
Model Serving Layer
       ↓
Risk Scoring / Decision Support
```

Real-world applications include:

* stroke risk prediction
* patient triage systems
* preventative care analytics
* hospital decision support tools

---

## Key Engineering Concepts Reinforced

* Structured healthcare data processing
* Feature engineering for ML
* Handling missing clinical data
* Numerical normalization
* Data → tensor transformation
* Model inference pipelines

---

## What Was NOT Done

This lab does **not** include:

* training a neural network
* hyperparameter tuning
* model architecture design

The focus is purely on **data preparation and inference integration**.

---

## Key Takeaway

The most important lesson:

> Machine learning success depends heavily on data engineering.

Even with a perfect model, poor feature preparation leads to poor results.

This lab demonstrates how structured medical data becomes usable input for AI systems.

---

## Running Tests

```bash
pytest test/ -v
```

All tests passing confirms:

* ETL pipeline correctness
* normalization logic
* tensor shape correctness
* inference output format

---

## Files Modified

```
src/ml_fhir/etl/patients.py
src/ml_fhir/etl/observations.py
src/ml_fhir/inference.py
```

---

## Final Reflection

This lab represents a realistic workflow where engineers:

* do not build models
* but prepare and structure data so models can operate reliably

Understanding this pipeline is foundational for real-world machine learning engineering in healthcare systems.




# Lab 6: FHIR Data Engineering with Neural Network Inference

This lab introduces students to ETL (Extract, Transform, Load) processes for FHIR (Fast Healthcare Interoperability Resources) data and extends it with neural network inference capabilities. This gives you a sample on how machine learning models can be used to make predictions on FHIR data.

## Overview

Students will learn to:
1. Process FHIR newline-delimited JSON data into structured features
2. Apply data transformations (normalization, one-hot encoding, imputation)
3. Transform processed data into PyTorch tensors
4. Run inference using a pre-trained neural network model
5. Complete the full pipeline from raw FHIR data to predictions

## Quick Start with Docker

The easiest way could be getting started with Docker, which provides a consistent environment across all platforms. 

### Option 1: Using Docker directly

```bash
# Build the image
docker build -t fhir-lab .

# Run the container using mac, linux, or WSL
docker run -it --rm \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/test:/app/test \
  fhir-lab bash
```

### Running Tests in Docker

```bash
# Run tests using docker-compose
docker-compose run --rm fhir-lab-test

# Or using docker directly
docker run --rm \
  -v $(pwd)/test:/app/test \
  -v $(pwd)/src:/app/src \
  fhir-lab uv run pytest test/ -v
```

### Running the Demo in Docker

```bash
# Run demo using docker-compose
docker-compose run --rm fhir-lab-demo

# Or using docker directly
docker run --rm \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/demo.py:/app/demo.py \
  fhir-lab python demo.py
```

## Quick start without Docker

It is entirely possible to run this lab without Docker. You just need to have python installed, be comfortable with virtual environments, or use `uv`.

### Using a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### Using UV

```bash
uv sync --all-extras
```

## Project Structure

```
Lab-6-FHIR-Data-Engineering/
├── src/ml_fhir/
│   ├── etl/                    # ETL processing classes
│   │   ├── _base.py           # Base class with tensor conversion
│   │   ├── patients.py        # Patient data processing (Part 1 Exercise 1)
│   │   ├── observations.py    # Clinical observations processing (Part 1 Exercises 2-3)
│   │   
│   ├── models.py              # Neural network model definition
│   ├── inference.py           # Inference engine and neural network (Part 2 Exercise 1-2)
│   ├── train.py               # Model training (hidden from students)
│   └── process.py             # Complete pipeline example
├── data/                      # FHIR data files
├── models/                    # Pre-trained model state dicts
├── test/                      # Test files
├── demo.py                    # Demonstration script
├── pyproject.toml            # Modern Python packaging (uv)
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Multi-service container setup
└── .dockerignore             # Docker build optimization
```

## Exercise Structure

### **PART 1: ETL EXERCISES**

#### Exercise 1: Patient Data Processing (`src/ml_fhir/etl/patients.py`)
- **Exercise 1-1**: Calculate age from birthDate
- **Exercise 1-2**: One-hot encode marital status (4 columns: Divorced, Married, Widowed, Never Married)

#### Exercise 2: Observation Data Processing (`src/ml_fhir/etl/observations.py`)
- **Exercise 2**: Impute missing values for glucose and triglycerides using LOINC codes
  - Glucose: "2339-0"
  - Triglycerides: "2571-8"

#### Exercise 3: Data Normalization (`src/ml_fhir/etl/observations.py`)
- **Exercise 3**: Apply z-score normalization to glucose and triglycerides columns

### **PART 2: NEURAL NETWORK EXERCISES**

#### Exercise 1: Tensor Conversion (`src/ml_fhir/inference.py`)
```python
def student_exercise_1_convert_to_tensor(df: pd.DataFrame) -> torch.Tensor:
    """
    Convert processed FHIR DataFrame to PyTorch tensor for neural network input.
    """
    # TODO: Implement tensor conversion
    raise NotImplementedError
```

#### Exercise 2: Neural Network Inference (`src/ml_fhir/inference.py`)
```python
def student_exercise_2_run_inference(tensor: torch.Tensor, model_manager: ModelManager) -> dict:
    """
    Run inference using the pre-trained neural network model and output the probabilities and the predictions. 
    """
    # TODO: Implement inference
    raise NotImplementedError
```

## Features

### ETL Processing
- **Patient Data**: Age calculation, marital status one-hot encoding
- **Observations**: Glucose and triglyceride measurements with imputation and normalization

### Neural Network Integration
- **Model Architecture**: 3-layer neural network (7 input features → 16 → 8 → 1 output)
- **Tensor Conversion**: Automatic conversion from processed DataFrames to PyTorch tensors
- **Inference Engine**: Complete pipeline from FHIR data to predictions
- **Pre-trained Models**: State dicts provided for immediate inference

## Usage Examples

### Basic ETL Processing
```python
from ml_fhir.etl import Patients, Observations, Label

# Process patient data
patients = Patients("data/Patient.ndjson")
patient_features = patients.pipeline()

# Process observations
observations = Observations("data/Observations.ndjson", "data/Patient.ndjson")
observation_features = observations.pipeline()

# Process labels
labels = Label("data/Observations.ndjson", "data/Patient.ndjson")
stroke_labels = labels.pipeline()
```

### Neural Network Inference
```python
from ml_fhir.inference import FHIRInferenceEngine

# Initialize inference engine
engine = FHIRInferenceEngine()

# Run complete inference pipeline
results = engine.run_inference_pipeline(
    patient_path="data/Patient.ndjson",
    observations_path="data/Observations.ndjson"
)

# Access predictions
probabilities = results['probabilities']
predictions = results['predictions']
```

### Tensor Conversion
```python
from ml_fhir.etl._base import DataFrameFromJSONMixin

# Convert DataFrame to tensor
feature_columns = ['age', 'married_Divorced', 'married_Married', 'married_Widowed', 
                  'married_Never Married', 'glucose', 'triglycerides']
tensor = DataFrameFromJSONMixin.to_tensor(processed_df, feature_columns)
```

## Model Architecture

The neural network model expects 7 input features:
1. **Age** (normalized)
2. **Marital Status** (one-hot encoded: 4 features)
   - Divorced
   - Married
   - Widowed
   - Never Married
3. **Glucose** (normalized)
4. **Triglycerides** (normalized)

The model architecture:
- Input Layer: 7 features
- Hidden Layer 1: 16 neurons with ReLU activation
- Hidden Layer 2: 8 neurons with ReLU activation
- Output Layer: 1 neuron with Sigmoid activation
- Dropout: 20% for regularization

## Setup and Instructions

1. **Verify data files exist under `data/`.** There should be 4 ndjson files:
   - `Patient.ndjson`
   - `Observations.ndjson`
   - `test-patients.ndjson`
   - `test-observations.ndjson`

2. **Verify model file exists under `model/`.** There should be 1 pth file:
   - `stroke_prediction_model.pth`

3. **Complete the ETL exercises** outlined above under PART 1: ETL EXERCISES

4. **Complete the neural network exercises** outlined above under PART 2: NEURAL NETWORK EXERCISES

5. **(Optional) Run the complete pipeline:**
```bash
python demo.py
```

### Troubleshooting

- **Model not found**: Run `python generate_model.py` to create the pre-trained model
- **Import errors**: Ensure `PYTHONPATH` includes the `src` directory
- **Docker issues**: Make sure Docker and Docker Compose are installed and running

## General Student Workflow

1. **Start with ETL Exercises**: Complete exercises 1-4 in the respective files
2. **Move to Neural Network Exercises**: Complete exercises 1-2 in `inference.py`
3. **Test Your Work**: Run `pytest tests`
4. **Run Complete Pipeline**: Use `demo.py` to see the full workflow

## Learning Objectives

By the end of this lab, students will be able to:
- Process FHIR JSON data into structured features
- Apply data transformations (normalization, one-hot encoding, imputation)
- Convert processed data to PyTorch tensors
- Run inference using pre-trained neural networks
- Understand the complete ML pipeline from raw data to predictions