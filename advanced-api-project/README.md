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


---

## Task 2: Implementing Filtering, Searching, and Ordering

### Overview
This task implements comprehensive filtering, searching, and ordering capabilities for the Book API, allowing users to efficiently query and retrieve books based on various criteria.

---

### Features Implemented

#### 1. **Filtering**
Advanced filtering capabilities using Django Filter Backend with custom FilterSet.

**Available Filters:**
- **Exact Match:**
  - `title`: Filter by exact title
  - `author`: Filter by author ID
  - `publication_year`: Filter by exact year
  
- **Range Filters:**
  - `publication_year__gte`: Books published in or after specified year
  - `publication_year__lte`: Books published in or before specified year
  
- **Contains Filter:**
  - `title__icontains`: Case-insensitive partial title match

**Examples:**
```bash
GET /api/books/?publication_year=2020
GET /api/books/?publication_year__gte=2000&publication_year__lte=2020
GET /api/books/?title__icontains=harry
GET /api/books/?author=1
```

#### 2. **Searching**
Full-text search across multiple fields using SearchFilter.

**Search Fields:**
- `title`: Book title
- `author__name`: Author's name

**Examples:**
```bash
GET /api/books/?search=Harry
GET /api/books/?search=Rowling
GET /api/books/?search=Potter
```

**How It Works:**
- Searches across both title and author name simultaneously
- Case-insensitive
- Returns books matching the search term in ANY search field

#### 3. **Ordering**
Flexible result ordering using OrderingFilter.

**Available Ordering Fields:**
- `title`: Sort by book title
- `publication_year`: Sort by publication year
- `author`: Sort by author ID

**Examples:**
```bash
GET /api/books/?ordering=title              # Ascending A-Z
GET /api/books/?ordering=-title             # Descending Z-A
GET /api/books/?ordering=-publication_year  # Newest first
GET /api/books/?ordering=author,title       # Multiple fields
```

**Ordering Syntax:**
- **Ascending:** Use field name (e.g., `ordering=title`)
- **Descending:** Prefix with `-` (e.g., `ordering=-title`)
- **Multiple:** Separate with commas (e.g., `ordering=author,title`)

#### 4. **Combining Features**
All features can be combined in a single query.

**Examples:**
```bash
# Filter by year range and sort by title
GET /api/books/?publication_year__gte=2000&publication_year__lte=2020&ordering=title

# Search and sort
GET /api/books/?search=Harry&ordering=-publication_year

# Filter by author and sort
GET /api/books/?author=1&ordering=-publication_year

# Complex query with all features
GET /api/books/?author=1&publication_year__gte=2000&search=Potter&ordering=title
```

---

### Implementation Details

#### Custom FilterSet
Created `BookFilter` class in `api/views.py`:
```python
class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='exact')
    author = filters.NumberFilter(field_name='author')
    publication_year = filters.NumberFilter(field_name='publication_year')
    publication_year__gte = filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    publication_year__lte = filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    title__icontains = filters.CharFilter(field_name='title', lookup_expr='icontains')
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
```

#### BookListView Configuration
```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Enable filtering, searching, and ordering
    filter_backends = [
        filters.DjangoFilterBackend,  # For filtering
        drf_filters.SearchFilter,      # For searching
        drf_filters.OrderingFilter     # For ordering
    ]
    
    # Use custom FilterSet
    filterset_class = BookFilter
    
    # Search configuration
    search_fields = ['title', 'author__name']
    
    # Ordering configuration
    ordering_fields = ['title', 'publication_year', 'author']
    ordering = ['-publication_year']  # Default ordering
```

#### Settings Configuration
```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # ... other settings
}
```

---

### Testing

#### Run Automated Tests
```bash
./test_filtering_searching_ordering.sh
```

#### Manual Testing Examples

**1. Filter by publication year:**
```bash
curl "http://127.0.0.1:8000/api/books/?publication_year=2020"
```

**2. Filter by year range:**
```bash
curl "http://127.0.0.1:8000/api/books/?publication_year__gte=2000&publication_year__lte=2020"
```

**3. Search for books:**
```bash
curl "http://127.0.0.1:8000/api/books/?search=Harry"
```

**4. Sort by title:**
```bash
curl "http://127.0.0.1:8000/api/books/?ordering=title"
```

**5. Complex query:**
```bash
curl "http://127.0.0.1:8000/api/books/?author=1&publication_year__gte=2000&ordering=-publication_year"
```

---

### Documentation Files

- **FILTERING_SEARCHING_ORDERING_GUIDE.md**: Comprehensive guide with all examples and use cases
- **test_filtering_searching_ordering.sh**: Automated testing script
- **README.md**: This file - project documentation

---

### Query Parameter Reference

