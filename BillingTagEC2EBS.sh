#/bin/bash

#AWS CLI 
#The point of this script is to tag EC2 fleet & EBS volumes so that it can be properly viewed in cost explorer based on the VPC spend. 
#1. Obtain EC2 Fleet ID and Volumes attached to those instances
#1.2 Once the list of IDs is retrive - Then we tag resources with an specific TAG
#Script
#1. 
#aws ec2 describe-instances --filters "Name=key-name,Values=dgo_iad_nt3eae" 
#aws ec2 describe-instances --filters "Name=vpc-id,Values=vpc-0832a05760d4b5726"
#aws ec2 describe-instances --filters "Name=vpc-id,Values=$getvpcid" --query "Reservations[*].Instances[*].[InstanceId]" --output text
#aws ec2 describe-instances --filters "Name=vpc-id,Values=vpc-0832a05760d4b5726" --query "Reservations[*].Instances[*].{Instance:InstanceId,Subnet:SubnetId}"
#1.2  
#aws ec2 create-tags --resource vol-08f1256eace1fb04a --tags Key=BillingTag,Value=vpc-0832a05760d4b5726
#1.3 #Not needed
#aws ec2 describe-volumes --filters Name=attachment.instance-id,Values=i-05466af2d4b3ab8df --query "Volumes[*].{ID:VolumeId}" --output text #this will display volumeId associated with Instance

##################################################################################
echo "Enter VPC-ID: "; read getvpcid
getinstancedi=$(aws ec2 describe-instances --filters "Name=vpc-id,Values=$getvpcid" --query "Reservations[*].Instances[*].[InstanceId]" --output text)
getvolumeidfrominstance=$(aws ec2 describe-instances --filters "Name=vpc-id,Values=vpc-0832a05760d4b5726" | grep 'VolumeId' | awk '{print$2}' | sed 's/"//g')

echo 
echo
#Getting and adding a TAG to the instance

echo "Updating EC2 fleet associated with $getvpcid :" 

for filename in $getinstancedi
do 
    #gettinggvolumesid=$(aws ec2 describe-volumes --filters Name=attachment.instance-id,Values=$filename --query "Volumes[*].{ID:VolumeId}" --output text)
    aws ec2 create-tags --resource $filename --tags Key=BillingTag,Value=vpc-0832a05760d4b5726
done
echo "done"


echo 
echo
#Getting and adding a TAG to the Volumes
echo "Updating all volumes attached to instances associated with $getvpcid :"

for filename in $getvolumeidfrominstance
do 
    aws ec2 create-tags --resource $filename --tags Key=BillingTag,Value=vpc-0832a05760d4b5726
done
echo "done"
