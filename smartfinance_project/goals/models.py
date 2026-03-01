from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Goal(models.Model):
    """
    Financial goal tracking model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    name = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_completed']),
        ]
    
    def __str__(self):
        return f"{self.name} - ${self.current_amount}/${self.target_amount}"
    
    def get_progress_percentage(self):
        if self.target_amount > 0:
            return float((self.current_amount / self.target_amount) * 100)
        return 0.0
    
    def get_remaining_amount(self):
        return self.target_amount - self.current_amount
