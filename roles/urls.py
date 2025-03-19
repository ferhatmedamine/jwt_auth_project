from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('restricted-view/', views.restricted_view, name='restricted_view'),

]