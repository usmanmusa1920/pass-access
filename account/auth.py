# -*- coding: utf-8 -*-
from django.shortcuts import (
    render,
    redirect
)
from django.contrib.auth import get_user_model
from django.contrib import messages as flash_msg
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    login,
    logout,
    authenticate
)
from .forms import (
    SignupForm,
    AccountPassCodeForm,
    PassCodeForm_1
)
from toolkit import (
    PasscodeSecurity,
    SliceDetector,
    get_token,
    check_user_passcode_set,
    NextUrl
)
from account.default import general_context


User = get_user_model()


def login_view(request):
    """Account login view function"""
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # authenticating user
        user = authenticate(username=username, password=password)

        if user is not None:
            flash_msg.success(request, f'You are logged in!')
            login(request, user)
            return redirect('auth:dashboard')
        
        flash_msg.warning(
            request, f'Re-check your login credentials, note that both fields may be case-sensitive.')
        return redirect('auth:login')
    
    context = {
        'general_context': general_context(request),
    }
    return render(request, 'account/login.html', context)


@login_required(login_url='auth:login')
def logout_view(request):
    """Account logout function view"""
    
    logout(request)
    flash_msg.success(request, f'You just logged out!')
    return redirect('auth:login')


def signup(request):
    """Signup view"""

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            flash_msg.success(request, f'New user you are welcome!')
            return redirect('auth:login')
    else:
        form = SignupForm()

    context = {
        'form': form,
        'general_context': general_context(request),
    }
    return render(request, 'account/signup.html', context)
    

@check_user_passcode_set(flash_for='update')
def validate_passcode(request, next_url):
    """Update profile view"""
    
    # url
    next_url_convert = NextUrl.reverse(next_url)

    # site host
    host = request.headers['Host']
    
    # getting passcode
    slc = SliceDetector(request)
    slice_hash = slc._hash
    slice_ingre = slc._ingre
    slice_salt = slc._salt
    slice_iter = slc._iter
    
    if request.method == 'POST':
        # Grabbing data from html template
        old_raw_passcode = request.POST['passcode']
        
        instance = request.user
        
        # if MFA is required for the user to log in
        try:
            lucky_number = int(request.POST['lucky_number'])
            childhood_name = request.POST['childhood_name']

            if lucky_number != int(instance.passcode.lucky_number):
                flash_msg.warning(request, f'Incorrect lucky number!')
                return redirect('auth:validate_passcode', next_url=next_url)
            
            if childhood_name != instance.passcode.childhood_name:
                flash_msg.warning(request, f'Incorrect childhood name!')
                return redirect('auth:validate_passcode', next_url=next_url)
        except:
            pass

        confirm_auth = PasscodeSecurity()
        confirm_result = confirm_auth.get_hash(slice_salt, int(slice_iter), old_raw_passcode)
        confirm_passcode = confirm_result[0]
        confirm_ingredient = confirm_result[1][: -len(confirm_passcode)]
        
        # comparing the second hash (old), with the new second hash (compare one), like wise also;
        # comparing the ingredient (old), with the new ingredient (compare one),
        # both must match to what we assign to them, in other to pass to the next step
        if slice_hash != confirm_passcode or slice_ingre != confirm_ingredient:
            if instance.passcode.count_passcode_trial >= 4:
                flash_msg.warning(request, f'You tried 5 unauthorised passcode, for security reason, now MFA must be provided in other to get access!')
            else:
                flash_msg.warning(request, f'Unauthorised passcode')
            if instance.passcode.count_passcode_trial < 5:
                instance.passcode.count_passcode_trial += 1
                instance.save()
            return redirect('auth:validate_passcode', next_url=next_url)
        
        # comparing the two html fields with each other, and comparing the old ingredient with the confirm one, for the renewal
        if slice_hash == confirm_passcode and slice_ingre == confirm_ingredient:
            # if user updated his/her session age which is less than 1 or greater than secconds, it will set it back to the default one (1 minute).
            if instance.passcode.session_age < 1 or instance.passcode.session_age > 30:
                instance.passcode.session_age = 1
            instance.passcode.auth_token = get_token(instance.passcode.session_age)
            instance.passcode.count_passcode_trial = 0
            instance.save()
            flash_msg.success(request, f'Passcode Authenticated!')
            return redirect(next_url_convert)
        
    context = {
        'next_url': {
            'host': host,
            'url': next_url_convert,
            },
        'general_context': general_context(request),
    }
    return render(request, 'account/vault.html', context)


