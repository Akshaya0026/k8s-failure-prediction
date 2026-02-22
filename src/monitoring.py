from prometheus_client import start_http_server, Gauge, Counter
import logging

# Define metrics
PREDICTION_COUNTER = Counter('k8s_failure_predictions_total', 'Total number of failure predictions made')
FAILURE_PROBABILITY = Gauge('k8s_failure_probability', 'Current estimated failure probability for a pod', ['pod_name'])
RESTART_COUNTER = Gauge('k8s_pod_restart_count', 'Current restart count of a pod', ['pod_name'])

logger = logging.getLogger(__name__)

def start_monitoring_server(port=9090):
    """
    Starts a Prometheus metrics server on the specified port.
    """
    try:
        start_http_server(port)
        logger.info(f"Prometheus monitoring server started on port {port}")
    except Exception as e:
        logger.error(f"Failed to start monitoring server: {e}")

def update_metrics(pod_name, is_failure, restart_count=0):
    """
    Updates the Prometheus metrics based on a prediction and restart count.
    """
    PREDICTION_COUNTER.inc()
    # In a real scenario, we might have a probability value from the model
    # For now, we use 1.0 for failure and 0.0 for normal
    status_value = 1.0 if is_failure else 0.0
    FAILURE_PROBABILITY.labels(pod_name=pod_name).set(status_value)
    RESTART_COUNTER.labels(pod_name=pod_name).set(restart_count)

if __name__ == "__main__":
    # Test monitoring server
    start_monitoring_server()
    while True:
        import time
        update_metrics("test-pod", True)
        time.sleep(10)
