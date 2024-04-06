from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe

from apps.user.models import User


admin.site.site_header = _('Adminsitration')
admin.site.index_title = _('Site adminsitration')            
admin.site.site_title = _('Site adminsitration') 


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    readonly_fields = ('last_login', 'date_joined', '_image')
    ordering = ['first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('_image', 'username', 'first_name', 'last_name', 'image')}),
        (_('Extra informations'), {'fields': ('password', 'last_login', 'date_joined')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'image', 'password1', 'password2'),
        }),
    )

    def _image(self, obj):
        image = obj.image
        return mark_safe(f'<img src="{image.url}" width=100 height=100 style="border-radius: 50%; object-fit: cover">')
    
    _image.short_description = ''

