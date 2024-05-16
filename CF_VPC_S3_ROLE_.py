Description: >-
  This template is to be used only to create an S3 bucket as well as a VPC w/ 1 CIDR and a total of 6 subnets in AZ (a,b).
  Subnets are pub, priv and trans and route tables associated with the subnets in question.
  S3 - creates a bucket w/ whatever name is assocaited with the cloudformation
Resources:
  Bucket:
    Type: AWS::S3::Bucket
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
        - Id: !Sub ${AWS::StackName}-bucketInterlTearing-{AWS::AccountId}
          Status: Enabled
          Tierings:
            - AccessTier: ARCHIVE_ACCESS
              Days: 90
  BucketBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref Bucket
      PolicyDocument:
        Id: RequireEncryptionInTransit
        Version: '2012-10-17'
        Statement:
          - Principal: '*'
            Action: '*'
            Effect: Deny
            Resource:
              - !GetAtt Bucket.Arn
              - !Sub ${Bucket.Arn}/*
            Condition:
              Bool:
                aws:SecureTransport: 'false'
  InstanceS3Role:
    Type: AWS::IAM::Role
    Properties:
      Description: "Role to be assumed by instance with R/W on CF created Bucket"
      RoleName: !Sub ${AWS::StackName}-RoleName-${AWS::AccountId}
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service:
                - ec2.amazonaws.com
            Action:
              - 'sts:AssumeRole'
      Path: /
  RolePolicies:
    Type: AWS::IAM::Policy
    Properties:
      PolicyName: !Sub ${AWS::StackName}-policyName-${AWS::AccountId}
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Action: "s3:*"
            Resource: !GetAtt Bucket.Arn
      Roles:
        - !Ref InstanceS3Role
  S3InstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Path: /
      Roles:
        - !Ref InstanceS3Role
  VPC2024:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 172.30.104.0/21
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: vpc2024
  Subnetappa:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId:
        Ref: VPC2024
      CidrBlock: 172.30.106.0/24
      AvailabilityZone: "us-east-1a"
      Tags:
        - Key: Name
          Value: subappa
  Subnetappb:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId:
        Ref: VPC2024
      CidrBlock: 172.30.107.0/24
      AvailabilityZone: "us-east-1b"
      Tags:
        - Key: Name
          Value: subappb
  Subnetpuba:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId:
        Ref: VPC2024
      CidrBlock: 172.30.104.0/24
      AvailabilityZone: "us-east-1a"
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: subpuba
  Subnetpubb:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId:
        Ref: VPC2024
      CidrBlock: 172.30.105.0/24
      AvailabilityZone: "us-east-1b"
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: subpubb
  Subnettransa:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId:
        Ref: VPC2024
      CidrBlock: 172.30.108.0/26
      AvailabilityZone: "us-east-1a"
      Tags:
        - Key: Name
          Value: subtransa
  Subnettransb:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId:
        Ref: VPC2024
      CidrBlock: 172.30.108.64/26
      AvailabilityZone: "us-east-1b"
      Tags:
        - Key: Name
          Value: subtransb
  Subnetfwa:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId:
        Ref: VPC2024
      CidrBlock: 172.30.108.128/26
      AvailabilityZone: "us-east-1a"
      Tags:
        - Key: Name
          Value: subfwa
  Subnetfwb:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId:
        Ref: VPC2024
      CidrBlock: 172.30.108.192/26
      AvailabilityZone: "us-east-1b"
      Tags:
        - Key: Name
          Value: subfwb
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
  SubnetRouteTableAssociationpub:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId:
        Ref: RouteTablePub
      SubnetId: !Ref Subnetpuba
  SubnetRouteTableAssociationpubB:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId:
        Ref: RouteTablePub
      SubnetId: !Ref Subnetpubb
  SubnetRouteTableAssociationapp:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId:
        Ref: RouteTableApp
      SubnetId: !Ref Subnetappa
  SubnetRouteTableAssociationappB:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId:
        Ref: RouteTableApp
      SubnetId: !Ref Subnetappb
  SubnetRouteTableAssociationfw:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId:
        Ref: RouteTableFw
      SubnetId: !Ref Subnetfwa
  SubnetRouteTableAssociationfwB:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId:
        Ref: RouteTableFw
      SubnetId: !Ref Subnetfwb
