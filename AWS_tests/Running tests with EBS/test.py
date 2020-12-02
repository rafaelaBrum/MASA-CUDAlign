import boto3
from botocore.exceptions import ClientError
import paramiko
import sys
import socket
from datetime import datetime

from ssh_client import SSHClient

def __attach_ebs(self, internal_device_name, path):


     # Mount Directory
     cmd = 'sudo mount {} {}'.format(internal_device_name, path)

     self.ssh.execute_command(cmd, output=True)  # mount directory

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
    except ClientError as e:
        print(
            "Couldn't create instance with image {}, instance type {}, and key {}.".format(image_id, instance_type, key_name))
        print(e)
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
imageId = {'t2.micro': "ami-09685b54c80020d8c",'g2.2xlarge' : "ami-035702788548e7738", 'g4dn.xlarge': "ami-0c4665c2149ec7fdc", 'g3s.xlarge':"ami-09b10133456de8dca", 'p2.xlarge': "ami-0b13bb0622a100af2", 'g4dn.2xlarge': "ami-0c4665c2149ec7fdc" }
type_instances = ['t2.micro', 'g2.2xlarge', 'g3s.xlarge', 'g4dn.xlarge', 'p2.xlarge', 'g4dn.2xlarge']
#type_instances = ['t2.micro', 'g2.2xlarge', 'g3s.xlarge', 'p2.xlarge']
path_to_key_pair = '/home/ubuntu/'
key_pair_name = "par_iam_rafaelabrum"
security_groups = ["rafaela"]
placement = {
        'AvailabilityZone': 'us-east-1a'
    }
# on-demand
#instance_market_options = {}
# spot
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
                    'Key': 'owner',
                    'Value': 'Rafaela Brum'
                },
            ]
        },
        {
            'ResourceType': 'spot-instances-request',
            'Tags': [
                {
                    'Key': 'owner',
                    'Value': 'Rafaela Brum'
                },
            ]
        },
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'owner',
                    'Value': 'Rafaela Brum'
                },
            ]
        },
    ]

run_file = 'run_1.sh'

export_command = 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.2/lib64; echo $LD_LIBRARY_PATH; export PATH=$PATH:/usr/local/cuda-10.2/bin:/home/ubuntu/MASA-CUDAlign/masa-cudalign-3.9.1.1024; echo $PATH; '

volume_id = 'vol-00e2d2c2debe85987'
internal_device_name = '/dev/xvdf'
ebs_path = 'tests_ebs/'

for type_instance in type_instances:
#  if type_instance == 't2.micro' or type_instance == 'g2.2xlarge':
  print("type_instance " + type_instance)
#  if type_instance != 'g3s.xlarge' or type_instance != 'p2.xlarge':
#    continue
  try:
    instance = create_instance(imageId[type_instance], type_instance, key_pair_name, placement, security_groups, instance_market_options, tags);
  except ClientError:
        print("Nao foi possivel alocar " + type_instance + "!")
        continue
  instance.wait_until_running()
  instance.load()
  print("Created instance " + instance.instance_id + " do tipo " + type_instance + " com IP " + instance.public_ip_address)
#  print "Preco spot do tipo " + type_instance + " = US$ " + str(get_preemptible_price(type_instance, placement['AvailabilityZone'])[0][1]) + " por hora"
  sys.stdout.flush()

  # attaching EBS volume to instance
  waiter = client_ec2.get_waiter('volume_available')
  waiter.wait(VolumeIds=[volume_id])
  try:
    client_ec2.attach_volume(VolumeId=volume_id, InstanceId=instance.instance_id,Device=internal_device_name)
    print("EBS attached")
    attached = True
  except Exception as e:
    print("Error while attaching EBS " + e)
    attached = False

  if attached:
    ssh = SSHClient(instance.public_ip_address, path_to_key_pair+key_pair_name+'.pem')
    connected = ssh.open_connection()
    if (connected):
      print("Conection successful")
      stdout, stderr, retcode = ssh.execute_command('ls', output=True)
      print("Command ls executed")
      print(stdout)
      # mounting EBS volume to ebs_path
      command = 'mkdir {}'.format(ebs_path)
      stdout, stderr, retcode = ssh.execute_command(command, output=True)
      print("Command mkdir executed")
      print(stdout)
      command = 'sudo mount {} {}'.format(internal_device_name, ebs_path)
      stdout, stderr, retcode = ssh.execute_command(command, output=True)
      print("Command mount executed")
      print(stdout)
      stdout, stderr, retcode = ssh.execute_command('ls -la', output=True)
      print("Command 'ls -la' executed")
      print(stdout)
      command = 'ls {}'.format(ebs_path)
      stdout, stderr, retcode = ssh.execute_command(command, output=True)
      print("Command '" + command + "' executed")
      print(stdout)
      # running tests (assuming the AMIs has already compiled the cudalign)
      command = '{} sh {} {}'.format(export_command, run_file, type_instance)
      stdout, stderr, retcode = ssh.execute_command(command, output=True)
      print("Command '" + command + "' executed")
      print(stdout)
      # unmount EBS volume
      command = 'sudo umount {}'.format(internal_device_name)
      stdout, stderr, retcode = ssh.execute_command(command, output=True)
      print("Command '" + command + "' executed")
      print(stdout)
      ssh.close_connection()
#    print "Preco spot do tipo " + type_instance + " = US$ " + str(get_preemptible_price(type_instance, placement['AvailabilityZone'])[0][1]) + " por hora"
#    sys.stdout.flush()
  response = client_ec2.cancel_spot_instance_requests(SpotInstanceRequestIds=[instance.spot_instance_request_id])
  print("Cancelling spot request")
  print(response)
  instance.terminate()
  instance.wait_until_terminated()
  print("Terminated instance of type " + type_instance + "!")
#  break
