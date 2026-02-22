import os
import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from .model import predict, load_or_train_model
from .config import STATIC_DIR
from .monitoring import start_monitoring_server, update_metrics
from .alerts import trigger_alerts
from .auto_healing import handle_auto_healing, get_pod_restart_count
from .recommendations import get_recommendation

# Historical data storage
prediction_history = []
MAX_HISTORY = 10

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Industry-Level K8s AI Auto-Healing System")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Pydantic model for request validation
class PredictionRequest(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_io: float
    network_io: float

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Industry-Level K8s AI Auto-Healing API...")
    load_or_train_model()
    # Start Prometheus monitoring server on port 9090
    start_monitoring_server(port=9090)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    logger.info("Serving root page")
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            return f.read()
    return "<h1>K8s Failure Prediction Dashboard</h1><p>Static index.html not found. API is running at /predict/</p>"

@app.post("/predict/")
async def predict_failure(request: PredictionRequest):
    logger.info(f"Received prediction request: {request}")
    
    # Pod name for identification (mocked for now)
    pod_name = "production-app-v1"
    
    # 0. Get current restart count
    initial_restarts = get_pod_restart_count(pod_name)
    
    # 1. Get AI Prediction with probability and root cause
    prediction_result = predict(
        request.cpu_usage, 
        request.memory_usage, 
        request.disk_io, 
        request.network_io
    )
    
    # 2. Trigger External Alerts
    trigger_alerts(pod_name, prediction_result)
    
    # 3. Trigger Auto-Healing (Scaling/Restarting)
    handle_auto_healing(pod_name, prediction_result)
    
    # 4. Final verification: check for restart
    import time
    if prediction_result.get("risk_percentage", 0) >= 40:
        # Give K8s a bit of time to reflect the restart in dry-run/mock
        time.sleep(1) 

    final_restarts = get_pod_restart_count(pod_name)
    prediction_result["restart_count"] = final_restarts
    prediction_result["healing_verified"] = final_restarts > initial_restarts
    
    # 5. Get Smart Recommendation
    recommendation = get_recommendation(
        prediction_result.get("risk_percentage", 0),
        prediction_result.get("root_cause", "N/A"),
        request.cpu_usage,
        request.memory_usage,
        request.disk_io,
        request.network_io
    )
    prediction_result["recommendation"] = recommendation

    # 6. Update Prometheus Metrics
    update_metrics(pod_name, prediction_result["is_failure"], final_restarts)

    # 7. Store in history
    history_entry = {
        "timestamp": time.strftime("%H:%M:%S"),
        "risk": prediction_result.get("risk_percentage", 0),
        "cpu": request.cpu_usage,
        "memory": request.memory_usage,
        "disk": request.disk_io,
        "network": request.network_io
    }
    prediction_history.append(history_entry)
    if len(prediction_history) > MAX_HISTORY:
        prediction_history.pop(0)
    
    logger.info(f"Full Prediction Report: {prediction_result}")
    return prediction_result

@app.get("/history/")
async def get_history():
    return prediction_history
