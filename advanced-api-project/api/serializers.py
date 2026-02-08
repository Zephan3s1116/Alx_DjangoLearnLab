from rest_framework import serializers
from .models import Author, Book
from datetime import date


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles the conversion of Book model instances to/from JSON.
    It includes all fields of the Book model and implements custom validation
    to ensure data integrity.
    
    Fields:
        - id: Auto-generated primary key (read-only)
        - title: The book's title
        - publication_year: The year the book was published
        - author: Foreign key to the Author model (ID reference)
    
    Custom Validation:
        - publication_year: Ensures the year is not in the future
        - publication_year: Ensures the year is reasonable (not before 1000 AD)
    
    Usage:
        # Serialize a book instance
        book = Book.objects.get(id=1)
        serializer = BookSerializer(book)
        json_data = serializer.data
        
        # Deserialize and create a book
        data = {'title': 'New Book', 'publication_year': 2020, 'author': 1}
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        # Make id read-only as it's auto-generated
        read_only_fields = ['id']

    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Validates that:
        1. The publication year is not in the future
        2. The publication year is not unreasonably old (before year 1000)
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        current_year = date.today().year
        
        # Check if publication year is in the future
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        # Check if publication year is unreasonably old
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year must be after year 1000."
            )
        
        return value

    def validate(self, data):
        """
        Object-level validation for the entire serializer.
        
        This method can be used to validate relationships between fields.
        For example, ensuring certain combinations of values are valid.
        
        Args:
            data (dict): Dictionary of all field values
            
        Returns:
            dict: The validated data
        """
        # Additional validation can be added here if needed
        # For example, checking if a book with the same title already exists for this author
        return data


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    This serializer demonstrates how to handle nested relationships in DRF.
    It includes a nested representation of all books written by the author,
    using the BookSerializer to serialize each related book.
    
    Fields:
        - id: Auto-generated primary key (read-only)
        - name: The author's full name
        - books: Nested serialization of all books by this author (read-only)
    
    Nested Serialization:
        The 'books' field uses BookSerializer to serialize all related Book instances.
        This creates a nested JSON structure where each author object contains
        a list of their books with full book details.
        
        - many=True: Indicates this is a one-to-many relationship
        - read_only=True: Books are not created/updated through this serializer
        
    Example JSON Output:
        {
            "id": 1,
            "name": "J.K. Rowling",
            "books": [
                {
                    "id": 1,
                    "title": "Harry Potter and the Philosopher's Stone",
                    "publication_year": 1997,
                    "author": 1
                },
                {
                    "id": 2,
                    "title": "Harry Potter and the Chamber of Secrets",
                    "publication_year": 1998,
                    "author": 1
                }
            ]
        }
    
    Relationship Handling:
        - The relationship between Author and Book is established via the ForeignKey
          in the Book model (author field).
        - The related_name='books' in the Book model's ForeignKey allows us to
          access all books for an author via author.books.all()
        - BookSerializer(many=True) serializes all related books automatically
        - This creates a denormalized JSON response that includes nested data,
          which is useful for API consumers who need complete information in one request
    
    Usage:
        # Serialize an author with all their books
        author = Author.objects.get(id=1)
        serializer = AuthorSerializer(author)
        json_data = serializer.data  # Includes nested books
        
        # Serialize all authors with their books
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        json_data = serializer.data
    """
    
    # Nested serializer: serializes all books related to this author
    # many=True because one author can have multiple books
    # read_only=True because we don't want to create books through the author endpoint
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id']

    def validate_name(self, value):
        """
        Custom validation for the name field.
        
        Ensures that:
        1. The name is not empty or just whitespace
        2. The name has a reasonable length
        
        Args:
            value (str): The author's name to validate
            
        Returns:
            str: The validated and cleaned name
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        # Remove leading/trailing whitespace
        value = value.strip()
        
        # Check if name is empty after stripping whitespace
        if not value:
            raise serializers.ValidationError(
                "Author name cannot be empty."
            )
        
        # Check minimum length
        if len(value) < 2:
            raise serializers.ValidationError(
                "Author name must be at least 2 characters long."
            )
        
        return value
