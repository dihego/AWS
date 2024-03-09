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

def get_ids(pass_ec2,GetToken):
    print
    list_vpcIds = []


    listvpcids = pass_ec2.describe_vpcs()
    for vpcattributes in listvpcids['Vpcs']:
        getvpcids = (vpcattributes['VpcId'])
        list_vpcIds.append(getvpcids)
    


    add_instances(pass_ec2,list_vpcIds)
    add_interfaces(pass_ec2,list_vpcIds,GetToken)
    get_securitygroups(pass_ec2,list_vpcIds)



def add_instances(pass_ec2,list_vpcIds):
    for matchingvpcs in list_vpcIds:
        resourcebyvpc = pass_ec2.describe_instances(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [matchingvpcs]
                }
            ])

        for resourceAttribute in resourcebyvpc['Reservations']:
            for i in  resourceAttribute['Instances']:
                getresourceid = (i['InstanceId'])
                getvpcid = (i['VpcId'])
                for x in i['BlockDeviceMappings']:
                    getvolumeid = (x['Ebs']['VolumeId'])
                    add_ebs_tags(pass_ec2,getresourceid,getvolumeid,getvpcid)
            add_tags(pass_ec2,getresourceid,getvpcid)
### Try filtering w/out for_loop_

    

def add_interfaces(pass_ec2,list_vpcIds,GetToken):
    for matchingvpcs in list_vpcIds:
        resourcebyvpc = pass_ec2.describe_network_interfaces(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [matchingvpcs]
                }
            ])

        for resourceAttribute in resourcebyvpc['NetworkInterfaces']:
            getresourceid = (resourceAttribute['NetworkInterfaceId'])
            getsvpcid = (resourceAttribute['VpcId'])
            add_tags(pass_ec2,getresourceid,getsvpcid)


def get_securitygroups(pass_ec2,list_vpcIds):
    for matchingvpcs in list_vpcIds:
        resourcebyvpc = pass_ec2.describe_security_groups(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [matchingvpcs]
                }
            ])

        for resourceAttribute in resourcebyvpc['SecurityGroups']:
            getresourceid = (resourceAttribute['GroupId'])
            getsgvpcid = (resourceAttribute['VpcId'])
            add_tags(pass_ec2,getresourceid,getsgvpcid)



def add_elbs():
    ...

def add_tags(ec2,resource_list,vpc_list):
    print (f"###### Applying Billing Tag {vpc_list} to Resource {resource_list} ############") 
    try:
        modifyec2 = ec2.create_tags(DryRun=False, Resources=[resource_list],Tags=[{'Key':'BillingTag','Value':vpc_list}])
    except botocore.exceptions.ClientError as error:
        print (error)
    print ()


def add_ebs_tags(ec2, resource_list, volume_list, vpc_list):
    print (f"###### Applying Billing Tag {vpc_list} <<{resource_list}>> to Resource {volume_list} ############")
    try:
        modifyebs = ec2.create_tags(DryRun=False, Resources=[volume_list],Tags=[{'Key':'BillingTag','Value':vpc_list}])
    except botocore.exceptions.ClientError as error:
        print (error)
    print ()


falsetoken = True
ec2 = boto3.client('ec2',"us-east-1")
#enter_vpc = input("Enter VPC ID: ")
print ()
print ("##################################################################################")
ids = get_ids(ec2,falsetoken)
