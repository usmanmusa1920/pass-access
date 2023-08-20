from django.db import models
from django.conf import settings
from django.utils import timezone
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


User = settings.AUTH_USER_MODEL


class UserAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number, password=None, **kwargs):
        """
        we provide `**kwargs` to accept other keyword argument, even though it is not in this way in the django default create_user method of user class.

        It help if you want to make a user not to be active when creating him, by making the `is_activ=False`:
            e.g:
                User.objects.create_user(first_name='Ali', is_active=False)
        """
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
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, phone_number, password=None, **kwargs):
        """
        we provide `**kwargs` to accept other keyword argument, even though it is not in this way in the django default create_superuser method of user class.

        It help if you want to make a user not to be active when creating him, by making the `is_activ=False`:
            e.g:
                User.objects.create_superuser(first_name='Ali', is_active=False)
        """
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number,
            password=password,
            **kwargs
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    first_name = models.CharField(max_length=100, unique=False)
    last_name = models.CharField(max_length=100, unique=False)
    GENDER_CHOICES = [('female', 'Female'), ('male', 'Male'),]
    gender = models.CharField(
        max_length=100, default='male', choices=GENDER_CHOICES)
    date_of_birth = models.DateField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=255, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = PhoneNumberField(max_length=100, unique=False)
    country = CountryField(max_length=100, blank_label='Select your country',)
    date_joined = models.DateTimeField(default=timezone.now) # date_joined (not editable)
    last_modified = models.DateTimeField(auto_now=True) # last modified (not editable)

    """
    `date_joined` above is not editable, also
    `last_modified` above is not editable too! but,

    the default `last_login` for users is editable, like wise
    the `pub_date` below is editable

    pub_date = models.DateTimeField(default=timezone.now) # (editable)
    """

    # user passcode hash
    passcode_hash = models.TextField(blank=True, null=True)

    # Default django permissions (is_active, is_staff, is_superuser)
    is_active = models.BooleanField(default=True)
    # Designates whether this user account should be considered active.
    # We recommend that you set this flag to False instead of deleting accounts;
    # that way, if your applications have any foreign keys to users, the foreign keys won`t break.

    is_staff = models.BooleanField(default=False)
    # Designates whether the user can log into this admin site.

    is_superuser = models.BooleanField(default=False)
    # Designates that this user has all permissions without explicitly assigning them.

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    
class PassCode(models.Model):
    """passcode table for storing users passcode"""
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    passcode_ingredient = models.TextField(blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner.username}\'s secure passcode'
