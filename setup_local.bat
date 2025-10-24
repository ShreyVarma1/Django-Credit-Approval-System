@echo off
echo Setting up Django Credit Approval System locally...
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Running Django migrations...
python manage.py migrate

echo.
echo Creating superuser (admin/admin123)...
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123') | python manage.py shell

echo.
echo Importing data from Excel files...
python ingest_data_simple.py

echo.
echo Setup complete! Starting Django server...
echo Admin panel: http://localhost:8000/admin/
echo Username: admin
echo Password: admin123
echo.
python manage.py runserver