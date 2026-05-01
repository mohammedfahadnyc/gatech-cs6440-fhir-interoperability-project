import pytest
import torch
import pandas as pd
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ml_fhir.models import StrokePredictionModel, ModelManager
from ml_fhir.inference import FHIRInferenceEngine, student_exercise_1_convert_to_tensor, student_exercise_2_run_inference


class TestNeuralNetwork:
    
    def test_model_architecture(self):
        """Test that the model has the correct architecture."""
        model = StrokePredictionModel()
        
        # Test input size
        test_input = torch.randn(10, 7)  # 10 samples, 7 features
        output = model(test_input)
        
        assert output.shape == (10, 1), f"Expected shape (10, 1), got {output.shape}"
        assert torch.all((output >= 0) & (output <= 1)), "Output should be between 0 and 1 (sigmoid)"
    
    def test_model_manager(self):
        """Test ModelManager functionality."""
        manager = ModelManager()
        
        # Test prediction methods
        X = torch.randn(5, 7)
        

        model_manager = ModelManager()
        model_manager.load_model()
        # Test predict_proba method
        probabilities = manager.predict_proba(X)
        results = student_exercise_2_run_inference(X, model_manager)
        print('Probabilities:', results['probabilities'])
        assert results['probabilities'].shape == (5,)
        assert np.all((results['probabilities'] >= 0) & (results['probabilities'] <= 1))
        
        # Test predict_classes method
        assert results['predictions'].shape == (5,)
        assert np.all((results['predictions'] == 0) | (results['predictions'] == 1))
    
    def test_tensor_conversion(self):
        """Test DataFrame to tensor conversion."""
        # Create sample DataFrame
        df = pd.DataFrame({
            'age': [25, 30, 35],
            'married_Divorced': [0, 1, 0],
            'married_Married': [1, 0, 1],
            'married_Widowed': [0, 0, 0],
            'married_Never Married': [0, 0, 0],
            'glucose': [0.5, -0.2, 0.8],
            'triglycerides': [0.1, 0.3, -0.1]
        })
        
        # Test the tensor conversion
        tensor = student_exercise_1_convert_to_tensor(df)
        
        assert isinstance(tensor, torch.Tensor)
        assert tensor.shape == (3, 7)
        assert tensor.dtype == torch.float32
    
    def test_inference_engine(self):
        """Test FHIRInferenceEngine functionality."""
        engine = FHIRInferenceEngine()
        
        # Test feature columns
        expected_columns = ['age', 'married_Divorced', 'married_Married', 'married_Widowed', 
                           'married_Never Married', 'glucose', 'triglycerides']
        assert engine.feature_columns == expected_columns
    
    def test_tensor_conversion_with_missing_features(self):
        """Test tensor conversion with missing features."""
        # Create DataFrame with missing features
        df = pd.DataFrame({
            'age': [25, 30],
            'glucose': [0.5, -0.2],
            'triglycerides': [0.1, 0.3]
        })
        
        engine = FHIRInferenceEngine()
        
        # Should raise ValueError for missing features
        with pytest.raises(ValueError):
            engine.convert_to_tensor(df)


if __name__ == "__main__":
    pytest.main([__file__]) 