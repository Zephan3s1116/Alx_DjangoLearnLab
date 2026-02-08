# Unit Testing Guide for Django REST Framework API

## Overview
This guide provides comprehensive information about the unit tests implemented for the Book API, including how to run tests, interpret results, and understand the testing strategy.

---

## Table of Contents
1. [Testing Strategy](#testing-strategy)
2. [Test Categories](#test-categories)
3. [Running Tests](#running-tests)
4. [Test Results Interpretation](#test-results-interpretation)
5. [Individual Test Cases](#individual-test-cases)
6. [Continuous Testing](#continuous-testing)

---

## Testing Strategy

### Goals
- Ensure all API endpoints function correctly
- Validate CRUD operations work as expected
- Verify filtering, searching, and ordering features
- Confirm permission and authentication mechanisms
- Test edge cases and error handling

### Approach
- **Unit Testing**: Test individual components in isolation
- **Integration Testing**: Test interactions between components
- **Test-Driven Development**: Write tests before or alongside code
- **Comprehensive Coverage**: Test both success and failure scenarios

### Test Database
- Django automatically creates a separate test database
- Test data is isolated from production/development data
- Database is created before tests and destroyed after

---

## Test Categories

### 1. Authentication Tests
Tests for token authentication and authorization mechanisms.

**Tests:**
- Token creation and validation
- Authenticated vs unauthenticated requests
- Invalid token handling
- Missing authentication

### 2. CRUD Operation Tests

#### Create (POST)
- Creating books with authentication
- Validation (future year, missing fields)
- Unauthorized creation attempts

#### Read (GET)
- Listing all books
- Retrieving single book by ID
- Retrieving nonexistent books

#### Update (PUT/PATCH)
- Full updates (PUT)
- Partial updates (PATCH)
- Unauthorized update attempts

#### Delete (DELETE)
- Deleting books with authentication
- Unauthorized deletion attempts
- Deleting nonexistent books

### 3. Filtering Tests
- Filter by publication year (exact)
- Filter by publication year range (gte, lte)
- Filter by author
- Case-insensitive title filtering

### 4. Searching Tests
- Search by title
- Search by author name
- Case-insensitive search
- No results scenarios

### 5. Ordering Tests
- Order by title (ascending/descending)
- Order by publication year (ascending/descending)
- Multiple field ordering

### 6. Combined Query Tests
- Filter + Order
- Search + Order
- Filter + Search + Order

### 7. Permission Tests
- Public read access
- Authenticated write access
- Permission enforcement

### 8. Edge Cases
- Invalid ID formats
- Empty request bodies
- Pagination

---

## Running Tests

### Run All Tests
```bash
python manage.py test
```

### Run API Tests Only
```bash
python manage.py test api
```

### Run Specific Test File
```bash
python manage.py test api.test_views
```

### Run Specific Test Class
```bash
python manage.py test api.test_views.BookAPITestCase
```

### Run Specific Test Method
```bash
python manage.py test api.test_views.BookAPITestCase.test_create_book_authenticated
```

### Run Tests with Verbose Output
```bash
python manage.py test api --verbosity=2
```

### Run Tests and Keep Test Database
```bash
python manage.py test api --keepdb
```

### Run Tests with Coverage Report
```bash
# Install coverage first
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test api
coverage report
coverage html  # Generate HTML report
```

---

## Test Results Interpretation

### Successful Test Run
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

**Meaning:**
- All 40 tests passed
- Each dot (.) represents a passed test
- No errors or failures

### Failed Test Run
```
Found 40 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.................F......................
======================================================================
FAIL: test_create_book_authenticated (api.test_views.BookAPITestCase)
Test creating a book with authentication.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "...", line 123, in test_create_book_authenticated
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
AssertionError: 400 != 201

----------------------------------------------------------------------
Ran 40 tests in 2.543s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

**Meaning:**
- 39 tests passed, 1 failed (F)
- The failed test is `test_create_book_authenticated`
- Expected status 201, but got 400
- Need to investigate why book creation returned 400 (Bad Request)

### Test Errors
```
ERROR: test_filter_by_author (api.test_views.BookAPITestCase)
Test filtering books by author.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "...", line 456, in test_filter_by_author
    response = self.client.get(url)
AttributeError: 'NoneType' object has no attribute 'id'
```

**Meaning:**
- Test encountered an error (not a failure)
- Usually indicates a bug in the test itself
- In this case, `self.author1` is None

---

## Individual Test Cases

### Authentication Tests (5 tests)

#### test_authentication_token_creation
**Purpose:** Verify tokens are created correctly  
**What it tests:** Token creation and user association  
**Success criteria:** Tokens exist and are linked to correct users

#### test_authenticated_request
**Purpose:** Verify authenticated requests work  
**What it tests:** Requests with valid token  
**Success criteria:** Returns 200 OK

#### test_unauthenticated_read_access
**Purpose:** Verify public can read  
**What it tests:** GET requests without auth  
**Success criteria:** Returns 200 OK for list endpoint

#### test_unauthenticated_create_denied
**Purpose:** Verify public cannot create  
**What it tests:** POST requests without auth  
**Success criteria:** Returns 401 Unauthorized

---

### CRUD Tests - Create (3 tests)

#### test_create_book_authenticated
**Purpose:** Verify book creation works  
**What it tests:**
- POST request with valid data and auth
- Book is saved to database
- Correct response data returned

**Success criteria:**
- Status 201 Created
- Response contains book data
- Book exists in database

#### test_create_book_validation_future_year
**Purpose:** Verify validation works  
**What it tests:** Creating book with invalid year  
**Success criteria:**
- Status 400 Bad Request
- Validation error in response

#### test_create_book_missing_required_fields
**Purpose:** Verify required field validation  
**What it tests:** Creating book without required fields  
**Success criteria:** Returns 400 Bad Request

---

### CRUD Tests - Read (3 tests)

#### test_list_books
**Purpose:** Verify book listing works  
**What it tests:** GET request to list endpoint  
**Success criteria:**
- Status 200 OK
- Paginated response format
- Correct number of books

#### test_retrieve_single_book
**Purpose:** Verify single book retrieval  
**What it tests:** GET request to detail endpoint  
**Success criteria:**
- Status 200 OK
- Correct book data returned

#### test_retrieve_nonexistent_book
**Purpose:** Verify 404 handling  
**What it tests:** GET request for invalid ID  
**Success criteria:** Returns 404 Not Found

---

### CRUD Tests - Update (3 tests)

#### test_update_book_authenticated
**Purpose:** Verify book update works  
**What it tests:**
- PUT request with auth
- Database is updated
- Correct response returned

**Success criteria:**
- Status 200 OK
- Book updated in database
- Response contains updated data

#### test_partial_update_book
**Purpose:** Verify partial updates work  
**What it tests:** PATCH request updates only specified fields  
**Success criteria:**
- Status 200 OK
- Only specified fields updated
- Other fields unchanged

#### test_update_book_unauthenticated
**Purpose:** Verify update requires auth  
**What it tests:** PUT request without auth  
**Success criteria:** Returns 401 Unauthorized

---

### CRUD Tests - Delete (3 tests)

#### test_delete_book_authenticated
**Purpose:** Verify book deletion works  
**What it tests:**
- DELETE request with auth
- Book removed from database
- Deleted data returned

**Success criteria:**
- Status 200 OK
- Book removed from database
- Response contains deleted data

#### test_delete_book_unauthenticated
**Purpose:** Verify delete requires auth  
**What it tests:** DELETE request without auth  
**Success criteria:**
- Returns 401 Unauthorized
- Book still exists

#### test_delete_nonexistent_book
**Purpose:** Verify 404 on delete nonexistent  
**What it tests:** DELETE request for invalid ID  
**Success criteria:** Returns 404 Not Found

---

### Filtering Tests (6 tests)

#### test_filter_by_publication_year
**Purpose:** Verify exact year filtering  
**What it tests:** `?publication_year=1997`  
**Success criteria:** Only books from 1997 returned

#### test_filter_by_publication_year_gte
**Purpose:** Verify >= year filtering  
**What it tests:** `?publication_year__gte=1997`  
**Success criteria:** Only books from 1997+ returned

#### test_filter_by_publication_year_lte
**Purpose:** Verify <= year filtering  
**What it tests:** `?publication_year__lte=1997`  
**Success criteria:** Only books up to 1997 returned

#### test_filter_by_publication_year_range
**Purpose:** Verify year range filtering  
**What it tests:** `?publication_year__gte=1996&publication_year__lte=1998`  
**Success criteria:** Only books in range returned

#### test_filter_by_author
**Purpose:** Verify author filtering  
**What it tests:** `?author=1`  
**Success criteria:** Only books by author 1 returned

#### test_filter_by_title_icontains
**Purpose:** Verify case-insensitive title filtering  
**What it tests:** `?title__icontains=harry`  
**Success criteria:** Returns books with "harry" in title (any case)

---

### Searching Tests (4 tests)

#### test_search_by_title
**Purpose:** Verify title search works  
**What it tests:** `?search=Harry`  
**Success criteria:** Books with "Harry" in title returned

#### test_search_by_author_name
**Purpose:** Verify author name search  
**What it tests:** `?search=Rowling`  
**Success criteria:** Books by authors with "Rowling" returned

#### test_search_case_insensitive
**Purpose:** Verify search is case-insensitive  
**What it tests:** `?search=harry` vs `?search=HARRY`  
**Success criteria:** Both return same results

#### test_search_no_results
**Purpose:** Verify empty search results  
**What it tests:** Search term matching nothing  
**Success criteria:** Empty results array, no errors

---

### Ordering Tests (4 tests)

#### test_order_by_title_ascending
**Purpose:** Verify title ordering (A-Z)  
**What it tests:** `?ordering=title`  
**Success criteria:** Results sorted alphabetically

#### test_order_by_title_descending
**Purpose:** Verify title ordering (Z-A)  
**What it tests:** `?ordering=-title`  
**Success criteria:** Results sorted reverse alphabetically

#### test_order_by_publication_year_ascending
**Purpose:** Verify year ordering (oldest first)  
**What it tests:** `?ordering=publication_year`  
**Success criteria:** Results sorted by year ascending

#### test_order_by_publication_year_descending
**Purpose:** Verify year ordering (newest first)  
**What it tests:** `?ordering=-publication_year`  
**Success criteria:** Results sorted by year descending

---

### Combined Tests (3 tests)

#### test_filter_and_order_combined
**Purpose:** Verify filter + order works  
**What it tests:** `?author=1&ordering=publication_year`  
**Success criteria:** Filtered and sorted correctly

#### test_search_and_order_combined
**Purpose:** Verify search + order works  
**What it tests:** `?search=Harry&ordering=title`  
**Success criteria:** Search results sorted correctly

#### test_filter_search_order_combined
**Purpose:** Verify all features together  
**What it tests:** `?author=1&search=Harry&ordering=-publication_year`  
**Success criteria:** All criteria applied correctly

---

### Permission Tests (2 tests)

#### test_permission_read_public
**Purpose:** Verify read is public  
**What it tests:** GET requests without auth  
**Success criteria:** All read operations return 200

#### test_permission_write_requires_auth
**Purpose:** Verify write requires auth  
**What it tests:** POST/PUT/DELETE without auth  
**Success criteria:** All return 401 Unauthorized

---

### Edge Case Tests (3 tests)

#### test_invalid_book_id_format
**Purpose:** Verify invalid ID handling  
**What it tests:** Request with non-numeric ID  
**Success criteria:** Returns 404 Not Found

#### test_empty_request_body_create
**Purpose:** Verify empty body handling  
**What it tests:** POST with empty JSON  
**Success criteria:** Returns 400 Bad Request

#### test_pagination
**Purpose:** Verify pagination works  
**What it tests:** Large result sets  
**Success criteria:**
- Results paginated (≤10 per page)
- Response includes count, next, prev

---

## Continuous Testing

### During Development
Run tests frequently while developing:
```bash
# Quick test run
python manage.py test api

# With verbosity for detailed output
python manage.py test api -v 2
```

### Before Committing
Always run full test suite before committing:
```bash
python manage.py test
```

### In CI/CD Pipeline
Configure your CI/CD to run tests automatically:
```yaml
# Example for GitHub Actions
- name: Run Tests
  run: python manage.py test
```

---

## Troubleshooting

### Tests Fail Unexpectedly
1. **Check database state:** Ensure test database is clean
   ```bash
   python manage.py test --keepdb=False
   ```

2. **Check for dependency issues:** Update packages
   ```bash
   pip install -r requirements.txt
   ```

3. **Check for model changes:** Run migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Slow Test Runs
1. **Use `--keepdb` flag:** Reuse test database
   ```bash
   python manage.py test --keepdb
   ```

2. **Run specific tests:** Don't run full suite every time
   ```bash
   python manage.py test api.test_views.BookAPITestCase
   ```

### Import Errors
- Ensure all dependencies are installed
- Check Python path
- Verify app is in INSTALLED_APPS

---

## Best Practices

1. **Run tests frequently** - Catch bugs early
2. **Write tests first** - Test-driven development
3. **Test edge cases** - Don't just test happy path
4. **Keep tests independent** - Each test should stand alone
5. **Use descriptive names** - Test names should explain what they test
6. **Mock external services** - Don't depend on external APIs
7. **Maintain test data** - Keep setUp() clean and minimal
8. **Document complex tests** - Add comments explaining why

---

## Test Coverage

### Checking Coverage
```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test api

# View report
coverage report

# Generate HTML report
coverage html
# Open htmlcov/index.html in browser
```

### Coverage Goals
- **Aim for >80% code coverage**
- **100% coverage for critical paths**
- **Cover all CRUD operations**
- **Test all permission scenarios**
- **Validate all filters and search**

---

## Summary

**Total Tests:** 40+  
**Categories:** 8  
**Coverage:** CRUD, Filtering, Searching, Ordering, Permissions, Edge Cases

**To run all tests:**
```bash
python manage.py test api
```

**Expected result:**
```
Ran 40 tests in X.XXXs

OK
```

All tests should pass! ✅
