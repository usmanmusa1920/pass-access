# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model
from .models import SecureItemInfo


User = get_user_model()


class SecureItemInfoForm_1(forms.ModelForm):
    category = forms.CharField(required=True)
    platform = forms.CharField(required=True)
    visibility = forms.CharField(required=True)

    i_label = forms.CharField(required=True)
    selected_category = forms.CharField(required=True)
    selected_platform = forms.CharField(required=True)

    class Meta:
        model = SecureItemInfo
        fields = ['category', 'platform', 'custom_platform', 'visibility', 'i_label']
        
        
class SecureItemInfoForm_2(forms.ModelForm):
    i_label = forms.CharField(required=True)
    category = forms.CharField(required=True)
    visibility = forms.CharField(required=True)
    platform = forms.CharField(required=True)
    
    class Meta:
        model = SecureItemInfo
        fields = ['the_key', 'custom_platform', 'i_username', 'i_phone', 'i_email', 'i_password', 'i_passphrase', 'i_api', 'i_ssh_key_pub', 'i_ssh_key_prt', 'i_card_no', 'i_card_valid_range', 'i_card_ccv', 'i_card_pin']
