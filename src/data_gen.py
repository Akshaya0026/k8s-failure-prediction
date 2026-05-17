import pandas as pd
import numpy as np

def generate_k8s_metrics(num_samples=1000):
    """
    Generates synthetic Kubernetes metrics data.
    """
    np.random.seed(42)
    
    normal_samples = int(num_samples * 0.7)
    fail_samples = num_samples - normal_samples
    
    # Normal data
    cpu_n = np.random.normal(40, 15, normal_samples)
    mem_n = np.random.normal(50, 15, normal_samples)
    disk_n = np.random.normal(20, 10, normal_samples)
    net_n = np.random.normal(15, 5, normal_samples)
    status_n = np.zeros(normal_samples)
    
    # Failure data (high resource usage)
    cpu_f = np.random.normal(90, 10, fail_samples)
    mem_f = np.random.normal(90, 10, fail_samples)
    disk_f = np.random.normal(80, 15, fail_samples)
    net_f = np.random.normal(70, 20, fail_samples)
    status_f = np.ones(fail_samples)
    
    data = {
        "timestamp": pd.date_range(start="2024-01-01", periods=num_samples, freq="h"),
        "cpu_usage": np.clip(np.concatenate([cpu_n, cpu_f]), 0, 100),
        "memory_usage": np.clip(np.concatenate([mem_n, mem_f]), 0, 100),
        "disk_io": np.clip(np.concatenate([disk_n, disk_f]), 0, 100),
        "network_io": np.clip(np.concatenate([net_n, net_f]), 0, 100),
        "pod_status": np.concatenate([status_n, status_f])
    }
    df = pd.DataFrame(data)
    
    # Shuffle dataframe
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

def preprocess_data(df):
    """
    Preprocesses the data by dropping unnecessary columns.
    """
    df = df.drop(columns=["timestamp"], errors='ignore')  # Drop timestamp for model simplicity
    return df

def generate_live_metrics(base_cpu=45, base_mem=55):
    """
    Generates a single snapshot of realistic, fluctuating metrics.
    """
    return {
        "cpu_usage": max(10, min(100, base_cpu + np.random.normal(0, 5))),
        "memory_usage": max(10, min(100, base_mem + np.random.normal(0, 5))),
        "disk_io": max(5, min(100, 30 + np.random.normal(0, 2))),
        "network_io": max(5, min(100, 20 + np.random.normal(0, 2)))
    }
