# -*- coding: utf-8 -*-
import random
import secrets
from django.shortcuts import (
    render,
    redirect
)
from django.contrib.auth import get_user_model
from django.contrib import messages as flash_msg
from .models import PasswordGenerator
from account.default import general_context
from toolkit import (
    PasscodeSecurity,
    passcode_required
)


User = get_user_model()


@passcode_required
def password_generator(request):
    """Password generator view"""

    if request.method == 'POST':
        pwd_length = int(request.POST['pwd_length'])

        if pwd_length < 32 or pwd_length > 1000:
            flash_msg.warning(request, f'Minimum length is 32 and a maximum of 1000')
            return redirect('auth:password_generator')
        # pwd_value = secrets.token_hex(pwd_length)[:pwd_length]

        # initially our `PasscodeSecurity().token_generate` has max length of 124
        # now we times it by 9 `124*9` which will give us total of `1116`
        # since our max value of strong password is 1000
        p_token = PasscodeSecurity().token_generate * 9
        p_token_list = list(p_token)
        random.shuffle(p_token_list) # shuffling the above list
        p_token_generate = ''.join(p_token_list)

        pwd_value = p_token_generate[:pwd_length]

        context = {
            'pwd_value': pwd_value,
            'general_context': general_context(request),
        }
        return render(request, 'account/generated_password.html', context)
    
    context = {
        'general_context': general_context(request),
    }
    return render(request, 'account/password_generator.html', context)


@passcode_required
def generated_password(request):
    """Generated password view"""

    if request.method == 'POST':
        pwd_label = request.POST['label']

        if PasswordGenerator.objects.filter(label=pwd_label).first():
            flash_msg.warning(request, f'You already have password with this label `{pwd_label}`')
            return redirect('auth:password_generator')
        
        new_gen_pwd = PasswordGenerator(
            owner=request.user, label=pwd_label, generated_password=request.POST['pwd_value'])
        new_gen_pwd.save()

        flash_msg.success(request, f'Your generated password successfully saved!')
        return redirect('auth:strong_password', pwd_id=new_gen_pwd.id)
    return redirect('auth:password_generator')


@passcode_required
def strong_password(request, pwd_id):
    """Generated password page"""
    
    my_pwd = PasswordGenerator.objects.filter(owner=request.user, id=pwd_id).first()

    context = {
        'my_pwd': my_pwd,
        'general_context': general_context(request),
    }
    return render(request, 'account/strong_password.html', context)
