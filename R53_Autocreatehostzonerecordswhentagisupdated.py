import json
import boto3
import os,sys
import socket

ec2 = boto3.client('ec2','us-east-1')
route53 = boto3.client('route53','us-east-1')


def ec2values(ec2,route53, ec2resource):
    response = ec2.describe_instances(InstanceIds=[ec2resource])
    if response ['Reservations']:
        instance = response['Reservations'][0]['Instances'][0]
        private_ip = instance.get('PrivateIpAddress')
        key_name = instance.get('KeyName')
        #print (private_ip)
        for x in instance['Tags']:
            if x['Key'] == 'Name':
                getresourceName = (x['Value'])
                #print (getresourceName)
                r53(route53,private_ip,getresourceName)

def r53(route53, private_ip, getresourceName):
    print ("Phase3 - Query Route53 if a Record already exist")
    hosted_zone_id = 'Z1000989IKE3CAYQBYLF'
    records = []
    paginator = route53.get_paginator('list_resource_record_sets')
    
    for page in paginator.paginate(HostedZoneId=hosted_zone_id):
        records.extend(page['ResourceRecordSets'])
    
    #print ("#" * 40)
    if private_ip in records or getresourceName in records:  #To add another OR if private_ip in records for the REVERSE LOOKUP!!!####
        print ("Either Node Name or Private IP already has a record within Route53! ")
        print ("Exiting...")
    else:
        print ("We can proceed in making your record in Route53 ")
        hosted_zone_id = 'Z1000989IKE3CAYQBYLF'
        domain_name = 'dgoptam.com'
        #record_name = (f" {getresourceName}.dgoptam.com")
        rname1 = (getresourceName)
        rname2 = ('.dgoptam.com')
        record_name = (rname1) + (rname2)
        #record_name = getresourceName
        record_type = 'A'
        record_value = private_ip
        ttl = 300
        print ("Phase4 - Create records in Route53")
        create_route53_record(route53, domain_name, record_name, record_type, record_value, ttl, hosted_zone_id)
        #print(route53response)
     

def create_route53_record(route53, domain_name, record_name, record_type, record_value, ttl, hosted_zone_id):
    r53response = route53.change_resource_record_sets(
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': (record_name),
                        'TTL': ttl,
                        'Type': 'A',
                        'ResourceRecords': [
                            {
                                'Value': (record_value),
                            },
                        ],
                    },
                },
            ],
            'Comment': 'Web Server',
        },
        HostedZoneId=hosted_zone_id,
    )
    print (r53response)
    
    
    ipaddresstoarpa = (record_value.split('.'))
    first2octects = ('.30.172.in-addr.arpa')
    firstoctect = (ipaddresstoarpa[3])
    secondoctect = (ipaddresstoarpa[2])
    reverseip = (firstoctect) + '.' + (secondoctect) + (first2octects)
    print (reverseip)


    print ("Phase5 - Creating reverse lookup PTR**")
    r53reverseresponse = route53.change_resource_record_sets(
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': (reverseip),
                        'TTL': ttl,
                        'Type': 'PTR',
                        'ResourceRecords': [
                            {
                                'Value': record_name,
                            },
                        ],
                    },
                },
            ],
            'Comment': 'reverse DNS Lookup',
        },
        HostedZoneId='Z01652272N1PH3TI2QGS4',
    )
    print (r53reverseresponse)



def lambda_handler(event, context):
    #print ("start")
    #print (event)
    print ("Phase1 - Validate response from eventbridge rule and extract resource ID")
    ctrail = event['detail']
    #print (ctrail.get('eventName'))
    for xx in ctrail['requestParameters']['resourcesSet']['items']:
        ec2resource = (xx['resourceId'])
        #print (ec2resource)
    print ("Phase2 - Query EC2 to get private IP as well as Ec2 TagName ")
    getec2ip = ec2values(ec2,route53,ec2resource)
    

    
            
