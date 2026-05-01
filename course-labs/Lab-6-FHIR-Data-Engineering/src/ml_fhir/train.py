import torch
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import MinMaxScaler
from .models import ModelManager
from .etl import Patients, Observations, Label


def train_neural_net():
    """
    Train the neural network model using processed FHIR data.
    This function will be hidden from students but used to generate the model state dict.
    """
    print("Loading and processing FHIR data...")
    
    # Load and process data
    patients = Patients("data/Patient.ndjson")
    patient_features = patients.pipeline()
    
    observations = Observations("data/Observations.ndjson", "data/Patient.ndjson")
    observation_features = observations.pipeline()
    
    labels = Label("data/Observations.ndjson", "data/Patient.ndjson")
    stroke_labels = labels.pipeline()
    
    # Merge all features
    final_df = patient_features.merge(observation_features, on='id', how='inner')
    final_df = final_df.merge(stroke_labels, on='id', how='inner')
    
    print(f"Final dataset shape: {final_df.shape}")
    print(f"Features: {list(final_df.columns)}")
    
    # Prepare features and labels
    feature_columns = ['age', 'married_Divorced', 'married_Married', 'married_Widowed', 
                      'married_Never Married', 'glucose', 'triglycerides']
    
    X = final_df[feature_columns].values
    y = final_df['stroke_ind'].values.reshape(-1, 1)
    
    # Normalize features using MinMaxScaler to ensure values are between 0 and 1
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Convert to tensors
    X_tensor = torch.FloatTensor(X_scaled)
    y_tensor = torch.FloatTensor(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_tensor, y_tensor, test_size=0.2, random_state=42, stratify=y_tensor
    )
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Initialize and train model
    model_manager = ModelManager()
    
    print("Training neural network...")
    history = model_manager.train(
        X_train, y_train, 
        X_test, y_test,
        epochs=150, 
        learning_rate=0.001
    )
    
    # Evaluate model
    print("\nEvaluating model...")
    y_pred_proba = model_manager.predict_proba(X_test)
    y_pred = model_manager.predict_classes(X_test, threshold=0.5)
    
    accuracy = accuracy_score(y_test.numpy(), y_pred)
    print(f"Test Accuracy: {accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test.numpy(), y_pred, target_names=['No Stroke', 'Stroke']))
    
    # Save model and scaler
    model_manager.save_model()
    
    # Save the scaler for inference
    import pickle
    with open('models/feature_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("\nTraining completed! Model and scaler saved for inference.")


if __name__ == "__main__":
    train_neural_net()
