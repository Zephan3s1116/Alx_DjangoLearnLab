"""
Blog Views

This module contains view functions and class-based views for the blog application,
including authentication, profile management, and CRUD operations for blog posts.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import CustomUserCreationForm, UserUpdateForm


# ============================================================================
# Blog Post CRUD Views (Class-Based Views)
# ============================================================================

class PostListView(ListView):
    """
    Display a list of all blog posts.
    
    Accessible to all users (authenticated or not).
    Posts are ordered by publication date (newest first).
    
    Template: blog/post_list.html
    Context: 'posts' (paginated list of Post objects)
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5  # Show 5 posts per page


class PostDetailView(DetailView):
    """
    Display a single blog post with full content.
    
    Accessible to all users (authenticated or not).
    
    Template: blog/post_detail.html
    Context: 'post' (single Post object)
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        """Add comment form to context."""
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create new blog posts.
    
    Only accessible to authenticated users.
    The author field is automatically set to the current user.
    
    Template: blog/post_form.html
    Success: Redirects to the newly created post's detail page
    """
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """
        Set the author to the current user before saving.
        
        Args:
            form: The validated form instance
            
        Returns:
            HttpResponse: Redirect to success URL
        """
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        context['button_text'] = 'Create Post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow post authors to edit their own blog posts.
    
    Only accessible to:
    - Authenticated users
    - The author of the post
    
    Template: blog/post_form.html
    Success: Redirects to the updated post's detail page
    """
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """
        Ensure the author remains unchanged during update.
        
        Args:
            form: The validated form instance
            
        Returns:
            HttpResponse: Redirect to success URL
        """
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        """
        Check if the current user is the author of the post.
        
        Returns:
            bool: True if current user is the post author, False otherwise
        """
        post = self.get_object()
        return self.request.user == post.author
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        context['button_text'] = 'Update Post'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow post authors to delete their own blog posts.
    
    Only accessible to:
    - Authenticated users
    - The author of the post
    
    Template: blog/post_confirm_delete.html
    Success: Redirects to the blog home page
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog-home')
    
    def delete(self, request, *args, **kwargs):
        """
        Display success message after deletion.
        
        Returns:
            HttpResponse: Redirect to success URL
        """
        messages.success(request, 'Your post has been deleted!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """
        Check if the current user is the author of the post.
        
        Returns:
            bool: True if current user is the post author, False otherwise
        """
        post = self.get_object()
        return self.request.user == post.author


# ============================================================================
# Function-Based Views (Home and About)
# ============================================================================

def home(request):
    """
    Display the home page with a list of all blog posts.
    
    This is a simple function-based view that can be replaced
    with PostListView if desired.
    
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


# ============================================================================
# Authentication Views (Function-Based)
# ============================================================================

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


# ============================================================================
# Comment Views
# ============================================================================

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create comments on blog posts.
    
    Template: blog/comment_form.html (or embedded in post_detail.html)
    Success: Redirects to the post detail page
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """
        Set the post and author before saving the comment.
        
        Args:
            form: The validated form instance
            
        Returns:
            HttpResponse: Redirect to post detail page
        """
        # Get the post from the URL
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        
        # Set the post and author
        form.instance.post = post
        form.instance.author = self.request.user
        
        messages.success(self.request, 'Your comment has been posted!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Add post to context."""
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow comment authors to edit their own comments.
    
    Only accessible to:
    - Authenticated users
    - The author of the comment
    
    Template: blog/comment_form.html
    Success: Redirects to the post detail page
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """Display success message after update."""
        messages.success(self.request, 'Your comment has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_context_data(self, **kwargs):
        """Add editing flag to context."""
        context = super().get_context_data(**kwargs)
        context['editing'] = True
        context['post'] = self.get_object().post
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow comment authors to delete their own comments.
    
    Only accessible to:
    - Authenticated users
    - The author of the comment
    
    Template: blog/comment_confirm_delete.html
    Success: Redirects to the post detail page
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def get_success_url(self):
        """Redirect to the post detail page after deletion."""
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
    
    def delete(self, request, *args, **kwargs):
        """Display success message after deletion."""
        messages.success(request, 'Your comment has been deleted!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """Check if the current user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author
