# Deployment Guide 🚀

The **Predictive Auto-Healing System (PAHS)** can be deployed in multiple ways depending on your environment.

---

## 1. Local Deployment (Python)
Best for development and testing.

```bash
# Set up environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the app
python src/main.py
```

---

## 2. Docker Deployment 🐳
Best for consistent environments and microservices.

### Build and Run
```bash
docker build -t k8s-predictor .
docker run -p 8000:8000 k8s-predictor
```

### Using Docker Compose
```bash
docker-compose up --build
```

---

## 3. Kubernetes Deployment (Production) ☸️
Best for industry-level scalability.

### Step 1: Push Image to Registry
```bash
docker tag k8s-predictor:latest your-username/k8s-predictor:latest
docker push your-username/k8s-predictor:latest
```

### Step 2: Apply Manifests
```bash
kubectl apply -f k8s/deployment.yaml
```

---

## 4. Cloud Deployment (Render / Railway) ☁️
Best for quick staging and live demos.

### Render
1. Connect your GitHub repository.
2. Select **Web Service**.
3. Set Build Command: `pip install -r requirements.txt`
4. Set Start Command: `uvicorn src.api:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variable: `PYTHON_VERSION=3.11`

### Railway
1. Link your GitHub repo.
2. Railway will automatically detect the `Dockerfile` and deploy the service.
3. Ensure the port is mapped to `8000`.
