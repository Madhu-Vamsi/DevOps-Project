import boto3
from botocore.exceptions import ClientError

def listRegions():
    response = ec2Client.describe_regions()
    print('Regions Available :')
    for regions in response['Regions']:
        print('Region : {}'.format(regions['RegionName']))

def listImages():
        allImages = ec2Client.describe_images(ExecutableUsers=['all'],Filters=[{'Name' : 'owner-alias', 'Values' :['amazon']}])
        for eachImage in allImages['Images']:
                print('{}\t{}'.format(eachImage['ImageId'], eachImage['ImageLocation']))

def createNewMachine(imgId, maxCount, minCount, instanceType, keyName):
    try:
        machineCreated = ec2Resource.create_instances(ImageId=imgId, MaxCount=maxCount, MinCount=minCount, InstanceType=instanceType, KeyName=keyName)
        print('Successfully created the machine {}'.format(machineCreated))
    except BaseException as exe:
        print(exe) 

def stopInstances(instancesToStop):
    print(instancesToStop)
    ec2Client.terminate_instances(InstanceIds=instancesToStop)
    print('Successfully terminated the instances with the id {}'.format(instancesToStop))

def listInstanceId():
    descriptionOfInstances = ec2Client.describe_instances()
    print('Number Of Instances : {}'.format(len(descriptionOfInstances['Reservations'])))
    listOfInstances = []
    for i in range(0,len(descriptionOfInstances['Reservations'])):
        listOfInstances.append(str(descriptionOfInstances['Reservations'][i]['Instances'][0]['InstanceId']))
    statusOfInstances = ec2Client.describe_instance_status(IncludeAllInstances=True)
    #for eachStatus in statusOfInstances['InstanceStatuses']:
    #    print('{}\t{}'.format(eachStatus['InstanceId'], eachStatus['InstanceState']['Name']))

def getRunningInstance():
    flag = False
    statusOfInstances = ec2Client.describe_instance_status(IncludeAllInstances=True)
    for eachStatus in statusOfInstances['InstanceStatuses']:
        if(eachStatus['InstanceState']['Name'] == 'running' or eachStatus['InstanceState']['Name'] == 'pending'):
            flag = True
            #print('{}\t{}'.format(eachStatus['InstanceId'], eachStatus['InstanceState']['Name']))
            runningInstance = eachStatus['InstanceId']
    
    if(not flag):
        print('No Running Instances')
        return 'None'
    else:
        return runningInstance

def getIp(instanceId):
    currentInstance = ec2Resource.Instance(instanceId)
    instanceip = currentInstance.public_ip_address
    print(instanceip)
    return instanceip

def createKeyPair(keyName):
    keyCreated = ec2Client.create_key_pair(KeyName = keyName)
    print('Successfully created key-pair : {}'.format(keyName))
    keyFile = open('{}.pem'.format(keyName),'w')
    keyFile.write(str(keyCreated['KeyMaterial']))
    keyFile.close()
    return keyCreated

def deleteKeyPair(keyName):
    ec2Client.delete_key_pair(KeyName = keyName)
    print('Successfully deleted key-pair : {}'.format(keyName))

# INITIALISATION AND DECLARING OBJECTS/VARIABLES
regionValue = 'us-east-2'
ec2Client = boto3.client('ec2', region_name=regionValue)
ec2Resource = boto3.resource('ec2', region_name=regionValue)
imgId = 'ami-0653e888ec96eab9b'#'ami-04328208f4f0cf1fe'
maxCount = 1
minCount = 1
instanceType = 't2.micro'
keyName = 'DeployMilestone'
keyExists = False
groupId = 10
groupName = 'DevopsTest4'

# Check if any instance is running
#listInstanceId()
instanceId = getRunningInstance()
print('Instance running is : {}'.format(instanceId))

if(instanceId!= 'None'):
    instanceiprunning = getIp(instanceId)

if(instanceId == 'None'):
    # List keypairs
    listOfKeypairs = ec2Client.describe_key_pairs()
    
    # Check if the given keypair exists
    for eachPair in listOfKeypairs['KeyPairs']:
        if(eachPair['KeyName']==keyName):
            print('Key already exists with that name')
            keyExists = True
    
    # If the keypair doesn't exist, create the keypair
    if(not keyExists):
        key = createKeyPair(keyName)        
    
    # Create a new machine
    createNewMachine(imgId, maxCount, minCount, instanceType, keyName)
    
    # Get the instance id
    listInstanceId()
    instanceId = getRunningInstance()
    
    # Get the IP address
    instanceip = getIp(instanceId)

    # Write inventory file
    file_ip = open('aws_inventory','w')
    file_ip.write('[web]\nec2-instance ansible_host={} ansible_user=ubuntu ansible_ssh_private_key_file={}.pem\n[web:vars]\nansible_python_interpreter=/usr/bin/python3'.format(instanceip, keyName))
    file_ip.close()

    # Write IP to a file
    file_ip = open('production-ip.txt','w')
    file_ip.write('{}'.format(instanceip))
    file_ip.close()

    # Create Security Group
    try:
        response = ec2Client.create_security_group(GroupName=groupName,
                                            Description='DESCRIPTION')
        groupId = response['GroupId']
        security_group_id = groupId
        file_sg = open('security-group.txt','w')
        file_sg.write(security_group_id)
        file_sg.close()

        data = ec2Client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 0,
                'ToPort': 65535,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)
        file_sg = open('security-group.txt','r')
        groupId = file_sg.readlines()[0]

    # Attach security group to running instance
    ec2Client.modify_instance_attribute(
     Groups = [groupId],
     InstanceId = instanceId   
    )

#FOLLWING CAN BE USED TO DELETE THE KEYPAIR IN CASE OF ANY MISTAKE OR IF IT ISN'T REQUIRED ANYMORE.
#deleteKeyPair(keyName)

# DELETE THE INSTANCE WHEN NOT NEEDED
#instanceId = getRunningInstance()
#instanceList = []
#instanceList.append(instanceId)
#stopInstances(instanceList)
#if os.path.exists(".txt"):
#    os.remove("demofile.txt")
