from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to retrieve list of books.
    GET /api/books/ - Returns a list of all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
