from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'month', 'year', 'created_at']
    list_filter = ['month', 'year', 'category']
    search_fields = ['user__username', 'category__name']
    ordering = ['-year', '-month']
