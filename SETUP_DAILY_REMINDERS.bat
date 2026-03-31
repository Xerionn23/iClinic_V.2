@echo off
echo ========================================
echo iClinic Daily Appointment Reminder
echo ========================================
echo.
echo Running appointment reminder scheduler...
echo.

cd /d "C:\xampp\htdocs\iClinic_V.2"

python services\appointment_reminder_scheduler.py

echo.
echo ========================================
echo Daily reminder check completed!
echo ========================================
echo.

pause
