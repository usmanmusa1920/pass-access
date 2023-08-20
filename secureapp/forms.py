from django import forms
from django.contrib.auth import get_user_model
from .models import SecureItemInfo
from account.models import PassCode


User = get_user_model()


class PassCodeForm(forms.ModelForm):
    """Setting up passcode for the first time, and renewing passcode form"""

    """
    the below field is not available in the model, it is just for comparing two fields,
    to make sure they match before we save into database
    """
    verify_email = forms.EmailField()
    """
    the below field is not available in the model, it is just for comparing two fields,
    (old passcode in database, and the old passcode that a user claim),
    to make sure they match before we save into database. It is use only when user is updating his/her passcode, that is why it is not `required=False`
    """
    old_passcode = forms.CharField(required=False)
    """
    the below field is not available in the model, it is just for comparing two fields,
    (new_passcode, and new_passcode_again) to make sure they match before we save into database
    """
    verify_passcode = forms.CharField()

    class Meta:
        model = PassCode
        fields = ['passcode_ingredient']
        

class AccountPassCodeForm(forms.ModelForm):
    """this is use along side with the (PassCodeForm and UpdatePassCodeForm) form, for passcode renew"""

    class Meta:
        model = User
        fields = ['passcode_hash']
        

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
