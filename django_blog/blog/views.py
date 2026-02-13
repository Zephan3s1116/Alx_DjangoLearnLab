"""
Blog Views

This module contains view functions and class-based views for the blog application,
including authentication, profile management, CRUD operations, comments, and search.
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
from django.db.models import Q
from taggit.models import Tag
from .models import Post, Comment
from .forms import (
    CustomUserCreationForm,
    UserUpdateForm,
    CommentForm,
    PostForm
)


# ============================================================================
# Blog Post CRUD Views (Class-Based Views)
# ============================================================================

class PostListView(ListView):
    """Display a list of all blog posts with pagination."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5


class PostDetailView(DetailView):
    """Display a single blog post with comments."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        """Add comment form to context."""
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Allow authenticated users to create new blog posts."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Set the author to the current user before saving."""
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
    """Allow post authors to edit their own blog posts."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Ensure the author remains unchanged during update."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        context['button_text'] = 'Update Post'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allow post authors to delete their own blog posts."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog-home')
    
    def delete(self, request, *args, **kwargs):
        """Display success message after deletion."""
        messages.success(request, 'Your post has been deleted!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author


# ============================================================================
# Search and Tag Views
# ============================================================================

def search_posts(request):
    """
    Search for posts based on title, content, or tags.
    
    Uses Django's Q objects for complex queries.
    Searches across post title, content, and tags.
    
    Args:
        request: The HTTP request object with GET parameter 'q'
        
    Returns:
        HttpResponse: Rendered search results page
    """
    query = request.GET.get('q', '')
    posts = Post.objects.none()  # Empty queryset by default
    
    if query:
        # Search in title, content, and tags
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-published_date')
    
    context = {
        'posts': posts,
        'query': query,
        'result_count': posts.count()
    }
    
    return render(request, 'blog/search_results.html', context)


class PostByTagListView(ListView):
    """
    Display all posts with a specific tag.
    
    Filters posts by tag slug and displays them in a list.
    """
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """Filter posts by the tag slug from the URL."""
        tag_slug = self.kwargs.get('tag_slug')
        return Post.objects.filter(tags__slug=tag_slug).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        """Add tag to context."""
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context


# ============================================================================
# Function-Based Views (Home and About)
# ============================================================================

def home(request):
    """Display the home page with a list of all blog posts."""
    posts = Post.objects.all().order_by('-published_date')
    
    # Get all tags for the sidebar
    tags = Tag.objects.all()
    
    context = {
        'posts': posts,
        'tags': tags
    }
    return render(request, 'blog/home.html', context)


def about(request):
    """Display the about page."""
    return render(request, 'blog/about.html')


# ============================================================================
# Comment Views
# ============================================================================

class CommentCreateView(LoginRequiredMixin, CreateView):
    """Allow authenticated users to create comments on blog posts."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """Set the post and author before saving the comment."""
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
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
    """Allow comment authors to edit their own comments."""
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
    """Allow comment authors to delete their own comments."""
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


# ============================================================================
# Authentication Views (Function-Based)
# ============================================================================

@csrf_protect
def register(request):
    """Handle user registration."""
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
    """Handle user login."""
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
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('blog-home')


@login_required(login_url='login')
@csrf_protect
def profile(request):
    """Display and handle user profile management."""
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
