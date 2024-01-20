# -*- coding: utf-8 -*-
from django.urls import path
from .update import (
    update_item,
    update_item_salt
)
from .views import (
    new_item,
    new_item_fields,
    item_info,
    search_trusted_user,
    add_trusted_user,
    remove_trusted_user,
    remove_all_trusted_user,
    delete_item,
)


app_name = 'secureapp'

urlpatterns = [
    # views.py module path (views routes)
    path(
        'update/item/<int:item_id>/', update_item, name='update_item'),
    path(
        'update/item/salt/<int:item_id>/', update_item_salt, name='update_item_salt'),


    # views.py module path (views routes)
    path(
        'new/item/', new_item, name='new_item'),
    path(
        'new/item/fields', new_item_fields, name='new_item_fields'),
    path(
        'item/info/<int:item_id>/', item_info, name='item_info'),
    path(
        'search/trusted/<int:item_id>/', search_trusted_user, name='search_trusted_user'),
    path(
        'add/trusted/<int:item_id>/<int:user_id>/', add_trusted_user, name='add_trusted_user'),
    path(
        'remove/trusted/<int:item_id>/<int:user_id>/', remove_trusted_user, name='remove_trusted_user'),
    path(
        'remove/all/trusted/<int:item_id>/', remove_all_trusted_user, name='remove_all_trusted_user'),
    path(
        'delete/item/<int:item_id>/', delete_item, name='delete_item'),
]
