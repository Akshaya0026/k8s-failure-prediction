import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

# Model Paths
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

# Data Paths
DATA_DIR = os.path.join(BASE_DIR, "data")

# Static Files
STATIC_DIR = os.path.join(SRC_DIR, "static")
