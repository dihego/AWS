Description: This template creates an S3 bucket{Activates Inteligent Tiering {S3 - creates a bucket
  w/ whatever name is assocaited with the cloudformation}}, a VPC w/ 1
  CIDR and a total of 4 subnets in AZ (a,b) { Subnets {pub, priv, fw and trans}},
  4 route tables associated with the subnets in question. A role that attaches to an instance allowing to R/W 
  into the Bucket. 
Parameters:
  InstanceName:
    Description: Private a name to the instance created by this CF
    Type: String
    MinLength: 5
    MaxLength: 12
    #MinValue: 4
    #MaxValue: 16
    ConstraintDescription: Invalid Number of Characteres
  InstanceType:
    Description: Select an Instance Type to be provisioned
    Type: String
    AllowedValues:
      - t2.micro
      - t2.small
      - t3.micro
      - t3.small
    Default: t3.small
  KeyNameKey:
    Description: Enter the name of the Key for your instance. This needs to be
      preconfigured!!!
    Type: AWS::EC2::KeyPair::KeyName
    ConstraintDescription: Invalid Key
  PutBucketSNS:
    Description: An SNS topic will be used to notify Bucket managers whenever an object is added
      Please enter a working email address!
    Type: String
    AllowedPattern: ^.*@\w+.\w+$
  CurrentTransitGatewayId:
    Description: Your Account is part of a Hub/Spoke topology participating to a pre-existing TGW.
      Whats your TransitGTW Id?
      Example => "tgw-0764cba494fbb77ed"
    Type: String
    AllowedPattern: ^tgw-[0-9].*$
    ConstraintDescription: Enter a valid Id!!


  #SelectSG:
  #  Description: Select the SG to assign to the instance. If none it will select the default
  #  Type: AWS::EC2::SecurityGroup::Id
  ### Modify this if a Security Group is already part of a VPC

#Creation of Buckets
Resources:
  BucketS3:
    Type: AWS::S3::Bucket
    DependsOn: 
      - SNSTopicPubBucketObjectPolicy
    Properties:
      BucketName: !Sub ${AWS::StackName}-bucket-${AWS::AccountId}
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: aws:kms
              KMSMasterKeyID: alias/aws/s3
      PublicAccessBlockConfiguration:
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      IntelligentTieringConfigurations:
        - Id: !Sub ${AWS::StackName}-bucketInterlTearing-${AWS::AccountId}
          Status: Enabled
          Tierings:
            - AccessTier: ARCHIVE_ACCESS
              Days: 90
      NotificationConfiguration:
           TopicConfigurations:
                - Event: s3:ObjectCreated:*
                  Topic: !Ref SNSTopicPutBucketObject
#  BucketBucketPolicy:
#    Type: AWS::S3::BucketPolicy
#    Properties:
#      Bucket: !Ref BucketS3
#      PolicyDocument:
#        Id: RequireEncryptionInTransit
#        Version: '2012-10-17'
#        Statement:
#          - Principal: '*'
#            Action: '*'
#            Effect: Deny
#            Resource:
#              - !GetAtt BucketS3.Arn
#              - !Sub ${BucketS3.Arn}/*
#            Condition:
#              Bool:
#                aws:SecureTransport: 'false'

#Creation an SNS
  SNSTopicPutBucketObject:
    Type: AWS::SNS::Topic
    Properties:
      DisplayName: SNSS3ObjectedCreated
      TopicName: SNSS3ObjectedCreated

  SNSTopicPubBucketObjectPolicy:
    Type: AWS::SNS::TopicPolicy
    Properties:
      PolicyDocument:
        Id: SNSTopicPolicy
        Version: '2012-10-17'
        Statement:
          - Sid: CFSNSPolicy
            Effect: Allow
            Principal:
              Service: 
                - s3.amazonaws.com
            Action: sns:Publish
            Resource: "*"
      Topics:
        - !Ref SNSTopicPutBucketObject

#Creation SNS Subscription
  SNSSubscriptionNotification:
    Type: AWS::SNS::Subscription
    Properties:
         TopicArn: !Ref SNSTopicPutBucketObject
         Protocol: email
         Endpoint: !Ref PutBucketSNS


