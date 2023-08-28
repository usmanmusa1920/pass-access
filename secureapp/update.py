# -*- coding: utf-8 -*-
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth import get_user_model


User = get_user_model()
THIS_YEARE = datetime.today().year


def update_item(request):
    """update item page view"""
    context = {
        'None': None,
    }
    return render(request, 'secureapp/update_item.html', context)


def update_item_salt(request):
    """update item salt page view"""
    context = {
        'None': None,
    }
    return render(request, 'secureapp/update_item_salt.html', context)
