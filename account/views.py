from django.shortcuts import (
    render,
    redirect
)
from django.contrib.auth import get_user_model
from toolkit import passcode_required
from account.default import general_context


User = get_user_model()


def landing(request):
    """Landing page view"""

    if request.user.is_authenticated:
        return redirect('auth:dashboard')
    
    context = {
        'general_context': general_context(request),
    }
    return render(request, 'account/landing.html', context)


@passcode_required
def dashboard(request):
    """Dashboard page view"""

    context = {
        'general_context': general_context(request),
    }
    return render(request, 'account/dashboard.html', context)


def about(request):
    """About page view"""

    context = {
        'general_context': general_context(request),
    }
    return render(request, 'account/about.html', context)


def privacy(request):
    """Privacy page view"""

    context = {
        'general_context': general_context(request),
    }
    return render(request, 'account/privacy.html', context)


def contact_us(request):
    """Contact page view"""

    context = {
        'general_context': general_context(request),
    }
    return render(request, 'account/contact_us.html', context)


def help_page(request):
    """Help page view"""
    
    context = {
        'general_context': general_context(request),
    }
    return render(request, 'account/help.html', context)