| Category | Parameter | Type | Description | Example |
|----------|-----------|------|-------------|---------|
| **Filter** | `title` | string | Exact title match | `?title=Harry Potter` |
| | `author` | integer | Filter by author ID | `?author=1` |
| | `publication_year` | integer | Exact year | `?publication_year=2020` |
| | `publication_year__gte` | integer | Year >= value | `?publication_year__gte=2000` |
| | `publication_year__lte` | integer | Year <= value | `?publication_year__lte=2020` |
| | `title__icontains` | string | Case-insensitive contains | `?title__icontains=harry` |
| **Search** | `search` | string | Multi-field search | `?search=Harry` |
| **Order** | `ordering` | string | Sort by field | `?ordering=title` |
| | | | Sort descending | `?ordering=-title` |
| | | | Multiple fields | `?ordering=author,title` |

---

### Expected Response Format

Successful queries return paginated results:
```json
{
    "count": 25,
    "next": "http://127.0.0.1:8000/api/books/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Harry Potter and the Sorcerer's Stone",
            "publication_year": 1997,
            "author": 1
        }
    ]
}
```

---

### Best Practices

1. **URL Encoding**: Always URL-encode special characters
   - Space: `%20`
   - `&`: `%26`

2. **Combining Filters**: Multiple filters work as AND conditions
   - `?author=1&publication_year=2020` means author 1 AND year 2020

3. **Search vs Filter**:
   - Use **search** for fuzzy, multi-field queries
   - Use **filters** for exact matches

4. **Performance**:
   - Filtering by indexed fields is faster
   - Consider pagination for large result sets

---

### Features Summary

✅ Custom FilterSet with advanced filtering options  
✅ Exact match filtering (title, author, publication_year)  
✅ Range filtering (publication_year__gte, publication_year__lte)  
✅ Case-insensitive contains filtering (title__icontains)  
✅ Full-text search across multiple fields  
✅ Flexible ordering by any field  
✅ Ascending and descending sort options  
✅ Ability to combine all features in single query  
✅ Comprehensive documentation and testing  

---

### Repository Information

- **GitHub Repository:** `Alx_DjangoLearnLab`
- **Project Directory:** `advanced-api-project`
- **Task:** Task 2 - Implementing Filtering, Searching, and Ordering in Django REST Framework


---

## Task 3: Writing Unit Tests for Django REST Framework APIs

### Overview
This task implements comprehensive unit tests for all API endpoints, ensuring code quality, reliability, and correctness of the Book API.

---

### Testing Strategy

#### Goals
- Ensure all API endpoints function correctly
- Validate CRUD operations work as expected
- Verify filtering, searching, and ordering features
- Confirm permission and authentication mechanisms
- Test edge cases and error handling

#### Approach
- **Unit Testing**: Test individual components in isolation
- **Integration Testing**: Test interactions between components
- **Comprehensive Coverage**: Test both success and failure scenarios
- **Automated Testing**: Run tests frequently during development

---

### Test Categories (40+ Tests)

#### 1. Authentication Tests (5 tests)
- Token creation and validation
- Authenticated vs unauthenticated requests
- Invalid token handling
- Missing authentication scenarios

#### 2. CRUD Operation Tests (12 tests)

**Create (3 tests):**
- Creating books with authentication
- Validation errors (future year, missing fields)
- Unauthorized creation attempts

**Read (3 tests):**
- Listing all books
- Retrieving single book by ID
- Handling nonexistent books (404)

**Update (3 tests):**
- Full updates (PUT)
- Partial updates (PATCH)
- Unauthorized update attempts

**Delete (3 tests):**
- Deleting books with authentication
- Unauthorized deletion attempts
- Handling nonexistent books (404)

#### 3. Filtering Tests (6 tests)
- Filter by publication year (exact match)
- Filter by publication year range (gte, lte)
- Filter by year range (combined gte + lte)
- Filter by author ID
- Case-insensitive title filtering

#### 4. Searching Tests (4 tests)
- Search by book title
- Search by author name
- Case-insensitive search verification
- Empty search results handling

#### 5. Ordering Tests (4 tests)
- Order by title (ascending/descending)
- Order by publication year (ascending/descending)
- Multiple field ordering
- Default ordering verification

#### 6. Combined Query Tests (3 tests)
- Filter + Order combinations
- Search + Order combinations
- Filter + Search + Order (complex queries)

#### 7. Permission Tests (2 tests)
- Public read access verification
- Authenticated write access enforcement

#### 8. Edge Cases (3 tests)
- Invalid book ID format handling
- Empty request body validation
- Pagination functionality

---

### Running Tests

#### Run All Tests
```bash
python manage.py test api
```

#### Run Specific Test Class
```bash
python manage.py test api.test_views.BookAPITestCase
```

#### Run Specific Test Method
```bash
python manage.py test api.test_views.BookAPITestCase.test_create_book_authenticated
```

#### Run with Verbose Output
```bash
python manage.py test api --verbosity=2
```

#### Run with Coverage Report
```bash
# Install coverage first
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test api
coverage report
coverage html  # Generate HTML report
```

---

### Test Results Interpretation

#### Successful Test Run
```
Found 40 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........................................
----------------------------------------------------------------------
Ran 40 tests in 2.345s

OK
Destroying test database for alias 'default'...
```

