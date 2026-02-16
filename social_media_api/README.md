# Social Media API

A Django REST Framework-based social media API with user authentication, profiles, and following functionality.

## Project Overview

This API provides core social media features including:
- User registration and authentication
- Token-based authentication
- User profiles with bio and profile pictures
- Following/follower system

## Technology Stack

- **Backend:** Django 4.x, Django REST Framework
- **Database:** SQLite (development)
- **Authentication:** Token-based (REST Framework)

## Project Structure

```
social_media_api/
├── accounts/                   # User authentication app
│   ├── migrations/            # Database migrations
│   ├── models.py              # CustomUser model
│   ├── serializers.py         # API serializers
│   ├── views.py               # API views
│   ├── urls.py                # App URL patterns
│   └── admin.py               # Admin configuration
├── social_media_api/          # Project settings
│   ├── settings.py           # Project settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI configuration
├── manage.py                  # Django management script
└── README.md                  # This file
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api
```

### Step 2: Install Dependencies

```bash
pip install django djangorestframework
```

### Step 3: Run Migrations

```bash
python manage.py migrate
```

### Step 4: Create a Superuser

```bash
python manage.py createsuperuser
```

### Step 5: Start the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication Endpoints

#### Register a New User

**POST** `/api/accounts/register/`

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "bio": "Hello, I'm John!"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Hello, I'm John!"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "User registered successfully"
}
```

#### Login

**POST** `/api/accounts/login/`

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Hello, I'm John!"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "Login successful"
}
```

#### Get User Profile

**GET** `/api/accounts/profile/`

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "bio": "Hello, I'm John!",
  "profile_picture": "/media/profile_pictures/john.jpg",
  "followers_count": 10,
  "following_count": 15,
  "date_joined": "2024-02-13T10:00:00Z"
}
```

#### Update User Profile

**PUT/PATCH** `/api/accounts/profile/`

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Request Body:**
```json
{
  "bio": "Updated bio!",
  "email": "newemail@example.com"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "newemail@example.com",
  "bio": "Updated bio!",
  "profile_picture": "/media/profile_pictures/john.jpg",
  "followers_count": 10,
  "following_count": 15,
  "date_joined": "2024-02-13T10:00:00Z"
}
```

## User Model

### CustomUser Model

The `CustomUser` model extends Django's `AbstractUser` with additional fields:

| Field | Type | Description |
|-------|------|-------------|
| username | CharField | Unique username (inherited) |
| email | EmailField | User's email address (inherited) |
| password | CharField | Hashed password (inherited) |
| bio | TextField | User biography (max 500 chars) |
| profile_picture | ImageField | User's profile picture |
| followers | ManyToManyField | Users who follow this user |
| following | ManyToManyField | Users this user follows (reverse relation) |

### Relationships

- **followers**: Many-to-many relationship representing follower/following connections
- **symmetrical=False**: Following is not mutual (if A follows B, B doesn't automatically follow A)
- **related_name='following'**: Access users that this user follows via `user.following.all()`

## Testing with Postman

### 1. Register a User

1. Create a new POST request to `http://127.0.0.1:8000/api/accounts/register/`
2. Set Body to raw JSON
3. Add user data (username, email, password, password_confirm)
4. Send request
5. Save the token from the response

### 2. Login

1. Create a new POST request to `http://127.0.0.1:8000/api/accounts/login/`
2. Set Body to raw JSON
3. Add username and password
4. Send request
5. Save the token from the response

### 3. Get Profile

1. Create a new GET request to `http://127.0.0.1:8000/api/accounts/profile/`
2. Add Header: `Authorization: Token YOUR_TOKEN_HERE`
3. Send request

### 4. Update Profile

1. Create a new PUT/PATCH request to `http://127.0.0.1:8000/api/accounts/profile/`
2. Add Header: `Authorization: Token YOUR_TOKEN_HERE`
3. Set Body to raw JSON with fields to update
4. Send request

## Authentication

This API uses **Token Authentication**. After registration or login:

1. Save the token provided in the response
2. Include the token in the Authorization header for all authenticated requests:
   ```
   Authorization: Token YOUR_TOKEN_HERE
   ```

## Security Features

- ✅ Password hashing with Django's built-in security
- ✅ Token-based authentication
- ✅ CSRF protection
- ✅ Email validation
- ✅ Password confirmation during registration

## Development

### Running Tests

```bash
python manage.py test accounts
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/`

- View and manage users
- See follower counts
- Manage user data

## Future Enhancements

Planned features for upcoming tasks:
- [ ] Posts and comments
- [ ] Likes and reactions
- [ ] Notifications
- [ ] Search functionality
- [ ] Activity feeds

## Troubleshooting

### Common Issues

**Issue:** Token not working
**Solution:** Ensure you're including `Token ` prefix (with space) before the token value

**Issue:** Permission denied
**Solution:** Check that you're sending the Authorization header with a valid token

**Issue:** User already exists
**Solution:** Use a different username or login with existing credentials

## Repository Information

- **GitHub Repository:** `Alx_DjangoLearnLab`
- **Directory:** `social_media_api`
- **Task:** Task 0 - Project Setup and User Authentication

## License

This project is created for educational purposes as part of the ALX Django Learning Lab.

---

**Created with ❤️ as part of ALX Django Learning Lab**

---

## Task 1: Posts and Comments Functionality

