from django.urls import path
from .views import (
    MonthlyReportView,
    CategoryBreakdownView,
    TrendsView,
    BudgetVsActualView
)

app_name = 'analytics'

urlpatterns = [
    path('monthly-report/', MonthlyReportView.as_view(), name='monthly-report'),
    path('category-breakdown/', CategoryBreakdownView.as_view(), name='category-breakdown'),
    path('trends/', TrendsView.as_view(), name='trends'),
    path('budget-vs-actual/', BudgetVsActualView.as_view(), name='budget-vs-actual'),
]
