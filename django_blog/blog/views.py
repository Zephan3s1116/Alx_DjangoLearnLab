"""
Blog Views

This module contains the view functions for the blog application.
"""

from django.shortcuts import render
from .models import Post


def home(request):
    """
    Display the home page with a list of all blog posts.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Rendered home page with blog posts
    """
    posts = Post.objects.all().order_by('-published_date')
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    """
    Display the about page.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Rendered about page
    """
    return render(request, 'blog/about.html')
