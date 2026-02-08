# API Testing Guide

## Overview
This document provides instructions for testing all API endpoints in the Advanced API Project.

## Prerequisites
1. Server must be running: `python manage.py runserver`
2. You must have authentication token (for protected endpoints)

## Getting Authentication Token

### Create a superuser:
```bash
python manage.py createsuperuser
```

### Get token via Django shell:
```bash
python manage.py shell
```
```python
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

user = User.objects.get(username='your_username')
token, created = Token.objects.get_or_create(user=user)
print(f"Your token: {token.key}")
```

## Testing Endpoints

### 1. List All Books (GET)
**Endpoint:** `GET http://127.0.0.1:8000/api/books/`

**Authentication:** Not required

**curl command:**
```bash
curl http://127.0.0.1:8000/api/books/
```

**With filtering:**
```bash
# Filter by publication year
curl "http://127.0.0.1:8000/api/books/?publication_year=2020"

# Search by title
curl "http://127.0.0.1:8000/api/books/?search=Harry"

# Order by title
curl "http://127.0.0.1:8000/api/books/?ordering=title"
```

**Expected Response (200 OK):**
```json
[
    {
        "id": 1,
        "title": "Book Title",
        "publication_year": 2020,
        "author": 1
    }
]
```

---

### 2. Retrieve Single Book (GET)
**Endpoint:** `GET http://127.0.0.1:8000/api/books/1/`

**Authentication:** Not required

**curl command:**
```bash
curl http://127.0.0.1:8000/api/books/1/
```

**Expected Response (200 OK):**
```json
{
    "id": 1,
    "title": "Book Title",
    "publication_year": 2020,
    "author": 1
}
```

**Error Response (404 Not Found):**
```json
{
    "detail": "Not found."
}
```

---

### 3. Create New Book (POST)
**Endpoint:** `POST http://127.0.0.1:8000/api/books/create/`

**Authentication:** Required (Token)

**curl command:**
```bash
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Book",
    "publication_year": 2023,
    "author": 1
  }'
```

**Request Body:**
```json
{
    "title": "New Book",
    "publication_year": 2023,
    "author": 1
}
```

**Expected Response (201 Created):**
```json
{
    "message": "Book created successfully",
    "book": {
        "id": 5,
        "title": "New Book",
        "publication_year": 2023,
        "author": 1
    }
}
```

**Error Response (400 Bad Request - Future Year):**
```json
{
    "message": "Failed to create book",
    "errors": {
        "publication_year": [
            "Publication year cannot be in the future. Current year is 2026."
        ]
    }
}
```

**Error Response (401 Unauthorized - No Token):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

### 4. Update Book (PUT/PATCH)
**Endpoint:** `PUT/PATCH http://127.0.0.1:8000/api/books/1/update/`

**Authentication:** Required (Token)

**Full Update (PUT) - all fields required:**
```bash
curl -X PUT http://127.0.0.1:8000/api/books/1/update/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "publication_year": 2023,
    "author": 1
  }'
```

**Partial Update (PATCH) - any fields:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/books/1/update/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title Only"
  }'
```

**Expected Response (200 OK):**
```json
{
    "message": "Book updated successfully",
    "book": {
        "id": 1,
        "title": "Updated Title",
        "publication_year": 2023,
        "author": 1
    }
}
```

---

### 5. Delete Book (DELETE)
**Endpoint:** `DELETE http://127.0.0.1:8000/api/books/1/delete/`

**Authentication:** Required (Token)

**curl command:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Expected Response (200 OK):**
```json
{
    "message": "Book deleted successfully",
    "deleted_book": {
        "id": 1,
        "title": "Deleted Book",
        "publication_year": 2020,
        "author": 1
    }
}
```

---

## Testing with Postman

### Setup:
1. Open Postman
2. Create a new collection: "Advanced API Project"
3. Add environment variables:
   - `base_url`: `http://127.0.0.1:8000`
   - `token`: `YOUR_TOKEN_HERE`

### For Protected Endpoints:
1. Go to "Headers" tab
2. Add header:
   - Key: `Authorization`
   - Value: `Token {{token}}`

### Test Scenarios:

#### Scenario 1: Create and Retrieve
1. POST /api/books/create/ (create a book)
2. GET /api/books/ (verify it appears in list)
3. GET /api/books/{id}/ (retrieve the specific book)

#### Scenario 2: Update and Verify
1. PATCH /api/books/{id}/update/ (update title only)
2. GET /api/books/{id}/ (verify changes)

#### Scenario 3: Permission Testing
1. GET /api/books/ WITHOUT token (should work)
2. POST /api/books/create/ WITHOUT token (should fail with 401)
3. POST /api/books/create/ WITH token (should succeed)

#### Scenario 4: Validation Testing
1. POST /api/books/create/ with future year (should fail)
2. POST /api/books/create/ with year < 1000 (should fail)
3. POST /api/books/create/ with valid year (should succeed)

---

## Expected Test Results Summary

| Endpoint | Method | Auth Required | Expected Status |
|----------|--------|---------------|-----------------|
| /api/books/ | GET | No | 200 OK |
| /api/books/{id}/ | GET | No | 200 OK / 404 |
| /api/books/create/ | POST | Yes | 201 Created / 401 |
| /api/books/{id}/update/ | PUT/PATCH | Yes | 200 OK / 401 |
| /api/books/{id}/delete/ | DELETE | Yes | 200 OK / 401 |

---

## Common Error Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid data (validation error)
- **401 Unauthorized**: Authentication required
- **404 Not Found**: Resource doesn't exist
- **500 Server Error**: Internal server error

---

## Troubleshooting

### Issue: 401 Unauthorized
**Solution:** Make sure you're including the token in the Authorization header

### Issue: 404 Not Found
**Solution:** Check that the book ID exists in the database

### Issue: 400 Bad Request
**Solution:** Verify request body matches required format and passes validation

### Issue: 500 Server Error
**Solution:** Check server logs for detailed error information
