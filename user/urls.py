from django.urls import path
from . import views

urlpatterns = [
    path('add-user/', views.add_user_to_organisation, name='add_user_to_organisation'),
    path('update-role/', views.update_user_role, name='update_user_role'),
    path('remove-user/', views.remove_user_from_organisation, name='remove_user_from_organisation'),
]