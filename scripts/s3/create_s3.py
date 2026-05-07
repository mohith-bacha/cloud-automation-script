import boto3
import random
import string
try:
    from logger import setup_logger
    from config import AWS_REGION, S3_BUCKET_BASE_NAME
except ImportError:
    from scripts.logger import setup_logger
    from scripts.config import AWS_REGION, S3_BUCKET_BASE_NAME

logger = setup_logger()

def create_s3():
    try:
        s3 = boto3.client('s3', region_name=AWS_REGION)
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        bucket_name = f"{S3_BUCKET_BASE_NAME}-{random_suffix}"

        if AWS_REGION == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
            )

        logger.info(f"S3 Bucket Created: {bucket_name}")
        return True, bucket_name

    except Exception as e:
        error_msg = f"Error creating S3 Bucket: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

if __name__ == "__main__":
    create_s3()
