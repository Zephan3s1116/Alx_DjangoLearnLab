"""
Blog Views

This module contains view functions for the blog application,
including authentication and profile management views.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm


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


@csrf_protect
def register(request):
    """
    Handle user registration.
    
    GET: Display registration form
    POST: Process registration form and create new user
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Rendered registration page or redirect to login
    """
    if request.user.is_authenticated:
        # If user is already logged in, redirect to home
        return redirect('blog-home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})


@csrf_protect
def user_login(request):
    """
    Handle user login.
    
    GET: Display login form
    POST: Process login credentials and authenticate user
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Rendered login page or redirect to home
    """
    if request.user.is_authenticated:
        # If user is already logged in, redirect to home
        return redirect('blog-home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # Redirect to next page if specified, otherwise to home
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('blog-home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'blog/login.html', {'form': form})


@login_required(login_url='login')
def user_logout(request):
    """
    Handle user logout.
    
    Logs out the current user and redirects to home page.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Redirect to home page
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('blog-home')


@login_required(login_url='login')
@csrf_protect
def profile(request):
    """
    Display and handle user profile management.
    
    GET: Display profile page with user information
    POST: Update user profile information
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Rendered profile page or redirect after update
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'blog/profile.html', context)
