"""
Accounts URL Configuration

This module defines URL patterns for user authentication, profile management,
and follow/unfollow functionality.
"""

from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    follow_user,
    unfollow_user,
    list_following,
    list_followers
)

urlpatterns = [
    # Authentication
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Follow management
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
    path('following/', list_following, name='list-following'),
    path('followers/', list_followers, name='list-followers'),
]
