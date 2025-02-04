from django.urls import path
from .views import OrganisationListCreateView, OrganisationDetailView

urlpatterns = [
    path('', OrganisationListCreateView.as_view(), name='organisation-list-create'),
    path('<int:pk>/', OrganisationDetailView.as_view(), name='organisation-detail'),
]
