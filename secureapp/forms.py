from django import forms
from django.contrib.auth import get_user_model
from .models import SecurePass, SecureItemInfo, ItemSecretIngredient, ItemSecret


User = get_user_model()


class SecurePassForm(forms.ModelForm):
    """Setting up passcode form for the first time"""

    """
    the below field is not available in the model, it is just for comparing two fields,
    to make sure they match before we save into database
    """
    verify_email = forms.EmailField()
    verify_passcode = forms.CharField()

    class Meta:
        model = SecurePass
        fields = ['passcode_ingredient']
        

class UpdateSecurePasscode(forms.ModelForm):
    """Renewing passcode form"""

    verify_email = forms.EmailField()
    """
    the below field is not available in the model, it is just for comparing two fields,
    (old passcode in database, and the old passcode that a user claim),
    to make sure they match before we save into database
    """
    old_passcode = forms.CharField()
    """
    the below field is not available in the model, it is just for comparing two fields,
    (new_passcode, and new_passcode_again) to make sure they match before we save into database
    """
    verify_passcode = forms.CharField()

    class Meta:
        model = SecurePass
        fields = ['passcode_ingredient']
        

class AccounFormForPasscode(forms.ModelForm):
    """this is use along side with the (SecurePassForm and UpdateSecurePasscode) form, for passcode renew"""

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
        

class InfoSecretForm(forms.ModelForm):
    """ # """

    class Meta:
        model = ItemSecret
        fields = ['the_hash', 'the_private']
        
        
class InfoIngredientForm(forms.ModelForm):
    """ # """

    class Meta:
        model = ItemSecretIngredient
        fields = ['ingredient']
