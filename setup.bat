@echo off
echo Setting up Django Portfolio Project...
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
echo.

echo Step 2: Creating migrations...
python manage.py makemigrations
echo.

echo Step 3: Applying migrations...
python manage.py migrate
echo.

echo Step 4: Creating superuser (optional)...
echo You can skip this by pressing Ctrl+C
python manage.py createsuperuser
echo.

echo Step 5: Creating sample data for portfolio and blog...
python manage.py create_all_sample_data
echo.

echo Setup complete!
echo You can now run the server with: python manage.py runserver

