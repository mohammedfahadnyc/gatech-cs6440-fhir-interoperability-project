import torch
import pandas as pd
from .models import ModelManager
from .etl import Patients, Observations, Label


# Student exercise functions
def student_exercise_1_convert_to_tensor(df: pd.DataFrame) -> torch.Tensor:
    """
    Student Exercise 1: Convert DataFrame to Tensor
    """
    feature_columns = [
        "age",
        "married_Divorced",
        "married_Married",
        "married_Widowed",
        "married_Never Married",
        "glucose",
        "triglycerides",
    ]

    tensor = torch.tensor(df[feature_columns].values, dtype=torch.float32)
    return tensor


def student_exercise_2_run_inference(
    tensor: torch.Tensor, model_manager: ModelManager
) -> dict:
    """
    Student Exercise 2: Run Neural Network Inference

    Use the provided model manager to run inference on the input tensor.

    Args:
        tensor: Input features tensor
        model_manager: Pre-trained model manager

    Returns:
        dict: Prediction results with probabilities and classes
        { 'probabilities': np.ndarray,
          'predictions': np.ndarray
        }
    """
    # TODO: Implement inference
    # Hint: Use model_manager.predict_proba() and model_manager.predict_classes()

    probabilities = model_manager.predict_proba(tensor).squeeze()
    predictions = model_manager.predict_classes(tensor).squeeze()

    return {"probabilities": probabilities, "predictions": predictions}


class FHIRInferenceEngine:
    def __init__(self, model_path: str = "models/stroke_prediction_model.pth"):
        self.model_manager = ModelManager()
        self.model_manager.load_model()
        self.feature_columns = [
            "age",
            "married_Divorced",
            "married_Married",
            "married_Widowed",
            "married_Never Married",
            "glucose",
            "triglycerides",
        ]

    def process_fhir_data(
        self, patient_path: str, observations_path: str
    ) -> pd.DataFrame:
        patients = Patients(patient_path)
        patient_features = patients.pipeline()

        observations = Observations(observations_path, patient_path)
        observation_features = observations.pipeline()

        final_df = patient_features.merge(observation_features, on="id", how="inner")
        return final_df

    def convert_to_tensor(self, df: pd.DataFrame) -> torch.Tensor:
        missing_features = set(self.feature_columns) - set(df.columns)
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")

        return student_exercise_1_convert_to_tensor(df)

    def predict_stroke_risk(self, tensor: torch.Tensor) -> dict:
        return student_exercise_2_run_inference(tensor, self.model_manager)
