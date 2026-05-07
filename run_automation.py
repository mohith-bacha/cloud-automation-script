import sys
import os
import argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

import time
from scripts.config import WAIT_TIME_SECONDS
from scripts.create_ec2 import create_ec2
from scripts.delete_ec2 import delete_ec2
from scripts.create_s3 import create_s3
from scripts.delete_s3 import delete_s3
from scripts.create_lambda import create_lambda
from scripts.delete_lambda import delete_lambda
from scripts.logger import setup_logger
from scripts.email_alert import send_email

def main():
    parser = argparse.ArgumentParser(description="AWS Automation Script")
    parser.add_argument('--ec2', action='store_true', help='Create and delete EC2 instance')
    parser.add_argument('--s3', action='store_true', help='Create and delete S3 bucket')
    parser.add_argument('--lambda-func', dest='lambda_func', action='store_true', help='Create and delete Lambda function')
    
    # New options for specific deletions and wait time
    parser.add_argument('--terminate-ec2', dest='term_ec2', help='Terminate a specific EC2 instance by ID')
    parser.add_argument('--delete-s3', dest='del_s3', help='Delete a specific S3 bucket by Name')
    parser.add_argument('--delete-lambda', dest='del_lambda', help='Delete a specific Lambda function by Name')
    parser.add_argument('--wait', help='Override the wait time in seconds (e.g. 60) or specify a specific end time (e.g. 11:20)')
    
    args = parser.parse_args()
    
    # Default to running everything if no flags are provided
    run_all = not (args.ec2 or args.s3 or args.lambda_func)
    run_ec2 = args.ec2 or run_all
    run_s3 = args.s3 or run_all
    run_lambda = args.lambda_func or run_all

    logger = setup_logger()
    logger.info("Starting AWS Automation...")
    
    # Direct deletion path
    if args.term_ec2 or args.del_s3 or args.del_lambda:
        logger.info("Executing specific targeted deletions...")
        if args.term_ec2:
            res = delete_ec2(args.term_ec2)
            logger.info(f"EC2 Deletion Result: {res or 'Success'}")
        if args.del_s3:
            res = delete_s3(args.del_s3)
            logger.info(f"S3 Deletion Result: {res or 'Success'}")
        if args.del_lambda:
            res = delete_lambda(args.del_lambda)
            logger.info(f"Lambda Deletion Result: {res or 'Success'}")
        return
    
    errors = []
    successes = []
    
    # 1. Create resources
    success_ec2 = False
    success_s3 = False
    success_lambda = False
    
    if run_ec2:
        success_ec2, res_ec2 = create_ec2()
        if success_ec2:
            successes.append(f"✅ EC2 Instance Created: {res_ec2}")
        else:
            errors.append(res_ec2)
            
    if run_s3:
        success_s3, res_s3 = create_s3()
        if success_s3:
            successes.append(f"✅ S3 Bucket Created: {res_s3}")
        else:
            errors.append(res_s3)
            
    if run_lambda:
        success_lambda, res_lambda = create_lambda()
        if success_lambda:
            successes.append(f"✅ Lambda Function Created: {res_lambda}")
        else:
            errors.append(res_lambda)
            
    # Send success email if any succeeded
    if successes:
        logger.info("Sending success email alert to admin...")
        success_msg = "PROVISIONING SUCCESS!\n\nHere are the details of the resources created:\n\n" + "\n".join(successes)
        send_email(success_msg, subject="AWS Automation Alert - Provisioning Success")
    
    # Send failure email if anything failed
    if errors:
        combined_error_message = "PROVISIONING ERRORS:\n\n" + "\n\n".join(errors)
        logger.info("Sending error email alert to admin...")
        send_email(combined_error_message, subject="AWS Automation Alert - Execution Error")
    
    if not successes:
        logger.info("No successful creations to clean up. Exiting.")
        return

    # 2. Wait
    wait_time = WAIT_TIME_SECONDS
    if args.wait:
        if ":" in args.wait:
            from datetime import datetime
            now = datetime.now()
            target_time = datetime.strptime(args.wait, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            if target_time < now:
                import datetime as dt
                target_time = target_time + dt.timedelta(days=1)
            wait_time = int((target_time - now).total_seconds())
        else:
            wait_time = int(args.wait)
            
    logger.info(f"Waiting {wait_time} seconds...")
    time.sleep(wait_time)
    
    # 3. Delete resources
    delete_errors = []
    delete_successes = []
    
    if run_ec2 and success_ec2:
        res_del_ec2 = delete_ec2(res_ec2)
        if res_del_ec2 and "Error" in res_del_ec2:
            delete_errors.append(res_del_ec2)
        else:
            delete_successes.append(f"✅ EC2 instance {res_ec2} cleaned up")
            
    if run_s3 and success_s3:
        res_del_s3 = delete_s3(res_s3)
        if res_del_s3 and "Error" in res_del_s3:
            delete_errors.append(res_del_s3)
        else:
            delete_successes.append(f"✅ S3 bucket {res_s3} cleaned up.")
            
    if run_lambda and success_lambda:
        res_del_lambda = delete_lambda(res_lambda)
        if res_del_lambda and "Error" in res_del_lambda:
            delete_errors.append(res_del_lambda)
        else:
            delete_successes.append(f"✅ Lambda function {res_lambda} cleaned up.")
    
    logger.info("Completed AWS Automation Cleanup")
    
    # 4. Send combined email if any errors occurred during deletion
    if delete_errors:
        combined_error_message = "CLEANUP ERRORS:\n\n" + "\n\n".join(delete_errors)
        logger.info("Sending combined error email alert to admin...")
        send_email(combined_error_message, subject="AWS Automation Alert - Cleanup Error")
        
    if delete_successes:
        success_msg = "CLEANUP SUCCESS!\n\nHere are the details of the resources that were successfully deleted:\n\n" + "\n".join(delete_successes)
        logger.info("Sending cleanup success email alert to admin...")
        send_email(success_msg, subject="AWS Automation Alert - Cleanup Success")

if __name__ == "__main__":
    if "--schedule" in sys.argv:
        try:
            import schedule
        except ImportError:
            print("Please install the 'schedule' library first: pip install schedule")
            sys.exit(1)
            
        schedule_index = sys.argv.index("--schedule")
        schedule_time = "11:00" # default
        
        # Check if the user provided a time after --schedule (like --schedule 10:33)
        if len(sys.argv) > schedule_index + 1 and not sys.argv[schedule_index + 1].startswith("--"):
            schedule_time = sys.argv[schedule_index + 1]
            sys.argv.pop(schedule_index + 1) # remove the time string so argparse doesn't crash
            
        # Remove --schedule from sys.argv
        sys.argv.remove("--schedule")
            
        print(f"Scheduler started. The automation will run every day at {schedule_time}.")
        print("Keep this terminal open to run in the background.")
        
        schedule.every().day.at(schedule_time).do(main)
        
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        main()
