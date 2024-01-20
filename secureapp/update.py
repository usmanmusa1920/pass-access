# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import get_user_model
from account.default import general_context


User = get_user_model()


def update_item(request):
    """Update item page view"""

    context = {
        'general_context': general_context(request),
    }
    return render(request, 'secureapp/update_item.html', context)


def update_item_salt(request):
    """Update item salt page view"""
    
    context = {
        'general_context': general_context(request),
    }
    return render(request, 'secureapp/update_item_salt.html', context)
