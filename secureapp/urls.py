# -*- coding: utf-8 -*-
from django.urls import path
from .views import (
    landing, dashboard, set_passcode, update_passcode
)
from .item import (
    new_item, new_item_fields, item_info, search_trusted_user, add_trusted_user, remove_trusted_user, remove_all_trusted_user, delete_item
)


app_name = 'secureapp'

urlpatterns = [
    path('', landing, name='landing'),
    path('dashboard/', dashboard, name='dashboard'),
    path(
        'set/passcode/', set_passcode, name='set_passcode'),
    path(
        'update/passcode/', update_passcode, name='update_passcode'),
    # item
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
