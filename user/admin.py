from django.contrib import admin
from .models import UserRole

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'organisation', 'role')
    list_editable = ('role',)
    search_fields = ('user__username', 'organisation__name')