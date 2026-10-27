from django.urls import path
from .views import DashboardSummaryView

app_name = 'dashboard'

urlpatterns = [
    # Endpoint principal pour le tableau de bord d'Ariane
    path('summary/', DashboardSummaryView.as_view(), name='summary'),
]
