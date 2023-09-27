from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages as flash_msg
from django.contrib.auth.decorators import login_required
from toolkit import passcode_required
from secureapp.models import SecureItemInfo


User = get_user_model()
THIS_YEARE = datetime.today().year


def landing(request):
    """landing page view"""
    if request.user.is_authenticated:
        return redirect('auth:dashboard')
    context = {
        'the_year': THIS_YEARE,
    }
    return render(request, 'account/landing.html', context)


@passcode_required
def dashboard(request):
    """dashboard page view"""
    user_items = SecureItemInfo.objects.filter(
        i_owner=request.user.passcode).order_by('-date_created')[:10]
    context = {
        'user_items': user_items,
        'the_year': THIS_YEARE,
        'monitor_session_age': True,
    }
    return render(request, 'account/dashboard.html', context)


def about(request):
    """about page view"""
    context = {
        'the_year': THIS_YEARE,
    }
    return render(request, 'account/about.html', context)


def privacy(request):
    """privacy page view"""
    context = {
        'the_year': THIS_YEARE,
    }
    return render(request, 'account/privacy.html', context)


def contact_us(request):
    """cantact page view"""
    context = {
        'the_year': THIS_YEARE,
    }
    return render(request, 'account/contact_us.html', context)


def help_page(request):
    """help page view"""
    context = {
        'the_year': THIS_YEARE,
    }
    return render(request, 'account/help.html', context)


@login_required
def coming(request, pg):
    """pages that are not implemented"""
    flash_msg.success(request, f'This page ({pg}) is coming soon!')
    return redirect(reverse('auth:landing'))
