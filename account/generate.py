# -*- coding: utf-8 -*-
import secrets
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages as flash_msg
from .models import PasswordGenerator
from toolkit import passcode_required


User = get_user_model()
THIS_YEARE = datetime.today().year


@passcode_required
def password_generator(request):
    """password generator view"""
    if request.method == 'POST':
        pwd_length = int(request.POST['pwd_length'])
        if pwd_length < 32 or pwd_length > 1000:
            flash_msg.warning(request, f'Minimum length is 32 and a maximum of 1000')
            return redirect('auth:password_generator')
        pwd_value = secrets.token_hex(pwd_length)
        context = {
            'pwd_value': pwd_value,
            'the_year': THIS_YEARE,
            'monitor_session_age': True,
        }
        return render(request, 'account/generated_password.html', context)
    context = {
        'the_year': THIS_YEARE,
        'monitor_session_age': True,
    }
    return render(request, 'account/password_generator.html', context)


@passcode_required
def generated_password(request):
    """generated password view"""
    if request.method == 'POST':
        pwd_label = request.POST['label']
        if PasswordGenerator.objects.filter(label=pwd_label).first():
            flash_msg.warning(request, f'You already have password with this label `{pwd_label}`')
            return redirect('auth:password_generator')
        new_gen_pwd = PasswordGenerator(
            owner=request.user, label=pwd_label, generated_password=request.POST['pwd_value'])
        new_gen_pwd.save()
        flash_msg.success(request, f'Your generated password successfully saved!')
    return redirect('auth:password_generator')
