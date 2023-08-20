from django.contrib import admin
from .models import (
    Category, Platform, SecureItemInfo, ItemSecretIngredient, ItemSecret
)


admin.site.register(Category)
admin.site.register(Platform)
admin.site.register(SecureItemInfo)
admin.site.register(ItemSecretIngredient)
admin.site.register(ItemSecret)