#Creation of Roles
  InstanceS3Role:
    Type: AWS::IAM::Role
    Properties:
      Description: Role to be assumed by instance with R/W on CF created Bucket
      RoleName: !Sub ${AWS::StackName}-RoleName-${AWS::AccountId}
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service:
                - ec2.amazonaws.com
            Action:
              - sts:AssumeRole
      Path: /
  RolePolicies:
    Type: AWS::IAM::Policy
    Properties:
      PolicyName: !Sub ${AWS::StackName}-policyName-${AWS::AccountId}
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action: s3:*
            Resource:
              - !GetAtt BucketS3.Arn
              - !Sub ${BucketS3.Arn}/*
      Roles:
        - !Ref InstanceS3Role
  S3InstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Path: /
      Roles:
        - !Ref InstanceS3Role
#Creation of VPCs
  VPC2024:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 172.30.104.0/21
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: vpc2024
#Creation of Subnets
  Subnetappa:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC2024
      CidrBlock: 172.30.106.0/24
      AvailabilityZone: us-east-1a
      Tags:
        - Key: Name
          Value: subappa
  Subnetappb:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC2024
      CidrBlock: 172.30.107.0/24
      AvailabilityZone: us-east-1b
      Tags:
        - Key: Name
          Value: subappb
  Subnetpuba:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC2024
      CidrBlock: 172.30.104.0/24
      AvailabilityZone: us-east-1a
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: subpuba
  Subnetpubb:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC2024
      CidrBlock: 172.30.105.0/24
      AvailabilityZone: us-east-1b
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: subpubb
  Subnettransa:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC2024
      CidrBlock: 172.30.108.0/26
      AvailabilityZone: us-east-1a
      Tags:
        - Key: Name
          Value: subtransa
  Subnettransb:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC2024
      CidrBlock: 172.30.108.64/26
      AvailabilityZone: us-east-1b
      Tags:
        - Key: Name
          Value: subtransb
  Subnetfwa:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC2024
      CidrBlock: 172.30.108.128/26
      AvailabilityZone: us-east-1a
      Tags:
        - Key: Name
          Value: subfwa
  Subnetfwb:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC2024
      CidrBlock: 172.30.108.192/26
      AvailabilityZone: us-east-1b
      Tags:
        - Key: Name
          Value: subfwb
#Creation of Route tables
  RouteTableApp:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC2024
      Tags:
        - Key: Name
          Value: App Route Table
  RouteTablePub:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC2024
      Tags:
        - Key: Name
          Value: Pub Route Table
  RouteTableFw:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC2024
      Tags:
        - Key: Name
          Value: FW Route Table
#TransitGatewayATTACHMENT
  TGWAttch:
    Type: AWS::EC2::TransitGatewayAttachment
    Properties:
      TransitGatewayId: !Ref CurrentTransitGatewayId
      VpcId: !Ref VPC2024
      SubnetIds:
        - !Ref Subnettransa
        - !Ref Subnettransb
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-stack

#Creation of Subnet association
# Note that there is no way to reference the MAIN RouteTable of a VPC outside the template
# Another way is to create nested stack calling a lambda function to retrieve the data needed
  SubnetRouteTableAssociationpub:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref RouteTablePub
      SubnetId: !Ref Subnetpuba
  SubnetRouteTableAssociationpubB:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref RouteTablePub
      SubnetId: !Ref Subnetpubb
  SubnetRouteTableAssociationapp:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref RouteTableApp
      SubnetId: !Ref Subnetappa
  SubnetRouteTableAssociationappB:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref RouteTableApp
      SubnetId: !Ref Subnetappb
  SubnetRouteTableAssociationfw:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref RouteTableFw
      SubnetId: !Ref Subnetfwa


# Creation of SGs
  AppSG:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub ${AWS::StackName}-SecurityGroup_
      GroupDescription: App Security Group
      SecurityGroupIngress:
        - CidrIp: 172.30.0.0/16
          IpProtocol: -1
          Description: Allow VPC CIDR
        - CidrIp: 192.168.101.0/24
          IpProtocol: -1
          Description: OutsideVPC         
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-SecurityGroup_
      VpcId: !Ref VPC2024

#Creation of Instances
#- !GetAtt VPC2024.DefaultSecurityGroup This can referenced as the securityGroup
  InstanceS3:
    Type: AWS::EC2::Instance
    Properties:
      AvailabilityZone: us-east-1a
      InstanceType: !Ref InstanceType
      ImageId: ami-0bb84b8ffd87024d8
      SubnetId: !Ref Subnetappa
      SecurityGroupIds: 
        - !Ref AppSG
      IamInstanceProfile: !Ref S3InstanceProfile
      KeyName: !Ref KeyNameKey
      Tags:
        - Key: Name
          Value: !Ref InstanceName
  InstanceS3B:
    Type: AWS::EC2::Instance
    Properties:
      AvailabilityZone: us-east-1b
      InstanceType: !Ref InstanceType
      ImageId: ami-0bb84b8ffd87024d8
      SubnetId: !Ref Subnetappb
      SecurityGroupIds:
        - !Ref AppSG
        
      IamInstanceProfile: !Ref S3InstanceProfile
      KeyName: !Ref KeyNameKey
      Tags:
        - Key: Name
          Value: !Ref InstanceName

# TGWRouteEntries
  TGWROUTESApp:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref RouteTableApp
      DestinationCidrBlock: 172.30.0.0/16
      TransitGatewayId: !Ref CurrentTransitGatewayId
    DependsOn:
         - TGWAttch

# Create Endpoints
  S3Endpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      RouteTableIds: 
        - !Ref RouteTableApp
      ServiceName: com.amazonaws.us-east-1.s3
      VpcId: !Ref VPC2024
