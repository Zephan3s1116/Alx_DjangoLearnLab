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
