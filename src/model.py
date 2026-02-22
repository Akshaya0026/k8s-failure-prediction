import logging
import joblib
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from .config import MODEL_PATH, MODEL_DIR
from .data_gen import generate_k8s_metrics, preprocess_data

logger = logging.getLogger(__name__)

_model = None

def load_or_train_model():
    global _model
    if os.path.exists(MODEL_PATH):
        logger.info(f"Loading existing model from {MODEL_PATH}...")
        _model = joblib.load(MODEL_PATH)
    else:
        logger.info("Model not found. Training new model...")
        train_model()
    return _model

def train_model():
    global _model
    logger.info("Generating synthetic data...")
    data = generate_k8s_metrics(num_samples=2000)
    data_processed = preprocess_data(data)
    
    X = data_processed.drop(columns=["pod_status"])
    y = data_processed["pod_status"]
    
    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model Training
    logger.info("Training RandomForestClassifier model...")
    _model = RandomForestClassifier(n_estimators=100, random_state=42)
    _model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = _model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Model Accuracy: {accuracy:.2f}")
    
    # Save trained model
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(_model, MODEL_PATH)
    logger.info(f"Model trained and saved to {MODEL_PATH}")
    return _model

def get_model():
    global _model
    if _model is None:
        load_or_train_model()
    return _model

def get_root_cause(input_data):
    """
    Identifies the primary metric responsible for the failure prediction.
    Using simple feature contribution logic for the current model.
    """
    model = get_model()
    features = ["cpu_usage", "memory_usage", "disk_io", "network_io"]
    
    # Simple logic: which feature is furthest from its mean in the training set
    # In a more advanced version, we'd use SHAP values.
    # For now, let's return the most significant feature importance from the model itself
    importances = model.feature_importances_
    root_cause_index = np.argmax(importances)
    return features[root_cause_index]

def predict(cpu_usage, memory_usage, disk_io, network_io):
    model = get_model()
    input_data = [cpu_usage, memory_usage, disk_io, network_io]
    
    # Probability prediction (0: normal, 1: failure)
    probs = model.predict_proba([input_data])[0]
    failure_probability = float(probs[1])
    
    # Binary prediction based on 0.5 threshold
    is_failure = bool(failure_probability > 0.5)
    
    # Identify root cause if risk is high
    root_cause = "N/A"
    if is_failure:
        root_cause = get_root_cause(input_data)
        
    return {
        "is_failure": is_failure,
        "failure_probability": failure_probability,
        "risk_percentage": round(failure_probability * 100, 2),
        "root_cause": root_cause
    }
