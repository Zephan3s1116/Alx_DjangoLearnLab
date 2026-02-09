"""
Django Blog URL Configuration

This module defines the main URL patterns for the Django blog project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
