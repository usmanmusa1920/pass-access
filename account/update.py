# -*- coding: utf-8 -*-
from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages as flash_msg
from django.contrib.auth import update_session_auth_hash
from .forms import (
    PassCodeForm_1, PassCodeForm_2, AccountPassCodeForm, PasswordChangeForm, UpdateForm
)
from toolkit import (
    PasscodeSecurity, SliceDetector, get_token, passcode_required, check_user_passcode_set
)


User = get_user_model()
THIS_YEARE = datetime.today().year


@passcode_required
def update_profile(request):
    """update profile view"""
    
    # storing user dob
    dob = request.user.date_of_birth
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=request.user)
        form_2 = PassCodeForm_2(request.POST, instance=request.user.passcode)
        if form.is_valid() and form_2.is_valid():
            instance = form.save(commit=False)
            instance_2 = form_2.save(commit=False)
            new_session_age = int(form_2.cleaned_data.get('session_age'))
            monitor_session_age = form_2.cleaned_data['monitor_session_age']

            # authenticating user passcode session age
            if new_session_age < 1 or new_session_age > 30:
                flash_msg.warning(request, f'Session must not be less than 1 or greater than 30 minutes!')
                return redirect('auth:update_profile')
            
            instance.passcode.auth_token = get_token(new_session_age)
            if form.cleaned_data.get('date_of_birth') == None or form.cleaned_data.get('date_of_birth') == '':
                instance.date_of_birth = dob
            if monitor_session_age == True:
                instance.passcode.monitor_session_age = True
            else:
                instance.passcode.monitor_session_age = False
            instance.passcode.session_age = new_session_age
            instance.save()
            instance_2.save()
            flash_msg.success(request, f'Your profile is updated!')
            return redirect('auth:landing')
    else:
        form = UpdateForm(instance=request.user)
    context = {
        'form': form,
        'the_year': THIS_YEARE,
        'monitor_session_age': True,
    }
    return render(request, 'account/update_profile.html', context)


@passcode_required
def change_password(request):
    """change account password view"""
    if request.user.is_authenticated:
        form = PasswordChangeForm(user=request.user, data=request.POST or None)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            flash_msg.success(
                request, f'That sound great {request.user.first_name}, your password has been changed')
            return redirect(reverse('auth:landing'))
        else:
            context = {
                'form': form,
                'the_year': THIS_YEARE,
                'monitor_session_age': True,
            }
            return render(request, 'account/change_password.html', context)
    return False


@check_user_passcode_set(flash_for='update')
@passcode_required
def update_passcode(request):
    """function for updating user passcode"""
    
    user_email = request.user.email
    
    # getting passcode
    slc = SliceDetector(request)
    slice_hash = slc._hash
    slice_ingre = slc._ingre
    slice_salt = slc._salt
    slice_iter = slc._iter
    
    if request.method == 'POST':
        # """
        # The acc_form is not going to be use in HTML template,
        # it will be use only within this function, so that to renew (second hash i.e passcode_hash) in the custome user model (UserAccount)
        # """
        acc_form = AccountPassCodeForm(request.POST, instance=request.user)
        pass_form = PassCodeForm_1(request.POST, instance=request.user.passcode)
        
        if pass_form.is_valid() and acc_form.is_valid():
            # """Grabbing data from html template"""
            verify_user_email = pass_form.cleaned_data.get('verify_email')
            old_raw_passcode = pass_form.cleaned_data.get('old_passcode')
            # old_raw_passcode = request.POST['old_passcode']
            new_raw_passcode = pass_form.cleaned_data.get('passcode_ingredient')
            verify_new_passcode = pass_form.cleaned_data.get('verify_passcode')
            
            # """authenticating email address"""
            if verify_user_email != user_email:
                flash_msg.warning(
                    request, f'Email address you enter didn`t match with your account email address')
                pass_form = PassCodeForm_1(instance=request.user.passcode)
                return render(request, 'account/update_passcode.html', {'pass_form': pass_form})
            
            # """length Validation of the three fields"""
            if len(old_raw_passcode) < 8 or len(new_raw_passcode) < 8 or len(verify_new_passcode) < 8:
                flash_msg.warning(request, f'Your passcode length must be at least 8 character')
                pass_form = PassCodeForm_1(instance=request.user.passcode)
                return render(request, 'account/update_passcode.html', {'pass_form': pass_form})
            
            # """
            # The below confirm_* is use to authenticate the old passcode that a user claim (old_raw_passcode),
            # and compare it with the one he/she want to change it (the one he/she is using, i.e `slice_ingre`).
            # """
            confirm_auth = PasscodeSecurity()
            confirm_result = confirm_auth.get_hash(slice_salt, int(slice_iter), old_raw_passcode)
            confirm_passcode = confirm_result[0]
            confirm_ingredient = confirm_result[1][: -len(confirm_passcode)]
            
            # """
            # comparing the second hash (old), with the new second hash (compare one), like wise also;
            # comparing the ingredient (old), with the new ingredient (compare one),
            # both must match to what we assign to them, in other to pass to the next step
            # """
            if slice_hash != confirm_passcode or slice_ingre != confirm_ingredient:
                flash_msg.warning(request, f'Your old passcode is incorrect')
                pass_form = PassCodeForm_1(instance=request.user.passcode)
                return render(request, 'account/update_passcode.html', {'pass_form': pass_form})
            
            # """authenticating two fields for new passcode"""
            if verify_new_passcode != new_raw_passcode:
                flash_msg.warning(request, f'The two passcode field mis-match, try again')
                pass_form = PassCodeForm_1(instance=request.user.passcode)
                return render(request, 'account/update_passcode.html', {'pass_form': pass_form})
            
            # """
            # comparing the two html fields with each other, and comparing the old ingredient with the confirm one, for the renewal
            # """
            if verify_new_passcode == new_raw_passcode and slice_ingre == confirm_ingredient:
                """invoking the PasscodeSecurity class"""
                renew_pass = PasscodeSecurity()
                new_salt = renew_pass.passcode_salt  # salt of the renew passcode
                new_iter = renew_pass.passcode_iteration  # iteration of  the renew passcode
                
                # the key of the passcode
                pass_result = renew_pass.get_hash(new_salt, new_iter, new_raw_passcode)
                # second hash after been encode using base64
                new_passcode = pass_result[0]
                # the ingredient of the hash (salt + iteration + second_hash) respectively
                new_ingredient = pass_result[1]
                
                # """committing the two forms save method to false"""
                instance_1 = pass_form.save(commit=False)
                instance_2 = acc_form.save(commit=False)
                
                # """assigning instances value"""
                instance_1.passcode_ingredient = new_ingredient
                instance_2.passcode_hash = new_passcode
                
                # """saving instances"""
                instance_1.save()
                instance_2.save()
                
                flash_msg.success(request, f'Your passcode is updated')
                return redirect('auth:landing')
    else:
        pass_form = PassCodeForm_1(instance=request.user.passcode)
    context = {
        'pass_form': pass_form,
        'monitor_session_age': True,
    }
    return render(request, 'account/update_passcode.html', context)
