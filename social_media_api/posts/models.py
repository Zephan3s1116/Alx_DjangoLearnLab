"""
Posts Models

This module defines models for posts and comments in the social media API.
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """
    Post model representing a user's post.
    
    Attributes:
        author: ForeignKey to User who created the post
        title: Title of the post
        content: Main content of the post
        created_at: Timestamp when post was created
        updated_at: Timestamp when post was last updated
    """
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="User who created this post"
    )
    
    title = models.CharField(
        max_length=200,
        help_text="Title of the post"
    )
    
    content = models.TextField(
        help_text="Main content of the post"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this post was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this post was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"


class Comment(models.Model):
    """
    Comment model representing a comment on a post.
    
    Attributes:
        post: ForeignKey to the Post being commented on
        author: ForeignKey to User who created the comment
        content: Content of the comment
        created_at: Timestamp when comment was created
        updated_at: Timestamp when comment was last updated
    """
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Post this comment belongs to"
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="User who created this comment"
    )
    
    content = models.TextField(
        help_text="Content of the comment"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this comment was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this comment was last updated"
    )
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
