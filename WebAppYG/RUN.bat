@echo off
echo Creating database migrations...
python manage.py makemigrations

echo.
echo Applying migrations...
python manage.py migrate

echo.
echo Loading real data from Excel...
python manage.py load_real_data

echo.
echo Starting server...
python manage.py runserver

