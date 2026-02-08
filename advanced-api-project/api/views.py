"""
Django REST Framework Views for the Advanced API Project.

This module contains view classes that handle CRUD operations for the Book model
using Django REST Framework's generic views. Each view is customized to handle
specific use cases and includes proper permission controls.

Views included:
- BookListView: List all books (GET) and create new books (POST)
- BookDetailView: Retrieve a single book (GET)
- BookCreateView: Create a new book (POST)
- BookUpdateView: Update an existing book (PUT/PATCH)
- BookDeleteView: Delete a book (DELETE)

All views use DRF's generic views for efficient, maintainable code.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    List all books in the database.
    
    This view provides a read-only endpoint that returns a list of all Book instances.
    It supports filtering, searching, and ordering for better data discovery.
    
    Endpoint: GET /api/books/
    
    Permissions:
        - Read access: Any user (authenticated or not)
    
    Features:
        - Filtering: Filter books by publication_year and author
        - Searching: Search books by title or author name
        - Ordering: Order results by publication_year or title
    
    Query Parameters:
        - ?publication_year=2020 - Filter by publication year
        - ?author=1 - Filter by author ID
        - ?search=Harry - Search in title and author name
        - ?ordering=-publication_year - Order by publication year (descending)
        - ?ordering=title - Order by title (ascending)
    
    Response Format (200 OK):
        [
            {
                "id": 1,
                "title": "Book Title",
                "publication_year": 2020,
                "author": 1
            },
            ...
        ]
    
    Usage:
        GET /api/books/
        GET /api/books/?publication_year=2020
        GET /api/books/?search=Potter
        GET /api/books/?ordering=-publication_year
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Anyone can read
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['publication_year', 'author']  # Fields to filter by
    search_fields = ['title', 'author__name']  # Fields to search in
    ordering_fields = ['publication_year', 'title']  # Fields to order by
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
    permission_classes = [IsAuthenticatedOrReadOnly]  # Anyone can read


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
            "id": 5,
            "title": "New Book Title",
            "publication_year": 2023,
            "author": 1
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
    permission_classes = [IsAuthenticated]  # Only authenticated users can create
    
    def perform_create(self, serializer):
        """
        Custom create logic executed when a new book is created.
        
        This method is called by CreateAPIView after validation but before
        saving the instance. It can be used to:
        - Add additional fields
        - Perform additional validation
        - Log creation events
        - Send notifications
        
        Args:
            serializer: The validated serializer instance
        """
        # Save the book instance
        book = serializer.save()
        
        # You can add custom logic here, such as:
        # - Logging the creation
        # - Sending notifications
        # - Updating related models
        
        # Example: Log book creation (in production, use proper logging)
        print(f"New book created: {book.title} by {book.author.name}")
    
    def create(self, request, *args, **kwargs):
        """
        Override create method to customize response and error handling.
        
        This method handles the entire create request lifecycle:
        1. Validate the request data
        2. Create the book instance
        3. Return appropriate response
        
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
    
    Custom Behavior:
        - Validates all updates using BookSerializer
        - Supports partial updates (PATCH) for updating specific fields
        - Maintains data integrity through validation
    
    Usage:
        PUT /api/books/1/update/
        Headers: Authorization: Token <your_token>
        Body: {"title": "New Title", "publication_year": 2023, "author": 1}
        
        PATCH /api/books/1/update/
        Headers: Authorization: Token <your_token>
        Body: {"title": "New Title"}
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update
    
    def perform_update(self, serializer):
        """
        Custom update logic executed when a book is updated.
        
        This method is called after validation but before saving.
        Useful for:
        - Logging updates
        - Sending notifications
        - Updating related models
        
        Args:
            serializer: The validated serializer instance
        """
        book = serializer.save()
        
        # Custom logic after update
        print(f"Book updated: {book.title}")
    
    def update(self, request, *args, **kwargs):
        """
        Override update method to customize response.
        
        Handles both PUT (full update) and PATCH (partial update) requests.
        
        Args:
            request: The HTTP request object
            
        Returns:
            Response: HTTP response with updated book data or errors
        """
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
    
    Custom Behavior:
        - Returns the deleted book data in the response
        - Includes custom success message
        - Can be extended to implement soft deletes
    
    Usage:
        DELETE /api/books/1/delete/
        Headers: Authorization: Token <your_token>
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete
    
    def perform_destroy(self, instance):
        """
        Custom delete logic executed when a book is deleted.
        
        This method is called before the instance is actually deleted.
        Useful for:
        - Logging deletions
        - Creating audit trails
        - Implementing soft deletes
        - Cleaning up related data
        
        Args:
            instance: The book instance to be deleted
        """
        # Log the deletion
        print(f"Book deleted: {instance.title} by {instance.author.name}")
        
        # Perform the actual deletion
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to customize response.
        
        Returns the deleted book data along with a success message.
        
        Args:
            request: The HTTP request object
            
        Returns:
            Response: HTTP response with deletion confirmation
        """
        instance = self.get_object()
        
        # Serialize the instance before deleting to return in response
        serializer = self.get_serializer(instance)
        book_data = serializer.data
        
        # Perform the deletion
        self.perform_destroy(instance)
        
        return Response(
            {
                'message': 'Book deleted successfully',
                'deleted_book': book_data
            },
            status=status.HTTP_200_OK
        )
