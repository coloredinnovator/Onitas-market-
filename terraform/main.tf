# =============================================================================
# MAROON PILLAR: onitas — Terraform Configuration
# Domain: economy
# =============================================================================
# This configuration provisions pillar-specific GCP resources.
# For the full 37-pillar mesh, use maroon-terraform-live.
# =============================================================================

terraform {
  required_version = ">= 1.9.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# BigQuery Dataset for this pillar
resource "google_bigquery_dataset" "onitas" {
  dataset_id  = "maroon_pillar_onitas"
  project     = var.project_id
  location    = "US"
  description = "Sovereign dataset for pillar: onitas (economy pod)"

  labels = {
    managed-by  = "maroon-orchestrator"
    environment = var.environment
    pillar      = "onitas"
    domain      = "economy"
  }

  delete_contents_on_destroy = false
}

# Cloud Storage Bucket
resource "google_storage_bucket" "onitas" {
  name                        = "maroon-${var.environment}-economy-onitas-${var.project_id}"
  project                     = var.project_id
  location                    = var.region
  storage_class               = "STANDARD"
  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition { age = 90 }
    action { type = "SetStorageClass"; storage_class = "NEARLINE" }
  }

  lifecycle_rule {
    condition { age = 365 }
    action { type = "SetStorageClass"; storage_class = "COLDLINE" }
  }

  lifecycle_rule {
    condition { age = 730 }
    action { type = "SetStorageClass"; storage_class = "ARCHIVE" }
  }

  labels = {
    managed-by  = "maroon-orchestrator"
    environment = var.environment
    pillar      = "onitas"
    domain      = "economy"
  }

  force_destroy = false
}

# Pub/Sub Event Bus Topic
resource "google_pubsub_topic" "onitas_events" {
  name    = "maroon-${var.environment}-economy-onitas-events"
  project = var.project_id

  labels = {
    managed-by  = "maroon-orchestrator"
    environment = var.environment
    pillar      = "onitas"
    domain      = "economy"
  }

  message_retention_duration = "604800s"
}

# Service Account
resource "google_service_account" "onitas" {
  account_id   = "mrn-${var.environment}-onitas"
  display_name = "Maroon economy - onitas"
  project      = var.project_id
}

# Outputs
output "dataset_id" {
  value = google_bigquery_dataset.onitas.dataset_id
}

output "bucket_name" {
  value = google_storage_bucket.onitas.name
}

output "topic_name" {
  value = google_pubsub_topic.onitas_events.name
}

output "service_account" {
  value = google_service_account.onitas.email
}
