import boto3
try:
    from logger import setup_logger
    from config import AWS_REGION, S3_BUCKET_BASE_NAME
except ImportError:
    from scripts.logger import setup_logger
    from scripts.config import AWS_REGION, S3_BUCKET_BASE_NAME

logger = setup_logger()

def delete_s3(target_bucket_name=None):
    try:
        s3 = boto3.client('s3', region_name=AWS_REGION)
        
        if target_bucket_name:
            buckets_to_delete = [target_bucket_name]
        else:
            response = s3.list_buckets()
            buckets_to_delete = [b['Name'] for b in response['Buckets'] if b['Name'].startswith(S3_BUCKET_BASE_NAME)]

        if not buckets_to_delete:
            logger.info("No matching S3 buckets found to delete.")
            return None

        s3_resource = boto3.resource('s3', region_name=AWS_REGION)
        for bucket_name in buckets_to_delete:
            bucket = s3_resource.Bucket(bucket_name)
            
            bucket.objects.all().delete()
            
            bucket.delete()
            logger.info(f"S3 Bucket Deleted: {bucket_name}")
            
        return None

    except Exception as e:
        error_msg = f"Error deleting S3 Bucket: {str(e)}"
        logger.error(error_msg)
        return error_msg

if __name__ == "__main__":
    delete_s3()
