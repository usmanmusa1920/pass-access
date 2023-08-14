#!/bin/bash
clear && source ~/.bashrc
source venv/bin/activate

rm -rf account/__pycache__
rm -rf account/migrations/*
touch account/migrations/__init__.py

rm -rf secureapp/__pycache__
rm -rf secureapp/migrations/*
touch secureapp/migrations/__init__.py

rm db.sqlite3

python manage.py makemigrations
python manage.py migrate
python manage.py shell

from django.contrib.auth import get_user_model
User = get_user_model()


user_no_1 = User.objects.create_superuser(
    first_name='Usman', last_name='Musa', username='usmanmusa1920', email='usmanmusa1920@gmail.com', phone_number='+2348123456789', password='19991125u')
user_no_1.save()

exit()
rm dump.json
python manage.py dumpdata --format json --indent 4 > dump.json
python manage.py runserver
