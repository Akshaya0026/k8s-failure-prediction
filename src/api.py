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
from .data_gen import generate_live_metrics
from .k8s_client import get_k8s_metrics
import asyncio
import time

# Historical data storage
prediction_history = []
MAX_HISTORY = 10
latest_autopilot_result = {"status": "initializing"}

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
    # Start the Auto-Pilot background loop
    asyncio.create_task(autopilot_loop())

async def autopilot_loop():
    """Background loop to fetch metrics and run predictions automatically."""
    logger.info("Auto-Pilot background loop started.")
    while True:
        try:
            # 1. Try to get real K8s metrics
            metrics_list = get_k8s_metrics()
            
            if metrics_list:
                # For now, just take the first pod's metrics
                m = metrics_list[0]
                cpu, mem = float(m['cpu_usage'].replace('n','').replace('u','')), float(m['memory_usage'].replace('Ki',''))
                # Simplified conversion for the model
                cpu = min(100, cpu / 1000000) 
                mem = min(100, mem / 1024 / 10)
                disk, net = 25.0, 15.0 # Mocked for now
            else:
                # Fallback to simulated metrics
                m = generate_live_metrics()
                cpu, mem, disk, net = m['cpu_usage'], m['memory_usage'], m['disk_io'], m['network_io']

            # 2. Run prediction
            pod_name = "production-app-v1"
            res = predict(cpu, mem, disk, net)
            
            # 3. Add recommendation
            res["recommendation"] = get_recommendation(
                res.get("risk_percentage", 0),
                res.get("root_cause", "N/A"),
                cpu, mem, disk, net
            )
            
            # 4. Update global status and history
            global latest_autopilot_result
            latest_autopilot_result = {
                "timestamp": time.strftime("%H:%M:%S"),
                "metrics": {"cpu": cpu, "memory": mem, "disk": disk, "network": net},
                "prediction": res
            }

            # Update history for the chart
            history_entry = {
                "timestamp": latest_autopilot_result["timestamp"],
                "risk": res.get("risk_percentage", 0),
                "cpu": cpu, "memory": mem, "disk": disk, "network": net
            }
            prediction_history.append(history_entry)
            if len(prediction_history) > MAX_HISTORY:
                prediction_history.pop(0)

            # 5. Handle Auto-Healing if critical
            handle_auto_healing(pod_name, res)
            update_metrics(pod_name, res["is_failure"], get_pod_restart_count(pod_name))

        except Exception as e:
            logger.error(f"Error in autopilot loop: {e}")
        
        await asyncio.sleep(5) # Run every 5 seconds for responsive demo

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

@app.get("/autopilot/status")
async def get_autopilot_status():
    return latest_autopilot_result
