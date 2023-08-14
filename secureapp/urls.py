from django.urls import path
from . import views as item_views


app_name = 'secureapp'

urlpatterns = [
    path('', item_views.home, name='home'),
    path('set/secure/', item_views.setSecurePasscode, name='set_secure'),
    path('update/secure/', item_views.updateSecurePasscode, name='update_secure'),
    path('item/info/<int:item_id>/', item_views.itemInfo, name='item_info'),
    path('add/trusted/<int:item_id>/<int:user_id>/', item_views.addTrustedUser, name='add_trusted'),
    path('remove/trusted/<int:item_id>/<int:user_id>/', item_views.removeTrustedUser, name='remove_trusted'),
    path('search/trusted/<int:item_id>/', item_views.searchTrustedUser, name='search_trusted'),
    path('new/item/', item_views.newItem, name='new_item'),
    path('new/item/fields', item_views.newItemFields, name='new_item_fields'),

    # for auth
    path('signup/', item_views.signup, name='signup'),
]
