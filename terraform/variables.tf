variable "kube_context" {
  description = "The kubeconfig context to use"
  type        = string
  default     = "docker-desktop"
}

variable "namespace" {
  description = "The namespace to deploy into"
  type        = string
  default     = "k8s-failure-prediction-ns"
}

variable "replica_count" {
  description = "Number of replicas for the predictor service"
  type        = number
  default     = 2
}

variable "app_image" {
  description = "The Docker image for the application"
  type        = string
  default     = "k8s-failure-prediction:latest"
}
