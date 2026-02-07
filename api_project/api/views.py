from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to retrieve list of books.
    GET /api/books/ - Returns a list of all books
    
    Permissions: Requires authentication
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access


class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for performing CRUD operations on Book model.
    
    Provides the following actions:
    - list: GET /api/books_all/ - List all books (requires authentication)
    - create: POST /api/books_all/ - Create a new book (requires authentication)
    - retrieve: GET /api/books_all/<id>/ - Retrieve a specific book (requires authentication)
    - update: PUT /api/books_all/<id>/ - Update a book (requires authentication)
    - partial_update: PATCH /api/books_all/<id>/ - Partially update a book (requires authentication)
    - destroy: DELETE /api/books_all/<id>/ - Delete a book (requires authentication)
    
    Permissions:
    - All operations require authentication (IsAuthenticated)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can perform CRUD operations
