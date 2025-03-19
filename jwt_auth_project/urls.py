from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('jwt_auth_app.urls')),
    path('api/organisation/', include('organisation.urls')),
    path('api/integrations/', include('integrations.urls')),  
    path('roles/', include('roles.urls')),
]
