from rest_framework import generics
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to retrieve list of books.
    GET /api/books/ - Returns a list of all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for performing CRUD operations on Book model.
    
    Provides the following actions:
    - list: GET /api/books_all/ - List all books
    - create: POST /api/books_all/ - Create a new book
    - retrieve: GET /api/books_all/<id>/ - Retrieve a specific book
    - update: PUT /api/books_all/<id>/ - Update a book
    - partial_update: PATCH /api/books_all/<id>/ - Partially update a book
    - destroy: DELETE /api/books_all/<id>/ - Delete a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
