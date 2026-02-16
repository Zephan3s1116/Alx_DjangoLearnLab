# Posts and Comments API Documentation

## Overview

This document provides comprehensive documentation for the Posts and Comments API endpoints in the Social Media API.

## Table of Contents

1. [Authentication](#authentication)
2. [Posts Endpoints](#posts-endpoints)
3. [Comments Endpoints](#comments-endpoints)
4. [Permissions](#permissions)
5. [Filtering and Search](#filtering-and-search)
6. [Pagination](#pagination)
7. [Testing Examples](#testing-examples)

---

## Authentication

All write operations (Create, Update, Delete) require authentication via Token.

**Header:**
```
Authorization: Token YOUR_TOKEN_HERE
```

Read operations (List, Retrieve) are public and don't require authentication.

---

## Posts Endpoints

### List All Posts

**GET** `/api/posts/posts/`

Get a paginated list of all posts.

**Query Parameters:**
- `page` (optional): Page number for pagination
- `search` (optional): Search in title and content
- `ordering` (optional): Order by field (created_at, updated_at, title)
- `author` (optional): Filter by author ID

**Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/posts/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": "johndoe",
      "author_id": 1,
      "title": "My First Post",
      "content": "This is the content of my first post.",
      "created_at": "2024-02-13T10:00:00Z",
      "updated_at": "2024-02-13T10:00:00Z",
      "comments_count": 5,
      "comments": [...]
    }
  ]
}
```

### Create a Post

**POST** `/api/posts/posts/`

Create a new post (requires authentication).

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "My New Post",
  "content": "This is the content of my new post."
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "author": "johndoe",
  "author_id": 1,
  "title": "My New Post",
  "content": "This is the content of my new post.",
  "created_at": "2024-02-13T11:00:00Z",
  "updated_at": "2024-02-13T11:00:00Z",
  "comments_count": 0,
  "comments": []
}
```

### Get a Single Post

**GET** `/api/posts/posts/{id}/`

Retrieve a specific post by ID.

**Response (200 OK):**
```json
{
  "id": 1,
  "author": "johndoe",
  "author_id": 1,
  "title": "My First Post",
  "content": "This is the content of my first post.",
  "created_at": "2024-02-13T10:00:00Z",
  "updated_at": "2024-02-13T10:00:00Z",
  "comments_count": 5,
  "comments": [
    {
      "id": 1,
      "post": 1,
      "author": "janedoe",
      "author_id": 2,
      "content": "Great post!",
      "created_at": "2024-02-13T10:30:00Z",
      "updated_at": "2024-02-13T10:30:00Z"
    }
  ]
}
```

### Update a Post

**PUT/PATCH** `/api/posts/posts/{id}/`

Update an existing post (requires authentication, author only).

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content."
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "author": "johndoe",
  "author_id": 1,
  "title": "Updated Title",
  "content": "Updated content.",
  "created_at": "2024-02-13T10:00:00Z",
  "updated_at": "2024-02-13T12:00:00Z",
  "comments_count": 5,
  "comments": [...]
}
```

### Delete a Post

**DELETE** `/api/posts/posts/{id}/`

Delete a post (requires authentication, author only).

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
```

**Response (204 No Content)**

### Get Comments for a Post

**GET** `/api/posts/posts/{id}/comments/`

Get all comments for a specific post.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "post": 1,
    "author": "janedoe",
    "author_id": 2,
    "content": "Great post!",
    "created_at": "2024-02-13T10:30:00Z",
    "updated_at": "2024-02-13T10:30:00Z"
  }
]
```

---

## Comments Endpoints

### List All Comments

**GET** `/api/posts/comments/`

Get a paginated list of all comments.

**Query Parameters:**
- `page` (optional): Page number
- `post` (optional): Filter by post ID
- `author` (optional): Filter by author ID
- `ordering` (optional): Order by created_at or updated_at

**Response (200 OK):**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/posts/comments/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "post": 1,
      "author": "janedoe",
      "author_id": 2,
      "content": "Great post!",
      "created_at": "2024-02-13T10:30:00Z",
      "updated_at": "2024-02-13T10:30:00Z"
    }
  ]
}
```

### Create a Comment

**POST** `/api/posts/comments/`

Create a new comment (requires authentication).

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
Content-Type: application/json
```

**Request Body:**
```json
{
  "post": 1,
  "content": "This is my comment!"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "post": 1,
  "author": "johndoe",
  "author_id": 1,
  "content": "This is my comment!",
  "created_at": "2024-02-13T11:00:00Z",
  "updated_at": "2024-02-13T11:00:00Z"
}
```

### Get a Single Comment

**GET** `/api/posts/comments/{id}/`

Retrieve a specific comment by ID.

**Response (200 OK):**
```json
{
  "id": 1,
  "post": 1,
  "author": "janedoe",
  "author_id": 2,
  "content": "Great post!",
  "created_at": "2024-02-13T10:30:00Z",
  "updated_at": "2024-02-13T10:30:00Z"
}
```

### Update a Comment

**PUT/PATCH** `/api/posts/comments/{id}/`

Update a comment (requires authentication, author only).

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "Updated comment content."
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "post": 1,
  "author": "janedoe",
  "author_id": 2,
  "content": "Updated comment content.",
  "created_at": "2024-02-13T10:30:00Z",
  "updated_at": "2024-02-13T12:00:00Z"
}
```

### Delete a Comment

**DELETE** `/api/posts/comments/{id}/`

Delete a comment (requires authentication, author only).

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
```

**Response (204 No Content)**

---

## Permissions

### IsAuthenticatedOrReadOnly
- **Read operations** (GET): Public access
- **Write operations** (POST, PUT, PATCH, DELETE): Requires authentication

### IsAuthorOrReadOnly
- Users can only **edit or delete** their own posts and comments
- Attempting to modify another user's content returns **403 Forbidden**

**Example Error (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Filtering and Search

### Search Posts

Search in title and content:

**GET** `/api/posts/posts/?search=django`

### Filter Posts by Author

**GET** `/api/posts/posts/?author=1`

### Filter Comments by Post

**GET** `/api/posts/comments/?post=1`

### Ordering

Order by created_at (ascending):
**GET** `/api/posts/posts/?ordering=created_at`

Order by created_at (descending):
**GET** `/api/posts/posts/?ordering=-created_at`

---

## Pagination

The API uses page number pagination with 10 items per page.

### Navigate Pages

- **Next page:** Use the `next` URL from the response
- **Previous page:** Use the `previous` URL from the response
- **Specific page:** Add `?page=N` to the URL

**Example:**
```
GET /api/posts/posts/?page=2
```

---

## Testing Examples

### Using cURL

#### Create a Post
```bash
curl -X POST http://localhost:8000/api/posts/posts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Post",
    "content": "Post content here"
  }'
