@echo off
echo ========================================
echo  iClinic Healthcare Management System
echo ========================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting iClinic server...
echo Server will be available at: http://localhost:5000
echo Default login: admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo ========================================

python run.py

pause
