from kubernetes import client, config
import logging

logger = logging.getLogger(__name__)

def get_k8s_metrics():
    """
    Fetches real-time metrics from the Kubernetes Metrics API.
    Requires 'kubernetes' python library and a configured cluster.
    """
    try:
        # Load kubeconfig (works in-cluster and locally)
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()

        api = client.CustomObjectsApi()
        
        # Querying the metrics.k8s.io API
        # This assumes the Metrics Server is installed in the cluster.
        resource = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods")
        
        pod_metrics = []
        for item in resource.get("items", []):
            pod_name = item["metadata"]["name"]
            namespace = item["metadata"]["namespace"]
            for container in item.get("containers", []):
                # Metrics are typically in nanocores (cpu) and kibibytes (memory)
                # Conversion might be needed based on model expectations
                cpu = container["usage"]["cpu"]
                memory = container["usage"]["memory"]
                
                pod_metrics.append({
                    "pod_name": pod_name,
                    "namespace": namespace,
                    "cpu_usage": cpu,
                    "memory_usage": memory
                })
        
        return pod_metrics
    except Exception as e:
        logger.error(f"Error fetching K8s metrics: {e}")
        return []

if __name__ == "__main__":
    # Test fetch (only works if connected to a cluster)
    metrics = get_k8s_metrics()
    print(metrics)
