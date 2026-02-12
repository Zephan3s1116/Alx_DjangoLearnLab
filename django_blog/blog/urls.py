"""
Blog URL Configuration

This module defines the URL patterns for the blog application,
including authentication and profile management URLs.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home and about pages
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Profile management
    path('profile/', views.profile, name='profile'),
]
