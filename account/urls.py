# -*- coding: utf-8 -*-
from django.urls import path
from .auth import signup, LoginCustom, validate_passcode, LogoutCustom, set_passcode
from .generate import password_generator, generated_password, strong_password
from .update import update_profile, change_password, update_passcode
from .views import landing, dashboard, about, privacy, contact_us, help_page, coming


app_name = 'auth'

urlpatterns = [
    # auth.py module path (views routes)
    path(
        'signup/', signup, name='signup'),
    path(
        'login/', LoginCustom.as_view(template_name='account/login.html'), name='login'),
    path(
        'validate/passcode/?next=/<str:next_url>/', validate_passcode, name='validate_passcode'),
    path(
        'logout/', LogoutCustom.as_view(template_name='account/logout.html'), name='logout'),
    path(
        'set/passcode/', set_passcode, name='set_passcode'),
        

    # generator.py module path (views routes)
    path(
        'password/generator/', password_generator, name='password_generator'),
    path(
        'generated/password/', generated_password, name='generated_password'),
    path(
        'strong/password/<int:pwd_id>/', strong_password, name='strong_password'),
        

    # update.py module path (views routes)
    path(
        'update/profile/', update_profile, name='update_profile'),
    path(
        'change/password/', change_password, name='change_password'),
    path(
        'update/passcode/', update_passcode, name='update_passcode'),
        

    # views.py module path (views routes)
    path(
        '', landing, name='landing'),
    path(
        'dashboard/', dashboard, name='dashboard'),
    path(
        'about/', about, name='about'),
    path(
        'privacy/', privacy, name='privacy'),
    path(
        'contact_us/', contact_us, name='contact_us'),
    path(
        'help/', help_page, name='help'),

    # coming
    path(
        'coming/<str:pg>/', coming, name='coming'),
]
