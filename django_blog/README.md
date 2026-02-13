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

---

## Task 2: Blog Post Management Features

### Overview
Comprehensive CRUD operations for blog posts using Django's class-based views with proper permissions and access control.

### Features

#### CRUD Operations
- ✅ **List** all posts (public access)
- ✅ **View** individual posts (public access)
- ✅ **Create** new posts (authenticated users)
- ✅ **Update** posts (post authors only)
- ✅ **Delete** posts (post authors only)

### Class-Based Views

| View | Base Class | Mixins | Access |
|------|------------|--------|--------|
| PostListView | ListView | - | Public |
| PostDetailView | DetailView | - | Public |
| PostCreateView | CreateView | LoginRequiredMixin | Authenticated |
| PostUpdateView | UpdateView | LoginRequiredMixin, UserPassesTestMixin | Author only |
| PostDeleteView | DeleteView | LoginRequiredMixin, UserPassesTestMixin | Author only |

### URL Patterns

| URL | View | Purpose |
|-----|------|---------|
| `/posts/` | PostListView | List all posts |
| `/posts/<int:pk>/` | PostDetailView | View post detail |
| `/posts/new/` | PostCreateView | Create new post |
| `/posts/<int:pk>/edit/` | PostUpdateView | Edit post |
| `/posts/<int:pk>/delete/` | PostDeleteView | Delete post |

### Permissions

**LoginRequiredMixin:**
- Applied to Create, Update, Delete views
- Redirects to login if not authenticated

**UserPassesTestMixin:**
- Applied to Update and Delete views
- Verifies user is post author
- Returns 403 Forbidden if not author

### Templates

- `post_list.html` - Paginated list of all posts
- `post_detail.html` - Full post content with actions
- `post_form.html` - Create/edit form (reusable)
- `post_confirm_delete.html` - Delete confirmation

### Testing

Run CRUD tests:
```bash
python manage.py test blog.test_post_crud
```

### Documentation

See [BLOG_POST_MANAGEMENT.md](BLOG_POST_MANAGEMENT.md) for:
- Complete view documentation
- Permission system details
- Usage guide
- Testing guide
- Developer guide

---

---

## Task 3: Comment Functionality

### Overview
Comprehensive comment system for blog posts with full CRUD operations and proper permissions.

### Features

#### Comment Operations
- ✅ **Create** comments (authenticated users)
- ✅ **Read** comments (public access)
- ✅ **Update** comments (comment authors only)
- ✅ **Delete** comments (comment authors only)

### Models

#### Comment Model
- `post` (ForeignKey to Post)
- `author` (ForeignKey to User)
- `content` (TextField)
- `created_at` (DateTimeField, auto)
- `updated_at` (DateTimeField, auto)

### Views

| View | Mixins | Access |
|------|--------|--------|
| CommentCreateView | LoginRequiredMixin | Authenticated |
| CommentUpdateView | LoginRequiredMixin, UserPassesTestMixin | Author only |
| CommentDeleteView | LoginRequiredMixin, UserPassesTestMixin | Author only |

### URL Patterns

| URL | Purpose |
|-----|---------|
| `/post/<int:pk>/comments/new/` | Create comment |
| `/comment/<int:pk>/update/` | Edit comment |
| `/comment/<int:pk>/delete/` | Delete comment |

### Templates

- `post_detail.html` (updated) - Displays comments and form
- `comment_form.html` - Create/edit comment
- `comment_confirm_delete.html` - Delete confirmation

### Testing

Run comment tests:
```bash
python manage.py test blog.test_comments
```

### Documentation

See [COMMENT_SYSTEM.md](COMMENT_SYSTEM.md) for:
- Complete feature documentation
- Usage guide
- API examples
- Security details

---

---

## Task 4: Tagging and Search Functionality

### Overview
Advanced tagging and search capabilities using django-taggit and Django's Q objects.

### Features

#### Tagging System
- ✅ Add multiple tags to posts (comma-separated)
- ✅ View all posts with specific tag
- ✅ Tags displayed on post listings
- ✅ Clickable tag badges
- ✅ Automatic tag creation

#### Search System
- ✅ Search across titles, content, and tags
- ✅ Search bar in navigation
- ✅ Dedicated search results page
- ✅ Result count display
- ✅ Django Q objects for complex queries

### Implementation

**django-taggit:**
```bash
pip install django-taggit
```

**Post Model:**
```python
from taggit.managers import TaggableManager

class Post(models.Model):
    tags = TaggableManager(blank=True)
```

**Search with Q Objects:**
```python
posts = Post.objects.filter(
    Q(title__icontains=query) |
    Q(content__icontains=query) |
    Q(tags__name__icontains=query)
).distinct()
```

### URL Patterns

| URL | Purpose |
|-----|---------|
| `/search/` | Search posts |
| `/tags/<slug>/` | Filter by tag |

### Templates

- `search_results.html` - Search results display
- `posts_by_tag.html` - Posts filtered by tag
- Updated `base.html` with search bar

### Documentation

See [TAGGING_AND_SEARCH.md](TAGGING_AND_SEARCH.md) for complete documentation.

---

**All Django Blog Tasks Complete!** 🎉

The blog now includes:
- ✅ User authentication
- ✅ Blog post CRUD operations
- ✅ Comment functionality
- ✅ Tagging system
- ✅ Search functionality
