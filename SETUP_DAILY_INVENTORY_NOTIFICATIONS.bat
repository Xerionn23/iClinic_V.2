@echo off
REM Setup Windows Task Scheduler for Daily Inventory Notifications
REM This script creates a scheduled task that runs every day at 8:00 AM

echo ========================================
echo iClinic Daily Inventory Notification Setup
echo ========================================
echo.

REM Get the current directory
set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%run_daily_inventory_check.py

echo Script Location: %PYTHON_SCRIPT%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Create the scheduled task
echo Creating scheduled task...
echo Task Name: iClinic_Daily_Inventory_Check
echo Schedule: Daily at 8:00 AM
echo.

schtasks /create /tn "iClinic_Daily_Inventory_Check" /tr "python \"%PYTHON_SCRIPT%\"" /sc daily /st 08:00 /f

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create scheduled task
    echo You may need to run this script as Administrator
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Scheduled task created
echo ========================================
echo.
echo Task Details:
echo - Task Name: iClinic_Daily_Inventory_Check
echo - Runs: Every day at 8:00 AM
echo - Script: %PYTHON_SCRIPT%
echo.
echo The system will automatically check inventory and send
echo email notifications to nurses every morning.
echo.
echo To view/modify the task:
echo 1. Open Task Scheduler (taskschd.msc)
echo 2. Look for "iClinic_Daily_Inventory_Check"
echo.
echo To test the task manually:
echo schtasks /run /tn "iClinic_Daily_Inventory_Check"
echo.
pause
