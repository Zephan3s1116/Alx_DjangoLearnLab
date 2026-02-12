# Django Blog Project

A comprehensive blogging platform built with Django as part of the ALX Django Learning Lab.

## Project Overview

This Django blog application demonstrates fundamental web development concepts including:
- Model-View-Template (MVT) architecture
- Database models and relationships
- Template inheritance and static files
- Django admin interface
- URL routing and views

## Features

- ✅ Create and manage blog posts
- ✅ User authentication and authorization
- ✅ Responsive design with Bootstrap
- ✅ Clean and intuitive admin interface
- ✅ Post listing and detail views
- ✅ Author attribution for posts

## Technology Stack

- **Backend:** Django 4.x (Python)
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Version Control:** Git

## Project Structure

```
django_blog/
├── blog/                          # Main blog application
│   ├── migrations/                # Database migrations
│   ├── static/                    # Static files (CSS, JS, images)
│   │   └── blog/
│   │       ├── css/
│   │       │   └── style.css
│   │       ├── js/
│   │       │   └── script.js
│   │       └── images/
│   ├── templates/                 # HTML templates
│   │   └── blog/
│   │       ├── base.html
│   │       ├── home.html
│   │       └── about.html
│   ├── admin.py                   # Admin configuration
│   ├── models.py                  # Data models
│   ├── views.py                   # View functions
│   ├── urls.py                    # URL patterns
│   └── apps.py                    # App configuration
├── django_blog/                   # Project settings
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL configuration
│   └── wsgi.py                   # WSGI configuration
├── manage.py                      # Django management script
└── README.md                      # This file
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/django_blog
```

### Step 2: Install Dependencies

```bash
pip install django
```

### Step 3: Run Migrations

```bash
python manage.py migrate
```

### Step 4: Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 5: Run the Development Server

```bash
python manage.py runserver
```

The blog will be available at `http://127.0.0.1:8000/`

## Usage

### Accessing the Blog

- **Home Page:** `http://127.0.0.1:8000/`
- **About Page:** `http://127.0.0.1:8000/about/`
- **Admin Panel:** `http://127.0.0.1:8000/admin/`

### Creating Blog Posts

1. Log in to the admin panel at `http://127.0.0.1:8000/admin/`
2. Click on "Posts" under the "Blog" section
3. Click "Add Post"
4. Fill in the title, content, and select an author
5. Click "Save"

### Managing Posts

The admin interface provides comprehensive post management:
- **List View:** See all posts with title, author, and publication date
- **Filters:** Filter posts by date and author
- **Search:** Search posts by title or content
- **Edit:** Click on any post to edit it
- **Delete:** Select posts and use the "Delete selected posts" action

## Models

### Post Model

The `Post` model represents a blog post with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| title | CharField(max_length=200) | The post title |
| content | TextField | The post content |
| published_date | DateTimeField | Auto-generated publication date |
| author | ForeignKey(User) | Reference to the post author |

**Relationships:**
- Each post has one author (User)
- Each author can have multiple posts (one-to-many relationship)

## Templates

### Template Hierarchy

```
base.html                          # Base template with common elements
├── home.html                      # Home page (extends base.html)
└── about.html                     # About page (extends base.html)
```

### Template Features

- **Template Inheritance:** All pages extend `base.html`
- **Static Files:** CSS and JS loaded using `{% static %}` tag
- **Dynamic Content:** Posts displayed using Django template tags
- **Bootstrap Integration:** Responsive design with Bootstrap 5
- **Navigation:** Consistent navigation across all pages

## Static Files

### CSS

- **Location:** `blog/static/blog/css/style.css`
- **Features:**
  - Custom blog post styling
  - Hover effects
  - Responsive design
  - Animations

### JavaScript

- **Location:** `blog/static/blog/js/script.js`
- **Features:**
  - Smooth scrolling
  - Active nav highlighting
  - Alert messages
  - DOM manipulation

## Development

### Running Migrations

After modifying models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating a Superuser

```bash
python manage.py createsuperuser
```

### Running Tests

```bash
python manage.py test blog
```

### Collecting Static Files

For production:

```bash
python manage.py collectstatic
```

## Future Enhancements

Potential features for future development:
- [ ] User registration and authentication
- [ ] Comment system
- [ ] Post categories and tags
- [ ] Search functionality
- [ ] Pagination
- [ ] Rich text editor
- [ ] Image uploads
- [ ] Social media sharing
- [ ] RSS feed
- [ ] Email notifications

## Troubleshooting

### Common Issues

**Issue:** Static files not loading
**Solution:** Run `python manage.py collectstatic` and ensure `STATIC_URL` is configured

**Issue:** Database errors
**Solution:** Delete `db.sqlite3` and run `python manage.py migrate`

**Issue:** Admin panel not accessible
**Solution:** Create a superuser with `python manage.py createsuperuser`

## Contributing

This project is part of the ALX Django Learning Lab. Contributions and improvements are welcome!

## License

This project is created for educational purposes as part of the ALX Django Learning Lab.

## Repository Information

- **GitHub Repository:** `Alx_DjangoLearnLab`
- **Directory:** `django_blog`
- **Task:** Task 0 - Initial Setup and Project Configuration for a Django Blog

## Contact

For questions or support, please refer to the ALX Django Learning Lab resources.

---

**Created with ❤️ as part of ALX Django Learning Lab**

---

## Task 1: User Authentication System

### Overview
Comprehensive user authentication system with registration, login, logout, and profile management.

### Features

#### Authentication
- ✅ User Registration with email
- ✅ User Login/Logout  
- ✅ Profile Management (view and edit)
- ✅ Password Security (Django's built-in hashing)
- ✅ CSRF Protection
- ✅ Login Required Decorator
- ✅ Form Validation
- ✅ Success/Error Messages

### URL Patterns

| URL | View | Purpose | Auth Required |
|-----|------|---------|---------------|
| `/register/` | `register` | Create account | No |
| `/login/` | `user_login` | Login | No |
| `/logout/` | `user_logout` | Logout | Yes |
| `/profile/` | `profile` | Manage profile | Yes |

### Forms

#### CustomUserCreationForm
Extended registration form with:
- Username
- Email (required)
- Password
- Password confirmation

#### UserUpdateForm  
Profile update form with:
- Username
- Email (with uniqueness validation)

### Security Features

1. **Password Hashing**: PBKDF2 algorithm with SHA256
2. **CSRF Protection**: All forms include CSRF tokens
3. **Login Required**: Protected routes with `@login_required`
4. **Form Validation**: Server-side validation for all inputs

### Testing

Run manual tests:
1. Register: http://127.0.0.1:8000/register/
2. Login: http://127.0.0.1:8000/login/
3. Profile: http://127.0.0.1:8000/profile/
4. Logout: Click logout in navbar

Run automated tests:
```bash
python manage.py test blog
```

### Documentation

See [AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md) for:
- Complete authentication flow
- Security measures
- Testing guide
- User guide
- Developer guide

---
