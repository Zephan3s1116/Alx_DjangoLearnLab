"""
Blog Models

This module defines the data models for the Django blog application.

Models:
    - Post: Represents a blog post with title, content, publication date, and author
    - Comment: Represents a comment on a blog post
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    """
    Post model representing a blog post.
    
    Attributes:
        title (CharField): The title of the blog post (max 200 characters)
        content (TextField): The main content of the blog post
        published_date (DateTimeField): The date and time when the post was published
        author (ForeignKey): Reference to the User who authored the post
    
    Methods:
        __str__: Returns the title of the post
        get_absolute_url: Returns the URL for the post detail page
        get_snippet: Returns a short excerpt of the post content
    
    Meta:
        ordering: Posts ordered by published_date in descending order (newest first)
    """
    
    title = models.CharField(
        max_length=200,
        help_text="Enter the title of your blog post"
    )
    
    content = models.TextField(
        help_text="Enter the main content of your blog post"
    )
    
    published_date = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when this post was published"
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        help_text="The author of this blog post"
    )
    
    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        """String representation of the Post model."""
        return self.title
    
    def get_absolute_url(self):
        """Get the URL for the post detail page."""
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_snippet(self, length=100):
        """Get a snippet of the post content."""
        if len(self.content) > length:
            return f"{self.content[:length]}..."
        return self.content


class Comment(models.Model):
    """
    Comment model representing a comment on a blog post.
    
    Attributes:
        post (ForeignKey): The blog post this comment belongs to
        author (ForeignKey): The user who wrote the comment
        content (TextField): The content of the comment
        created_at (DateTimeField): When the comment was created
        updated_at (DateTimeField): When the comment was last updated
    
    Methods:
        __str__: Returns a string representation of the comment
        get_absolute_url: Returns the URL to the post detail page
    
    Meta:
        ordering: Comments ordered by creation date (oldest first)
    """
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The blog post this comment belongs to"
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The user who wrote this comment"
    )
    
    content = models.TextField(
        help_text="Enter your comment"
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
        ordering = ['created_at']  # Oldest comments first
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        """String representation of the Comment model."""
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_absolute_url(self):
        """Return the URL to the post detail page where this comment appears."""
        return reverse('post-detail', kwargs={'pk': self.post.pk})
