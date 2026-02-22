from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'type', 'category', 'amount', 'user', 'created_at']
    list_filter = ['type', 'category', 'date']
    search_fields = ['description', 'user__username']
    ordering = ['-date', '-created_at']
