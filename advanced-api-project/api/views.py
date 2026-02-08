"""
Django REST Framework Views for the Advanced API Project.

This module contains view classes that handle CRUD operations for the Book model
using Django REST Framework's generic views. Each view includes advanced query
capabilities: filtering, searching, and ordering.

Views included:
- BookListView: List all books with filtering, searching, and ordering
- BookDetailView: Retrieve a single book by ID
- BookCreateView: Create a new book
- BookUpdateView: Update an existing book
- BookDeleteView: Delete a book

Features:
- Filtering: Filter books by title, author, and publication_year
- Searching: Search across title and author name
- Ordering: Sort by any field, especially title and publication_year
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from .models import Book
from .serializers import BookSerializer


class BookFilter(filters.FilterSet):
    """
    Custom FilterSet for the Book model.
    
    Provides advanced filtering capabilities including:
    - Exact match filtering for title, author, and publication_year
    - Range filtering for publication_year (gte, lte)
    - Case-insensitive contains filtering for title
    
    Usage Examples:
        ?title=Harry Potter
        ?author=1
        ?publication_year=2020
        ?publication_year__gte=2000
        ?publication_year__lte=2020
        ?title__icontains=harry
    """
    
    # Exact match filters
    title = filters.CharFilter(field_name='title', lookup_expr='exact')
    author = filters.NumberFilter(field_name='author')
    publication_year = filters.NumberFilter(field_name='publication_year')
    
    # Range filters for publication year
    publication_year__gte = filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gte',
        help_text='Publication year greater than or equal to'
    )
    publication_year__lte = filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lte',
        help_text='Publication year less than or equal to'
    )
    
    # Case-insensitive contains filter for title
    title__icontains = filters.CharFilter(
        field_name='title', 
        lookup_expr='icontains',
        help_text='Case-insensitive title search'
    )
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']


class BookListView(generics.ListAPIView):
    """
    List all books in the database with advanced query capabilities.
    
    This view provides a read-only endpoint that returns a list of all Book instances
    with comprehensive filtering, searching, and ordering features.
    
    Endpoint: GET /api/books/
    
    Permissions:
        - Read access: Any user (authenticated or not)
    
    Features:
        
        1. FILTERING:
           Filter books by specific field values.
           
           Available Filters:
           - title: Exact title match
           - author: Filter by author ID
           - publication_year: Exact year match
           - publication_year__gte: Books published in or after specified year
           - publication_year__lte: Books published in or before specified year
           - title__icontains: Case-insensitive title search
           
           Examples:
           ?title=Harry Potter and the Sorcerer's Stone
           ?author=1
           ?publication_year=2020
           ?publication_year__gte=2000&publication_year__lte=2020
           ?title__icontains=harry
        
        2. SEARCHING:
           Search across multiple fields simultaneously.
           
           Search Fields:
           - title: Book title
           - author__name: Author's name
           
           Examples:
           ?search=Harry
           ?search=Rowling
           ?search=Potter
        
        3. ORDERING:
           Sort results by any field.
           
           Ordering Fields:
           - title: Sort by title (ascending)
           - publication_year: Sort by publication year (ascending)
           - -title: Sort by title (descending)
           - -publication_year: Sort by publication year (descending)
           
           Examples:
           ?ordering=title
           ?ordering=-publication_year
           ?ordering=author,title
        
        4. COMBINING FEATURES:
           Multiple query parameters can be combined.
           
           Examples:
           ?publication_year__gte=2000&ordering=-publication_year
           ?search=Harry&ordering=title
           ?author=1&publication_year__gte=2000&ordering=-publication_year
    
    Response Format (200 OK):
        {
            "count": 10,
            "next": "http://api.example.com/books/?page=2",
            "previous": null,
            "results": [
                {
                    "id": 1,
                    "title": "Book Title",
                    "publication_year": 2020,
                    "author": 1
                },
                ...
            ]
        }
    
    Query Parameter Reference:
        Filtering:
        - ?title=<exact_title>
        - ?author=<author_id>
        - ?publication_year=<year>
        - ?publication_year__gte=<year>
        - ?publication_year__lte=<year>
        - ?title__icontains=<partial_title>
        
        Searching:
        - ?search=<search_term>
        
        Ordering:
        - ?ordering=<field_name>
        - ?ordering=-<field_name> (descending)
        
        Pagination:
        - ?page=<page_number>
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Enable filtering, searching, and ordering
    filter_backends = [
        filters.DjangoFilterBackend,  # For filtering
        drf_filters.SearchFilter,      # For searching
        drf_filters.OrderingFilter     # For ordering
    ]
    
    # Use custom FilterSet for advanced filtering
    filterset_class = BookFilter
    
    # Also support simple field filtering
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Configure search fields
    search_fields = ['title', 'author__name']
    
    # Configure ordering fields
    ordering_fields = ['title', 'publication_year', 'author']
    ordering = ['-publication_year']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single book by its ID.
    
    This view provides read-only access to a specific Book instance identified
    by its primary key (ID).
    
    Endpoint: GET /api/books/<int:pk>/
    
    Permissions:
        - Read access: Any user (authenticated or not)
    
    URL Parameters:
        - pk (int): The primary key (ID) of the book to retrieve
    
    Response Format (200 OK):
        {
            "id": 1,
            "title": "Book Title",
            "publication_year": 2020,
            "author": 1
        }
    
    Error Responses:
        - 404 Not Found: If book with given ID doesn't exist
    
    Usage:
        GET /api/books/1/
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    Create a new book.
    
    This view allows authenticated users to create new Book instances.
    It includes custom validation and error handling.
    
    Endpoint: POST /api/books/create/
    
    Permissions:
        - Create access: Authenticated users only
    
    Request Body:
        {
            "title": "New Book Title",
            "publication_year": 2023,
            "author": 1
        }
    
    Response Format (201 Created):
        {
            "message": "Book created successfully",
            "book": {
                "id": 5,
                "title": "New Book Title",
                "publication_year": 2023,
                "author": 1
            }
        }
    
    Error Responses:
        - 400 Bad Request: Invalid data (e.g., future publication year)
        - 401 Unauthorized: User not authenticated
    
    Custom Behavior:
        - Validates publication year using BookSerializer's custom validation
        - Returns detailed error messages for validation failures
        - Automatically associates the book with the provided author
    
    Usage:
        POST /api/books/create/
        Headers: Authorization: Token <your_token>
        Body: {"title": "New Book", "publication_year": 2023, "author": 1}
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Custom create logic executed when a new book is created.
        
        Args:
            serializer: The validated serializer instance
        """
        book = serializer.save()
        print(f"New book created: {book.title} by {book.author.name}")
    
    def create(self, request, *args, **kwargs):
        """
        Override create method to customize response and error handling.
        
        Args:
            request: The HTTP request object
            
        Returns:
            Response: HTTP response with created book data or errors
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    'message': 'Book created successfully',
                    'book': serializer.data
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        else:
            return Response(
                {
                    'message': 'Failed to create book',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book.
    
    This view allows authenticated users to update Book instances.
    Supports both full updates (PUT) and partial updates (PATCH).
    
    Endpoints:
        - PUT /api/books/<int:pk>/update/  (full update)
        - PATCH /api/books/<int:pk>/update/  (partial update)
    
    Permissions:
        - Update access: Authenticated users only
    
    URL Parameters:
        - pk (int): The primary key (ID) of the book to update
    
    Request Body (PUT - all fields required):
        {
            "title": "Updated Title",
            "publication_year": 2023,
            "author": 1
        }
    
    Request Body (PATCH - any fields):
        {
            "title": "Updated Title"
        }
    
    Response Format (200 OK):
        {
            "message": "Book updated successfully",
            "book": {
                "id": 1,
                "title": "Updated Title",
                "publication_year": 2023,
                "author": 1
            }
        }
    
    Error Responses:
        - 400 Bad Request: Invalid data
        - 401 Unauthorized: User not authenticated
        - 404 Not Found: Book doesn't exist
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        """Custom update logic."""
        book = serializer.save()
        print(f"Book updated: {book.title}")
    
    def update(self, request, *args, **kwargs):
        """Override update method to customize response."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {
                    'message': 'Book updated successfully',
                    'book': serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'message': 'Failed to update book',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book.
    
    This view allows authenticated users to delete Book instances.
    Deletion is permanent and cannot be undone.
    
    Endpoint: DELETE /api/books/<int:pk>/delete/
    
    Permissions:
        - Delete access: Authenticated users only
    
    URL Parameters:
        - pk (int): The primary key (ID) of the book to delete
    
    Response Format (200 OK):
        {
            "message": "Book deleted successfully",
            "deleted_book": {
                "id": 1,
                "title": "Deleted Book",
                "publication_year": 2020,
                "author": 1
            }
        }
    
    Error Responses:
        - 401 Unauthorized: User not authenticated
        - 404 Not Found: Book doesn't exist
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        """Custom delete logic."""
        print(f"Book deleted: {instance.title} by {instance.author.name}")
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy method to customize response."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        book_data = serializer.data
        self.perform_destroy(instance)
        
        return Response(
            {
                'message': 'Book deleted successfully',
                'deleted_book': book_data
            },
            status=status.HTTP_200_OK
        )
