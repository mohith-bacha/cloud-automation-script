# AWS Cloud Automation Project

## Overview
This project automates AWS EC2 provisioning and deletion using Python and Bash scripting.

## Features
- EC2 instance creation
- EC2 termination
- Logging and error handling
- Scheduled automation using cron
- Git version control

## Technologies
- Python (boto3)
- AWS CLI
- Bash scripting
- Cron jobs

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Configure AWS:
   aws configure

3. Run:
   bash bash/run_automation.sh

## Logs
logs/automation.log

## Output
output/sample_output.txt

## Automated Scheduling Using Cron

To schedule the execution of this project, you can use Linux cron. We provide a shell wrapper (`run_automation.sh`) that safely sets up the environment, executes the Python script, and logs output.

**Make the script executable:**
```bash
chmod +x run_automation.sh
```

**Example Cron Schedules (using `crontab -e`):**

- **Every 5 minutes:**
  ```cron
  */5 * * * * /path/to/your/project/run_automation.sh
  ```
- **Every day at 9 AM:**
  ```cron
  0 9 * * * /path/to/your/project/run_automation.sh
  ```
- **Every midnight:**
  ```cron
  0 0 * * * /path/to/your/project/run_automation.sh
  ```

For more detailed information, troubleshooting, and best practices, see [docs/cron_setup.md](docs/cron_setup.md).