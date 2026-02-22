from django.urls import path
from .views import (
    TransactionListCreateView,
    TransactionDetailView,
    TransactionSummaryView
)

app_name = 'transactions'

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('summary/', TransactionSummaryView.as_view(), name='transaction-summary'),
]
