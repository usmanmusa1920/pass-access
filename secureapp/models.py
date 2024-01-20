from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from account.models import PassCode


User = get_user_model()


class Category(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    category_key = models.CharField(max_length=255)
    category_value = models.CharField(max_length=255)

    def __str__(self):
        return f"This category is \'{self.category_key}\'"
    

class Platform(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    platform_key = models.CharField(max_length=255)
    platform_value = models.CharField(max_length=255)

    def __str__(self):
        return f"This platform is \'{self.platform_key}\'"
    

class SecureItemInfo(models.Model):
    """Items table for storing users item information"""

    category = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    # the custom platform will be inputed by end user
    custom_platform = models.CharField(max_length=100, blank=True, null=True)
    visibility = models.CharField(max_length=100, default='private')

    i_owner = models.ForeignKey(PassCode, on_delete=models.CASCADE)
    trusted_user = models.ManyToManyField(User, blank=True)
    i_label = models.CharField(max_length=255, blank=False, null=False, unique=True)

    # the_key is for (just like the raw passcode of a user) before applying any encryption or hashing,
    # since it is randomly choosen, but it will look like something else, plus key (of pbkdf2_hmac)
    the_key = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)
    last_review = models.DateTimeField(auto_now=True) # last review (not editable)
    # last_visit = models.DateTimeField("last visit", blank=True, null=True)

    # for social
    i_username = models.TextField(blank=True, null=True)
    i_phone = models.CharField(max_length=100, blank=True, null=True)
    i_email = models.EmailField(max_length=300, blank=True, null=True)
    i_password = models.CharField(max_length=300, blank=True, null=True)

    # for cloud
    i_passphrase = models.CharField(max_length=300, blank=True, null=True)
    i_api = models.CharField(max_length=300, blank=True, null=True)
    i_ssh_key_pub = models.CharField(max_length=300, blank=True, null=True)
    i_ssh_key_prt = models.CharField(max_length=300, blank=True, null=True)

    # for AWS S3
    # i_aws_secret_access_key
    # i_aws_access_key_id
    # i_aws_default_acl
    # i_aws_storage_bucket_name
    # i_aws_s3_file_overite
    # i_default_files_storage

    # for card
    i_card_no = models.CharField(max_length=300, blank=True, null=True)
    i_card_valid_range = models.CharField(max_length=300, blank=True, null=True)
    i_card_ccv = models.CharField(max_length=300, blank=True, null=True)
    i_card_pin = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"An item information ({self.id})"
    

class ItemSecretIngredient(models.Model):
    """
    `rely_on` is just like the (owner), in which it belongs to,

    ingredient models
    """

    trusted_people = models.ManyToManyField(User, blank=True, related_name='trusted_people')
    rely_on = models.OneToOneField(SecureItemInfo, on_delete=models.CASCADE)
    ingredient = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Item secret ingredient for {self.rely_on} ({self.id})"
    
    
class ItemSecret(models.Model):
    """
    `rely_on` is just like the (owner), in which it belongs to,

    the_hash
    """
    
    rely_on = models.OneToOneField(SecureItemInfo, on_delete=models.CASCADE)
    the_hash = models.TextField(blank=True, null=True)
    the_private = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Item secret for {self.rely_on} ({self.id})"
