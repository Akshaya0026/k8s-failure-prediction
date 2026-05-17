# K8S-FAILURE-PREDICTION 🚀
### Industry-Level AI Auto-Healing System for Kubernetes Clusters

This project predicts Kubernetes failures based on real-time resource usage metrics using *Machine Learning (Isolation Forest/Random Forest)*. It features a premium, self-healing dashboard that not only predicts failures but also takes automated action to stabilize the cluster.

---

## ✨ Key Features & Enhancements

- **🧠 Robust AI Prediction**: Detects anomalies using an edge-case optimized Random Forest model trained on synthetic Kubernetes telemetry.
- **🛡️ Auto-Healing Logic**: Automated pod restarts and HPA scaling executed via the Kubernetes Python API based on calculated AI risk.
- **📊 Interactive Glassmorphic Dashboard**: A stunning UI featuring dynamic, color-shifting **Resource Sliders** for live metric simulations.
- **🌐 Live Cluster Architecture Map**: An interactive 2D physics-based network graph (Vis.js) that visually reacts and turns nodes red during critical failures.
- **💻 Real-Time DevOps Console**: A built-in terminal stream that types out live background logs and API commands for an authentic MLOps experience.
- **🤖 Floating AI Chatbot**: An integrated smart assistant window to query cluster health status and model functionality.
- **🌗 Multi-Theming**: Instant, smooth toggle between an enterprise Light Mode and a futuristic Dark Mode.
- **💡 Smart Recommendation Engine**: Provides human-readable root-cause advice based on resource anomalies.
- **📈 Health History Chart**: Visualizes system risk trends to spot cascading failure patterns early.
- **🚨 Prometheus & ELK Integration**: Built for comprehensive observability, external logging, and webhooks (Slack/Discord).
- **🚀 Auto-Pilot Mode**: Zero-touch background polling of Kubernetes metrics for automatic, human-free health analysis.

---

## 🖼️ Project Demo
### 🚀 Comprehensive Walkthrough
The recording below demonstrates the full system lifecycle: Manual resource monitoring, AI-driven failure prediction, and the zero-touch **Auto-Pilot Mode** in action.

![Project Demo](./screenshots/project_demo.webp)

---

## 📂 Project Structure
```text
k8s-failure-prediction/
├── 📁 src/                # Source code (FastAPI, ML model, Logic)
│   ├── api.py            # REST API with History & Recommendations
│   ├── auto_healing.py   # Self-Healing & Scaling Logic
│   ├── recommendations.py # AI Advice Generation
│   └── 📁 static/        # Glassmorphic Dashboard (HTML/JS)
├── 📁 models/             # Trained model (model.pkl)
├── 📁 data/               # Training Datasets
├── 📁 k8s/                # Kubernetes Deployment Manifests
├── requirements.txt      # Dependencies
├── DEPLOYMENT.md         # Detailed Deployment Guide
└── README.md             # Project Overview
```

---

## 🛠️ Installation & Setup

> [!TIP]
> For detailed deployment options (Docker, Kubernetes, Cloud), please refer to the **[Deployment Guide](./DEPLOYMENT.md)**.

### Step 1: Clone the Repository
```bash
git clone https://github.com/Akshaya0026/k8s-failure-prediction.git
cd k8s-failure-prediction
```

### Step 2: Set Up Environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### Step 3: Run the System
```bash
uvicorn src.api:app --reload --port 8000
```

---

 Safe Operation (Healthy) ![Safe State](./screenshots/risk_safe.png)  Warning: Scaling Triggered ![Warning State](./screenshots/risk_warning.png)  Critical: Auto-Healing![Critical State](./screenshots/risk_critical.png) 
 Health Trend Tracking 
![Health Trend](./screenshots/health_trend_chart.png) 

---

## 🧪 Testing the API
1. Open: `http://127.0.0.1:8000` to access the Dashboard.
2. API Documentation: `http://127.0.0.1:8000/docs`
3. Try the `/predict/` endpoint with high resource values to trigger auto-healing!


