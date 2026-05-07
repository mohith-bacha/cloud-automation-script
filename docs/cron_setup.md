# Cron Job Setup Guide

## What is Cron?
Cron is a time-based job scheduler in Unix-like operating systems. It enables users to schedule jobs (commands or scripts) to run periodically at fixed times, dates, or intervals.

## Why use Cron in Automation?
Cron is crucial in automation because it allows scripts (like our AWS provisioning or reporting tasks) to execute autonomously without human intervention. This ensures consistency, reduces manual toil, and ensures tasks run accurately on schedule.

## Making the Script Executable
Before cron can run the shell script, it must have executable permissions.
Run the following command in the project root:
```bash
chmod +x run_automation.sh
```

## Example Cron Commands
You can edit your cron jobs using the command:
```bash
crontab -e
```

Here are some example schedules for `run_automation.sh`:

- **Every 5 minutes:**
  ```cron
  */5 * * * * /path/to/project/run_automation.sh
  ```
- **Every day at 9 AM:**
  ```cron
  0 9 * * * /path/to/project/run_automation.sh
  ```
- **Every midnight:**
  ```cron
  0 0 * * * /path/to/project/run_automation.sh
  ```
*(Note: Replace `/path/to/project` with the actual absolute path to this project directory.)*

## How to Verify Cron Jobs
To list all active cron jobs for the current user, run:
```bash
crontab -l
```

## Checking Cron Logs
The wrapper script automatically manages its own output logs. You can inspect the logs to verify successful runs or identify issues:
```bash
cat logs/cron.log
# Or follow logs in real-time:
tail -f logs/cron.log
```

## Troubleshooting Steps
1. **Script Permissions:** Ensure `chmod +x run_automation.sh` was run.
2. **Absolute Paths:** Cron executes in a restricted environment. Ensure you use the absolute path to `run_automation.sh` in the crontab.
3. **Environment Variables:** Cron may not have access to your `.bashrc` environment variables. If your python script requires AWS credentials, configure them for the user running the cron job (e.g., using `aws configure` for that user), or pass them explicitly.
4. **Log Analysis:** Check `logs/cron.log` for any captured stderr messages from Python.
