from kubernetes import client, config
import logging
import os

logger = logging.getLogger(__name__)

def load_k8s_config():
    """Reads K8s configuration (in-cluster or local)."""
    try:
        config.load_incluster_config()
    except config.ConfigException:
        try:
            config.load_kube_config()
        except config.ConfigException:
            logger.warning("No Kubernetes config found. Auto-healing will run in dry-mode.")
            return False
    return True

def scale_deployment(deployment_name, namespace, replicas):
    """
    Scales a deployment as part of the predictive HPA strategy.
    """
    if not load_k8s_config():
        logger.info(f"[Dry-Run] Scaling deployment {deployment_name} to {replicas} replicas.")
        return

    try:
        apps_v1 = client.AppsV1Api()
        body = {"spec": {"replicas": replicas}}
        apps_v1.patch_namespaced_deployment_scale(deployment_name, namespace, body)
        logger.info(f"Successfully scaled deployment {deployment_name} to {replicas} replicas.")
    except Exception as e:
        logger.error(f"Error scaling deployment: {e}")

def get_pod_restart_count(pod_name, namespace="default"):
    """
    Fetches the current restart count of a pod from the Kubernetes API.
    """
    if not load_k8s_config():
        # Mock logic for dry-run
        import random
        return random.randint(0, 5)

    try:
        core_v1 = client.CoreV1Api()
        pod = core_v1.read_namespaced_pod(pod_name, namespace)
        # Assuming the first container is the one we care about
        if pod.status.container_statuses:
            return pod.status.container_statuses[0].restart_count
        return 0
    except Exception as e:
        logger.error(f"Error fetching restart count for {pod_name}: {e}")
        return 0

def restart_pod(pod_name, namespace):
    """
    Deletes a pod to trigger a restart (Self-Healing).
    """
    if not load_k8s_config():
        logger.info(f"[Dry-Run] Restarting pod {pod_name} in namespace {namespace}.")
        return

    try:
        core_v1 = client.CoreV1Api()
        core_v1.delete_namespaced_pod(pod_name, namespace)
        logger.info(f"Successfully triggered restart for pod {pod_name}.")
    except Exception as e:
        logger.error(f"Error restarting pod: {e}")

def handle_auto_healing(pod_name, prediction_result):
    """
    Decides and triggers auto-healing actions based on AI risk assessment.
    """
    risk = prediction_result.get("risk_percentage", 0)
    namespace = "default" # Fallback
    
    # Example logic:
    # 30% < Risk < 40% -> Scale up to handle load (HPA)
    # Risk >= 40% -> Replace pod (Self-Healing)
    
    if risk >= 40:
        logger.warning(f"CRITICAL RISK ({risk}%). Triggering Self-Healing for {pod_name}.")
        restart_pod(pod_name, namespace)
    elif risk >= 30:
        logger.info(f"HIGH RISK ({risk}%). Triggering HPA scaling for {pod_name}.")
        # In a real scenario, we'd map pod_name to its deployment
        deployment_name = pod_name.split("-")[0] # Mock mapping
        scale_deployment(deployment_name, namespace, replicas=5)
