import os
import boto3
import ipaddress
import urllib3
import json
from botocore.vendored import requests
from datetime import datetime

def get_cloudflare_ip_list():
    """Call the CloudFlare API and return a list of IPs"""
    http = urllib3.PoolManager()
    response = http.request("GET","https://api.cloudflare.com/client/v4/ips")
    temp = json.loads(response.data.decode("utf-8"))
    ip_addresses_list = []
    if 'result' in temp:
        if 'ipv4_cidrs' in temp['result']:
            for ip in temp['result']['ipv4_cidrs']:
                ip_addresses_list.append(ip)
        if 'ipv6_cidrs' in temp['result']:
            for ip in temp['result']['ipv6_cidrs']:
                ip_addresses_list.append(ip)
    return ip_addresses_list

def get_aws_security_group(group_id):
    """Return the defined Security Group"""
    ec2 = boto3.resource('ec2')
    group = ec2.SecurityGroup(group_id)
    if group.group_id == group_id:
        return group
    raise Exception('Failed to retrieve Security Group')

def check_rule_exists(rules, address, port):
    """Check if the rule currently exists"""
    rule_exists = False
    for rule in rules:
        for ip_range in rule['IpRanges']:
            if ip_range['CidrIp'] == address and rule['FromPort'] == port:
                rule_exists = True
        for ip_range in rule['Ipv6Ranges']:
            if ip_range['CidrIpv6'] == address and rule['FromPort'] == port:
                rule_exists = True
    return rule_exists

def get_existing_ip_addresses(rules):
    ip_addresses = []
    for rule in rules:
        for ip_range in rule['IpRanges']:
            ip_addresses.append(ip_range['CidrIp'])
        for ip_range in rule['Ipv6Ranges']:
            ip_addresses.append(ip_range['CidrIpv6'])
    return set(ip_addresses)

def add_rule(group, address, port):
    """Add the ip address/port to the security group"""
    ip = ipaddress.ip_network(address)
    if isinstance(ip, ipaddress.IPv4Network):
        group.authorize_ingress(IpProtocol="tcp", CidrIp=address, FromPort=port, ToPort=port)
    elif isinstance(ip, ipaddress.IPv6Network):
        permission = [
            {  
            'IpProtocol': 'TCP',
            'FromPort': port,
            'ToPort': port,
            'Ipv6Ranges': [{'CidrIpv6': address}]
            }
        ]
        group.authorize_ingress(IpPermissions=permission)

    print("Added %s : %i  " % (address, port))

def remove_rule(group, address, port):
    """Remove the ip address/port from the security group"""
    ip = ipaddress.ip_network(address)
    if isinstance(ip, ipaddress.IPv4Network):
        group.revoke_ingress(IpProtocol="tcp", CidrIp=address, FromPort=port, ToPort=port)
    elif isinstance(ip, ipaddress.IPv6Network):
        permission = [
            {  
            'IpProtocol': 'TCP',
            'FromPort': port,
            'ToPort': port,
            'Ipv6Ranges': [{'CidrIpv6': address}]
            }
        ]
        group.revoke_ingress(IpPermissions=permission)
    
    print("Removed %s : %i  " % (address, port))


def lambda_handler(event, context):
    """aws lambda main func"""
    ports = [int(x) for x in os.environ.get('PORTS_LIST', '').split(",") if x]
    if not ports:
        ports = [80,443]

    security_group = get_aws_security_group(os.environ['SECURITY_GROUP_ID'])
    current_rules = security_group.ip_permissions
    ip_addresses = get_cloudflare_ip_list()

    ## Add IPs
    for ip_address in ip_addresses:
        for port in ports:
            if not check_rule_exists(current_rules, ip_address, port):
                add_rule(security_group, ip_address, port)

    ## Remove IPs from SG that are not in list
    for ip_address in get_existing_ip_addresses(current_rules):
        if (ip_address not in ip_addresses):
            for port in ports:
                remove_rule(security_group, ip_address, port)