import boto3
try:
    from logger import setup_logger
    from config import AWS_REGION, LAMBDA_FUNCTION_BASE_NAME
except ImportError:
    from scripts.logger import setup_logger
    from scripts.config import AWS_REGION, LAMBDA_FUNCTION_BASE_NAME

logger = setup_logger()

def delete_lambda(target_function_name=None):
    try:
        lambda_client = boto3.client('lambda', region_name=AWS_REGION)
        
        if target_function_name:
            functions_to_delete = [target_function_name]
        else:
            response = lambda_client.list_functions()
            functions_to_delete = [
                fn['FunctionName'] 
                for fn in response.get('Functions', []) 
                if fn['FunctionName'].startswith(LAMBDA_FUNCTION_BASE_NAME)
            ]

        if not functions_to_delete:
            logger.info("No matching Lambda functions found to delete.")
            return None

        for func_name in functions_to_delete:
            lambda_client.delete_function(FunctionName=func_name)
            logger.info(f"Lambda Function Deleted: {func_name}")
            
        return None

    except Exception as e:
        error_msg = f"Error deleting Lambda Function: {str(e)}"
        logger.error(error_msg)
        return error_msg

if __name__ == "__main__":
    delete_lambda()
