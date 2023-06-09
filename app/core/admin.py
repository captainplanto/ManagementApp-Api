# Django admin customization, Needed to register the models you want to have control on in the Admin Panel



from core import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    # Define the admin page edit for users.
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = ((None, {'fields': ('email', 'password')}),
                 (
        _('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser')}
    ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
# use classes to add custom css to django admin
    add_fieldsets = ((None, {'classes': ('wide',),
                             'fields': (
        'email',
        'password1', 
        'password2',
        'name',
        'is_active',
        'is_staff',
        'is_superuser'

    )}),
    )
    readonly_fields = ['last_login']


admin.site.register(models.User, UserAdmin)
