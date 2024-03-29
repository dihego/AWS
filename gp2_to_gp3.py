#/bin/python3


import os,sys
import boto3
import botocore
import time

#os.system('clear')
#os.system('date')

ec2 = boto3.resource('ec2',"us-east-1")
volume = ec2.volumes.all() #can be specific with ec2.describe_volumes or ec2.modify_volume


vols = [vol for vol in volume if vol.volume_type == 'gp2' and vol.state == 'available']



enterr = input('''##########################################
Filtering is done  via API.resource 
Execution is done via AWS CLI OR can be done via Client once filtered

[[Dry-run Flag is enabled]] AND execution is commented out!!
[[Press-Enter:]]''')
print (' ')
print (' ')

print ("@@@@ Output example of gp2 and available volumes only!!")
print (' ')
print (' ')
for x in vols:
    print (x.id)
    print (x.tags)
    print (x.state)
    print (x.volume_type)


print ("#######")
print ("Execution AWS CLI command \n")
for xx in vols:
    cmd1 =  ("aws ec2 modify-volume --volume-type gp3 --volume-id ") +  (xx.id)
    print (cmd1)

#time.sleep(2)

print ('''###############################################################
###############################################################
Filtering is done  via API.CLIENT********* 
* Execution is done via API.CLIENT

       
[[Dry-run Flag is enabled]] 
[[Enter:]]
       
''')


client = boto3.client('ec2','us-east-1')
response = client.describe_volumes()







enter = input('Option#2 ')
print (' ')
print (' ')
for z in response['Volumes']:
    printing1 = (z['VolumeId'])
    printing2 = (z['State'])
    printing3 =  (z['VolumeType'])
    print (f"Volume ID:  {printing1}  ((Type: {printing3})) (( In-use: {printing2}))")


print ('       \n' )



enter = input('''###############################################################
###############################################################
--filtering on [[gp2]]
--status [[available]]
--Dry-run  (Execution Status)
[[Enter:]]          
              ''')

respuesta = client.describe_volumes(
    Filters=[
        {
            'Name': 'volume-type',
            'Values': ['gp2']
        },
        {
            'Name': 'status',
            'Values': ['available']
        }
    ])
    




for z in respuesta['Volumes']:
    print (z['VolumeId']) 
    founder = (z['VolumeId'])
    print ("found a match and converting")
    
    try: 
        modify = client.modify_volume(VolumeId=founder, VolumeType='gp3', DryRun=True)
        print(f"{VolumeId} changed to gp3")
    except botocore.exceptions.ClientError as error:
        print (error)

