from ml_fhir.etl import Patients, Observations, Label
from ml_fhir.inference import FHIRInferenceEngine
import pandas as pd

'''
Process the data pipeline to run all of the transformations needed to create
the final dataset for machine learning training and inference.
'''

def process_pipeline(): 
    """
    Complete ETL pipeline that processes FHIR data and prepares it for ML.
    """
    # Process patient data
    patients = Patients("data/Patient.ndjson")
    patient_features = patients.pipeline()
    
    # Process observation data
    observations = Observations("data/Observations.ndjson", "data/Patient.ndjson")
    observation_features = observations.pipeline()
    
    # Process labels
    labels = Label("data/Observations.ndjson", "data/Patient.ndjson")
    stroke_labels = labels.pipeline()
    
    # Merge all features
    final_df = patient_features.merge(observation_features, on='id', how='inner')
    final_df = final_df.merge(stroke_labels, on='id', how='inner')
    
    print(f"Final dataset shape: {final_df.shape}")
    print(f"Features: {list(final_df.columns)}")
    
    return final_df


def run_inference_example():
    """
    Example of running neural network inference on FHIR data.
    This demonstrates the complete pipeline from FHIR data to predictions.
    """
    print("Running FHIR to Neural Network Inference Example...")
    
    # Initialize inference engine
    inference_engine = FHIRInferenceEngine()
    
    # Run complete inference pipeline
    results = inference_engine.run_inference_pipeline(
        patient_path="data/Patient.ndjson",
        observations_path="data/Observations.ndjson"
    )
    
    # Display results
    print(f"\nInference Results:")
    print(f"Number of patients processed: {len(results['patient_ids'])}")
    print(f"Average stroke risk: {results['predictions'].mean():.4f}")
    print(f"Number of high-risk patients (risk > 0.5): {(results['predictions'] > 0.5).sum()}")
    
    # Show first few predictions
    print(f"\nFirst 5 predictions:")
    for i in range(min(5, len(results['patient_ids']))):
        patient_id = results['patient_ids'][i]
        risk = results['predictions'][i]
        prediction = results['predictions']['predictions'][i]
        print(f"Patient {patient_id}: Risk={risk:.4f}, Prediction={'Stroke' if prediction else 'No Stroke'}")
    
    return results


if __name__ == "__main__":
    # Run ETL pipeline
    print("Running ETL Pipeline...")
    final_data = process_pipeline()
    
    # Run inference example
    print("\n" + "="*50)
    inference_results = run_inference_example()
