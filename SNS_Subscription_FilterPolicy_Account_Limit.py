#/bin/python3
import os,sys
import boto3
import botocore
import time

#Good blog
#https://www.packetswitch.co.uk/how-to-use-nexttoken-in-boto3-aws-api-calls/f

print ('''##################################################################################
To query SNS there is a limit on the number of results in return "100". 
To go beyond that, SNS provides a token for you to query the remaining and so on.      
Alternatevely, there is get_paginator. However, there is a limitation of what you can query. See SDK documentation!   

##################################################################################
##################################################################################''')

falsetoken = True

def listsubstopics (passingsns,tokenbreaker):

    getsubs = passingsns.list_subscriptions()
    results = getsubs['Subscriptions']
    numeroenlista = (len(results))
    compilelistofsubsarn = []
    print (f'We know there are 5 subscriptions but only {numeroenlista} in this response!!!')
    
    for resultz in getsubs['Subscriptions']:
        arn = (resultz['SubscriptionArn'])
        if "Deleted" in arn:
            print("There is a deleted item")
        else:

            print (arn)
            compilelistofsubsarn.append(arn)
            obtainingtoken = (getsubs.get('NextToken', 'None'))

    while tokenbreaker:

        if obtainingtoken != 'None':
            print ()
            print ()
            getsubs = passingsns.list_subscriptions(NextToken=obtainingtoken)
            numeroenlista = (len(getsubs))
            print (f"Number of subscriptions to go through {numeroenlista} $$")
            for resultz2 in getsubs['Subscriptions']:
                arn = (resultz2['SubscriptionArn'])
                print (arn)
                compilelistofsubsarn.append(arn)

            print()
            obtainingtoken = (getsubs.get('NextToken', 'None'))
        elif obtainingtoken == 'None':
            print ("there isnt any else________")
            print ()
            print ("########################################################################")
            break

    numberofsubscriptions = (len(compilelistofsubsarn))
    print ("Now going through all subscriptionARNs to see if there are any FilterPolicies configured!")
    print ()
    print ()
    filterpolicynumber = []
    for x in compilelistofsubsarn:
        getsubattributes = passingsns.get_subscription_attributes(SubscriptionArn=x)
        filtersubscriberattributes = getsubattributes['Attributes']
        subsattributes_topic = (filtersubscriberattributes['TopicArn'])
        subsattribute_arn = (filtersubscriberattributes['SubscriptionArn'])

        if "FilterPolicy" in filtersubscriberattributes.keys():
            print ("FilterPolicy Found::")
            print (f"TopicARN ==> {subsattributes_topic}")
            print (f"SubscriptionARN ==> {subsattribute_arn}")
            print("value =", filtersubscriberattributes['FilterPolicy'])
            print()
            filterpolicynumber.append(subsattribute_arn)

    print ()
    print ()
    filterpolicynumberlength = (len(filterpolicynumber))
    print (f"There is a total of (({filterpolicynumberlength})) FilterPolicies configured in the account!")

        #for xx in getsubattributes['Attribures']:
        #    print (xx)

    




sns = boto3.client('sns','us-east-1')
subscriptionsTopics = listsubstopics(sns,falsetoken)
