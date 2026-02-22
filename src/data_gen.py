import pandas as pd
import numpy as np

def generate_k8s_metrics(num_samples=1000):
    """
    Generates synthetic Kubernetes metrics data.
    """
    np.random.seed(42)
    data = {
        "timestamp": pd.date_range(start="2024-01-01", periods=num_samples, freq="h"),
        "cpu_usage": np.random.normal(50, 10, num_samples),
        "memory_usage": np.random.normal(60, 15, num_samples),
        "disk_io": np.random.normal(30, 5, num_samples),
        "network_io": np.random.normal(20, 3, num_samples)
    }
    df = pd.DataFrame(data)
    
    # Realistic failure correlation: High CPU or Memory increases risk
    # Failure condition: CPU > 80 or Memory > 85 with some randomness
    risk_score = (df["cpu_usage"] / 100) * 0.4 + (df["memory_usage"] / 100) * 0.4 + (df["disk_io"] / 100) * 0.2
    df["pod_status"] = (risk_score > 0.7).astype(int)
    
    # Add some random failures (edge cases)
    random_failures = np.random.choice([0, 1], num_samples, p=[0.98, 0.02])
    df["pod_status"] = np.maximum(df["pod_status"], random_failures)
    
    return df

def preprocess_data(df):
    """
    Preprocesses the data by dropping unnecessary columns.
    """
    df = df.drop(columns=["timestamp"], errors='ignore')  # Drop timestamp for model simplicity
    return df
