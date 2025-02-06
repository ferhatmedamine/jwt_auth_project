from django.urls import path
from .views import IntegrationListCreateView, IntegrationDetailView

urlpatterns = [
    path('', IntegrationListCreateView.as_view(), name='integration-list-create'),
    path('<int:pk>/', IntegrationDetailView.as_view(), name='integration-detail'),
]
