import boto3
import random
import string
try:
    from logger import setup_logger
    from config import AWS_REGION, EC2_AMI_ID, EC2_INSTANCE_TYPE, EC2_KEY_NAME
except ImportError:
    from scripts.logger import setup_logger
    from scripts.config import AWS_REGION, EC2_AMI_ID, EC2_INSTANCE_TYPE, EC2_KEY_NAME

logger = setup_logger()

def create_ec2():
    try:
        ec2 = boto3.resource('ec2', region_name=AWS_REGION)
        
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        instance_name = f"sprint-automation-ec2-{random_suffix}"

        instance = ec2.create_instances(
            ImageId=EC2_AMI_ID,
            MinCount=1,
            MaxCount=1,
            InstanceType=EC2_INSTANCE_TYPE,
            KeyName=EC2_KEY_NAME,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        },
                    ]
                },
            ]
        )

        instance_id = instance[0].id
        logger.info(f"EC2 Created: {instance_id} (Name: {instance_name})")
        return True, instance_id

    except Exception as e:
        error_msg = f"Error creating EC2: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

if __name__ == "__main__":
    create_ec2()