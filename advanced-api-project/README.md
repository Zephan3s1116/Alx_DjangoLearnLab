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

## Task 1: Building Custom Views and Generic Views in Django REST Framework

### Overview
This task implements a complete set of CRUD operations for the Book model using Django REST Framework's generic views. Each view is customized with proper permissions, filtering, searching, and ordering capabilities.

---

### Views Implemented

#### 1. **BookListView** (ListView)
- **Endpoint:** `GET /api/books/`
- **Description:** List all books in the database
- **Permissions:** Public (read-only access for everyone)
- **Features:**
  - **Filtering:** Filter books by `publication_year` and `author`
  - **Searching:** Search books by `title` or `author name`
  - **Ordering:** Order results by `publication_year` or `title`
- **Query Examples:**
  ```bash
  GET /api/books/?publication_year=2020
  GET /api/books/?search=Harry
  GET /api/books/?ordering=-publication_year
  ```

#### 2. **BookDetailView** (DetailView)
- **Endpoint:** `GET /api/books/<id>/`
- **Description:** Retrieve a single book by ID
- **Permissions:** Public (read-only access for everyone)
- **Features:** Returns detailed information about a specific book

#### 3. **BookCreateView** (CreateView)
- **Endpoint:** `POST /api/books/create/`
- **Description:** Create a new book
- **Permissions:** Authenticated users only
- **Features:**
  - Custom validation for publication year
  - Detailed error messages
  - Custom success response with message
- **Request Body:**
  ```json
  {
    "title": "New Book",
    "publication_year": 2023,
    "author": 1
  }
  ```

#### 4. **BookUpdateView** (UpdateView)
- **Endpoints:** 
  - `PUT /api/books/<id>/update/` (full update)
  - `PATCH /api/books/<id>/update/` (partial update)
- **Description:** Update an existing book
- **Permissions:** Authenticated users only
- **Features:**
  - Supports both full (PUT) and partial (PATCH) updates
  - Validates all updates
  - Custom response messages

#### 5. **BookDeleteView** (DeleteView)
- **Endpoint:** `DELETE /api/books/<id>/delete/`
- **Description:** Delete a book
- **Permissions:** Authenticated users only
- **Features:**
  - Returns deleted book data in response
  - Custom confirmation message
  - Can be extended for soft deletes

---

### Permissions System

The project uses Django REST Framework's built-in permission classes:

1. **IsAuthenticatedOrReadOnly**
   - Applied to: `BookListView`, `BookDetailView`
   - Behavior: Anyone can read (GET), only authenticated users can modify

2. **IsAuthenticated**
   - Applied to: `BookCreateView`, `BookUpdateView`, `BookDeleteView`
   - Behavior: Only authenticated users can access

---

### URL Configuration

All endpoints are properly configured in `api/urls.py`:

| Endpoint | Method | View | Permission |
|----------|--------|------|------------|
| `/api/books/` | GET | BookListView | Public |
| `/api/books/<id>/` | GET | BookDetailView | Public |
| `/api/books/create/` | POST | BookCreateView | Auth Required |
| `/api/books/<id>/update/` | PUT/PATCH | BookUpdateView | Auth Required |
| `/api/books/<id>/delete/` | DELETE | BookDeleteView | Auth Required |

---

### Custom Behaviors Implemented

1. **Custom Create Logic** (`BookCreateView`)
   - Overrides `perform_create()` for logging
   - Overrides `create()` for custom response format

2. **Custom Update Logic** (`BookUpdateView`)
   - Overrides `perform_update()` for logging
   - Overrides `update()` for custom response format
   - Supports partial updates via PATCH

3. **Custom Delete Logic** (`BookDeleteView`)
   - Overrides `perform_destroy()` for logging
   - Overrides `destroy()` to return deleted data

4. **Filtering and Searching** (`BookListView`)
   - Integrated DjangoFilterBackend for filtering
   - Integrated SearchFilter for text searching
   - Integrated OrderingFilter for result ordering

---

### Dependencies

The project requires the following packages (defined in `requirements.txt`):

```txt
Django>=4.2.0
djangorestframework>=3.14.0
django-filter>=23.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

### Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser (for authentication):**
   ```bash
   python manage.py createsuperuser
   ```

4. **Get authentication token:**
   ```bash
   python manage.py shell
   ```
   ```python
   from rest_framework.authtoken.models import Token
   from django.contrib.auth.models import User
   
   user = User.objects.get(username='your_username')
   token, created = Token.objects.get_or_create(user=user)
   print(f"Token: {token.key}")
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

---

### Testing the API

#### Quick Test (no authentication required):
```bash
# List all books
curl http://127.0.0.1:8000/api/books/

# Get a specific book
curl http://127.0.0.1:8000/api/books/1/

# Filter by publication year
curl "http://127.0.0.1:8000/api/books/?publication_year=2020"

# Search for books
curl "http://127.0.0.1:8000/api/books/?search=Potter"
```

#### Authenticated Operations:
```bash
# Create a book
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Book",
    "publication_year": 2023,
    "author": 1
  }'

# Update a book (partial)
curl -X PATCH http://127.0.0.1:8000/api/books/1/update/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'

# Delete a book
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

#### Run automated tests:
```bash
./test_views.sh
```

---

### Documentation Files

- **TEST_API.md**: Comprehensive testing guide with all endpoints, examples, and troubleshooting
- **test_views.sh**: Automated testing script for all endpoints
- **README.md**: This file - complete project documentation

---

### Features Summary

✅ Generic views for all CRUD operations  
✅ Custom permission classes (IsAuthenticated, IsAuthenticatedOrReadOnly)  
✅ Filtering by publication_year and author  
✅ Searching by title and author name  
✅ Ordering by publication_year and title  
✅ Custom validation for publication year  
✅ Custom response messages for all operations  
✅ Token authentication support  
✅ Comprehensive documentation and testing guide  
✅ Automated testing script  

---

### Next Steps

To continue developing this project, consider:
1. Adding pagination for large datasets
2. Implementing custom permissions (e.g., only authors can delete their books)
3. Adding more complex filtering options
4. Implementing API versioning
5. Adding throttling to prevent API abuse
6. Creating API documentation with drf-spectacular or similar tools

---

### Repository Information

- **GitHub Repository:** `Alx_DjangoLearnLab`
- **Project Directory:** `advanced-api-project`
- **Task:** Task 1 - Building Custom Views and Generic Views in Django REST Framework

