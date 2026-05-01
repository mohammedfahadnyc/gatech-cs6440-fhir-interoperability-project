import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import Tuple, Optional
import os


class StrokePredictionModel(nn.Module):
    """
    Simple neural network for stroke prediction using FHIR patient data.
    
    Features expected:
    - age (normalized)
    - marital status (one-hot encoded: 4 features)
    - glucose (normalized)
    - triglycerides (normalized)
    
    Total input features: 7
    """
    
    def __init__(self, input_size: int = 7, hidden_size: int = 16, output_size: int = 1):
        super(StrokePredictionModel, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, hidden_size // 2)
        self.layer3 = nn.Linear(hidden_size // 2, output_size)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.dropout(x)
        x = self.relu(self.layer2(x))
        x = self.dropout(x)
        x = self.sigmoid(self.layer3(x))
        return x


class ModelManager:
    """
    Manages model training, saving, loading, and inference.
    """
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        self.model = StrokePredictionModel()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Create model directory if it doesn't exist
        os.makedirs(model_dir, exist_ok=True)
    
    def train(self, X_train: torch.Tensor, y_train: torch.Tensor, 
              X_val: Optional[torch.Tensor] = None, y_val: Optional[torch.Tensor] = None,
              epochs: int = 100, learning_rate: float = 0.001) -> dict:
        """
        Train the neural network model.
        
        Args:
            X_train: Training features tensor
            y_train: Training labels tensor
            X_val: Validation features tensor (optional)
            y_val: Validation labels tensor (optional)
            epochs: Number of training epochs
            learning_rate: Learning rate for optimizer
            
        Returns:
            dict: Training history with loss values
        """
        criterion = nn.BCELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        
        train_losses = []
        val_losses = []
        
        for epoch in range(epochs):
            # Training
            self.model.train()
            optimizer.zero_grad()
            outputs = self.model(X_train)
            loss = criterion(outputs, y_train)
            loss.backward()
            optimizer.step()
            
            train_losses.append(loss.item())
            
            # Validation
            if X_val is not None and y_val is not None:
                self.model.eval()
                with torch.no_grad():
                    val_outputs = self.model(X_val)
                    val_loss = criterion(val_outputs, y_val)
                    val_losses.append(val_loss.item())
            
            if epoch % 20 == 0:
                print(f"Epoch {epoch}, Train Loss: {loss.item():.4f}", end="")
                if X_val is not None and y_val is not None:
                    print(f", Val Loss: {val_loss.item():.4f}")
                else:
                    print()
        
        return {
            'train_losses': train_losses,
            'val_losses': val_losses
        }
    
    def save_model(self, filename: str = "stroke_prediction_model.pth"):
        """Save the trained model state dict."""
        model_path = os.path.join(self.model_dir, filename)
        torch.save(self.model.state_dict(), model_path)
        print(f"Model saved to {model_path}")
    
    def load_model(self, filename: str = "stroke_prediction_model.pth"):
        """Load a trained model state dict."""
        model_path = os.path.join(self.model_dir, filename)
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()
            print(f"Model loaded from {model_path}")
        else:
            print(f"Model file not found: {model_path}")
    
    def predict(self, X: torch.Tensor) -> torch.Tensor:
        """
        Make predictions using the trained model.
        
        Args:
            X: Input features tensor
            
        Returns:
            torch.Tensor: Predicted probabilities
        """
        self.model.eval()
        with torch.no_grad():
            predictions = self.model(X)
        return predictions
    
    def predict_proba(self, X: torch.Tensor) -> np.ndarray:
        """
        Get prediction probabilities.
        
        Args:
            X: Input features tensor
            
        Returns:
            np.ndarray: Prediction probabilities
        """
        predictions = self.predict(X)
        return predictions.cpu().numpy()
    
    def predict_classes(self, X: torch.Tensor, threshold: float = 0.5) -> np.ndarray:
        """
        Get predicted classes based on threshold.
        
        Args:
            X: Input features tensor
            threshold: Classification threshold
            
        Returns:
            np.ndarray: Predicted classes (0 or 1)
        """
        probabilities = self.predict_proba(X)
        return (probabilities > threshold).astype(int) 