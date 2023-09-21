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
from secureapp.models import Category, Platform

User = get_user_model()


user_no_1 = User.objects.create_superuser(
    first_name='Usman', last_name='Musa', username='usmanmusa1920', email='usmanmusa1920@gmail.com', phone_number='+2348123456789', password='passwd123')
user_no_2 = User.objects.create_user(
    first_name='Aliyu', last_name='Muhammad', username='aliyumuhammad', email='aliyumuhammad@gmail.com', phone_number='+2348123456789', password='passwd123')
user_no_3 = User.objects.create_user(
    first_name='Fatima', last_name='Sani', username='fatimasani', email='fatimasani@gmail.com', phone_number='+2348123456789', password='passwd123')
user_no_4 = User.objects.create_user(
    first_name='Ahmad', last_name='Amiun', username='ahmadaminu', email='ahmadaminu@gmail.com', phone_number='+2348123456789', password='passwd123')
user_no_5 = User.objects.create_user(
    first_name='John', last_name='Christain', username='johnchristain', email='johnchristain@gmail.com', phone_number='+2348123456789', password='passwd123')
user_no_6 = User.objects.create_user(
    first_name='Nura', last_name='Ali', username='nuraali', email='nuraali@gmail.com', phone_number='+2348123456789', password='passwd123')
user_no_7 = User.objects.create_user(
    first_name='Zainab', last_name='Musa', username='zainabmusa', email='zainabmusa@gmail.com', phone_number='+2348123456789', password='passwd123')
user_no_8 = User.objects.create_user(
    first_name='Adamu', last_name='Musa', username='adamunmusa', email='adamunmusa@gmail.com', phone_number='+2348123456789', password='passwd123')
user_no_9 = User.objects.create_user(
    first_name='Maryam', last_name='Yusuf', username='maryamyusuf', email='maryamyusuf@gmail.com', phone_number='+2348123456789', password='passwd123')
user_no_10 = User.objects.create_user(
    first_name='Joshua', last_name='Andy', username='joshuaandy', email='joshuaandy@gmail.com', phone_number='+2348123456789', password='passwd123')
user_no_1.save()
user_no_2.save()
user_no_3.save()
user_no_4.save()
user_no_5.save()
user_no_6.save()
user_no_7.save()
user_no_8.save()
user_no_9.save()
user_no_10.save()


cat_1 = Category(category_key='Social media', category_value='social media')
cat_2 = Category(category_key='Cloud', category_value='cloud')
cat_3 = Category(category_key='Card', category_value='card')
cat_4 = Category(category_key='Other', category_value='other')
cat_1.save()
cat_2.save()
cat_3.save()
cat_4.save()


plat_1 = Platform(category=cat_1, platform_key='Facebook', platform_value='facebook')
plat_2 = Platform(category=cat_1, platform_key='Twitter', platform_value='twitter')
plat_3 = Platform(category=cat_1, platform_key='Instagram', platform_value='instagram')
plat_4 = Platform(category=cat_1, platform_key='LinkedIn', platform_value='linkedin')
plat_5 = Platform(category=cat_2, platform_key='Linode', platform_value='linode')
plat_6 = Platform(category=cat_2, platform_key='AWS', platform_value='aws')
plat_7 = Platform(category=cat_2, platform_key='Heroku', platform_value='heroku')
plat_8 = Platform(category=cat_2, platform_key='Digital ocean', platform_value='digital ocean')
plat_9 = Platform(category=cat_2, platform_key='Github', platform_value='github')
plat_10 = Platform(category=cat_2, platform_key='Docker', platform_value='docker')
plat_11 = Platform(category=cat_2, platform_key='Gitlab', platform_value='gitlab')
plat_12 = Platform(category=cat_2, platform_key='Namecheap', platform_value='namecheap')
plat_13 = Platform(category=cat_2, platform_key='Bitbucket', platform_value='bitbucket')
plat_14 = Platform(category=cat_4, platform_key='Gmail', platform_value='gmail')
plat_15 = Platform(category=cat_4, platform_key='ChatGPT', platform_value='chatgpt')
plat_16 = Platform(category=cat_2, platform_key='Azure', platform_value='azure')
plat_17 = Platform(category=cat_1, platform_key='Qiskit api', platform_value='qiskit api')
plat_18 = Platform(category=cat_2, platform_key='Hostinger', platform_value='hostinger')
plat_19 = Platform(category=cat_3, platform_key='Bank card', platform_value='bank card')
plat_20 = Platform(category=cat_1, platform_key='Snapchat', platform_value='snapchat')
plat_21 = Platform(category=cat_3, platform_key='Visa card', platform_value='visa card')
plat_22 = Platform(category=cat_3, platform_key='ID card', platform_value='id card')
plat_23 = Platform(category=cat_3, platform_key='Store id', platform_value='store id')
plat_24 = Platform(category=cat_3, platform_key='Credit card', platform_value='credit card')
plat_1.save()
plat_2.save()
plat_3.save()
plat_4.save()
plat_5.save()
plat_6.save()
plat_7.save()
plat_8.save()
plat_9.save()
plat_10.save()
plat_11.save()
plat_12.save()
plat_13.save()
plat_14.save()
plat_15.save()
plat_16.save()
plat_17.save()
plat_18.save()
plat_19.save()
plat_20.save()
plat_21.save()
plat_22.save()
plat_23.save()
plat_24.save()


exit()
rm dump.json
python manage.py dumpdata --format json --indent 4 > dump.json
# python manage.py loaddata dump.json
python manage.py runserver
