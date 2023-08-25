# -*- coding: utf-8 -*-
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from account.models import PassCode


User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_securepass(sender, instance, created, **kwargs):
    if created:
        PassCode.objects.create(owner=instance)
        
        
@receiver(post_save, sender=User)
def save_securepass(sender, instance, **kwargs):
    instance.passcode.save()
