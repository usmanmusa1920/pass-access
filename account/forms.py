# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    PasswordChangeForm,
    UserCreationForm
)
from account.models import PassCode


User = get_user_model()


class SignupForm(UserCreationForm):
    """Signup form class"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'username', 'email', 'phone_number', 'country', 'password1', 'password2']
        

class PasswordChangeForm(PasswordChangeForm):
    """Password change form class"""

    class Meta:
        model = User
        

class UpdateForm(forms.ModelForm):
    """Update form class"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'username', 'phone_number', 'country']
        

class PassCodeForm_1(forms.ModelForm):
    """Setting up passcode for the first time, and renewing passcode form"""

    # the below field is not available in the model, it is just for comparing two fields,
    # to make sure they match before we save into database
    verify_email = forms.EmailField()
    # the below field is not available in the model, it is just for comparing two fields,
    # (old passcode in database, and the old passcode that a user claim),
    # to make sure they match before we save into database. It is use only when user is updating his/her passcode, that is why it is not `required=False`
    old_passcode = forms.CharField(required=False)
    # the below field is not available in the model, it is just for comparing two fields,
    # (new_passcode, and new_passcode_again) to make sure they match before we save into database
    verify_passcode = forms.CharField()

    class Meta:
        model = PassCode
        fields = ['passcode_ingredient', 'lucky_number', 'childhood_name']


class PassCodeForm_1x(forms.ModelForm):
    """Update passcode form"""
    
    class Meta:
        model = PassCode
        fields = []


class PassCodeForm_2(forms.ModelForm):
    """Update form class"""

    class Meta:
        model = PassCode
        fields = ['session_age', 'monitor_session_age']
        

class AccountPassCodeForm(forms.ModelForm):
    """
    This is use along side with the (PassCodeForm and UpdatePassCodeForm) form, for passcode renew
    """
    
    class Meta:
        model = User
        fields = ['passcode_hash']
