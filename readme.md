How to run app?

Create a virtual environment(python 2.7)
clone repo
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata --app=students demo_data.json
python manage.py runserver
login for admin - mkrbk
password - students
or create your superuser run command: python manage.py createsuperuser
in case the admin site not work - in settings.py remove line 'students.middleware.sql_log.SQLLogMiddleware', restart server,
go to admin, login and go back to settings.py paste that line again - it's work.