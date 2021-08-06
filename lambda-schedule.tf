resource "aws_lambda_permission" "allow_cloudwatch" {
  count         = var.enabled == "true" ? 1 : 0
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update-ips[0].function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.cloudflare-update-schedule[0].arn
}

resource "aws_cloudwatch_event_rule" "cloudflare-update-schedule" {
  count       = var.enabled == "true" ? 1 : 0
  name        = "cloudflare-update-schedule"
  description = "Update cloudflare ips every day"

  schedule_expression = var.schedule_expression
}


resource "aws_cloudwatch_event_target" "cloudflare-update-schedule" {
  count = var.enabled == "true" ? 1 : 0
  rule  = aws_cloudwatch_event_rule.cloudflare-update-schedule[0].name
  arn   = aws_lambda_function.update-ips[0].arn
}
