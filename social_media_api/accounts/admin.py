"""
Accounts Admin Configuration

This module registers the CustomUser model with the Django admin interface.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model.
    
    Extends Django's UserAdmin to include custom fields.
    """
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'followers_count')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'profile_picture', 'followers')
        }),
    )
    
    def followers_count(self, obj):
        """Display follower count in admin list."""
        return obj.followers_count
    
    followers_count.short_description = 'Followers'
