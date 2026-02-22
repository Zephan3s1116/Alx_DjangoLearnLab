from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from decimal import Decimal

class Transaction(models.Model):
    """
    Transaction model for tracking income and expenses.
    """
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'category']),
            models.Index(fields=['user', 'type']),
        ]
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.amount} on {self.date}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.amount <= 0:
            raise ValidationError({'amount': 'Amount must be greater than zero.'})
        if self.category.type != self.type:
            raise ValidationError({'category': f'Category type must match transaction type ({self.type}).'})
