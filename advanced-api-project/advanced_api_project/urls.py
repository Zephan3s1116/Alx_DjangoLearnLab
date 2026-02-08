"""
Main URL Configuration for Advanced API Project.

This module includes the main URL routing for the entire project,
connecting the admin interface and the API endpoints.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints (defined in api/urls.py)
    path('api/', include('api.urls')),
]
