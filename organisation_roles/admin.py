from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'organisation', 'is_staff', 'is_superuser')
    list_filter = ('role', 'organisation')
    fieldsets = UserAdmin.fieldsets + (
        ('Organisation Info', {'fields': ('organisation', 'role')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
