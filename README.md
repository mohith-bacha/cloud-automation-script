# AWS Cloud Automation Orchestrator

## Overview
This project is a comprehensive, production-ready AWS automation suite built with Python and `boto3`. It automates the provisioning, lifecycle management, and clean-up of AWS resources including **EC2 instances, S3 buckets, and Lambda functions**. 

It is designed with DevOps best practices in mind, featuring targeted tear-downs, custom wait intervals, automated SNS email alerting, extensive logging, and dynamic background scheduling.

## Features
- **Multi-Resource Provisioning:** Dynamically provisions EC2, S3, and Lambda functions with randomized, unique identifiers.
- **Targeted Cleanup:** Cleanly deletes specific individual resources by ID/Name, or tears down the entire stack automatically.
- **Dynamic Scheduling:** Run the automation seamlessly in the background at custom-defined times using built-in Python scheduling.
- **Linux Cron Support:** Fully integrated wrapper scripts (`run_automation.sh`) for seamless deployment on remote Linux servers using cron.
- **Automated SNS Alerts:** Automatically detects success or failure across the lifecycle and dispatches structured email reports to the administrator.
- **Robust Logging:** Maintains continuous operational logs stored locally in the `logs/automation.log` directory.

## File Structure
- **`run_automation.py`** - The primary orchestrator script. Handles CLI arguments, triggers provisioning modules, controls sleep intervals, and manages scheduling.
- **`run_automation.sh`** - A safe bash wrapper script designed for executing the automation inside a restricted Linux cron environment.
- **`scripts/config.py`** - Centralized configuration variables (Region, AMI IDs, IAM Roles, Admin Email).
- **`scripts/email_alert.py`** - Handles AWS SNS integrations for administrator notifications.
- **`scripts/logger.py`** - Dual-stream logging setup (outputs to terminal and writes to file).
- **`scripts/ec2/`**, **`scripts/s3/`**, & **`scripts/aws_lambda/`** - Modular Python sub-packages isolating the `boto3` creation and deletion logic for their respective AWS resources.
- **`docs/cron_setup.md`** - Comprehensive instructions on deploying the project in a Linux scheduled environment.

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your AWS credentials are appropriately configured:
```bash
aws configure
```

3. Update the required IAM Role ARNs and email endpoints inside `scripts/config.py` before running.

## Usage Guide

### Standard Execution
Run the full provisioning lifecycle (Create all resources -> Wait -> Delete all):
```bash
python run_automation.py
```

### Target Specific Resource Creation
If you only want to provision a specific service (instead of all three), you can use targeted flags:
```bash
python run_automation.py --ec2
python run_automation.py --s3
python run_automation.py --lambda-func
```

### Custom Wait Times
You can override the default sleep interval by providing a number of seconds, OR provide a specific clock time to calculate exactly when to execute the deletion step:
```bash
# Wait for 60 seconds before deleting
python run_automation.py --wait 60

# Wait until exactly 2:07 PM (14:07) before deleting
python run_automation.py --wait 14:07

# You can also use --stop-time and specify seconds (HH:MM:SS)
python run_automation.py --stop-time 14:07:30
```

### Targeted Deletion
Bypass creation entirely and immediately destroy specific existing resources:
```bash
python run_automation.py --terminate-ec2 i-1234567890abcdef0
python run_automation.py --delete-s3 my-bucket-name
python run_automation.py --delete-lambda my-function-name
```

### Background Scheduling
Instruct the script to run continuously in the background and execute at a specific clock time every day:
```bash
# Start every day at 11:00 AM (default)
python run_automation.py --schedule

# Start every day at 10:30 AM
python run_automation.py --schedule 10:30

# You can also use --start-time with seconds
python run_automation.py --start-time 14:00:00 --wait 1800

# Advanced Combo: Start every day at 2:05 PM (14:05), and trigger cleanup exactly at 2:07 PM (14:07)
python run_automation.py --schedule 14:05 --wait 14:07
```

## Logs
Detailed operational logs are automatically generated and stored locally in `logs/automation.log`. 