### Overview
Full CRUD operations for posts and comments with filtering, searching, and pagination.

### Features

#### Posts
- ✅ Create posts (authenticated users)
- ✅ List all posts (public, paginated)
- ✅ View single post (public)
- ✅ Update posts (author only)
- ✅ Delete posts (author only)
- ✅ Search posts by title/content
- ✅ Filter posts by author
- ✅ Nested comments in response

#### Comments
- ✅ Create comments (authenticated users)
- ✅ List all comments (public, paginated)
- ✅ View single comment (public)
- ✅ Update comments (author only)
- ✅ Delete comments (author only)
- ✅ Filter comments by post

### API Endpoints

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/api/posts/posts/` | GET | List posts | No |
| `/api/posts/posts/` | POST | Create post | Yes |
| `/api/posts/posts/{id}/` | GET | View post | No |
| `/api/posts/posts/{id}/` | PUT/PATCH | Update post | Author |
| `/api/posts/posts/{id}/` | DELETE | Delete post | Author |
| `/api/posts/posts/{id}/comments/` | GET | Post comments | No |
| `/api/posts/comments/` | GET | List comments | No |
| `/api/posts/comments/` | POST | Create comment | Yes |
| `/api/posts/comments/{id}/` | GET | View comment | No |
| `/api/posts/comments/{id}/` | PUT/PATCH | Update comment | Author |
| `/api/posts/comments/{id}/` | DELETE | Delete comment | Author |

### Permissions

**IsAuthenticatedOrReadOnly:**
- Public can read (GET)
- Authentication required for write (POST, PUT, DELETE)

**IsAuthorOrReadOnly:**
- Only authors can edit/delete their own content
- Returns 403 Forbidden for unauthorized attempts

### Filtering & Search

**Search:**
- `/api/posts/posts/?search=keyword` - Search in title and content

**Filter:**
- `/api/posts/posts/?author=1` - Filter by author
- `/api/posts/comments/?post=1` - Filter comments by post

**Ordering:**
- `/api/posts/posts/?ordering=-created_at` - Newest first
- `/api/posts/posts/?ordering=title` - Alphabetical

### Pagination

- 10 items per page
- Navigate: `?page=2`
- Response includes `next` and `previous` URLs

### Documentation

See [POSTS_API_DOCUMENTATION.md](POSTS_API_DOCUMENTATION.md) for:
- Complete endpoint documentation
- Request/response examples
- Testing examples with cURL and Postman
- Error responses

---

---

## Task 2: User Follows and Feed Functionality

### Overview
Social networking features including follow/unfollow functionality and personalized content feed.

### Features

#### Follow System
- ✅ Follow users
- ✅ Unfollow users
- ✅ View following list
- ✅ View followers list
- ✅ Prevent self-following
- ✅ Check if already following

#### Feed Functionality
- ✅ Personalized feed from followed users
- ✅ Chronological ordering (newest first)
- ✅ Pagination support
- ✅ Empty feed handling

### API Endpoints

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/api/accounts/follow/<user_id>/` | POST | Follow user | Yes |
| `/api/accounts/unfollow/<user_id>/` | POST | Unfollow user | Yes |
| `/api/accounts/following/` | GET | List following | Yes |
| `/api/accounts/followers/` | GET | List followers | Yes |
| `/api/posts/feed/` | GET | Get personalized feed | Yes |

### User Model Updates

**New Field:**
- `following` (ManyToManyField) - Users this user follows
  - Asymmetrical relationship
  - Related name: `followers`

**Properties:**
- `followers_count` - Number of followers
- `following_count` - Number of users being followed

### Feed Algorithm

The feed shows posts from followed users:
1. Gets all users in current user's following list
2. Fetches posts from those users
3. Orders by creation date (newest first)
4. Paginates results (10 per page)

### Documentation

See [FOLLOWS_AND_FEED_DOCUMENTATION.md](FOLLOWS_AND_FEED_DOCUMENTATION.md) for:
- Complete API endpoint documentation
- Request/response examples
- Testing examples with cURL and Postman
- Complete workflow examples

---

---

## Task 3: Notifications and Likes Functionality

### Overview
User engagement features including likes on posts and real-time notifications.

### Features

#### Likes System
- ✅ Like posts
- ✅ Unlike posts
- ✅ View likes count
- ✅ Check if user liked a post
- ✅ Prevent duplicate likes
- ✅ Automatic notifications

#### Notifications
- ✅ Notifications for likes
- ✅ Notifications for comments
- ✅ Notifications for new followers
- ✅ Mark as read
- ✅ Mark all as read
- ✅ Unread first ordering

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/posts/posts/<id>/like/` | POST | Like post |
| `/api/posts/posts/<id>/unlike/` | POST | Unlike post |
| `/api/notifications/` | GET | Get notifications |
| `/api/notifications/<id>/read/` | POST | Mark as read |
| `/api/notifications/read-all/` | POST | Mark all as read |

### Models

**Like Model:**
- `user` - Who liked
- `post` - What was liked
- `unique_together` - No duplicates

**Notification Model:**
- `recipient` - Who receives
- `actor` - Who performed action
- `verb` - What happened
- `target` - GenericForeignKey
- `read` - Read status

### Documentation

See [LIKES_AND_NOTIFICATIONS_DOCUMENTATION.md](LIKES_AND_NOTIFICATIONS_DOCUMENTATION.md)

---
