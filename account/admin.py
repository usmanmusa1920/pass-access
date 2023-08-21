from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import PassCode


User = get_user_model()


class PassCodeInline(admin.TabularInline):
    model = PassCode
    extra = 0


class UserAdminForm(UserAdmin):
    search_fields = ('username', 'email',)
    list_filter = ('first_name', 'last_name', 'username', 'email', 'is_active', 'is_superuser', 'is_staff')
    ordering = ('-date_joined',)

    # list to display
    list_display = ('first_name', 'last_name', 'last_login', 'date_joined', 'last_modified', 'username', 'email', 'is_active', 'is_superuser', 'is_staff')

    # These are the field that will display when you want to edit user account via admin
    '''
    Don`t put `last_modified` and `date_joined` in the below fieldset because they are not editable.

    But `last_login` is editable, but don`t put it also, why? to avoid mistakely editing it for a user that is why we comment it out below
    '''
    fieldsets = (
        (None, {"fields": ('password', 'username')}),
        ('Personal', {"fields": ('first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'phone_number', 'country')}),
        # ('Account activity', {"fields": ('last_login',)}),
        ('Permissions', {"fields": ('is_active',
         'is_staff', 'is_superuser')}),
         ('Security', {"fields": ('passcode_hash', 'auth_token')})
    )
    
    # These are the field that will display when you want to create new user account via admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'password1', 'password2')
        }),
    )
    inlines = [PassCodeInline]
    filter_horizontal = ()


class PassCodeAdmin(admin.ModelAdmin):
    search_fields = ('owner', 'passcode_ingredient', 'date_modified')
    ordering = ('-owner',)
    list_filter = ('owner', 'passcode_ingredient')
    list_display = ('owner', 'passcode_ingredient', 'date_modified')
    fieldsets = (
        (None, {"fields": ('owner',), }),
        ('Date Information', {'fields': ('passcode_ingredient',)}),
    )


admin.site.site_header = 'Encme'
admin.site.site_title = 'Encme'
admin.site.index_title = 'Encme admin'

admin.site.register(User, UserAdminForm)
admin.site.register(PassCode, PassCodeAdmin)
admin.site.unregister(Group)
