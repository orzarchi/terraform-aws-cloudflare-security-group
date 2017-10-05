variable "security_group_id" {
  description = "An existing security group to populate with cloudflare ips as ingress rules."
}
variable "enabled" {
  description = "Whether to do anything at all, useful if cloudflare is not needed on all environments. Accepts the string 'true' or 'false'."
  default = "true"
}
variable "schedule_expression" {
  description = "The cloudwatch schedule expression used to run the updater lambda."
  default = "cron(0 20 * * ? *)"
}
