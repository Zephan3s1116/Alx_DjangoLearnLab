from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from decimal import Decimal
from transactions.models import Transaction
from budgets.models import Budget
from categories.models import Category

class MonthlyReportView(APIView):
    """
    Get detailed monthly financial report.
    
    Query params:
    - ?month=2
    - ?year=2026
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        month = request.query_params.get('month', datetime.now().month)
        year = request.query_params.get('year', datetime.now().year)
        
        transactions = Transaction.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year
        )
        
        # Calculate totals
        income_total = transactions.filter(type='income').aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')
        
        expense_total = transactions.filter(type='expense').aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')
        
        net_savings = income_total - expense_total
        savings_rate = float((net_savings / income_total * 100) if income_total > 0 else 0)
        
        # Breakdown by category
        expense_by_category = transactions.filter(type='expense').values(
            'category__name', 'category__id'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        income_by_category = transactions.filter(type='income').values(
            'category__name', 'category__id'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        # Top expenses
        top_expenses = transactions.filter(type='expense').order_by('-amount')[:5].values(
            'id', 'description', 'amount', 'category__name', 'date'
        )
        
        data = {
            'month': int(month),
            'year': int(year),
            'summary': {
                'total_income': income_total,
                'total_expenses': expense_total,
                'net_savings': net_savings,
                'savings_rate': round(savings_rate, 2),
                'transaction_count': transactions.count(),
            },
            'expenses_by_category': list(expense_by_category),
            'income_by_category': list(income_by_category),
            'top_expenses': list(top_expenses),
        }
        
        return Response(data)


class CategoryBreakdownView(APIView):
    """
    Get spending breakdown by category with percentages.
    
    Query params:
    - ?month=2
    - ?year=2026
    - ?type=expense (or income)
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        trans_type = request.query_params.get('type', 'expense')
        
        queryset = Transaction.objects.filter(user=request.user, type=trans_type)
        
        if month and year:
            queryset = queryset.filter(date__month=month, date__year=year)
        
        # Get total
        total = queryset.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Breakdown by category
        breakdown = queryset.values(
            'category__name', 'category__id', 'category__color'
        ).annotate(
            amount=Sum('amount'),
            count=Count('id')
        ).order_by('-amount')
        
        # Add percentages
        breakdown_with_percentage = []
        for item in breakdown:
            percentage = float((item['amount'] / total * 100) if total > 0 else 0)
            breakdown_with_percentage.append({
                'category_id': item['category__id'],
                'category_name': item['category__name'],
                'color': item['category__color'],
                'amount': item['amount'],
                'percentage': round(percentage, 2),
                'transaction_count': item['count'],
            })
        
        data = {
            'type': trans_type,
            'period': {
                'month': month,
                'year': year,
            } if month and year else None,
            'total': total,
            'categories': breakdown_with_percentage,
        }
        
        return Response(data)


class TrendsView(APIView):
    """
    Get 6-month financial trends.
    
    Shows income, expenses, and savings over the last 6 months.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get last 6 months of data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        
        transactions = Transaction.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lte=end_date
        )
        
        # Group by month
        monthly_data = transactions.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            income=Sum('amount', filter=Sum('amount', filter={'type': 'income'})),
            expenses=Sum('amount', filter={'type': 'expense'})
        ).order_by('month')
        
        # Process data
        trends = []
        for item in monthly_data:
            income = item.get('income') or Decimal('0.00')
            expenses = item.get('expenses') or Decimal('0.00')
            savings = income - expenses
            
            trends.append({
                'month': item['month'].strftime('%Y-%m'),
                'income': income,
                'expenses': expenses,
                'savings': savings,
            })
        
        # Calculate averages
        if trends:
            avg_income = sum(t['income'] for t in trends) / len(trends)
            avg_expenses = sum(t['expenses'] for t in trends) / len(trends)
            avg_savings = sum(t['savings'] for t in trends) / len(trends)
        else:
            avg_income = avg_expenses = avg_savings = Decimal('0.00')
        
        data = {
            'period': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d'),
            },
            'trends': trends,
            'averages': {
                'income': avg_income,
                'expenses': avg_expenses,
                'savings': avg_savings,
            }
        }
        
        return Response(data)


class BudgetVsActualView(APIView):
    """
    Compare budgets vs actual spending.
    
    Query params:
    - ?month=2
    - ?year=2026
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        month = request.query_params.get('month', datetime.now().month)
        year = request.query_params.get('year', datetime.now().year)
        
        budgets = Budget.objects.filter(
            user=request.user,
            month=month,
            year=year
        )
        
        comparison = []
        for budget in budgets:
            spent = budget.get_spent_amount()
            remaining = budget.get_remaining_amount()
            percentage = budget.get_percentage_used()
            status = budget.get_status()
            
            comparison.append({
                'category': {
                    'id': budget.category.id,
                    'name': budget.category.name,
                    'color': budget.category.color,
                },
                'budgeted': budget.amount,
                'spent': spent,
                'remaining': remaining,
                'percentage_used': round(percentage, 2),
                'status': status,
            })
        
        # Overall summary
        total_budgeted = sum(b.amount for b in budgets)
        total_spent = sum(b.get_spent_amount() for b in budgets)
        total_remaining = total_budgeted - total_spent
        overall_percentage = float(
            (total_spent / total_budgeted * 100) if total_budgeted > 0 else 0
        )
        
        data = {
            'month': int(month),
            'year': int(year),
            'summary': {
                'total_budgeted': total_budgeted,
                'total_spent': total_spent,
                'total_remaining': total_remaining,
                'overall_percentage': round(overall_percentage, 2),
            },
            'comparisons': comparison,
        }
        
        return Response(data)
