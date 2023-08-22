from django.urls import path
from .views import (
    landing, dashboard, set_pass_code, UpdatePassCode, itemInfo, addTrustedUser, removeTrustedUser, searchTrustedUser, newItem, newItemFields
)


app_name = 'secureapp'

urlpatterns = [
    path('', landing, name='landing'),
    path('dashboard/', dashboard, name='dashboard'),

    # below two path are for setting user passcode, the first path route is for setting user passcode if not set directly, while the second path route will be use if user try to go to route that required user passcode to be set, e.g if creating new item.
    path(
        'set/passcode/', set_pass_code, name='set_passcode'),
    path(
        'set/passcode/?next=/<str:next_url>/', set_pass_code, name='set_passcode'),

    # update route
    path(
        'update/passcode/', UpdatePassCode, name='update_passcode'),
    path(
        'item/info/<int:item_id>/', itemInfo, name='item_info'),
    path(
        'add/trusted/<int:item_id>/<int:user_id>/', addTrustedUser, name='add_trusted'),
    path(
        'remove/trusted/<int:item_id>/<int:user_id>/', removeTrustedUser, name='remove_trusted'),
    path(
        'search/trusted/<int:item_id>/', searchTrustedUser, name='search_trusted'),
    path(
        'new/item/', newItem, name='new_item'),
    path(
        'new/item/fields', newItemFields, name='new_item_fields'),
]
