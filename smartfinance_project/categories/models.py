from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
    Category model for income and expense categorization.
    
    Categories can be:
    - Default (system-provided, cannot be deleted)
    - Custom (user-created, can be modified/deleted)
    """
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='categories',
        null=True,  # Null for default categories
        blank=True
    )
    is_default = models.BooleanField(default=False)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, blank=True)  # Hex color
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['type', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ['name', 'user', 'type']
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"
