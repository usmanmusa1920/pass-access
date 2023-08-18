from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class PasswordChangeForm(PasswordChangeForm):
    """password change form class"""
    class Meta:
        model = User


class SignupForm(UserCreationForm):
    """signup form class"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'username', 'email', 'phone_number', 'country', 'password1', 'password2']


class UpdateForm(forms.ModelForm):
    """update form class"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'username', 'phone_number', 'country']
