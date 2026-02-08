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

## Task 1: Custom Views and Generic Views

### Views Implemented

1. **BookListView** (ListView)
   - Endpoint: `GET /api/books/`
   - Features: Filtering, searching, ordering
   - Permissions: Public (read-only)

2. **BookDetailView** (DetailView)
   - Endpoint: `GET /api/books/<id>/`
   - Features: Retrieve single book
   - Permissions: Public (read-only)

3. **BookCreateView** (CreateView)
   - Endpoint: `POST /api/books/create/`
   - Features: Create new book with validation
   - Permissions: Authenticated users only

4. **BookUpdateView** (UpdateView)
   - Endpoints: `PUT/PATCH /api/books/<id>/update/`
   - Features: Full or partial update
   - Permissions: Authenticated users only

5. **BookDeleteView** (DeleteView)
   - Endpoint: `DELETE /api/books/<id>/delete/`
   - Features: Delete with confirmation
   - Permissions: Authenticated users only

### Permissions

- **IsAuthenticatedOrReadOnly**: Applied to List and Detail views (anyone can read)
- **IsAuthenticated**: Applied to Create, Update, Delete views (auth required)

### Features

- **Filtering**: Filter books by publication year and author
- **Searching**: Search books by title or author name
- **Ordering**: Order results by publication year or title
- **Custom Validation**: Publication year validation in serializer
- **Custom Responses**: Enhanced response messages for all operations

### Testing

See [TEST_API.md](TEST_API.md) for comprehensive testing instructions.

### Quick Test
```bash
# Start server
python manage.py runserver

# List books (no auth required)
curl http://127.0.0.1:8000/api/books/

# Create book (auth required)
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Book", "publication_year": 2023, "author": 1}'
```