@login_required
def set_passcode(request):
    """Set user passcode view"""
    
    user_email = request.user.email
    
    # block user from setting passcode if already setted id
    if request.user.passcode.passcode_ingredient != '' and request.user.passcode.passcode_ingredient != None and request.user.passcode_hash != '' and request.user.passcode_hash != None:
        flash_msg.warning(request, f'You already setup passcode, you can change it here!')
        return redirect('auth:update_passcode')
    
    if request.method == 'POST':
        # The acc_form is not going to be use in HTML template,
        # it will be use only within this function, so that to save it (second hash i.e passcode_hash)
        # to the custome user model (UserAccount)
        acc_form = AccountPassCodeForm(request.POST, instance=request.user)
        pass_form = PassCodeForm_1(request.POST, instance=request.user.passcode)
        
        if pass_form.is_valid() and acc_form.is_valid():
            # getting data from HTML template, only for pass_form
            verify_user_email = pass_form.cleaned_data.get('verify_email')
            verify_new_passcode = pass_form.cleaned_data.get('verify_passcode')
            verify_new_passcode_again = pass_form.cleaned_data.get('passcode_ingredient')
            lucky_number = int(request.POST['lucky_number'])
            childhood_name = request.POST['childhood_name']
            
            # authenticating email address
            if verify_user_email != user_email:
                flash_msg.warning(
                    request, f'Email address you enter didn`t match with your account email address')
                pass_form = PassCodeForm_1(instance=request.user.passcode)
                return render(request, 'account/set_passcode.html', {'pass_form': pass_form})
            
            # length Validation of the two fields
            if len(verify_new_passcode) < 8 or len(verify_new_passcode_again) < 8:
                flash_msg.warning(request, f'Your passcode length must be at least 8 character')
                pass_form = PassCodeForm_1(instance=request.user.passcode)
                return render(request, 'account/set_passcode.html', {'pass_form': pass_form})
            
            # Validating the two fields
            if verify_new_passcode != verify_new_passcode_again:
                flash_msg.warning(request, f'The two passcode field mis-match, try again')
                pass_form = PassCodeForm_1(instance=request.user.passcode)
                return render(request, 'account/set_passcode.html', {'pass_form': pass_form})
            
            # authenticating lucky number length
            if lucky_number > 100 or lucky_number < 1:
                flash_msg.warning(
                    request, f'lucky number must be between `1 - 100`')
                pass_form = PassCodeForm_1(instance=request.user.passcode)
                return render(request, 'account/set_passcode.html', {'pass_form': pass_form})
            
            # committing the two forms save method to false
            instance_1 = pass_form.save(commit=False)
            instance_2 = acc_form.save(commit=False)
            
            # invoking the PasscodeSecurity class
            auth_pass = PasscodeSecurity()
            salt_q = auth_pass.passcode_salt  # salt of the passcode
            iter_q = auth_pass.passcode_iteration  # iteration of the passcode
            
            # the key of the passcode
            auth_result = auth_pass.get_hash(salt_q, iter_q, verify_new_passcode_again)

            # second hash after been encoded using base64
            hashed_passcode = auth_result[0]

            # the ingredient of the hash (salt + iteration + second_hash) respectively
            pass_ingredient = auth_result[1]
            
            # assigning instances value
            instance_1.passcode_ingredient = pass_ingredient
            instance_1.lucky_number = lucky_number
            instance_1.childhood_name = childhood_name
            instance_2.passcode_hash = hashed_passcode
            
            # saving the instances
            instance_1.save()
            instance_2.save()
            flash_msg.success(request, f'Your master passcode is set just now!')
            return redirect('auth:landing')
    else:
        pass_form = PassCodeForm_1(instance=request.user.passcode)
        
    context = {
        'pass_form': pass_form,
        'monitor_passcode.session_age': True,
        'general_context': general_context(request),
    }
    return render(request, 'account/set_passcode.html', context)
