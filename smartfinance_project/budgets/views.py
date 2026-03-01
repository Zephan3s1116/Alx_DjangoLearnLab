from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from decimal import Decimal
from .models import Budget
from .serializers import BudgetSerializer, BudgetStatusSerializer

class BudgetListCreateView(generics.ListCreateAPIView):
    """
    List all budgets or create a new budget.
    
    Filtering:
    - ?month=2
    - ?year=2026
    - ?category=1
    """
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['month', 'year', 'category']
    ordering_fields = ['month', 'year', 'amount']
    ordering = ['-year', '-month']
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a budget.
    """
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

class BudgetStatusView(APIView):
    """
    Get overall budget status summary.
    
    Query params:
    - ?month=2
    - ?year=2026
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Budget.objects.filter(user=request.user)
        
        # Filter by month/year if provided
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        
        if month:
            queryset = queryset.filter(month=month)
        if year:
            queryset = queryset.filter(year=year)
        
        # Calculate statistics
        budgets = list(queryset)
        
        if not budgets:
            data = {
                'total_budgeted': Decimal('0.00'),
                'total_spent': Decimal('0.00'),
                'total_remaining': Decimal('0.00'),
                'overall_percentage': 0.0,
                'budgets_count': 0,
                'over_budget_count': 0,
                'near_limit_count': 0,
                'under_budget_count': 0,
            }
        else:
            total_budgeted = sum(b.amount for b in budgets)
            total_spent = sum(b.get_spent_amount() for b in budgets)
            total_remaining = total_budgeted - total_spent
            overall_percentage = float((total_spent / total_budgeted * 100) if total_budgeted > 0 else 0)
            
            # Count by status
            over_budget_count = sum(1 for b in budgets if b.get_status() == 'over')
            near_limit_count = sum(1 for b in budgets if b.get_status() == 'near')
            under_budget_count = sum(1 for b in budgets if b.get_status() == 'under')
            
            data = {
                'total_budgeted': total_budgeted,
                'total_spent': total_spent,
                'total_remaining': total_remaining,
                'overall_percentage': round(overall_percentage, 2),
                'budgets_count': len(budgets),
                'over_budget_count': over_budget_count,
                'near_limit_count': near_limit_count,
                'under_budget_count': under_budget_count,
            }
        
        serializer = BudgetStatusSerializer(data)
        return Response(serializer.data)
