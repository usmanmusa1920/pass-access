from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages as flash_msg
from django.contrib.auth.decorators import login_required
from toolkit import passcode_required
from .default import default


User = get_user_model()


def landing(request):
    """landing page view"""
    if request.user.is_authenticated:
        return redirect('auth:dashboard')
    context = {
        'default': default(request),
    }
    return render(request, 'account/landing.html', context)


@passcode_required
def dashboard(request):
    """dashboard page view"""
    context = {
        'default': default(request),
    }
    return render(request, 'account/dashboard.html', context)


def about(request):
    """about page view"""
    context = {
        'default': default(request),
    }
    return render(request, 'account/about.html', context)


def privacy(request):
    """privacy page view"""
    context = {
        'default': default(request),
    }
    return render(request, 'account/privacy.html', context)


def contact_us(request):
    """cantact page view"""
    context = {
        'default': default(request),
    }
    return render(request, 'account/contact_us.html', context)


def help_page(request):
    """help page view"""
    context = {
        'default': default(request),
    }
    return render(request, 'account/help.html', context)
