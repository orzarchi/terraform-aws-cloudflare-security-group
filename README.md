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

Variables
--------

* security_group_id: An existing security group to populate with cloudflare ips as ingress rules.
* schedule_expression: The cloudwatch schedule expression used to run the updater lambda. Defaults to every day at 20:00.
* enabled (Optional) - whether to do anything at all, useful if cloudflare is not needed on all environments. 
Accepts the string "true" or "false". Defaults to "true"
