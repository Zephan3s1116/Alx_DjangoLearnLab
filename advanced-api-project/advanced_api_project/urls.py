"""
Main URL Configuration for Advanced API Project.

This module includes the main URL routing for the entire project,
connecting the admin interface and the API endpoints.

Includes:
    - /admin/ - Django admin interface
    - /api/ - All API endpoints (books CRUD operations)
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints (defined in api/urls.py)
    # This includes all book-related endpoints:
    # - /api/books/ - List all books
    # - /api/books/<id>/ - Retrieve single book
    # - /api/books/create/ - Create new book
    # - /api/books/<id>/update/ - Update book
    # - /api/books/update/ - Update book (alternative)
    # - /api/books/<id>/delete/ - Delete book
    # - /api/books/delete/ - Delete book (alternative)
    path('api/', include('api.urls')),
]
