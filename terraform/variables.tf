variable "region" {
  type    = string
  default = "us-east-1"
}

variable "cluster_name" {
  type    = string
  default = "gitops-demo"
}

variable "kubernetes_version" {
  type    = string
  default = "1.30"
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "node_instance_types" {
  type    = list(string)
  default = ["t3.medium"]
}

variable "node_capacity_type" {
  type        = string
  default     = "SPOT"
  description = "SPOT is cheaper for demos; use ON_DEMAND for stability"
}

variable "services" {
  type        = list(string)
  default     = ["catalog", "orders"]
  description = "One ECR repository is created per service"
}

variable "github_org" {
  type        = string
  description = "GitHub username or organisation that owns the repo"
}

variable "github_repo" {
  type    = string
  default = "gitops-eks-platform"
}

variable "create_github_oidc_provider" {
  type        = bool
  default     = true
  description = "Set false if the GitHub OIDC provider already exists in this AWS account"
}
