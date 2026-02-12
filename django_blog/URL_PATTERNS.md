# Blog URL Patterns Documentation

## Overview
This document details all URL patterns used in the Django blog application.

---

## URL Pattern Reference

### Blog Post URLs

| Pattern | Name | View | Method | Description |
|---------|------|------|--------|-------------|
| `/posts/` | `post-list` | PostListView | GET | List all blog posts |
| `/post/<int:pk>/` | `post-detail` | PostDetailView | GET | View single post |
| `/post/new/` | `post-create` | PostCreateView | GET/POST | Create new post |
| `/post/<int:pk>/update/` | `post-update` | PostUpdateView | GET/POST | Update existing post |
| `/post/<int:pk>/delete/` | `post-delete` | PostDeleteView | GET/POST | Delete post |

### Authentication URLs

| Pattern | Name | View | Method | Description |
|---------|------|------|--------|-------------|
| `/register/` | `register` | register | GET/POST | User registration |
| `/login/` | `login` | user_login | GET/POST | User login |
| `/logout/` | `logout` | user_logout | GET | User logout |
| `/profile/` | `profile` | profile | GET/POST | User profile |

### Other URLs

| Pattern | Name | View | Method | Description |
|---------|------|------|--------|-------------|
| `/` | `blog-home` | home | GET | Home page |
| `/about/` | `blog-about` | about | GET | About page |

---

## URL Pattern Examples

### Accessing Posts

**List all posts:**
```
http://127.0.0.1:8000/posts/
```

**View specific post (ID: 1):**
```
http://127.0.0.1:8000/post/1/
```

**Create new post:**
```
http://127.0.0.1:8000/post/new/
```

**Update post (ID: 1):**
```
http://127.0.0.1:8000/post/1/update/
```

**Delete post (ID: 1):**
```
http://127.0.0.1:8000/post/1/delete/
```

---

## URL Naming Conventions

### Why `/post/<int:pk>/` instead of `/posts/<int:pk>/`?

The URL patterns follow Django conventions:
- **Plural for collections:** `/posts/` (list of posts)
- **Singular for individual resources:** `/post/1/` (single post)

This is a common RESTful convention that makes URLs more intuitive.

---

## Using URLs in Templates

### URL Tag Syntax

```django
{% url 'url-name' %}                  <!-- For URLs without parameters -->
{% url 'url-name' object.pk %}        <!-- For URLs with pk parameter -->
```

### Examples

**Link to post list:**
```django
<a href="{% url 'post-list' %}">All Posts</a>
```

**Link to specific post:**
```django
<a href="{% url 'post-detail' post.pk %}">{{ post.title }}</a>
```

**Link to create post:**
```django
<a href="{% url 'post-create' %}">Create New Post</a>
```

**Link to edit post:**
```django
<a href="{% url 'post-update' post.pk %}">Edit</a>
```

**Link to delete post:**
```django
<a href="{% url 'post-delete' post.pk %}">Delete</a>
```

---

## URL Reverse in Views

### Using reverse() and reverse_lazy()

**In views.py:**
```python
from django.urls import reverse, reverse_lazy

# In function-based views
def my_view(request):
    return redirect(reverse('post-list'))

# In class-based views
class PostDeleteView(DeleteView):
    success_url = reverse_lazy('post-list')
```

---

## Common URL Patterns

### Pattern: `<int:pk>`
- Captures an integer value
- Stores it in the `pk` variable
- Used for identifying specific database objects

**Example:**
```python
path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail')
```

Matches:
- ✅ `/post/1/`
- ✅ `/post/123/`
- ❌ `/post/abc/` (not an integer)

---

## Testing URLs

### Manual Testing

**Test in browser:**
```bash
# Start server
python manage.py runserver

# Test each URL:
http://127.0.0.1:8000/posts/
http://127.0.0.1:8000/post/1/
http://127.0.0.1:8000/post/new/
http://127.0.0.1:8000/post/1/update/
http://127.0.0.1:8000/post/1/delete/
```

### Test with curl

```bash
# List posts
curl http://127.0.0.1:8000/posts/

# View post
curl http://127.0.0.1:8000/post/1/

# Create post (requires authentication)
curl -X POST http://127.0.0.1:8000/post/new/ \
  -H "Cookie: sessionid=YOUR_SESSION" \
  -d "title=Test&content=Content"
```

---

## Troubleshooting

### Issue: "Page not found (404)"
**Possible causes:**
- URL pattern doesn't match
- View doesn't exist
- Object with that pk doesn't exist

**Solution:**
- Check URL pattern in `urls.py`
- Verify view is imported correctly
- Check database for object

### Issue: "NoReverseMatch"
**Possible causes:**
- URL name is incorrect
- Missing required parameters
- URL not defined in urlpatterns

**Solution:**
- Check URL name in `urls.py`
- Ensure all parameters are provided
- Verify URL is included in urlpatterns

---

## Summary

### Key Points
- Use `post-list` for listing posts
- Use `post-detail` for individual posts
- Use `post-create` for creating posts
- Use `post-update` for editing posts
- Use `post-delete` for deleting posts

### URL Structure
```
/posts/                    → List
/post/<pk>/                → Detail
/post/new/                 → Create
/post/<pk>/update/         → Update
/post/<pk>/delete/         → Delete
```

All URL patterns are now correctly configured! ✅
