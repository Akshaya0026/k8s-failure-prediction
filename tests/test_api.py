import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_predict_endpoint_success():
    payload = {
        "cpu_usage": 50.0,
        "memory_usage": 60.0,
        "disk_io": 30.0,
        "network_io": 20.0
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_percentage" in data
    assert "is_failure" in data
    assert "recommendation" in data

def test_predict_endpoint_high_risk():
    payload = {
        "cpu_usage": 95.0,
        "memory_usage": 90.0,
        "disk_io": 80.0,
        "network_io": 70.0
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_percentage" in data
    assert "is_failure" in data
    assert isinstance(data["is_failure"], bool)

def test_health_history_endpoint():
    response = client.get("/history/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
