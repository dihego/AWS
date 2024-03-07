#bin/python3
import os,sys
import boto3
import botocore
import time
from tqdm import tqdm

os.system('clear')
os.system('date')
print ('''#############################################################################################
Tagging resources [EC2 Fleet, EBS Volumes, Security Groups and ENIs] to VPC-ID or value of your choice.
Get detail billing with TAG association in Cost Explorer.
#######################################################################################################
#######################################################################################################''')


def get_arguments():
    ...

def get_ids(pass_ec2):
    print
    list_ec2ids = []
    list_volumeids = []
    list_eniIds = []
    list_sgIds = []
    list_vpcIds = []





    listvpcids = pass_ec2.descibe_vpcs():
    for vpcattributes in listvpcids['Vpcs']:
        getvpcids = (vpcattributes['vpc-id'])
        print (getvpcids)
        listvpcids.append(getvpcids)
    
    print (len(list_vpcIds))
    for x in list_vpcIds:
        print (x)



'''
    instancesbyvpc = pass_ec2.describe_instances(Filters=[{'Name': 'vpc-id','Values': [pass_vpcid]}])
    for ec2attributes in instancesbyvpc['Reservations']:
        for i in ec2attributes['Instances']:
            getec2id = (i['InstanceId'])
            list_ec2ids.append(getec2id)
            for x in i['BlockDeviceMappings']:
                getvolumeid = (x['Ebs']['VolumeId'])
                list_volumeids.append(getvolumeid)
    
    enisbyvpc = pass_ec2.describe_network_interfaces(Filters=[{'Name': 'vpc-id','Values': [pass_vpcid]}])
    for eniattributes  in enisbyvpc['NetworkInterfaces']:
        geteniId = (eniattributes['NetworkInterfaceId'])
        list_eniIds.append(geteniId)

    sgbyvpc = pass_ec2.describe_security_groups(Filters=[{'Name': 'vpc-id','Values': [pass_vpcid]}])
    for sgattributes  in sgbyvpc['SecurityGroups']:
         getsgId = (sgattributes['GroupId'])
         list_sgIds.append(getsgId)


    add_tags(pass_ec2, list_ec2ids,list_volumeids,list_eniIds,list_sgIds)

def add_tags(ec2, ec2_list, volumeid_list, eni_list, sg_list):
    # ...
    print (f"Updating EC2 Fleet. A total of {(len(ec2_list))} resources!")
    testlenth = (len(ec2_list))
    for a in ec2_list:
        try:
            modifyec2 = ec2.create_tags(DryRun=True, Resources=[a],Tags=[{'Key':'BillingTag','Value':'vpc-0832a05760d4b5726'}])
        except botocore.exceptions.ClientError as error:
            print (error)
    

    print ()
    print (f"Updating EBS Volumes. A total of {(len(volumeid_list))} resources!")
    for b in volumeid_list:
        try:
            modifyebs = ec2.create_tags(DryRun=True, Resources=[b],Tags=[{'Key':'BillingTag','Value':'vpc-0832a05760d4b5726'}])
        except botocore.exceptions.ClientError as error:
            print (error)
    print ()
    print (f"Updating ENIs. A total of {(len(eni_list))} resources!")
    for c in eni_list:
        try:
            modifyeni = ec2.create_tags(DryRun=True, Resources=[c],Tags=[{'Key':'BillingTag','Value':'vpc-0832a05760d4b5726'}])
        except botocore.exceptions.ClientError as error:
            print (error)
    print ()
    print (f"Updating Security Groups. A total of {(len(sg_list))} resources!")
    for d in sg_list:
        try:
            modifysg = ec2.create_tags(DryRun=True, Resources=[d],Tags=[{'Key':'BillingTag','Value':'vpc-0832a05760d4b5726'}])
        except botocore.exceptions.ClientError as error:
            print (error)
'''

def add_interfaces():
    ...

def add_elbs():
    ...

ec2 = boto3.client('ec2',"us-east-1")
#enter_vpc = input("Enter VPC ID: ")
print ()
print ("##################################################################################")
ids = get_ids(ec2)
#enis = add_interfaces()
#elbs = add_elbs()
