import joblib
import numpy as np
import os

# Load the trained model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
model = joblib.load(MODEL_PATH)

def predict_failure(cpu_usage, memory_usage, disk_io, network_io):
    input_data = np.array([[cpu_usage, memory_usage, disk_io, network_io]])
    prediction = model.predict(input_data)
    return {"failure": bool(prediction[0] == -1)}

# Example usage
if __name__ == "__main__":
    sample_input = {"cpu_usage": 80, "memory_usage": 90, "disk_io": 50, "network_io": 30}
    print(predict_failure(**sample_input))