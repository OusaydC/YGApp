@echo off
echo ======================================
echo MOROCCO YIELD GAP - DATA UPDATE
echo ======================================
echo.

echo This script will reload data from Excel files.
echo.
echo IMPORTANT: Make sure you have:
echo 1. Updated plot_v_p.xlsx with new data
echo 2. Kept the same column structure
echo 3. Added data for years 2019-2025 if available
echo.

pause

echo.
echo Clearing old data and loading new data...
python manage.py load_real_data

echo.
echo ======================================
echo DATA UPDATE COMPLETE!
echo ======================================
echo.
echo You can now run the server with: python manage.py runserver
echo Or use RUN.bat
echo.
pause


