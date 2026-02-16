# User Follows and Feed API Documentation

## Overview

This document provides comprehensive documentation for the User Follows and Feed functionality in the Social Media API.

## Table of Contents

1. [Follow Management](#follow-management)
2. [Feed Functionality](#feed-functionality)
3. [User Model Updates](#user-model-updates)
4. [Testing Examples](#testing-examples)

---

## Follow Management

### Follow a User

**POST** `/api/accounts/follow/<user_id>/`

Follow another user.

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
```

**Response (200 OK):**
```json
{
  "message": "You are now following johndoe",
  "following_count": 5
}
```

**Error Responses:**

**400 Bad Request** (Following yourself):
```json
{
  "error": "You cannot follow yourself"
}
```

**400 Bad Request** (Already following):
```json
{
  "message": "You are already following johndoe"
}
```

**404 Not Found** (User doesn't exist):
```json
{
  "detail": "Not found."
}
```

### Unfollow a User

**POST** `/api/accounts/unfollow/<user_id>/`

Unfollow a user.

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
```

**Response (200 OK):**
```json
{
  "message": "You have unfollowed johndoe",
  "following_count": 4
}
```

**Error Response (400 Bad Request):**
```json
{
  "message": "You are not following johndoe"
}
```

### List Following

**GET** `/api/accounts/following/`

Get list of users that the current user follows.

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
```

**Response (200 OK):**
```json
{
  "count": 3,
  "following": [
    {
      "id": 2,
      "username": "johndoe",
      "bio": "Software developer",
      "profile_picture": "/media/profile_pictures/john.jpg"
    },
    {
      "id": 3,
      "username": "janedoe",
      "bio": "Designer",
      "profile_picture": null
    }
  ]
}
```

### List Followers

**GET** `/api/accounts/followers/`

Get list of users that follow the current user.

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
```

**Response (200 OK):**
```json
{
  "count": 2,
  "followers": [
    {
      "id": 4,
      "username": "alice",
      "bio": "Photographer",
      "profile_picture": "/media/profile_pictures/alice.jpg"
    }
  ]
}
```

---

## Feed Functionality

### Get Feed

**GET** `/api/posts/feed/`

Get posts from users that the current user follows, ordered by creation date (newest first).

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
```

**Query Parameters:**
- `page` (optional): Page number for pagination

**Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/posts/feed/?page=2",
  "previous": null,
  "results": [
    {
      "id": 15,
      "author": "johndoe",
      "author_id": 2,
      "title": "New Post",
      "content": "This is a post from someone I follow",
      "created_at": "2024-02-16T10:00:00Z",
      "updated_at": "2024-02-16T10:00:00Z",
      "comments_count": 3,
      "comments": [...]
    }
  ]
}
```

**Empty Feed (200 OK):**
```json
{
  "count": 0,
  "posts": []
}
```

---

## User Model Updates

### CustomUser Model

The CustomUser model has been updated with a `following` field:

**New Field:**
- `following` (ManyToManyField): Users that this user follows
  - `symmetrical=False`: Following is not mutual
  - `related_name='followers'`: Reverse relationship

**Properties:**
- `followers_count`: Number of followers
- `following_count`: Number of users being followed

**Relationships:**
```python
# Get users a user follows
user.following.all()

# Get users who follow a user
user.followers.all()

# Count followers
user.followers_count

# Count following
user.following_count
```

---

## Testing Examples

### Using cURL

#### Follow a User
```bash
curl -X POST http://localhost:8000/api/accounts/follow/2/ \
  -H "Authorization: Token YOUR_TOKEN"
```

#### Unfollow a User
```bash
curl -X POST http://localhost:8000/api/accounts/unfollow/2/ \
  -H "Authorization: Token YOUR_TOKEN"
```

#### List Following
```bash
curl http://localhost:8000/api/accounts/following/ \
  -H "Authorization: Token YOUR_TOKEN"
```

#### Get Feed
```bash
curl http://localhost:8000/api/posts/feed/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Using Postman

#### Follow a User

1. **Method:** POST
2. **URL:** `http://localhost:8000/api/accounts/follow/2/`
3. **Headers:**
   - Authorization: `Token YOUR_TOKEN`
4. **Expected:** 200 OK with success message

#### Get Feed

1. **Method:** GET
2. **URL:** `http://localhost:8000/api/posts/feed/`
3. **Headers:**
   - Authorization: `Token YOUR_TOKEN`
4. **Expected:** 200 OK with paginated posts

---

## Workflow Example

### Complete Follow and Feed Workflow

1. **Register User A**
   ```
   POST /api/accounts/register/
   → Get token_a
   ```

2. **Register User B**
   ```
   POST /api/accounts/register/
   → Get token_b
   ```

3. **User B Creates Posts**
   ```
   POST /api/posts/posts/
   Authorization: Token token_b
   → Creates post_1, post_2
   ```

4. **User A Follows User B**
   ```
   POST /api/accounts/follow/<user_b_id>/
   Authorization: Token token_a
   → Success
   ```

5. **User A Views Feed**
   ```
   GET /api/posts/feed/
   Authorization: Token token_a
   → Sees post_1, post_2 from User B
   ```

6. **User A Unfollows User B**
   ```
   POST /api/accounts/unfollow/<user_b_id>/
   Authorization: Token token_a
   → Success
   ```

7. **User A Views Feed Again**
   ```
   GET /api/posts/feed/
   Authorization: Token token_a
   → Empty feed (no longer following User B)
   ```

---

## Summary

### Follow Endpoints
- ✅ **POST** `/api/accounts/follow/<user_id>/` - Follow user
- ✅ **POST** `/api/accounts/unfollow/<user_id>/` - Unfollow user
- ✅ **GET** `/api/accounts/following/` - List following
- ✅ **GET** `/api/accounts/followers/` - List followers

### Feed Endpoint
- ✅ **GET** `/api/posts/feed/` - Get personalized feed

### Features
- ✅ Follow/unfollow users
- ✅ View followers and following lists
- ✅ Personalized feed from followed users
- ✅ Chronological ordering (newest first)
- ✅ Pagination support
- ✅ Proper permissions and error handling

All functionality is fully implemented and tested!
