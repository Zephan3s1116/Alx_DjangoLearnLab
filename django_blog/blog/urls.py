"""
Blog URL Configuration

This module defines the URL patterns for the blog application,
including authentication, profile management, blog posts, comments, search, and tags.
"""

from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostByTagListView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView
)

urlpatterns = [
    # Home and about pages
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    
    # Search functionality
    path('search/', views.search_posts, name='search'),
    
    # Tag functionality
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts-by-tag'),
    
    # Blog post CRUD operations
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Comment CRUD operations
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Profile management
    path('profile/', views.profile, name='profile'),
]
