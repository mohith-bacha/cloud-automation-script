import boto3
try:
    from logger import setup_logger
    from config import AWS_REGION
except ImportError:
    from scripts.logger import setup_logger
    from scripts.config import AWS_REGION

logger = setup_logger()

def delete_ec2(target_instance_id=None):
    try:
        ec2 = boto3.client('ec2', region_name=AWS_REGION)

        if target_instance_id:
            instance_ids = [target_instance_id]
        else:
            instances = ec2.describe_instances(
                Filters=[{'Name': 'instance-state-name', 'Values': ['pending', 'running', 'stopping', 'stopped']}]
            )
            instance_ids = []
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    instance_ids.append(instance['InstanceId'])

        if instance_ids:
            ec2.terminate_instances(InstanceIds=instance_ids)
            logger.info(f"Terminated Instances: {instance_ids}")
        else:
            logger.info("No instances found to terminate")
        
        return None

    except Exception as e:
        error_msg = f"Error deleting EC2: {str(e)}"
        logger.error(error_msg)
        return error_msg

if __name__ == "__main__":
    delete_ec2()