from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

from django.conf import settings
User = settings.AUTH_USER_MODEL


class UserAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number, password=None):
        if not first_name:
            raise ValueError('Your first name is required')
        if not last_name:
            raise ValueError('Your last name is required')
        if not username:
            raise ValueError('Your username is required')
        if not email:
            raise ValueError('You must provide your email address')
        if not phone_number:
            raise ValueError('Please include your phone number')
        if not password:
            raise ValueError('You must include password')

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = self.normalize_email(email),
            phone_number = phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def account_verified(self, first_name, last_name, username, email, phone_number, password):
        user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = self.normalize_email(email),
            phone_number = phone_number,
            password = password,
        )

        user.save(using=self._db)
        return user
    
    def create_staffuser(self, first_name, last_name, username, email, phone_number, password):
        user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = self.normalize_email(email),
            phone_number = phone_number,
            password = password,
        )

        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def create_adminuser(self, first_name, last_name, username, email, phone_number, password=None):
        user = self.create_user(
        first_name = first_name,
        last_name = last_name,
        username = username,
        email = self.normalize_email(email),
        phone_number = phone_number,
        password = password,
        )
        
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, phone_number, password=None):
        user = self.create_user(
        first_name = first_name,
        last_name = last_name,
        username = username,
        email = self.normalize_email(email),
        phone_number = phone_number,
        password = password,
        )
        
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class UserAccount(AbstractBaseUser):
    first_name = models.CharField(max_length=100, unique=False)
    last_name = models.CharField(max_length=100, unique=False)
    GENDER_CHOICES = [('female', 'Female'), ('male', 'Male'),]
    gender = models.CharField(max_length=100, default='male', choices=GENDER_CHOICES)
    date_of_birth = models.DateField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=False)
    phone_number = PhoneNumberField(max_length=100, unique=True)
    country = CountryField(max_length=100, blank_label='Select your country',)
    date_joined = models.DateTimeField(default=timezone.now)

    # user passcode hash
    passcode_hash = models.TextField(blank=True, null=True)
        
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserAccountManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'email']

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
