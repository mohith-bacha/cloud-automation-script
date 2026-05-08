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

Here is a simple explanation of the commands you can use:

### 1. Default Run (Create & Delete)
```bash
python run_automation.py
```
* **What it does:** This creates all resources (EC2, S3, Lambda), waits for a default time, and then deletes everything.

### 2. Create Specific Resources
```bash
python run_automation.py --ec2
python run_automation.py --s3
python run_automation.py --lambda-func
```
* **What it does:** Creates *only* the resource you specify (EC2, S3, or Lambda) instead of all three.

### 3. Delete Specific Resources (Targeted Deletion)
```bash
python run_automation.py --terminate-ec2 i-1234567890abcdef0
python run_automation.py --delete-s3 my-bucket-name
python run_automation.py --delete-lambda my-function-name
```
* **What it does:** Immediately deletes the specific resource you mention by its ID or Name. It doesn't create anything.
* **Handling Multiple Instances:** If you have multiple EC2 instances running and want to delete a specific one:
    * First, find the **Instance ID** of the instance you want to delete. You can find this in the AWS Console or by using the AWS CLI:
      ```bash
      aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,State.Name]" --output table
      ```
    * Then, pass that specific ID to the command:
      ```bash
      python run_automation.py --terminate-ec2 i-1234567890abcdef0
      ```
    * The script will terminate **only** that specific instance, leaving other running instances safe.

### 4. Custom Wait Times
```bash
python run_automation.py --wait 60
```
* **What it does:** Tells the script to wait for 60 seconds before deleting resources.

```bash
python run_automation.py --wait 14:07
```
* **What it does:** Tells the script to wait until exactly 2:07 PM (14:07) before deleting resources.

```bash
python run_automation.py --stop-time 14:07:30
```
* **What it does:** Tells the script to stop/delete at exactly 2:07:30 PM.

### 5. Background Scheduling
```bash
python run_automation.py --schedule 10:30
```
* **What it does:** Runs the script in the background every day at 10:30 AM.

---

## Git Commands Used

Here are the Git commands used in this project to manage the code:

```bash
# Initialize a new Git repository (only done once)
git init

# Check the status of your files
git status

# Add all changes to be committed
git add .

# Commit the changes with a message
git commit -m "Your commit message"

# Rename the branch to main
git branch -M main

# Add the remote GitHub repository
git remote add origin https://github.com/mohith-bacha/cloud-automation-script.git

# Push the changes to GitHub
git push -u origin main
```

## Logs
Detailed operational logs are automatically generated and stored locally in `logs/automation.log`. 