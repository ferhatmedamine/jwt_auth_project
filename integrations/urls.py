from django.urls import path
from .views import (
    IntegrationListCreateView, IntegrationDetailView,
    MoodleIntegrationListCreateView, MoodleIntegrationDetailView
)

urlpatterns = [
    path('', IntegrationListCreateView.as_view(), name='integration-list-create'),
    path('<int:pk>/', IntegrationDetailView.as_view(), name='integration-detail'),

    # Moodle Integration Endpoints
    path('moodle/', MoodleIntegrationListCreateView.as_view(), name='moodle-integration-list-create'),
    path('moodle/<int:pk>/', MoodleIntegrationDetailView.as_view(), name='moodle-integration-detail'),  # This now correctly matches the view
]
