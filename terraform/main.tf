terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.0"
    }
  }
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = var.kube_context
}

resource "kubernetes_namespace" "k8s_predictor_namespace" {
  metadata {
    name = var.namespace
  }
}

# Example deployment for the k8s-failure-prediction application
resource "kubernetes_deployment" "k8s_predictor" {
  metadata {
    name      = "k8s-predictor"
    namespace = kubernetes_namespace.k8s_predictor_namespace.metadata[0].name
    labels = {
      app = "k8s-predictor"
    }
  }

  spec {
    replicas = var.replica_count

    selector {
      match_labels = {
        app = "k8s-predictor"
      }
    }

    template {
      metadata {
        labels = {
          app = "k8s-predictor"
        }
      }

      spec {
        container {
          image = var.app_image
          name  = "k8s-predictor"

          port {
            container_port = 8000
          }

          resources {
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "k8s_predictor_service" {
  metadata {
    name      = "k8s-predictor-service"
    namespace = kubernetes_namespace.k8s_predictor_namespace.metadata[0].name
  }
  spec {
    selector = {
      app = kubernetes_deployment.k8s_predictor.metadata[0].labels.app
    }
    session_affinity = "ClientIP"
    port {
      port        = 80
      target_port = 8000
    }
    type = "LoadBalancer"
  }
}
