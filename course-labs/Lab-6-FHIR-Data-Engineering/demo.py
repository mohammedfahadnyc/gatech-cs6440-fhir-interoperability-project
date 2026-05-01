#!/usr/bin/env python3
"""
Demo script showing the complete FHIR to Neural Network pipeline.

This script demonstrates:
1. ETL processing of FHIR data
2. Tensor conversion
3. Neural network inference
4. Complete end-to-end pipeline
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ml_fhir.etl import Patients, Observations, Label
from ml_fhir.inference import FHIRInferenceEngine
from ml_fhir.models import ModelManager
import pandas as pd


def demo_etl_pipeline():
    """Demonstrate the ETL pipeline."""
    print("=" * 60)
    print("DEMO: ETL Pipeline")
    print("=" * 60)
    
    try:
        # Process patient data
        print("1. Processing patient data...")
        patients = Patients("data/Patient.ndjson")
        patient_features = patients.pipeline()
        print(f"   ✓ Patient features shape: {patient_features.shape}")
        print(f"   ✓ Patient features: {list(patient_features.columns)}")
        
        # Process observation data
        print("\n2. Processing observation data...")
        observations = Observations("data/Observations.ndjson", "data/Patient.ndjson")
        observation_features = observations.pipeline()
        print(f"   ✓ Observation features shape: {observation_features.shape}")
        print(f"   ✓ Observation features: {list(observation_features.columns)}")
        
        # Process labels
        print("\n3. Processing labels...")
        labels = Label("data/Observations.ndjson", "data/Patient.ndjson")
        stroke_labels = labels.pipeline()
        print(f"   ✓ Stroke labels shape: {stroke_labels.shape}")
        print(f"   ✓ Stroke labels: {list(stroke_labels.columns)}")
        
        # Merge all features
        print("\n4. Merging features...")
        final_df = patient_features.merge(observation_features, on='id', how='inner')
        final_df = final_df.merge(stroke_labels, on='id', how='inner')
        print(f"   ✓ Final dataset shape: {final_df.shape}")
        print(f"   ✓ Final features: {list(final_df.columns)}")
        
        return final_df
        
    except Exception as e:
        print(f"   ✗ Error in ETL pipeline: {e}")
        return None


def demo_tensor_conversion(df):
    """Demonstrate tensor conversion."""
    print("\n" + "=" * 60)
    print("DEMO: Tensor Conversion")
    print("=" * 60)
    
    try:
        from ml_fhir.etl._base import DataFrameFromJSONMixin
        
        feature_columns = ['age', 'married_Divorced', 'married_Married', 'married_Widowed', 
                          'married_Never Married', 'glucose', 'triglycerides']
        
        print("1. Converting DataFrame to tensor...")
        tensor = DataFrameFromJSONMixin.to_tensor(df, feature_columns)
        print(f"   ✓ Tensor shape: {tensor.shape}")
        print(f"   ✓ Tensor dtype: {tensor.dtype}")
        print(f"   ✓ Tensor device: {tensor.device}")
        
        return tensor
        
    except Exception as e:
        print(f"   ✗ Error in tensor conversion: {e}")
        return None


def demo_neural_network_inference(tensor):
    """Demonstrate neural network inference."""
    print("\n" + "=" * 60)
    print("DEMO: Neural Network Inference")
    print("=" * 60)
    
    try:
        print("1. Loading pre-trained model...")
        model_manager = ModelManager()
        model_manager.load_model()
        print("   ✓ Model loaded successfully")
        
        print("\n2. Running inference...")
        predictions = model_manager.predict_proba(tensor)
        classes = model_manager.predict_classes(tensor, threshold=0.5)
        
        print(f"   ✓ Predictions shape: {predictions.shape}")
        print(f"   ✓ Classes shape: {classes.shape}")
        
        # Show some statistics
        print(f"\n3. Prediction statistics:")
        print(f"   ✓ Average stroke risk: {predictions.mean():.4f}")
        print(f"   ✓ High-risk patients (risk > 0.5): {(predictions > 0.5).sum()}")
        print(f"   ✓ Predicted strokes: {classes.sum()}")
        
        return predictions, classes
        
    except Exception as e:
        print(f"   ✗ Error in neural network inference: {e}")
        return None, None


def demo_complete_pipeline():
    """Demonstrate the complete pipeline."""
    print("\n" + "=" * 60)
    print("DEMO: Complete Pipeline")
    print("=" * 60)
    
    try:
        print("1. Running complete inference pipeline...")
        inference_engine = FHIRInferenceEngine()
        
        results = inference_engine.run_inference_pipeline(
            patient_path="data/Patient.ndjson",
            observations_path="data/Observations.ndjson"
        )
        
        print(f"   ✓ Number of patients processed: {len(results['patient_ids'])}")
        print(f"   ✓ Average stroke risk: {results['predictions'].mean():.4f}")
        print(f"   ✓ High-risk patients: {(results['predictions'] > 0.5).sum()}")
        
        # Show first few predictions
        print(f"\n2. Sample predictions:")
        for i in range(min(3, len(results['patient_ids']))):
            patient_id = results['patient_ids'][i]
            risk = results['predictions'][i]
            prediction = results['predictions']['predictions'][i]
            print(f"   Patient {patient_id}: Risk={risk:.4f}, Prediction={'Stroke' if prediction else 'No Stroke'}")
        
        return results
        
    except Exception as e:
        print(f"   ✗ Error in complete pipeline: {e}")
        return None


def main():
    """Run all demos."""
    print("FHIR Data Engineering with Neural Network Inference - DEMO")
    print("This demo shows the complete pipeline from FHIR data to predictions.")
    
    # Check if model exists
    model_path = "models/stroke_prediction_model.pth"
    if not os.path.exists(model_path):
        print(f"\n⚠️  Warning: Pre-trained model not found at {model_path}")
        print("   Instructors should run 'python generate_model.py' to create the model.")
        print("   Continuing with ETL demo only...\n")
        
        # Run ETL demo only
        df = demo_etl_pipeline()
        if df is not None:
            demo_tensor_conversion(df)
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETED (ETL only - no model available)")
        print("=" * 60)
        return
    
    # Run all demos
    df = demo_etl_pipeline()
    if df is not None:
        tensor = demo_tensor_conversion(df)
        if tensor is not None:
            demo_neural_network_inference(tensor)
    
    demo_complete_pipeline()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main() 