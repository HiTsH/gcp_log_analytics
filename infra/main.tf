variable "gcp_credentials" {
  description = "GCP Service Account JSON"
  default     = jsondecode(file("${path.module}/../.env"))["GCP_SERVICE_ACCOUNT_JSON"]
}

provider "google" {
  credentials = var.gcp_credentials
  project     = var.project_id
  region      = var.region
}

resource "google_storage_bucket" "data_lake" {
  name          = "${var.project_id}-${var.bucket_name}"
  location      = var.region
  force_destroy = true
}

resource "google_bigquery_dataset" "logs" {
  dataset_id = "server_logs"
  location   = var.region
}

resource "google_pubsub_topic" "alerts" {
  name = "dataflow-alerts"
}

resource "google_dataflow_job" "log_pipeline" {
  name              = "1tb-log-pipeline"
  template_gcs_path = "gs://dataflow-templates/latest/Beam_Python"
  temp_gcs_location = "${google_storage_bucket.data_lake.url}/temp"
  parameters = {
    input  = "${google_storage_bucket.data_lake.url}/logs/raw/*.csv"
    output = "${google_bigquery_dataset.logs.dataset_id}.user_metrics"
  }
  machine_type = "n1-standard-4"
  max_workers  = 10
}
