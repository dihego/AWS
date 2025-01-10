#!bin/python3
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

def get_ids(pass_ec2,pass_elb,pass_lambdaa,GetToken):
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


    #get_lambdaa(pass_lambdaa,vpc_names,GetToken)
    #get_tgwattachment(pass_ec2,vpc_names,GetToken)
    get_nat_gateways(pass_ec2,vpc_names,GetToken)
    get_endpoints(pass_ec2,vpc_names,GetToken)
    get_routetables(pass_ec2,vpc_names,GetToken)
    get_subnets(pass_ec2,vpc_names,GetToken)
    get_vpcs(pass_ec2,vpc_names,GetToken)
    get_instances(pass_ec2,vpc_names,GetToken)
    get_interfaces(pass_ec2,vpc_names,GetToken)
    get_securitygroups(pass_ec2,vpc_names,GetToken)
    #get_elbs(pass_elb,vpc_names,GetToken)


def get_lambdaa(pass_lambdaa,vpc_names,GetToken):
    resourcebyvpc = pass_lambdaa.list_functions()

    for matchingvpcs in resourcebyvpc['Functions']:
        getresourceid = (matchingvpcs['FunctionName'])
        print (getresourceid)



       # try:
        function_config = pass_lambdaa.get_function(FunctionName='dgo_tagging_ec2_resources')
        #getsvpcid = function_config['VpcConfig']
        print (function_config)
        #print (getsvpcid)
        #except:
        #    print ("nothing there")

        #add_tags(pass_ec2,getresourceid,getsvpcid,vpc_names)



def get_tgwattachment(pass_ec2,vpc_names,GetToken):
    resourcebyvpc = pass_ec2.describe_transit_gateway_attachments()


    for matchingvpcs in resourcebyvpc['Functions']:
        getresourceid = (matchingvpcs['TransitGatewayAttachmentId'])
        getsvpcid = (matchingvpcs['ResourceId'])
        add_tags(pass_ec2,getresourceid,getsvpcid,vpc_names)



def get_nat_gateways(pass_ec2,vpc_names,GetToken):
    for matchingvpcs in vpc_names:
        resourcebyvpc = pass_ec2.describe_nat_gateways(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [matchingvpcs]
                }
            ])

        for resourceAttribute in resourcebyvpc['NatGateways']:
            getresourceid = (resourceAttribute['NatGatewayId'])
            getsvpcid = (resourceAttribute['VpcId'])
            add_tags(pass_ec2,getresourceid,getsvpcid,vpc_names)


def get_endpoints(pass_ec2,vpc_names,GetToken):
    for matchingvpcs in vpc_names:
        resourcebyvpc = pass_ec2.describe_vpc_endpoints(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [matchingvpcs]
                }
            ])

        for resourceAttribute in resourcebyvpc['VpcEndpoints']:
            getresourceid = (resourceAttribute['VpcEndpointId'])
            getsvpcid = (resourceAttribute['VpcId'])
            add_tags(pass_ec2,getresourceid,getsvpcid,vpc_names)


def get_routetables(pass_ec2,vpc_names,GetToken):
    for matchingvpcs in vpc_names:
        resourcebyvpc = pass_ec2.describe_route_tables(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [matchingvpcs]
                }
            ])

        for resourceAttribute in resourcebyvpc['RouteTables']:
            getresourceid = (resourceAttribute['RouteTableId'])
            getsvpcid = (resourceAttribute['VpcId'])
            add_tags(pass_ec2,getresourceid,getsvpcid,vpc_names)





def get_subnets(pass_ec2,vpc_names,GetToken):
    for matchingvpcs in vpc_names:
        resourcebyvpc = pass_ec2.describe_subnets(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [matchingvpcs]
                }
            ])

        for resourceAttribute in resourcebyvpc['Subnets']:
            getresourceid = (resourceAttribute['SubnetId'])
            getsvpcid = (resourceAttribute['VpcId'])
            add_tags(pass_ec2,getresourceid,getsvpcid,vpc_names)




def get_vpcs(pass_ec2,vpc_names,GetToken):
    for matchingvpcs in vpc_names:
        resourcebyvpc = pass_ec2.describe_vpcs(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [matchingvpcs]
                }
            ])

        for resourceAttribute in resourcebyvpc['Vpcs']:
            getresourceid = (resourceAttribute['VpcId'])
            getsvpcid = (resourceAttribute['VpcId'])
            add_tags(pass_ec2,getresourceid,getsvpcid,vpc_names)



def get_instances(pass_ec2,vpc_names,GetToken):
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


def get_interfaces(pass_ec2,vpc_names,GetToken):
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



def get_elbs(pass_elb,vpc_names,GetToken):
    print (pass_elb)
    #resourcebyvpc = pass_elb.describe_load_balancers()
    #print (resourcebyvpc)
    for matchingvpcs in pass_elb:
        #resourcebyvpc = pass_elb.describe_load_balancers()#'''(
            #Filters=[
                #{
               #     'Name': 'vpc-id',
              #      'Values': [matchingvpcs]
             #   }
            #])
        print (matchingvpcs)
        #for resourceAttribute in resourcebyvpc['LoadBalancers']:
        #    getresourceid = (resourceAttribute['LoadBalancerArn'])
        #    getsgvpcid = (resourceAttribute['VpcId'])
        #    add_tags(pass_ec2,getresourceid,getsgvpcid,vpc_names)


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
                modifyec2 = ec2.create_tags(DryRun=False, Resources=[getvolumeid],Tags=[{'Key':'BillingTag','Value':value}])
            except botocore.exceptions.ClientError as error:
                print (error)
    print ()


falsetoken = True
ec2 = boto3.client('ec2',"us-east-1")
elb = boto3.client('elbv2',"us-east-1")
lambdaa = boto3.client('lambda', region_name="us-east-1")

def lambda_handler(event, Context):
    get_ids(ec2,elb,lambdaa,falsetoken)
    

print ()
print ("##################################################################################")
