from django.contrib import admin
from .models import (
    Categories, Platforms, SecurePass, SecureItemInfo, ItemSecretIngredient, ItemSecret
)


admin.site.register(Categories)
admin.site.register(Platforms)
admin.site.register(SecurePass)
admin.site.register(SecureItemInfo)
admin.site.register(ItemSecretIngredient)
admin.site.register(ItemSecret)
