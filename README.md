# K8S-FAILURE-PREDICTION 🚀
### Industry-Level AI Auto-Healing System for Kubernetes Clusters

This project predicts Kubernetes failures based on real-time resource usage metrics using *Machine Learning (Isolation Forest/Random Forest)*. It features a premium, self-healing dashboard that not only predicts failures but also takes automated action to stabilize the cluster.

---

## ✨ Key Features

- **🧠 AI-Powered Prediction**: Detects anomalies and predicts potential pod failures with high accuracy.
- **🛡️ Auto-Healing Logic**: Automated pod restarts and HPA scaling triggered by AI risk assessment.
- **📊 Real-time Dashboard**: A premium, glassmorphic UI for monitoring cluster health and risk trends.
- **💡 Smart Recommendation Engine**: Provides human-readable advice based on resource usage patterns (CPU load, memory pressure, etc.).
- **📈 Health History Chart**: Visualizes system risk trends to spot cascading failure patterns early.
- **🚨 Prometheus Integration**: Exports metrics for comprehensive observability and alerting.
- **🤖 Auto-Pilot Mode**: Zero-touch background monitoring and automatic health analysis.

---

## 📂 Project Structure
```text
k8s-failure-prediction/
├── 📁 src/                # Source code (FastAPI, ML model, Logic)
│   ├── api.py            # REST API with History & Recommendations
│   ├── auto_healing.py   # Self-Healing & Scaling Logic
│   ├── recommendations.py # AI Advice Generation
│   ├── model.py          # ML Model training & prediction
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
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Step 3: Run the System
```bash
# Set up a local development server
uvicorn src.api:app --reload --port 8000
```

---

## 🖥️ Enhanced AI Dashboard

The new dashboard provides a unified view of cluster health:
1. **Auto-Pilot Mode**: Background monitoring with live UI updates.
2. **Resource Monitor**: Real-time visualization of system parameters.
3. **Risk Gauge**: AI-driven risk assessment (Safe, Warning, Critical).
4. **Health Trend**: Historical tracking of risk levels via live charts.
5. **AI ADVICE**: Contextual recommendations for cluster optimization.

---

## 🖼️ Screenshots & Demo

### Video Walkthrough
Experience the full auto-healing flow from failure detection to stabilization.

![Dashboard Demo](./screenshots/ui_transformation.webp)

### 🤖 Auto-Pilot Demo
See the system autonomously fetching metrics and running predictions in the background.

![Auto-Pilot Demo](./screenshots/auto_pilot_demo.webp)

### UI Gallery
| Initial State (Healthy) | Analysis & Recommendation | Auto-Healing Active |
| :---: | :---: | :---: |
| ![Healthy Dashboard](./screenshots/initial_dashboard_1771754027052.png) | ![Analysis Results](./screenshots/final_dashboard_analysis_1771754082170.png) | ![Critical State](./screenshots/critical_healing.png) |

---

## 🧪 Testing the API
1. Open: `http://127.0.0.1:8000` to access the Dashboard.
2. API Documentation: `http://127.0.0.1:8000/docs`
3. Try the `/predict/` endpoint with high resource values to trigger auto-healing!
