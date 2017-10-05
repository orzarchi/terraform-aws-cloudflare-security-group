resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.update-ips.function_name}"
  principal = "events.amazonaws.com"
  source_arn = "${aws_cloudwatch_event_rule.cloudflare-update-schedule.arn}"
}

resource "aws_cloudwatch_event_rule" "cloudflare-update-schedule" {
  name = "cloudflare-update-schedule"
  description = "Update cloudflare ips every day"

  schedule_expression = "${var.schedule_expression}"
}


resource "aws_cloudwatch_event_target" "cloudflare-update-schedule" {
  rule = "${aws_cloudwatch_event_rule.cloudflare-update-schedule.name}"
  arn = "${aws_lambda_function.update-ips.arn}"
}
