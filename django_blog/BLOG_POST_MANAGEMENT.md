# Blog Post Management Documentation

## Overview
Comprehensive CRUD (Create, Read, Update, Delete) operations for blog posts using Django's class-based views with proper permissions and access control.

---

## Table of Contents
1. [Features](#features)
2. [Class-Based Views](#class-based-views)
3. [URL Patterns](#url-patterns)
4. [Permissions](#permissions)
5. [Templates](#templates)
6. [Usage Guide](#usage-guide)
7. [Testing](#testing)

---

## Features

### Implemented Features
- ✅ List all blog posts (public access)
- ✅ View individual post details (public access)
- ✅ Create new posts (authenticated users only)
- ✅ Edit own posts (post authors only)
- ✅ Delete own posts (post authors only)
- ✅ Pagination (5 posts per page)
- ✅ Author attribution
- ✅ Success/error messages
- ✅ Responsive design

---

## Class-Based Views

### 1. PostListView (ListView)
**Purpose:** Display all blog posts

**Attributes:**
- `model`: Post
- `template_name`: 'blog/post_list.html'
- `context_object_name`: 'posts'
- `ordering`: ['-published_date']
- `paginate_by`: 5

**Access:** Public (no authentication required)

**Features:**
- Ordered by publication date (newest first)
- Pagination (5 posts per page)
- Shows edit/delete buttons for post authors

### 2. PostDetailView (DetailView)
**Purpose:** Display single blog post with full content

**Attributes:**
- `model`: Post
- `template_name`: 'blog/post_detail.html'
- `context_object_name`: 'post'

**Access:** Public (no authentication required)

**Features:**
- Full post content
- Author information
- Publication date
- Edit/delete buttons for post author

### 3. PostCreateView (CreateView)
**Purpose:** Allow authenticated users to create new posts

**Mixins:**
- `LoginRequiredMixin`: Requires authentication

**Attributes:**
- `model`: Post
- `fields`: ['title', 'content']
- `template_name`: 'blog/post_form.html'

**Access:** Authenticated users only

**Features:**
- Automatically sets author to current user
- Form validation
- Success message
- Redirects to post detail after creation

**Methods:**
```python
def form_valid(self, form):
    form.instance.author = self.request.user
    messages.success(self.request, 'Your post has been created!')
    return super().form_valid(form)
```

### 4. PostUpdateView (UpdateView)
**Purpose:** Allow post authors to edit their posts

**Mixins:**
- `LoginRequiredMixin`: Requires authentication
- `UserPassesTestMixin`: Requires post ownership

**Attributes:**
- `model`: Post
- `fields`: ['title', 'content']
- `template_name`: 'blog/post_form.html'

**Access:** Post author only

**Features:**
- Pre-fills form with existing data
- Verifies user is post author
- Success message
- Redirects to post detail after update

**Methods:**
```python
def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
```

### 5. PostDeleteView (DeleteView)
**Purpose:** Allow post authors to delete their posts

**Mixins:**
- `LoginRequiredMixin`: Requires authentication
- `UserPassesTestMixin`: Requires post ownership

**Attributes:**
- `model`: Post
- `template_name`: 'blog/post_confirm_delete.html'
- `success_url`: reverse_lazy('blog-home')

**Access:** Post author only

**Features:**
- Confirmation page before deletion
- Verifies user is post author
- Success message
- Redirects to home after deletion

**Methods:**
```python
def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
```

---

## URL Patterns

### CRUD URLs

| URL | View | Name | Method | Auth | Owner Only |
|-----|------|------|--------|------|------------|
| `/posts/` | PostListView | post-list | GET | No | No |
| `/posts/<int:pk>/` | PostDetailView | post-detail | GET | No | No |
| `/posts/new/` | PostCreateView | post-create | GET/POST | Yes | No |
| `/posts/<int:pk>/edit/` | PostUpdateView | post-update | GET/POST | Yes | Yes |
| `/posts/<int:pk>/delete/` | PostDeleteView | post-delete | GET/POST | Yes | Yes |

### URL Configuration
```python
urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
```

---

## Permissions

### Permission Matrix

| View | Authentication | Ownership | Implementation |
|------|---------------|-----------|----------------|
| PostListView | Not required | N/A | Public access |
| PostDetailView | Not required | N/A | Public access |
| PostCreateView | Required | N/A | `LoginRequiredMixin` |
| PostUpdateView | Required | Required | `LoginRequiredMixin` + `UserPassesTestMixin` |
| PostDeleteView | Required | Required | `LoginRequiredMixin` + `UserPassesTestMixin` |

### Implementation Details

#### LoginRequiredMixin
```python
class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'  # Redirect to login if not authenticated
```

#### UserPassesTestMixin
```python
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Only author can edit
```

### Access Control Flow

```
User attempts to access view
    ↓
LoginRequiredMixin checks authentication
    ↓
If not authenticated → Redirect to login
If authenticated → Continue
    ↓
UserPassesTestMixin runs test_func()
    ↓
If test passes → Allow access
If test fails → 403 Forbidden
```

---

## Templates

### Template Structure
```
blog/templates/blog/
├── post_list.html          # List all posts
├── post_detail.html        # View single post
├── post_form.html          # Create/edit form
└── post_confirm_delete.html # Delete confirmation
```

### Template Features

#### post_list.html
- Lists all posts with pagination
- Shows title, author, date, and excerpt
- Edit/delete buttons for post owners
- "Create New Post" button for authenticated users
- Responsive design with Bootstrap cards

#### post_detail.html
- Displays full post content
- Shows author and publication date
- Edit/delete buttons for post owner
- "Back to All Posts" link

#### post_form.html
- Reusable form for create and edit
- Title field (max 200 characters)
- Content field (textarea)
- CSRF protection
- Form validation errors
- Cancel and submit buttons

#### post_confirm_delete.html
- Shows post preview
- Warning message about permanent deletion
- Confirm and cancel buttons
- CSRF protection

---

## Usage Guide

### For End Users

#### Viewing Posts
1. Navigate to home page or `/posts/`
2. Browse list of all posts
3. Click post title or "Read More" to view full post

#### Creating a Post
1. Log in to your account
2. Click "New Post" in navigation or "Create New Post" button
3. Fill in title and content
4. Click "Create Post"
5. You'll be redirected to your new post

#### Editing a Post
1. Navigate to your post
2. Click "Edit Post" button (only visible to post author)
3. Modify title or content
4. Click "Update Post"
5. You'll be redirected to the updated post

#### Deleting a Post
1. Navigate to your post
2. Click "Delete Post" button (only visible to post author)
3. Confirm deletion on the confirmation page
4. Post will be permanently deleted

### For Developers

#### Adding New Fields to Post Model
```python
# blog/models.py
class Post(models.Model):
    # ... existing fields
    featured_image = models.ImageField(upload_to='post_images/', blank=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
```

#### Customizing Views
```python
# blog/views.py
class PostListView(ListView):
    def get_queryset(self):
        # Custom filtering
        return Post.objects.filter(published=True)
    
    def get_context_data(self, **kwargs):
        # Add custom context
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.objects.order_by('-views')[:5]
        return context
```

---

## Testing

### Manual Testing

#### Test 1: List Posts (Public)
```
1. Open browser (logged out)
2. Navigate to http://127.0.0.1:8000/posts/
3. Expected: See list of all posts
4. Expected: No edit/delete buttons
```

#### Test 2: View Post Detail (Public)
```
1. Open browser (logged out)
2. Navigate to http://127.0.0.1:8000/posts/1/
3. Expected: See full post content
4. Expected: No edit/delete buttons
```

#### Test 3: Create Post (Authenticated)
```
1. Log in to account
2. Click "New Post" in navigation
3. Fill in:
   - Title: "Test Post"
   - Content: "This is a test post."
4. Click "Create Post"
5. Expected: Redirect to new post detail page
6. Expected: Success message displayed
```

#### Test 4: Edit Post (Author Only)
```
1. Log in as post author
2. Navigate to your post
3. Click "Edit Post"
4. Change title to "Updated Test Post"
5. Click "Update Post"
6. Expected: Post updated
7. Expected: Success message displayed
```

#### Test 5: Edit Post (Unauthorized)
```
1. Log in as different user
2. Try to navigate to http://127.0.0.1:8000/posts/1/edit/
3. Expected: 403 Forbidden error
```

#### Test 6: Delete Post (Author Only)
```
1. Log in as post author
2. Navigate to your post
3. Click "Delete Post"
4. Confirm deletion
5. Expected: Post deleted
6. Expected: Redirect to home
7. Expected: Success message displayed
```

#### Test 7: Delete Post (Unauthorized)
```
1. Log in as different user
2. Try to navigate to http://127.0.0.1:8000/posts/1/delete/
3. Expected: 403 Forbidden error
```

#### Test 8: Pagination
```
1. Create 10+ posts
2. Navigate to /posts/
3. Expected: Only 5 posts per page
4. Expected: Pagination controls visible
5. Click "Next"
6. Expected: Next 5 posts displayed
```

### Automated Testing

Create `blog/test_post_crud.py`:
```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post

class PostCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user1
        )
    
    def test_post_list_view(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
    
    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
    
    def test_post_create_requires_login(self):
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_post_create_authenticated(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('post-create'), {
            'title': 'New Post',
            'content': 'New content'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Post.objects.filter(title='New Post').exists())
    
    def test_post_update_author_only(self):
        # Login as author
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('post-update', args=[self.post.pk]), {
            'title': 'Updated Title',
            'content': 'Updated content'
        })
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
    
    def test_post_update_non_author_forbidden(self):
        # Login as different user
        self.client.login(username='user2', password='pass123')
        response = self.client.get(reverse('post-update', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_post_delete_author_only(self):
        # Login as author
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('post-delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
    
    def test_post_delete_non_author_forbidden(self):
        # Login as different user
        self.client.login(username='user2', password='pass123')
        response = self.client.get(reverse('post-delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)  # Forbidden
```

Run tests:
```bash
python manage.py test blog.test_post_crud
```

---

## Summary

### Completed Features
✅ Class-based views for all CRUD operations  
✅ Public access to list and detail views  
✅ Authentication required for create  
✅ Author-only access for edit and delete  
✅ Responsive Bootstrap templates  
✅ Pagination support  
✅ Success/error messaging  
✅ CSRF protection  
✅ Comprehensive documentation  
✅ Automated tests  

### Security Features
✅ `LoginRequiredMixin` for authenticated access  
✅ `UserPassesTestMixin` for ownership verification  
✅ CSRF tokens in all forms  
✅ Proper HTTP method handling  
✅ 403 Forbidden for unauthorized access  

All blog post management features are fully functional and tested!
