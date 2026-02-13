# Comment System Documentation

## Overview
Comprehensive comment functionality for blog posts allowing users to read, create, edit, and delete comments with proper authentication and permissions.

---

## Table of Contents
1. [Features](#features)
2. [Models](#models)
3. [Forms](#forms)
4. [Views](#views)
5. [Templates](#templates)
6. [URL Patterns](#url-patterns)
7. [Permissions](#permissions)
8. [Usage Guide](#usage-guide)
9. [Testing](#testing)

---

## Features

### Implemented Features
- ✅ Create comments on blog posts (authenticated users)
- ✅ Read/view all comments on a post (public access)
- ✅ Edit own comments (comment authors only)
- ✅ Delete own comments (comment authors only)
- ✅ Display comment count
- ✅ Show edit timestamps
- ✅ Author badges (post author identification)
- ✅ Responsive design

---

## Models

### Comment Model

**Fields:**
- `post` (ForeignKey to Post) - The blog post being commented on
- `author` (ForeignKey to User) - The user who wrote the comment
- `content` (TextField) - The comment text
- `created_at` (DateTimeField) - When the comment was created
- `updated_at` (DateTimeField) - When the comment was last updated

**Methods:**
- `__str__()` - Returns "Comment by {username} on {post_title}"
- `get_absolute_url()` - Returns URL to the post detail page

**Meta:**
- Ordering: `['created_at']` (oldest first)

**Relationships:**
- Many-to-one with Post (many comments per post)
- Many-to-one with User (many comments per user)

---

## Forms

### CommentForm

**Fields:**
- `content` - Textarea for comment text

**Validation:**
- Content is required
- No maximum length (TextField)

**Bootstrap Styling:**
- Form control classes
- Placeholder text
- 4-row textarea

---

## Views

### 1. CommentCreateView (CreateView)

**Purpose:** Create new comments on blog posts

**Mixins:**
- `LoginRequiredMixin` - Requires authentication

**Features:**
- Auto-sets post from URL parameter
- Auto-sets author to current user
- Success message
- Redirects to post detail page

**Template:** `blog/comment_form.html`

### 2. CommentUpdateView (UpdateView)

**Purpose:** Edit existing comments

**Mixins:**
- `LoginRequiredMixin` - Requires authentication
- `UserPassesTestMixin` - Requires comment ownership

**Features:**
- Pre-fills form with current content
- Verifies user is comment author
- Success message
- Redirects to post detail page

**Template:** `blog/comment_form.html`

### 3. CommentDeleteView (DeleteView)

**Purpose:** Delete comments

**Mixins:**
- `LoginRequiredMixin` - Requires authentication
- `UserPassesTestMixin` - Requires comment ownership

**Features:**
- Confirmation page
- Verifies user is comment author
- Success message
- Redirects to post detail page

**Template:** `blog/comment_confirm_delete.html`

---

## Templates

### post_detail.html (Updated)

**Features:**
- Displays all comments for the post
- Shows comment count
- Comment form for authenticated users
- Login prompt for unauthenticated users
- Edit/delete buttons for comment authors
- Author badge for post author
- Edit timestamp display

### comment_form.html

**Features:**
- Reusable for create and edit
- Shows post title being commented on
- Cancel and submit buttons
- Different heading for create vs edit

### comment_confirm_delete.html

**Features:**
- Shows comment preview
- Warning message
- Confirms deletion
- Cancel and delete buttons

---

## URL Patterns

### Comment URLs

| URL | View | Name | Method | Auth | Owner |
|-----|------|------|--------|------|-------|
| `/post/<int:pk>/comments/new/` | CommentCreateView | comment-create | GET/POST | Yes | No |
| `/comment/<int:pk>/update/` | CommentUpdateView | comment-update | GET/POST | Yes | Yes |
| `/comment/<int:pk>/delete/` | CommentDeleteView | comment-delete | GET/POST | Yes | Yes |

---

## Permissions

### Permission Matrix

| Action | Authentication | Ownership | Implementation |
|--------|---------------|-----------|----------------|
| View comments | Not required | N/A | Public access on post detail |
| Create comment | Required | N/A | `LoginRequiredMixin` |
| Edit comment | Required | Required | `LoginRequiredMixin` + `UserPassesTestMixin` |
| Delete comment | Required | Required | `LoginRequiredMixin` + `UserPassesTestMixin` |

### Permission Implementation

```python
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
```

---

## Usage Guide

### For End Users

#### Viewing Comments
1. Navigate to any blog post
2. Scroll down to the comments section
3. See all comments and comment count

#### Posting a Comment
1. Log in to your account
2. Navigate to a blog post
3. Scroll to the comment form
4. Write your comment
5. Click "Post Comment"
6. Your comment appears at the bottom

#### Editing a Comment
1. Find your comment on the post
2. Click "Edit" button (only visible to you)
3. Modify the content
4. Click "Update Comment"
5. The comment is updated with "edited" timestamp

#### Deleting a Comment
1. Find your comment on the post
2. Click "Delete" button (only visible to you)
3. Confirm deletion
4. The comment is permanently removed

### For Developers

#### Accessing Comments in Templates

```django
{# Get all comments for a post #}
{% for comment in post.comments.all %}
    {{ comment.content }}
    {{ comment.author.username }}
    {{ comment.created_at }}
{% endfor %}

{# Get comment count #}
{{ post.comments.count }}
```

#### Creating Comments Programmatically

```python
from blog.models import Comment, Post
from django.contrib.auth.models import User

post = Post.objects.get(pk=1)
user = User.objects.get(username='john')

comment = Comment.objects.create(
    post=post,
    author=user,
    content='Great post!'
)
```

---

## Testing

### Manual Testing

#### Test 1: View Comments (Public)
```
1. Open browser (logged out)
2. Navigate to http://127.0.0.1:8000/post/1/
3. Expected: See all comments
4. Expected: See login prompt for comment form
```

#### Test 2: Create Comment (Authenticated)
```
1. Log in to account
2. Navigate to a blog post
3. Write comment in form
4. Click "Post Comment"
5. Expected: Comment appears at bottom
6. Expected: Success message displayed
```

#### Test 3: Edit Comment (Author Only)
```
1. Log in as comment author
2. Navigate to post with your comment
3. Click "Edit" on your comment
4. Modify content
5. Click "Update Comment"
6. Expected: Comment updated
7. Expected: "edited" timestamp shown
```

#### Test 4: Edit Comment (Unauthorized)
```
1. Log in as different user
2. Try to navigate to /comment/1/update/
3. Expected: 403 Forbidden
```

#### Test 5: Delete Comment (Author Only)
```
1. Log in as comment author
2. Navigate to post with your comment
3. Click "Delete" on your comment
4. Confirm deletion
5. Expected: Comment removed
6. Expected: Success message displayed
```

### Automated Testing

Run comment tests:
```bash
python manage.py test blog.test_comments
```

**Expected output:**
```
Found 9 test(s).
.........
----------------------------------------------------------------------
Ran 9 tests in X.XXXs

OK
```

---

## API Examples

### Display Comments on Post Detail

```django
{% extends 'blog/base.html' %}

{% block content %}
<!-- Post content here -->

<!-- Comments Section -->
<h3>Comments ({{ post.comments.count }})</h3>

{% for comment in post.comments.all %}
<div class="comment">
    <strong>{{ comment.author.username }}</strong>
    <small>{{ comment.created_at|date:"F d, Y" }}</small>
    <p>{{ comment.content }}</p>
    
    {% if user == comment.author %}
    <a href="{% url 'comment-update' comment.pk %}">Edit</a>
    <a href="{% url 'comment-delete' comment.pk %}">Delete</a>
    {% endif %}
</div>
{% endfor %}
{% endblock %}
```

---

## Security Features

### Authentication
- ✅ `LoginRequiredMixin` for create, edit, delete
- ✅ Session-based authentication
- ✅ CSRF protection on all forms

### Authorization
- ✅ `UserPassesTestMixin` for edit and delete
- ✅ Verifies comment ownership
- ✅ 403 Forbidden for unauthorized access

### Data Integrity
- ✅ ForeignKey relationships
- ✅ CASCADE deletion (comments deleted with post)
- ✅ Form validation

---

## Database Schema

### Comment Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| post_id | INTEGER | FOREIGN KEY (Post) |
| author_id | INTEGER | FOREIGN KEY (User) |
| content | TEXT | NOT NULL |
| created_at | DATETIME | NOT NULL |
| updated_at | DATETIME | NOT NULL |

### Relationships

```
Post (1) ←→ (Many) Comment
User (1) ←→ (Many) Comment
```

---

## Summary

### Features Completed
✅ Comment model with timestamps  
✅ Create comments (authenticated users)  
✅ Edit comments (author only)  
✅ Delete comments (author only)  
✅ View comments (public)  
✅ Comment count display  
✅ Edit timestamp tracking  
✅ Author badge for post authors  
✅ Responsive templates  
✅ Comprehensive testing  
✅ Complete documentation  

### Security Features
✅ Authentication required for write operations  
✅ Ownership verification for edit/delete  
✅ CSRF protection  
✅ Permission enforcement  

All comment features are fully functional and tested! ✅
