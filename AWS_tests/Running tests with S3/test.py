import boto3
from botocore.exceptions import ClientError
import paramiko
import sys
import socket
from datetime import datetime

from ssh_client import SSHClient

def create_instance(
        image_id, instance_type, key_name, placement, security_group_names, instance_market_options, tags):
    """
    Creates a new Amazon EC2 instance. The instance automatically starts immediately after
    it is created.
    The instance is created in the default VPC of the current account.
    :param image_id: The Amazon Machine Image (AMI) that defines the kind of
                     instance to create. The AMI defines things like the kind of
                     operating system, such as Amazon Linux, and how the instance is
                     stored, such as Elastic Block Storage (EBS).
    :param instance_type: The type of instance to create, such as 't2.micro'.
                          The instance type defines things like the number of CPUs and
                          the amount of memory.
    :param key_name: The name of the key pair that is used to secure connections to
                     the instance.
    :param security_group_names: A list of security groups that are used to grant
                                 access to the instance. When no security groups are
                                 specified, the default security group of the VPC
                                 is used.
    :return: The newly created instance.
    """
    try:
        instance_params = {
            'ImageId': image_id, 'InstanceType': instance_type, 'KeyName': key_name
        }
        if security_group_names is not None:
            instance_params['SecurityGroups'] = security_group_names
        instance = ec2.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType=instance_type, KeyName=key_name, SecurityGroups=security_group_names, Placement=placement, InstanceMarketOptions=instance_market_options, TagSpecifications=tags)[0]
    except ClientError:
        print(
            "Couldn't create instance with image %s, instance type %s, and key %s.",
            image_id, instance_type, key_name)
        raise
    else:
        return instance

def get_preemptible_price(instance_type, zone):

        _filters = [
            {
                'Name': 'product-description',
                'Values': ['Linux/UNIX']
            }
        ]

        if zone is not None:
            _filters.append(
                {
                    'Name': 'availability-zone',
                    'Values': [zone]
                }
            )

        history = client_ec2.describe_spot_price_history(
            InstanceTypes=[instance_type],
            Filters=_filters,
            StartTime=datetime.now()
        )

        return [(h['AvailabilityZone'], float(h['SpotPrice'])) for h in history['SpotPriceHistory']]

ec2 = boto3.resource('ec2')
client_ec2 = boto3.client('ec2')
imageId = {'t2.micro': "ami-03bc2d95428a71d1e",'g2.2xlarge' : "ami-02b90f3f453ce325a", 'g4dn.xlarge': "ami-01eac07b415f7d9f9", 'g3s.xlarge':"ami-0fc557c504ee0156b", 'p2.xlarge': "ami-0837e95cd7284c31f", 'g4dn.2xlarge': "ami-01eac07b415f7d9f9" }
cuda_arch = {'t2.micro': "sm_10",'g2.2xlarge' : "sm_30", 'g4dn.xlarge': "sm_75", 'g3s.xlarge':"sm_52", 'p2.xlarge': "sm_37", 'g4dn.2xlarge': "sm_75" }
#type_instances = ['t2.micro', 'g2.2xlarge', 'g3s.xlarge', 'g4dn.xlarge', 'p2.xlarge', 'g4dn.2xlarge']
type_instances = ['t2.micro', 'g2.2xlarge', 'g3s.xlarge', 'p2.xlarge']
path_to_key_pair = '/home/rafaela/'
key_pair_name = "par_iam_rafaelabrum"
security_groups = ["rafaela"]
placement = {
        'AvailabilityZone': 'us-east-1a'
    }
instance_market_options = {
        'MarketType': 'spot',
        'SpotOptions': {
            'SpotInstanceType': 'one-time'
        }
    }
tags = [
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Owner',
                    'Value': 'Rafaela Brum'
                },
            ]
        },
        {
            'ResourceType': 'spot-instances-request',
            'Tags': [
                {
                    'Key': 'Owner',
                    'Value': 'Rafaela Brum'
                },
            ]
        },
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Owner',
                    'Value': 'Rafaela Brum'
                },
            ]
        },
    ]
run_file = 'run_1.sh'

export_command = 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.2/lib64; echo $LD_LIBRARY_PATH; export PATH=$PATH:/usr/local/cuda-10.2/bin:/home/ubuntu/MASA-CUDAlign/masa-cudalign-3.9.1.1024; echo $PATH; '

for type_instance in type_instances:
  if type_instance == 't2.micro' or type_instance == 'g2.2xlarge':
#  print "type_instance " + type_instance
#  if type_instance != 'g3s.xlarge' or type_instance != 'p2.xlarge':
    continue
  try:
    instance = create_instance(imageId[type_instance], type_instance, key_pair_name, placement, security_groups, instance_market_options, tags);
  except ClientError:
        print "Nao foi possivel alocar " + type_instance + "!"
        continue
  instance.wait_until_running()
  instance.load()
  print "Created instance " + instance.instance_id + " do tipo " + type_instance + " com IP " + instance.public_ip_address
  print "Preco spot do tipo " + type_instance + " = US$ " + str(get_preemptible_price(type_instance, placement['AvailabilityZone'])[0][1]) + " por hora"
  sys.stdout.flush()
  if type_instance == 'g3s.xlarge' or type_instance == 'p2.xlarge':
    ssh = SSHClient(instance.public_ip_address, path_to_key_pair+key_pair_name+'.pem')
    connected = ssh.open_connection()
    if (connected):
      print("Conection successful")
      stdout, stderr, retcode = ssh.execute_command('ls', output=True)
      print("Command ls executed")
      print(stdout)
      command = 'sh config.sh ' + cuda_arch[type_instance]
      #command += 'sh ' + run_file + ' ' + type_instance
      stdout, stderr, retcode = ssh.execute_command(command, output=True)
      print("Command '" + command + "' executed")
      #print(stdout)
      #command = export_command + 'cudalign --list-gpus'
      command = export_command + 'sh ' + run_file + ' ' + type_instance
      stdout, stderr, retcode = ssh.execute_command(command, output=True)
      print("Command '" + command + "' executed")
      print(stdout)
      ssh.close_connection()
      print "Preco spot do tipo " + type_instance + " = US$ " + str(get_preemptible_price(type_instance, placement['AvailabilityZone'])[0][1]) + " por hora"
      sys.stdout.flush()
  response = client_ec2.cancel_spot_instance_requests(SpotInstanceRequestIds=[instance.spot_instance_request_id])
  print "Cancelling spot request"
  print(response)
  instance.terminate()
  instance.wait_until_terminated()
  print "Terminated instance of type " + type_instance + "!"
  #break
