from django.urls import path
from .views import BudgetListCreateView, BudgetDetailView, BudgetStatusView

app_name = 'budgets'

urlpatterns = [
    path('', BudgetListCreateView.as_view(), name='budget-list'),
    path('<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),
    path('status/', BudgetStatusView.as_view(), name='budget-status'),
]
