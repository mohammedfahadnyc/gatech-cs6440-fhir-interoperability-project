import pandas as pd
import torch
import numpy as np


class DataFrameFromJSONMixin:
    def __init__(self, path):
        self.path = path
        self.data = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        return pd.read_json(self.path, lines = True)
    
    def to_tensor(self, df: pd.DataFrame, feature_columns: list) -> torch.Tensor:
        """
        Convert DataFrame features to PyTorch tensor for neural network inference.
        
        Args:
            df: DataFrame with features
            feature_columns: List of column names to include as features
            
        Returns:
            torch.Tensor: Tensor ready for neural network input
        """
        features = df[feature_columns].values
        return torch.FloatTensor(features)
