from datetime import datetime
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from .forms import (PasswordChangeForm, SignupForm, UpdateForm)


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


@login_required
def change_password(request):
    """change account password view"""
    if request.user.is_authenticated:
        form = PasswordChangeForm(user=request.user, data=request.POST or None)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, f'That sound great {request.user.first_name}, your password has been changed')
            return redirect(reverse('secureapp:home'))
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
            messages.success(request, f'New user you are welcome!')
            return redirect('auth:login')
    else:
        form = SignupForm()
    context = {
        'form': form,
        'the_year': THIS_YEARE,
    }
    return render(request, 'account/signup.html', context)


@login_required
def update_profile(request):
    """update profile view"""
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile is updated!')
            return redirect('secureapp:home')
    else:
        form = UpdateForm(instance=request.user)
    context = {
        'form': form,
        'the_year': THIS_YEARE,
    }
    return render(request, 'account/update_profile.html', context)
