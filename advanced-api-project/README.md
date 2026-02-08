# Advanced API Project

## Overview
This project demonstrates advanced Django REST Framework concepts including:
- Custom serializers with nested relationships
- Custom validation logic
- One-to-Many model relationships
- Comprehensive model and serializer documentation

## Models

### Author
- Represents book authors
- One-to-Many relationship with Book

### Book
- Represents published books
- Foreign key to Author
- Includes title and publication year

## Serializers

### BookSerializer
- Serializes all Book fields
- Custom validation:
  - Publication year cannot be in the future
  - Publication year must be after year 1000

### AuthorSerializer
- Includes nested BookSerializer
- Shows all books by an author in a single request
- Demonstrates nested relationship handling

## Setup Instructions

1. Install dependencies:
```bash
pip install django djangorestframework
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create superuser:
```bash
python manage.py createsuperuser
```

4. Run server:
```bash
python manage.py runserver
```

## Testing

### Using Django Shell:
```bash
python manage.py shell < test_serializers.py
```

### Using Django Admin:
1. Visit http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Create authors and books
4. View relationships

### Manual Testing:
```bash
python manage.py shell
```
```python
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

# Create author
author = Author.objects.create(name="Test Author")

# Create book
book = Book.objects.create(
    title="Test Book",
    publication_year=2020,
    author=author
)

# Serialize author with nested books
serializer = AuthorSerializer(author)
print(serializer.data)
```

## Project Structure
```
advanced-api-project/
├── advanced_api_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── models.py          # Author and Book models
│   ├── serializers.py     # Custom serializers with validation
│   ├── admin.py           # Admin configuration
│   └── migrations/
├── manage.py
├── test_serializers.py    # Testing script
└── README.md
```

## Key Concepts Demonstrated

1. **Nested Serialization**: AuthorSerializer includes nested BookSerializer
2. **Custom Validation**: BookSerializer validates publication_year
3. **Model Relationships**: One-to-Many (Author to Books)
4. **Related Names**: Access books via `author.books.all()`
5. **Read-Only Fields**: Nested books are read-only in AuthorSerializer
