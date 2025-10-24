@echo off
echo Django Credit Approval System - Complete Setup and Run
echo =====================================================
echo.

echo Step 1: Installing dependencies...
pip install Django djangorestframework django-cors-headers python-decouple openpyxl pandas

echo.
echo Step 2: Running migrations...
python manage.py migrate

echo.
echo Step 3: Creating admin user...
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123') | python manage.py shell

echo.
echo Step 4: Importing data...
python ingest_data_simple.py

echo.
echo Step 5: Verifying system...
python FINAL_VERIFICATION.py

echo.
echo Setup complete! Starting server...
echo.
echo Access your application at:
echo - API Base: http://localhost:8000/
echo - Admin Panel: http://localhost:8000/admin/
echo - Username: admin
echo - Password: admin123
echo.
python manage.py runserver