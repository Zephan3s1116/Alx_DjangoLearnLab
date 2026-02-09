"""
Blog Admin Configuration

This module registers the blog models with the Django admin interface.
"""

from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Post model.
    
    Displays: title, author, published_date
    Filters: published_date, author
    Search: title, content
    """
    
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    
    # Make published_date read-only since it's auto-generated
    readonly_fields = ('published_date',)
    
    # Organize fields in the admin form
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'author', 'content')
        }),
        ('Metadata', {
            'fields': ('published_date',),
            'classes': ('collapse',)
        }),
    )
