from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages as flash_msg
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from .forms import (PasswordChangeForm, SignupForm, UpdateForm)
from toolkit import (
    PasscodeSecurity, SliceDetector, get_token, passcode_required, check_user_passcode_set, NextUrl
)


User = get_user_model()
THIS_YEARE = datetime.today().year


class LoginCustom(LoginView):
    """account login class"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            'the_year': THIS_YEARE, # include current year
            **(self.extra_context or {})
        })
        return context
    

class LogoutCustom(LoginRequiredMixin, LogoutView):
    """account logout class"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            'site': current_site,
            'site_name': current_site.name,
            'the_year': THIS_YEARE, # include current year
            # 'title': _('Logged out'),
            **(self.extra_context or {})
        })
        return context
    

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
            return redirect(reverse('secureapp:landing'))
        else:
            context = {
                'form': form,
                'the_year': THIS_YEARE,
            }
            return render(request, 'account/change_password.html', context)
    return False


def signup(request):
    """signup view"""
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
        'the_year': THIS_YEARE,
    }
    return render(request, 'account/signup.html', context)


@passcode_required
def update_profile(request):
    """update profile view"""
    
    # storing user dob
    dob = request.user.date_of_birth
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            new_session_age = form.cleaned_data.get('session_age')
            # if user updated his/her session age which is les than 60 sec, it will set it back to the default one (60 seconds)
            if new_session_age < 60 or new_session_age > 1800:
                flash_msg.warning(request, f'Session must not be less than 60 or greater than 1800 seconds!')
                return redirect('auth:update_profile')
            instance.auth_token = get_token(new_session_age)
            if form.cleaned_data.get('date_of_birth') == None or form.cleaned_data.get('date_of_birth') == '':
                instance.date_of_birth = dob
            instance.save()
            flash_msg.success(request, f'Your profile is updated!')
            return redirect('secureapp:landing')
    else:
        form = UpdateForm(instance=request.user)
    context = {
        'form': form,
        'the_year': THIS_YEARE,
    }
    return render(request, 'account/update_profile.html', context)


@check_user_passcode_set(flash_for='update')
def validate_passcode(request, next_url):
    """update profile view"""
    
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
        # """Grabbing data from html template"""
        old_raw_passcode = request.POST['passcode']
        
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
            flash_msg.warning(request, f'Unauthorised passcode')
            return redirect('auth:validate_passcode', next_url=next_url)
        
        # """
        # comparing the two html fields with each other, and comparing the old ingredient with the confirm one, for the renewal
        # """
        if slice_hash == confirm_passcode and slice_ingre == confirm_ingredient:
            # if user updated his/her session age which is less than 60 or greater than secconds, it will set it back to the default one (60 seconds).
            ru = request.user
            if ru.session_age < 60 or ru.session_age > 1800:
                ru.session_age = 60
            ru.auth_token = get_token()
            ru.save()
            flash_msg.success(request, f'Passcode Authenticated!')
            return redirect(next_url_convert)
    context = {
        'next_url': {
            'host': host,
            'url': next_url_convert,
            },
        'the_year': THIS_YEARE,
    }
    return render(request, 'account/vault.html', context)