**Interpretation:**
- All 40 tests passed ✅
- Each dot (.) represents a passed test
- Test database created and destroyed automatically
- No errors or failures

#### Failed Test Example
```
======================================================================
FAIL: test_create_book_authenticated (api.test_views.BookAPITestCase)
----------------------------------------------------------------------
AssertionError: 400 != 201
```

**Interpretation:**
- One test failed ❌
- Test expected status 201 (Created) but got 400 (Bad Request)
- Need to investigate the book creation endpoint

---

### Key Test Cases

#### Authentication Tests
```python
def test_authenticated_request(self):
    """Test that authenticated requests work correctly."""
    self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    response = self.client.get(self.list_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
```

#### CRUD Tests
```python
def test_create_book_authenticated(self):
    """Test creating a book with authentication."""
    self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    data = {
        'title': 'New Test Book',
        'publication_year': 2020,
        'author': self.author1.id
    }
    response = self.client.post(self.create_url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertTrue(Book.objects.filter(title='New Test Book').exists())
```

#### Filtering Tests
```python
def test_filter_by_publication_year(self):
    """Test filtering books by publication year."""
    url = f'{self.list_url}?publication_year=1997'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data['results']), 1)
```

#### Searching Tests
```python
def test_search_by_title(self):
    """Test searching books by title."""
    url = f'{self.list_url}?search=Harry'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    for book in response.data['results']:
        self.assertIn('Harry', book['title'])
```

#### Ordering Tests
```python
def test_order_by_title_ascending(self):
    """Test ordering books by title (ascending)."""
    url = f'{self.list_url}?ordering=title'
    response = self.client.get(url)
    titles = [book['title'] for book in response.data['results']]
    self.assertEqual(titles, sorted(titles))
```

---

### Test Data Setup

Each test uses the `setUp()` method to create consistent test data:

```python
def setUp(self):
    # Create test users
    self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    # Create authentication tokens
    self.token = Token.objects.create(user=self.user)
    
    # Create test authors
    self.author1 = Author.objects.create(name='J.K. Rowling')
    
    # Create test books
    self.book1 = Book.objects.create(
        title='Harry Potter and the Sorcerer\'s Stone',
        publication_year=1997,
        author=self.author1
    )
```

---

### Continuous Integration

#### Pre-commit Tests
Always run tests before committing:
```bash
python manage.py test
```

#### CI/CD Integration
Configure your CI/CD pipeline to run tests automatically:
```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: python manage.py test
```

---

### Documentation Files

- **api/test_views.py**: Complete test suite (40+ tests)
- **TESTING_GUIDE.md**: Comprehensive testing documentation
- **README.md**: This file - project documentation

---

### Test Coverage

**Coverage Goals:**
- ✅ >80% code coverage
- ✅ 100% coverage for CRUD operations
- ✅ All filtering scenarios tested
- ✅ All searching scenarios tested
- ✅ All ordering scenarios tested
- ✅ All permission scenarios tested

**Check Coverage:**
```bash
coverage run --source='.' manage.py test api
coverage report
```

---

### Best Practices Implemented

1. ✅ **Descriptive test names** - Each test name explains what it tests
2. ✅ **Independent tests** - Each test can run independently
3. ✅ **Comprehensive coverage** - Both success and failure scenarios
4. ✅ **Clear assertions** - Each test has clear pass/fail criteria
5. ✅ **Test data isolation** - Each test uses fresh test database
6. ✅ **Edge case testing** - Invalid inputs and boundary conditions
7. ✅ **Documentation** - Docstrings explain test purpose
8. ✅ **Organized structure** - Tests grouped by category

---

### Features Summary

✅ **40+ comprehensive unit tests**  
✅ **Authentication and permission testing**  
✅ **Complete CRUD operation coverage**  
✅ **Filtering functionality tests**  
✅ **Searching functionality tests**  
✅ **Ordering functionality tests**  
✅ **Combined query tests**  
✅ **Edge case and error handling**  
✅ **Automated test execution**  
✅ **Detailed test documentation**  

---

### Quick Reference

**Run all tests:**
```bash
python manage.py test api
```

**Run with verbose output:**
```bash
python manage.py test api -v 2
```

**Run specific test:**
```bash
python manage.py test api.test_views.BookAPITestCase.test_create_book_authenticated
```

**Check coverage:**
```bash
coverage run --source='.' manage.py test api
coverage report
```

---

### Expected Output

When you run the tests, you should see:

```
Found 40 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........................................
----------------------------------------------------------------------
Ran 40 tests in 2.345s

OK
Destroying test database for alias 'default'...
```

**All tests should pass!** ✅

---

### Repository Information

- **GitHub Repository:** `Alx_DjangoLearnLab`
- **Project Directory:** `advanced-api-project`
- **Task:** Task 3 - Writing Unit Tests for Django REST Framework APIs
- **Test File:** `api/test_views.py`

