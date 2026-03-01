from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from transactions.models import Transaction
from django.db.models import Sum
from decimal import Decimal

class Budget(models.Model):
    """
    Budget model for tracking spending limits by category.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='budgets')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['user', 'category', 'month', 'year']
        indexes = [
            models.Index(fields=['user', 'month', 'year']),
        ]
    
    def __str__(self):
        return f"{self.category.name} - {self.month}/{self.year}: ${self.amount}"
    
    def get_spent_amount(self):
        spent = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            type='expense',
            date__month=self.month,
            date__year=self.year
        ).aggregate(total=Sum('amount'))['total']
        return spent or Decimal('0.00')
    
    def get_remaining_amount(self):
        return self.amount - self.get_spent_amount()
    
    def get_percentage_used(self):
        spent = self.get_spent_amount()
        if self.amount > 0:
            return float((spent / self.amount) * 100)
        return 0.0
    
    def get_status(self):
        percentage = self.get_percentage_used()
        if percentage >= 100:
            return 'over'
        elif percentage >= 80:
            return 'near'
        else:
            return 'under'
