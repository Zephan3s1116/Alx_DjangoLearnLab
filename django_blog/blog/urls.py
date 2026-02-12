"""
Blog URL Configuration

This module defines the URL patterns for the blog application,
including authentication, profile management, and CRUD operations for blog posts.
"""

from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    # Home and about pages
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    
    # Blog post CRUD operations (Class-Based Views)
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Profile management
    path('profile/', views.profile, name='profile'),
]
