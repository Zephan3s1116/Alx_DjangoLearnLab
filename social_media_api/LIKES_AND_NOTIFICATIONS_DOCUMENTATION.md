# Likes and Notifications API Documentation

## Overview

Complete documentation for the Likes and Notifications functionality in the Social Media API.

## Table of Contents

1. [Likes Functionality](#likes-functionality)
2. [Notifications System](#notifications-system)
3. [Models](#models)
4. [Testing Examples](#testing-examples)

---

## Likes Functionality

### Like a Post

**POST** `/api/posts/posts/<post_id>/like/`

Like a post and create a notification for the post author.

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**Response (200 OK):**
```json
{
  "message": "Post liked successfully"
}
```

**Error (400 Bad Request):**
```json
{
  "message": "You already liked this post"
}
```

### Unlike a Post

**POST** `/api/posts/posts/<post_id>/unlike/`

Remove your like from a post.

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**Response (200 OK):**
```json
{
  "message": "Post unliked successfully"
}
```

**Error (400 Bad Request):**
```json
{
  "message": "You have not liked this post"
}
```

### View Post with Like Info

**GET** `/api/posts/posts/<post_id>/`

**Response:**
```json
{
  "id": 1,
  "author": "johndoe",
  "title": "My Post",
  "content": "Post content",
  "likes_count": 5,
  "is_liked": true,
  "comments_count": 3
}
```

---

## Notifications System

### Get All Notifications

**GET** `/api/notifications/`

Get all notifications for the authenticated user (unread first).

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**Response (200 OK):**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "actor": "janedoe",
      "verb": "liked your post",
      "timestamp": "2024-02-16T10:00:00Z",
      "read": false
    },
    {
      "id": 2,
      "actor": "bob",
      "verb": "commented on your post",
      "timestamp": "2024-02-16T09:00:00Z",
      "read": true
    }
  ]
}
```

### Mark Notification as Read

**POST** `/api/notifications/<notification_id>/read/`

Mark a specific notification as read.

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**Response (200 OK):**
```json
{
  "message": "Notification marked as read"
}
```

### Mark All Notifications as Read

**POST** `/api/notifications/read-all/`

Mark all notifications as read.

**Headers:**
```
Authorization: Token YOUR_TOKEN
```

**Response (200 OK):**
```json
{
  "message": "All notifications marked as read"
}
```

---

## Models

### Like Model

```python
class Like(models.Model):
    user = ForeignKey(User)
    post = ForeignKey(Post)
    created_at = DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
```

**Features:**
- Ensures a user can only like a post once
- Tracks when the like was created

### Notification Model

```python
class Notification(models.Model):
    recipient = ForeignKey(User)  # Who receives the notification
    actor = ForeignKey(User)      # Who performed the action
    verb = CharField()             # What action was performed
    target = GenericForeignKey()  # What object was affected
    timestamp = DateTimeField()
    read = BooleanField()
```

**Notification Types:**
- "liked your post"
- "commented on your post"
- "started following you"

---

## Testing Examples

### Like a Post

```bash
curl -X POST http://localhost:8000/api/posts/posts/1/like/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Unlike a Post

```bash
curl -X POST http://localhost:8000/api/posts/posts/1/unlike/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Get Notifications

```bash
curl http://localhost:8000/api/notifications/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Mark Notification as Read

```bash
curl -X POST http://localhost:8000/api/notifications/1/read/ \
  -H "Authorization: Token YOUR_TOKEN"
```

---

## Complete Workflow

1. **User A creates a post**
   ```
   POST /api/posts/posts/
   ```

2. **User B likes the post**
   ```
   POST /api/posts/posts/1/like/
   → Creates Like
   → Creates Notification for User A
   ```

3. **User A checks notifications**
   ```
   GET /api/notifications/
   → Sees "User B liked your post"
   ```

4. **User A marks notification as read**
   ```
   POST /api/notifications/1/read/
   ```

5. **User B unlikes the post**
   ```
   POST /api/posts/posts/1/unlike/
   → Deletes Like
   ```

---

## Summary

✅ Like/unlike posts  
✅ Automatic notification creation  
✅ View all notifications  
✅ Mark notifications as read  
✅ Prevent duplicate likes  
✅ Unread notifications shown first  

All features fully implemented and tested!
