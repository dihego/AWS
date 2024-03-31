#bin/python3
import os,sys
import boto3
import botocore
import time

#os.system('clear')
os.system('date')
print ('''#############################################################################################
Tagging resources [EC2 Fleet, EBS Volumes, Security Groups and ENIs] to VPC-ID or value of your choice.
Get detail billing with TAG association in Cost Explorer.
#######################################################################################################
#######################################################################################################''')


def get_arguments():
    ...

def get_ids(pass_ec2,GetToken):
    vpc_names = []

    print ("#####")
    response = pass_ec2.describe_vpcs()
    vpc_ids = [vpc['VpcId'] for vpc in response['Vpcs']]
    vpc_names = {}
    for testing in vpc_ids:
        listtags = pass_ec2.describe_tags(
            Filters=[
                {
                    'Name': 'resource-type',
                    'Values': ['vpc']
                },
                {
                    'Name': 'resource-id',
                    'Values': [testing]
                }
                #{
                #    'Name': 'key',
                #    'Values':['Name']
                #}
                ])['Tags']
        getname_tag = [tag['Value'] for tag in listtags if tag ['Key'] == 'Name']
        if getname_tag:
            vpc_names[testing] = getname_tag[0]
        else:
            print (f"All VPCs should have a ***NAME***")
            return None        
        
    add_instances(pass_ec2,vpc_names,GetToken)
    add_interfaces(pass_ec2,vpc_names,GetToken)
    get_securitygroups(pass_ec2,vpc_names,GetToken)




def add_instances(pass_ec2,vpc_names,GetToken):
    for matchingvpcs in vpc_names:
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
                    add_ebs_tags(pass_ec2,getresourceid,getvolumeid,getvpcid,vpc_names)

            add_tags(pass_ec2,getresourceid,getvpcid,vpc_names)
### Try filtering w/out for_loop_

    

def add_interfaces(pass_ec2,vpc_names,GetToken):
    for matchingvpcs in vpc_names:
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
            add_tags(pass_ec2,getresourceid,getsvpcid,vpc_names)


def get_securitygroups(pass_ec2,vpc_names,GetToken):
    for matchingvpcs in vpc_names:
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
            add_tags(pass_ec2,getresourceid,getsgvpcid,vpc_names)



def add_elbs():
    ...

def add_tags(ec2,resource_list,vpc_list,vpc_names):
    for key, value in vpc_names.items():
        if key == vpc_list:
            print (f"{resource_list} ___ Applying Billing Tag ___ {value} ___ part of __{vpc_list}____")
            try:
                modifyec2 = ec2.create_tags(DryRun=False, Resources=[resource_list],Tags=[{'Key':'BillingTag','Value':value}])
            except botocore.exceptions.ClientError as error:
                print (error)
    print ()


def add_ebs_tags(ec2,resource_list,getvolumeid,vpc_list,vpc_names):
    for key, value in vpc_names.items():
        if key == vpc_list:
            print (f"VOLUMES@@@@ Applying Billing Tag {value}___ for __{vpc_list}__ to Resource {getvolumeid} from instance {resource_list} ############")
            try:
                modifyec2 = ec2.create_tags(DryRun=True, Resources=[getvolumeid],Tags=[{'Key':'BillingTag','Value':value}])
            except botocore.exceptions.ClientError as error:
                print (error)
    print ()


falsetoken = True
ec2 = boto3.client('ec2',"us-east-1")
print ()
print ("##################################################################################")
ids = get_ids(ec2,falsetoken)
