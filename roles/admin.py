from django.contrib import admin
from .models import Organisation, Profile

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'organisation')