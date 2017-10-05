data "http" "cloudflare_ipv4" {
  url = "https://www.cloudflare.com/ips-v4"
}

data "http" "cloudflare_ipv6" {
  url = "https://www.cloudflare.com/ips-v6"
}

resource "aws_security_group_rule" "cloudflare_to_https" {
  count = "${var.enabled == "true" ? 1 : 0}"
  type = "ingress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  cidr_blocks = [
    "${split("\n",trimspace(data.http.cloudflare_ipv4.body))}"]
  ipv6_cidr_blocks = [
    "${split("\n",trimspace(data.http.cloudflare_ipv6.body))}"]
  security_group_id = "${var.security_group_id}"
}
