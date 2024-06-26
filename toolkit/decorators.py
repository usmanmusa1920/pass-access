# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib import messages as flash_msg
from django.contrib.auth.decorators import login_required
from toolkit.signer import verify_token
from toolkit.utils import NextUrl


def check_user_passcode_set(**kwargs_1):
    """Decorator for checking if the user has setup his/her secure passcode"""

    def decorator(view):
        @login_required
        def wrapper(request, *args, **kwargs):
            """Decorator wrapper"""
            
            if request.user.passcode.passcode_ingredient == '' or request.user.passcode.passcode_ingredient == None or request.user.passcode_hash == '' or request.user.passcode_hash == None:
                if kwargs_1['flash_for'] == 'item':
                    flash_msg.warning(request, f'You must finish setting up your account passcode, before you store any item')
                elif kwargs_1['flash_for'] == 'update':
                    flash_msg.warning(request, f'You have not even setup your secure passcode since you register, set it here now!')
                else:
                    flash_msg.warning(request, f'You must finish setting up your account passcode, before you store any item')
                return redirect('auth:set_passcode')
            return view(request, *args, **kwargs)
        return wrapper
    return decorator


def passcode_required(view):
    """Decorator for checking if the user passcode is real"""

    @login_required
    def wrapper(request, *args, **kwargs):
        """Decorator wrapper"""
        
        next_url = NextUrl.foward(request)
        
        if request.user.passcode.auth_token != None and request.user.passcode.auth_token != '':
            # taking the user auth_token, by default it is in string including the bytes characters e.g (b'eyJhyc'), we remove the first `b`, single qoute `'` and last single qoute `'`
            u_token = request.user.passcode.auth_token[2:-1].encode('utf-8')
            verify = verify_token(u_token)
            if verify:
                # if session is not expired
                return view(request, *args, **kwargs)
        return redirect('auth:validate_passcode', next_url=next_url)
    return wrapper


def trusted_user(request):
    """Only trusted user will pass"""
    
    pass
