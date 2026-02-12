# User Authentication System Documentation

## Overview
This Django blog project includes a comprehensive user authentication system that enables user registration, login, logout, and profile management with secure password handling and CSRF protection.

---

## Table of Contents
1. [Features](#features)
2. [Authentication Flow](#authentication-flow)
3. [Security Measures](#security-measures)
4. [URL Patterns](#url-patterns)
5. [Views and Forms](#views-and-forms)
6. [Templates](#templates)
7. [Testing Guide](#testing-guide)
8. [User Guide](#user-guide)

---

## Features

### Implemented Features
- ✅ User Registration with email
- ✅ User Login/Logout
- ✅ Profile Management (view and edit)
- ✅ Password Security (Django's built-in hashing)
- ✅ CSRF Protection
- ✅ Login Required Decorator
- ✅ Form Validation
- ✅ Success/Error Messages
- ✅ Responsive Design

---

## Authentication Flow

### 1. Registration Flow
```
User visits /register/
    ↓
Fills registration form (username, email, password)
    ↓
Form validation (checks username uniqueness, password strength, email format)
    ↓
If valid:
    - Create new user
    - Hash password
    - Save to database
    - Redirect to login with success message
If invalid:
    - Display form errors
    - Keep user data (except passwords)
```

### 2. Login Flow
```
User visits /login/
    ↓
Fills login form (username, password)
    ↓
Django authenticates credentials
    ↓
If valid:
    - Create session
    - Redirect to home (or 'next' parameter)
    - Display welcome message
If invalid:
    - Display error message
    - Keep username in form
```

### 3. Profile Management Flow
```
Authenticated user visits /profile/
    ↓
Views current profile information
    ↓
Edits username or email
    ↓
Submits form
    ↓
Form validation
    ↓
If valid:
    - Update user information
    - Display success message
    - Reload profile page
If invalid:
    - Display error messages
    - Keep form data
```

### 4. Logout Flow
```
Authenticated user clicks logout
    ↓
Session destroyed
    ↓
Redirect to home page
    ↓
Display logout message
```

---

## Security Measures

### 1. Password Security
**Django's Built-in Password Hashing:**
- Uses PBKDF2 algorithm with SHA256 hash
- Automatically salts passwords
- Passwords are never stored in plain text

**Password Validation:**
- Minimum length requirement
- Cannot be too similar to username
- Cannot be entirely numeric
- Cannot be a commonly used password

### 2. CSRF Protection
**Implementation:**
- All forms include `{% csrf_token %}`
- Django validates CSRF token on POST requests
- Prevents Cross-Site Request Forgery attacks

**Example:**
```html
<form method="POST">
    {% csrf_token %}
    <!-- Form fields -->
</form>
```

### 3. Login Required Decorator
**Protects sensitive views:**
```python
@login_required(login_url='login')
def profile(request):
    # Only accessible to logged-in users
    ...
```

### 4. Form Validation
**Server-side validation:**
- Username uniqueness
- Email format
- Email uniqueness (in profile update)
- Password strength
- Password confirmation match

---

## URL Patterns

### Authentication URLs

| URL | View | Purpose | Auth Required |
|-----|------|---------|---------------|
| `/register/` | `register` | User registration | No |
| `/login/` | `user_login` | User login | No |
| `/logout/` | `user_logout` | User logout | Yes |
| `/profile/` | `profile` | Profile management | Yes |

### URL Configuration
```python
# blog/urls.py
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
```

---

## Views and Forms

### Views

#### 1. Register View
```python
@csrf_protect
def register(request):
    """
    Handle user registration.
    - GET: Display form
    - POST: Create user account
    """
```

**Features:**
- Redirects if already authenticated
- Custom registration form with email
- Success message on registration
- Redirects to login after successful registration

#### 2. Login View
```python
@csrf_protect
def user_login(request):
    """
    Handle user login.
    - GET: Display login form
    - POST: Authenticate and login user
    """
```

**Features:**
- Uses Django's AuthenticationForm
- Redirects if already authenticated
- Supports 'next' parameter for redirect after login
- Welcome message on successful login

#### 3. Logout View
```python
@login_required(login_url='login')
def user_logout(request):
    """
    Handle user logout.
    """
```

**Features:**
- Requires authentication
- Destroys session
- Logout message
- Redirects to home

#### 4. Profile View
```python
@login_required(login_url='login')
@csrf_protect
def profile(request):
    """
    Handle profile viewing and editing.
    - GET: Display profile
    - POST: Update profile
    """
```

**Features:**
- Requires authentication
- Pre-fills form with current data
- Validates email uniqueness
- Success message on update

### Forms

#### 1. CustomUserCreationForm
```python
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
```

**Features:**
- Extends Django's UserCreationForm
- Adds required email field
- Bootstrap styling
- Custom placeholders

#### 2. UserUpdateForm
```python
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email')
```

**Features:**
- Updates username and email
- Email uniqueness validation
- Bootstrap styling

---

## Templates

### Template Structure
```
blog/templates/blog/
├── base.html           # Base template with nav (shows auth links)
├── login.html          # Login form
├── register.html       # Registration form
└── profile.html        # Profile management
```

### Template Features

#### 1. base.html
**Authentication Navigation:**
- Shows different links for authenticated vs unauthenticated users
- Authenticated: Profile, Logout, (Admin if staff)
- Unauthenticated: Login, Register

#### 2. login.html
**Features:**
- Bootstrap-styled login form
- Error message display
- Link to registration
- CSRF token

#### 3. register.html
**Features:**
- Bootstrap-styled registration form
- Field validation errors
- Help text for each field
- Link to login
- CSRF token

#### 4. profile.html
**Features:**
- Profile update form
- Account information sidebar
- Success/error messages
- Logout button
- CSRF token

---

## Testing Guide

### Manual Testing

#### Test 1: User Registration
```
1. Navigate to http://127.0.0.1:8000/register/
2. Fill in:
   - Username: testuser
   - Email: test@example.com
   - Password: SecurePass123!
   - Confirm Password: SecurePass123!
3. Click "Sign Up"
4. Expected: Redirect to login with success message
```

#### Test 2: Login
```
1. Navigate to http://127.0.0.1:8000/login/
2. Enter credentials from Test 1
3. Click "Login"
4. Expected: Redirect to home with welcome message
5. Expected: Navbar shows "testuser" and "Logout" link
```

#### Test 3: Profile Update
```
1. While logged in, navigate to http://127.0.0.1:8000/profile/
2. Change email to newemail@example.com
3. Click "Update Profile"
4. Expected: Success message, email updated in sidebar
```

#### Test 4: Logout
```
1. Click "Logout" in navbar
2. Expected: Redirect to home with logout message
3. Expected: Navbar shows "Login" and "Register"
```

#### Test 5: Protected Routes
```
1. Logout if logged in
2. Navigate to http://127.0.0.1:8000/profile/
3. Expected: Redirect to login page
```

#### Test 6: Form Validation
```
Registration validation:
- Try registering with existing username → Error
- Try weak password → Error  
- Try non-matching passwords → Error
- Try invalid email format → Error

Profile validation:
- Try email already in use → Error
```

### Automated Testing

Create `blog/tests.py`:
```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
```

Run tests:
```bash
python manage.py test blog
```

---

## User Guide

### For End Users

#### How to Create an Account
1. Click "Register" in the navigation bar
2. Fill in the form:
   - Choose a unique username
   - Provide a valid email address
   - Create a strong password
   - Confirm your password
3. Click "Sign Up"
4. You'll be redirected to the login page

#### How to Login
1. Click "Login" in the navigation bar
2. Enter your username and password
3. Click "Login"
4. You'll be redirected to the home page

#### How to Update Your Profile
1. While logged in, click your username in the navigation bar
2. Or navigate to the "Profile" link
3. Update your username or email
4. Click "Update Profile"
5. Your changes will be saved

#### How to Logout
1. Click "Logout" in the navigation bar
2. You'll be logged out and redirected to the home page

### For Developers

#### Adding New Authentication Fields

**1. Extend the User model:**
```python
# blog/models.py
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
```

**2. Update forms:**
```python
# blog/forms.py
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture')
```

**3. Update views and templates accordingly**

---

## Troubleshooting

### Common Issues

#### Issue: "CSRF verification failed"
**Solution:**
- Ensure `{% csrf_token %}` is in all POST forms
- Check that CSRF middleware is enabled in settings

#### Issue: "User already exists"
**Solution:**
- Each username must be unique
- Try a different username

#### Issue: "Password too weak"
**Solution:**
- Password must be at least 8 characters
- Cannot be too similar to username
- Cannot be entirely numeric
- Cannot be a common password

#### Issue: "Email already in use"
**Solution:**
- Email addresses must be unique in profile updates
- Use a different email address

---

## Security Best Practices

1. **Never display passwords in templates**
2. **Always use HTTPS in production**
3. **Keep Django SECRET_KEY secret**
4. **Use environment variables for sensitive data**
5. **Regularly update Django and dependencies**
6. **Implement rate limiting for login attempts**
7. **Add email verification for registration**
8. **Implement password reset functionality**

---

## Summary

The authentication system provides:
- ✅ Secure user registration and login
- ✅ Profile management
- ✅ Password hashing with Django's built-in security
- ✅ CSRF protection
- ✅ Form validation
- ✅ User-friendly interface
- ✅ Comprehensive error handling

All authentication features are fully functional and tested!
