def get_recommendation(risk, root_cause, cpu, memory, disk, network):
    """
    Generates a smart recommendation string based on predictive risk and metrics.
    """
    if risk < 30:
        return "System is operating within optimal parameters. No action required."
    
    recommendations = []
    
    if root_cause == 'cpu_usage' or cpu > 80:
        recommendations.append("High CPU load detected. Consider scaling vertically or checking for inefficient process loops.")
    
    if root_cause == 'memory_usage' or memory > 85:
        recommendations.append("Memory pressure is high. Monitor for potential OOM kills and consider increasing memory limits.")
    
    if root_cause == 'disk_io' or disk > 70:
        recommendations.append("Disk I/O bottleneck identified. Verify storage performance or reduce log-heavy operations.")
    
    if root_cause == 'network_io' or network > 70:
        recommendations.append("Significant network traffic spike. Inspect ingress/egress patterns for unusual activity.")

    if risk >= 40:
        recommendations.append("AI Auto-healing has triggered a pod restart to mitigate potential cascading failure.")
    elif risk >= 30:
        recommendations.append("Predictive HPA is scaling resources to maintain cluster stability.")

    return " | ".join(recommendations) if recommendations else "Risk level elevated. Continue monitoring system health."
