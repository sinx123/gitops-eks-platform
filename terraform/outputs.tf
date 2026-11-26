output "cluster_name" {
  value = module.eks.cluster_name
}

output "kubeconfig_command" {
  value = "aws eks update-kubeconfig --region ${var.region} --name ${module.eks.cluster_name}"
}

output "ecr_registry" {
  value = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com"
}

output "github_actions_role_arn" {
  description = "Add this as the AWS_ROLE_ARN secret in GitHub"
  value       = aws_iam_role.github_ci.arn
}

output "grafana_admin_password" {
  value     = random_password.grafana.result
  sensitive = true
}