```

#### Get All Posts
```bash
curl http://localhost:8000/api/posts/posts/
```

#### Search Posts
```bash
curl "http://localhost:8000/api/posts/posts/?search=django"
```

#### Create a Comment
```bash
curl -X POST http://localhost:8000/api/posts/comments/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "Great post!"
  }'
```

### Using Postman

1. **Set Authorization:**
   - Type: Token
   - Token: YOUR_TOKEN_HERE

2. **Create Post:**
   - Method: POST
   - URL: `http://localhost:8000/api/posts/posts/`
   - Body (JSON):
     ```json
     {
       "title": "Test Post",
       "content": "This is a test."
     }
     ```

3. **Search Posts:**
   - Method: GET
   - URL: `http://localhost:8000/api/posts/posts/?search=test`

4. **Filter by Author:**
   - Method: GET
   - URL: `http://localhost:8000/api/posts/posts/?author=1`

---

## Error Responses

### 400 Bad Request
```json
{
  "title": ["This field is required."],
  "content": ["This field may not be blank."]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Summary

### Posts API
- ✅ List all posts (public, paginated)
- ✅ Create post (authenticated)
- ✅ Retrieve single post (public)
- ✅ Update post (author only)
- ✅ Delete post (author only)
- ✅ Get post comments (public)
- ✅ Search and filter posts
- ✅ Pagination support

### Comments API
- ✅ List all comments (public, paginated)
- ✅ Create comment (authenticated)
- ✅ Retrieve single comment (public)
- ✅ Update comment (author only)
- ✅ Delete comment (author only)
- ✅ Filter by post
- ✅ Pagination support

All CRUD operations are fully functional with proper permissions!
