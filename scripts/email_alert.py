import boto3
try:
    from config import AWS_REGION, ADMIN_EMAIL, SNS_TOPIC_NAME
except ImportError:
    from scripts.config import AWS_REGION, ADMIN_EMAIL, SNS_TOPIC_NAME

def send_email(message, subject="AWS Automation Alert"):
    """
    Sends an email to the admin using AWS SNS.
    """
    try:
        sns_client = boto3.client('sns', region_name=AWS_REGION)

        topic_response = sns_client.create_topic(Name=SNS_TOPIC_NAME)
        topic_arn = topic_response['TopicArn']

        subscriptions = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
        is_subscribed = any(sub['Endpoint'] == ADMIN_EMAIL for sub in subscriptions.get('Subscriptions', []))

        if not is_subscribed:
            sns_client.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=ADMIN_EMAIL
            )
            print(f"\n⚠️ WARNING: An SNS subscription email was just sent to {ADMIN_EMAIL}.")
            print("The admin must click 'Confirm subscription' in that email to receive future alerts!\n")

        sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )

    except Exception as e:
        print(f"Failed to send email alert: {str(e)}")

if __name__ == "__main__":
    send_email("This is a test message from the email_alert script.")
