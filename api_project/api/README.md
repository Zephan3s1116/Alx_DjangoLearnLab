# API Authentication and Permissions Documentation

## Overview
This API uses Token Authentication to secure endpoints. All API endpoints require authentication.

## Authentication Setup

### 1. Token Authentication
The API uses Django REST Framework's Token Authentication system.

**Configuration:**
- `rest_framework.authtoken` is added to INSTALLED_APPS
- Token authentication is set as the default authentication class
- All endpoints require authentication by default

### 2. Obtaining a Token

**Endpoint:** `POST /api/auth/token/`

**Request Body:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "token": "your_authentication_token_here"
}
```

### 3. Using the Token

Include the token in the Authorization header of your requests:

**Header:**
```
Authorization: Token your_authentication_token_here
```

**Example with curl:**
```bash
curl -H "Authorization: Token your_token_here" http://127.0.0.1:8000/api/books_all/
```

**Example with Postman:**
1. Go to the "Headers" tab
2. Add a new header:
   - Key: `Authorization`
   - Value: `Token your_token_here`

## Permissions

### IsAuthenticated
All endpoints require users to be authenticated. Unauthenticated requests will receive a `401 Unauthorized` response.

**Endpoints requiring authentication:**
- `GET /api/books/` - List all books
- `GET /api/books_all/` - List all books (ViewSet)
- `POST /api/books_all/` - Create a new book
- `GET /api/books_all/<id>/` - Retrieve a specific book
- `PUT /api/books_all/<id>/` - Update a book
- `PATCH /api/books_all/<id>/` - Partially update a book
- `DELETE /api/books_all/<id>/` - Delete a book

## Testing Authentication

### 1. Create a User
```bash
python manage.py createsuperuser
```

### 2. Obtain a Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'
```

### 3. Access Protected Endpoint
```bash
curl -H "Authorization: Token your_token_here" \
  http://127.0.0.1:8000/api/books_all/
```

### 4. Test Without Token (Should Fail)
```bash
curl http://127.0.0.1:8000/api/books_all/
```
**Expected Response:** `401 Unauthorized`

## Available Endpoints

| Method | Endpoint | Description | Authentication Required |
|--------|----------|-------------|------------------------|
| POST | `/api/auth/token/` | Obtain authentication token | No |
| GET | `/api/books/` | List all books | Yes |
| GET | `/api/books_all/` | List all books (ViewSet) | Yes |
| POST | `/api/books_all/` | Create a new book | Yes |
| GET | `/api/books_all/<id>/` | Retrieve a book | Yes |
| PUT | `/api/books_all/<id>/` | Update a book | Yes |
| PATCH | `/api/books_all/<id>/` | Partially update a book | Yes |
| DELETE | `/api/books_all/<id>/` | Delete a book | Yes |

## Security Notes

1. **Token Storage:** Tokens should be stored securely on the client side
2. **HTTPS:** In production, always use HTTPS to encrypt token transmission
3. **Token Expiration:** Consider implementing token expiration for enhanced security
4. **Permissions:** Additional permission classes can be added for fine-grained access control

## Example Workflow

1. **Create a user account** (if you haven't already)
2. **Obtain a token** by sending your credentials to `/api/auth/token/`
3. **Save the token** securely
4. **Include the token** in all subsequent API requests
5. **Access protected endpoints** with your token

