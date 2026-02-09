"""
Blog Models

This module defines the data models for the Django blog application.

Models:
    - Post: Represents a blog post with title, content, publication date, and author
"""

from django.db import models
from django.contrib.auth.models import User


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
        ordering = ['-published_date']  # Newest posts first
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        """
        String representation of the Post model.
        
        Returns:
            str: The title of the post
        """
        return self.title
    
    def get_snippet(self, length=100):
        """
        Get a snippet of the post content.
        
        Args:
            length (int): Maximum length of the snippet
            
        Returns:
            str: Truncated content with ellipsis if needed
        """
        if len(self.content) > length:
            return f"{self.content[:length]}..."
        return self.content
