#!/bin/bash
# ==============================================================================
# Script: run_automation.sh
# Purpose: Wrapper script to safely execute the Python AWS automation logic via cron.
# Usage instructions: 
#   1. Make script executable: chmod +x run_automation.sh
#   2. Add to crontab: crontab -e
# ==============================================================================

# Ensure we operate in the project directory regardless of where cron calls from
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${PROJECT_DIR}" || exit 1

# Define log directory and file
LOG_DIR="logs"
LOG_FILE="${LOG_DIR}/cron.log"

# Create log directory if it doesn't exist
mkdir -p "${LOG_DIR}"

# Safe python execution path discovery (prefer active venv if running manually, else system python3)
PYTHON_BIN=$(command -v python3 || command -v python)

if [ -z "${PYTHON_BIN}" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR: Python executable not found." >> "${LOG_FILE}" 2>&1
    exit 1
fi

echo "========================================" >> "${LOG_FILE}"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting AWS automation execution." >> "${LOG_FILE}"

# Execute the python script, redirecting stdout and stderr to the log file
"${PYTHON_BIN}" run_automation.py >> "${LOG_FILE}" 2>&1

# Check execution status
EXECUTION_STATUS=$?
if [ ${EXECUTION_STATUS} -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - AWS automation execution completed successfully." >> "${LOG_FILE}"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - AWS automation execution failed with exit code ${EXECUTION_STATUS}." >> "${LOG_FILE}"
fi
echo "========================================" >> "${LOG_FILE}"

exit ${EXECUTION_STATUS}
