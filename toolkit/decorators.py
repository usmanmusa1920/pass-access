# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib import messages as flash_msg
from django.contrib.auth.decorators import login_required


def check_user_pascode_set(*args_1, **kwargs_1):
    """decorator for checking if the user has setup his/her secure passcode"""
    def decorator(view):
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.passcode.passcode_ingredient == '' or request.user.passcode.passcode_ingredient == None or request.user.passcode_hash == '' or request.user.passcode_hash == None:
                if kwargs_1['flash_for'] == 'item':
                    flash_msg.warning(request, f'You must finish setting up your account passcode, before you store any item')
                elif kwargs_1['flash_for'] == 'update':
                    flash_msg.warning(request, f'You have not even setup your secure passcode since you register, set it here now!')
                else:
                    flash_msg.warning(request, f'You must finish setting up your account passcode, before you store any item')
                return redirect('secureapp:set_passcode')
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
