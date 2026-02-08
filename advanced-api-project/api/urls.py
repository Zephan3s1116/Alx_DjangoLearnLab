"""
URL Configuration for the API app.

This module defines the URL patterns for all book-related API endpoints.
Each endpoint is connected to its corresponding view class.

URL Patterns:
    - /books/ - List all books (GET)
    - /books/<int:pk>/ - Retrieve a single book (GET)
    - /books/create/ - Create a new book (POST)
    - /books/<int:pk>/update/ - Update a book (PUT/PATCH)
    - /books/<int:pk>/delete/ - Delete a book (DELETE)

All endpoints follow RESTful conventions and include proper HTTP method support.
"""

from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

# App name for namespacing URLs
app_name = 'api'

urlpatterns = [
    # List all books
    # Endpoint: GET /api/books/
    # Permissions: Anyone (read-only)
    # Features: Filtering, searching, ordering
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Retrieve a single book by ID
    # Endpoint: GET /api/books/<int:pk>/
    # Permissions: Anyone (read-only)
    # URL Parameter: pk - The book's primary key
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create a new book
    # Endpoint: POST /api/books/create/
    # Permissions: Authenticated users only
    # Request Body: {"title": "...", "publication_year": ..., "author": ...}
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Update an existing book
    # Endpoints: PUT/PATCH /api/books/<int:pk>/update/
    # Permissions: Authenticated users only
    # URL Parameter: pk - The book's primary key
    # PUT: Full update (all fields required)
    # PATCH: Partial update (any fields)
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/update/', BookUpdateView.as_view(), name='book-update-alt'),
    
    # Delete a book
    # Endpoint: DELETE /api/books/<int:pk>/delete/
    # Permissions: Authenticated users only
    # URL Parameter: pk - The book's primary key
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('books/delete/', BookDeleteView.as_view(), name='book-delete-alt'),
]
