variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "humansafe"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}
