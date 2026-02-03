variable "project_id" {
  description = "L'ID du projet GCP"
  type        = string
}

variable "region" {
  description = "La région GCP (ex: europe-west1)"
  default     = "europe-west1"
}

variable "zone" {
  description = "La zone de disponibilité (ex: europe-west1-b)"
  default     = "europe-west1-b"
}

variable "image_name" {
  description = "Le nom EXACT de l'image créée par Packer"
  type        = string
}
