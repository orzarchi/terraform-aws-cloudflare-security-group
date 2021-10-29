AWS CloudFlare security group Terraform module
==============================================

Terraform module that populates a security group with cloudflare ip ranges and keeps it updated daily.

The following resources are created:

* A lambda function that keeps your security group's ingress rules updated with published cloudflare ip ranges.
* A cloudwatch event rule with a schedule to trigger the lambda daily

Usage
-----

```hcl
module "cloudflare-ips" {
  source = "github.com/orzarchi/terraform-aws-cloudflare-security-group"

  security_group_id = "${aws_security_group.cloudflare.id}"
  enabled= "${var.use_cloudflare}"
}
```
<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | n/a |
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_event_rule.cloudflare-update-schedule](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.cloudflare-update-schedule](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_log_group.lambda-log-group](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_iam_policy.policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.iam_for_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_function.update-ips](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_permission.allow_cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [aws_security_group_rule.egress_http](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group_rule) | resource |
| [aws_security_group_rule.egress_https](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group_rule) | resource |
| [archive_file.lambda_zip](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_enabled"></a> [enabled](#input\_enabled) | Whether to do anything at all, useful if cloudflare is not needed on all environments. Accepts the string 'true' or 'false'. | `string` | `"true"` | no |
| <a name="input_schedule_expression"></a> [schedule\_expression](#input\_schedule\_expression) | The cloudwatch schedule expression used to run the updater lambda. | `string` | `"cron(0 20 * * ? *)"` | no |
| <a name="input_security_group_id"></a> [security\_group\_id](#input\_security\_group\_id) | An existing security group to populate with cloudflare ips as ingress rules. | `any` | n/a | yes |

## Outputs

No outputs.
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
Variables
--------

* security_group_id: An existing security group to populate with cloudflare ips as ingress rules.
* schedule_expression: The cloudwatch schedule expression used to run the updater lambda. Defaults to every day at 20:00.
* enabled (Optional) - whether to do anything at all, useful if cloudflare is not needed on all environments. 
Accepts the string "true" or "false". Defaults to "true"
