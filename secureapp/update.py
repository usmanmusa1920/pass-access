# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import get_user_model
from account.default import default


User = get_user_model()


def update_item(request):
    """update item page view"""
    context = {
        'default': default(request),
    }
    return render(request, 'secureapp/update_item.html', context)


def update_item_salt(request):
    """update item salt page view"""
    context = {
        'default': default(request),
    }
    return render(request, 'secureapp/update_item_salt.html', context)
