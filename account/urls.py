# -*- coding: utf-8 -*-
from django.urls import path
from .views import (LoginCustom, LogoutCustom, change_password, signup, update_profile, validate_passcode, password_generator, generated_password)


app_name = 'auth'

urlpatterns = [
    # login
    path(
        'login/', LoginCustom.as_view(template_name='account/login.html'), name='login'),
    # logout
    path(
        'logout/', LogoutCustom.as_view(template_name='account/logout.html'), name='logout'),
    # change password
    path(
        'change/password/', change_password, name='change_password'),
    # register new administrator
    path(
        'signup/', signup, name='signup'),
    # administrator update profile info...
    path(
        'update/profile/', update_profile, name='update_profile'),
    # validate passcode
    path(
        'validate/passcode/?next=/<str:next_url>/', validate_passcode, name='validate_passcode'),
    # password generator
    path(
        'password/generator/', password_generator, name='password_generator'),
    # generated password
    path(
        'generated/password/', generated_password, name='generated_password'),
]
