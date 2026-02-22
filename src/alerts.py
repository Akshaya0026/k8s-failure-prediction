import requests
import logging
import os

logger = logging.getLogger(__name__)

# Replace with your actual Slack Webhook URL
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

def send_slack_alert(pod_name, risk_percentage, root_cause):
    """
    Sends an alert message to a Slack channel via a webhook.
    """
    if not SLACK_WEBHOOK_URL:
        logger.warning("SLACK_WEBHOOK_URL not set. Skipping Slack alert.")
        return

    message = {
        "text": f"🚨 *K8s Failure Prediction Alert* 🚨",
        "attachments": [
            {
                "color": "#ff0000",
                "fields": [
                    {"title": "Pod Name", "value": pod_name, "short": True},
                    {"title": "Failure Risk", "value": f"{risk_percentage}%", "short": True},
                    {"title": "Potential Root Cause", "value": root_cause, "short": False}
                ],
                "footer": "AI Auto-Healing System"
            }
        ]
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        if response.status_code == 200:
            logger.info("Slack alert sent successfully.")
        else:
            logger.error(f"Failed to send Slack alert: {response.text}")
    except Exception as e:
        logger.error(f"Error sending Slack alert: {e}")

def trigger_alerts(pod_name, prediction_result):
    """
    Triggers configured alerts if the failure risk exceeds the threshold.
    """
    risk = prediction_result.get("risk_percentage", 0)
    
    # Alert threshold (e.g., 30% risk for demo)
    if risk >= 30:
        logger.info(f"Triggering alerts for {pod_name} (Risk: {risk}%)")
        send_slack_alert(
            pod_name, 
            risk, 
            prediction_result.get("root_cause", "Unknown")
        )
