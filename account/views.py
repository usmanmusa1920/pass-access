from django.utils.html import format_html
from django.contrib import messages as flash_msg
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

    if request.method == 'POST':
        sender_name = request.POST['name']
        sender_email = request.POST['email']
        text_body = request.POST['feedback']
        
        import os
        import kyaah

        subj = f'An email sent through PassAccess App - {sender_name}'
        body = f'Dear! PassAccess,\n\n{text_body}\n\nSender details:\n\tName: {sender_name}\n\tEmail: {sender_email}'

        mail_serve ='gmail'
        sender = 'GMAIL_ADDRESS'
        passwd = 'GMAIL_APP_PWD'
        receiver = []
        
        r = os.environ.get('GMAIL_ADDRESS_RECEIVER')
        receiver.append(r)
        
        kyaah.sendMail(
            from_usr=sender, to_usr=receiver, svr=mail_serve, subject=subj, body=body, mail_passwd=passwd, env=True
        )

        flash_msg.success(request, format_html('Thanks<b>&nbsp;{}&nbsp;</b>for your message,&nbsp;<b>PassAccess</b>&nbsp;will response at the earliest.', sender_name))
        return redirect('auth:contact_us')
    
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
