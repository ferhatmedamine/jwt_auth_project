from django.urls import path
from .views import LoginView, LogoutView, RegisterView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Use the class-based view for login
    path('logout/', LogoutView.as_view(), name='logout'),  # Use the class-based view for logout
    path('register/', RegisterView.as_view(), name='register'),  # Manually map RegisterView to /register/
]
