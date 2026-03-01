from django.contrib import admin
from .models import Goal

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'current_amount', 'target_amount', 'is_completed', 'deadline']
    list_filter = ['is_completed', 'deadline']
    search_fields = ['name', 'user__username']
    ordering = ['-created_at']
