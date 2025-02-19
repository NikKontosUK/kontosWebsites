from django.contrib import admin
from userauths.models import User
# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User()
    list_display = ('email', 'phone_number', 'id', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'phone_number')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

