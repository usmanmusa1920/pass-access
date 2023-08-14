from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SecurePass
from django.conf import settings


User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_securepass(sender, instance, created, **kwargs):
    if created:
        SecurePass.objects.create(owner=instance)
        
        
@receiver(post_save, sender=User)
def save_securepass(sender, instance, **kwargs):
    instance.securepass.save()
