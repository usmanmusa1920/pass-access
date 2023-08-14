from django.urls import path
from .views import (
    home, setSecurePasscode, updateSecurePasscode, itemInfo, addTrustedUser, removeTrustedUser, searchTrustedUser, newItem, newItemFields, signup
)


app_name = 'secureapp'

urlpatterns = [
    path('', home, name='home'),
    path('set/secure/', setSecurePasscode, name='set_secure'),
    path('update/secure/', updateSecurePasscode, name='update_secure'),
    path('item/info/<int:item_id>/', itemInfo, name='item_info'),
    path('add/trusted/<int:item_id>/<int:user_id>/',
         addTrustedUser, name='add_trusted'),
    path('remove/trusted/<int:item_id>/<int:user_id>/',
         removeTrustedUser, name='remove_trusted'),
    path('search/trusted/<int:item_id>/',
         searchTrustedUser, name='search_trusted'),
    path('new/item/', newItem, name='new_item'),
    path('new/item/fields', newItemFields, name='new_item_fields'),

    # for auth
    path('signup/', signup, name='signup'),
]
