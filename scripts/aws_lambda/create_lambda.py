import boto3
import random
import string
import zipfile
import io
try:
    from logger import setup_logger
    from config import AWS_REGION, LAMBDA_FUNCTION_BASE_NAME, LAMBDA_EXECUTION_ROLE_ARN
except ImportError:
    from scripts.logger import setup_logger
    from scripts.config import AWS_REGION, LAMBDA_FUNCTION_BASE_NAME, LAMBDA_EXECUTION_ROLE_ARN

logger = setup_logger()

def create_lambda():
    try:
        lambda_client = boto3.client('lambda', region_name=AWS_REGION)
        
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        function_name = f"{LAMBDA_FUNCTION_BASE_NAME}-{random_suffix}"

        # Dynamically create the lambda code zip file in memory
        lambda_code = """
def lambda_handler(event, context):
    print("Automation Lambda is running!")
    return {
        'statusCode': 200,
        'body': 'Hello from AWS Automation Sprint!'
    }
"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('lambda_function.py', lambda_code)
        
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.9',
            Role=LAMBDA_EXECUTION_ROLE_ARN,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_buffer.getvalue()},
            Description='Created by AWS Automation Script',
            Timeout=5,
            MemorySize=128
        )

        logger.info(f"Lambda Function Created: {function_name}")
        return True, function_name

    except Exception as e:
        error_msg = f"Error creating Lambda Function: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

if __name__ == "__main__":
    create_lambda()
