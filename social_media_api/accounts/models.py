"""
Accounts Models

This module defines the custom user model for the social media API.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Additional fields:
        - bio: User biography/description
        - profile_picture: URL or path to user's profile picture
        - followers: Many-to-many relationship for users who follow this user
        - following: Many-to-many relationship for users this user follows
    """
    
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="User biography or description"
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text="User's profile picture"
    )
    
    # Many-to-many relationship for following
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
        help_text="Users that this user follows"
    )
    
    def __str__(self):
        return self.username
    
    @property
    def followers_count(self):
        """Return the number of followers."""
        return self.followers.count()
    
    @property
    def following_count(self):
        """Return the number of users this user is following."""
        return self.following.count()
