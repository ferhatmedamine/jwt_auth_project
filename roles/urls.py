from django.urls import path
from . import views

urlpatterns = [
    # Role-based dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    # CRUD operations
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    # Example restricted view
    path('restricted/', views.restricted_view, name='restricted_view'),
]