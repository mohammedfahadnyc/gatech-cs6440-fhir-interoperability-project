#!/usr/bin/env python3
"""
Script to generate a pre-trained neural network model for student use.
This script will be run by instructors to create the model state dict.
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ml_fhir.train import train_neural_net


def main():
    """
    Generate a pre-trained model for student inference.
    """
    print("Generating pre-trained neural network model...")
    print("This will train a model on the FHIR data and save it for student use.")
    
    try:
        # Train the model
        train_neural_net()
        
        print("\n" + "="*50)
        print("Model generation completed successfully!")
        print("The model state dict has been saved to models/stroke_prediction_model.pth")
        print("Students can now use this model for inference exercises.")
        
    except Exception as e:
        print(f"Error generating model: {e}")
        print("Please ensure all data files are present and the ETL pipeline works correctly.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 