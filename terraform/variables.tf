variable "project_id" {
  description = "The Google Cloud Project ID"
  type        = string
  default     = "swifthub-data-platform"
}

variable "region" {
  description = "GCP Region for resource deployment"
  type        = string
  default     = "asia-southeast2" # Jakarta
}

variable "environment" {
  description = "Deployment environment (e.g. dev, staging, prod)"
  type        = string
  default     = "staging"
}

variable "bucket_names" {
  description = "Names of the GCS buckets to create for the Medallion layers"
  type        = map(string)
  default = {
    bronze = "swifthub-medallion-bronze"
    silver = "swifthub-medallion-silver"
    gold   = "swifthub-medallion-gold"
  }
}

variable "github_owner" {
  description = "GitHub repository owner"
  type        = string
  default     = "adespc"
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
  default     = "super-app-data-projects"
}
