from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Sum, Count, Q
from decimal import Decimal
from .models import Transaction
from .serializers import TransactionSerializer, TransactionSummarySerializer

class TransactionListCreateView(generics.ListCreateAPIView):
    """
    List all transactions or create a new one.
    
    Filtering options:
    - ?type=income or ?type=expense
    - ?category=1
    - ?date_from=2026-01-01
    - ?date_to=2026-01-31
    - ?search=grocery (searches in description)
    - ?ordering=-date (order by date descending)
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'category']
    search_fields = ['description']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Date range filtering
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        return queryset

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a transaction.
    
    Can only access own transactions.
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class TransactionSummaryView(APIView):
    """
    Get transaction summary statistics.
    
    Query params:
    - ?month=2 (1-12)
    - ?year=2026
    - ?date_from=2026-01-01
    - ?date_to=2026-01-31
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Transaction.objects.filter(user=request.user)
        
        # Filter by month/year or date range
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        if month and year:
            queryset = queryset.filter(date__month=month, date__year=year)
        elif date_from and date_to:
            queryset = queryset.filter(date__gte=date_from, date__lte=date_to)
        
        # Calculate statistics
        income_sum = queryset.filter(type='income').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        expense_sum = queryset.filter(type='expense').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        net_savings = income_sum - expense_sum
        savings_rate = float((net_savings / income_sum * 100) if income_sum > 0 else 0)
        
        data = {
            'total_income': income_sum,
            'total_expenses': expense_sum,
            'net_savings': net_savings,
            'savings_rate': round(savings_rate, 2),
            'transaction_count': queryset.count(),
            'income_count': queryset.filter(type='income').count(),
            'expense_count': queryset.filter(type='expense').count(),
        }
        
        serializer = TransactionSummarySerializer(data)
        return Response(serializer.data)
