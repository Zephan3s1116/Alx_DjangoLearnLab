"""
Blog Post CRUD Tests

This module contains test cases for blog post CRUD operations.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post


class PostCRUDTests(TestCase):
    """Test cases for Post CRUD operations."""
    
    def setUp(self):
        """Set up test users and posts."""
        self.client = Client()
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='Pass123!'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='Pass123!'
        )
        
        # Create test post
        self.post = Post.objects.create(
            title='Test Post',
            content='This is test content.',
            author=self.user1
        )
    
    def test_post_list_view_public(self):
        """Test that post list is accessible to public."""
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
    
    def test_post_detail_view_public(self):
        """Test that post detail is accessible to public."""
        response = self.client.get(reverse('post-detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'This is test content.')
    
    def test_post_create_requires_login(self):
        """Test that creating post requires authentication."""
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_post_create_authenticated(self):
        """Test creating post when authenticated."""
        self.client.login(username='user1', password='Pass123!')
        
        response = self.client.post(reverse('post-create'), {
            'title': 'New Test Post',
            'content': 'New test content'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Post.objects.filter(title='New Test Post').exists())
        
        new_post = Post.objects.get(title='New Test Post')
        self.assertEqual(new_post.author, self.user1)
    
    def test_post_update_author_only(self):
        """Test that only author can update their post."""
        # Login as post author
        self.client.login(username='user1', password='Pass123!')
        
        response = self.client.post(reverse('post-update', args=[self.post.pk]), {
            'title': 'Updated Title',
            'content': 'Updated content'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after update
        
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.content, 'Updated content')
    
    def test_post_update_non_author_forbidden(self):
        """Test that non-author cannot update post."""
        # Login as different user
        self.client.login(username='user2', password='Pass123!')
        
        response = self.client.get(reverse('post-update', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_post_delete_author_only(self):
        """Test that only author can delete their post."""
        # Login as post author
        self.client.login(username='user1', password='Pass123!')
        
        response = self.client.post(reverse('post-delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
    
    def test_post_delete_non_author_forbidden(self):
        """Test that non-author cannot delete post."""
        # Login as different user
        self.client.login(username='user2', password='Pass123!')
        
        response = self.client.get(reverse('post-delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_post_absolute_url(self):
        """Test get_absolute_url method."""
        url = self.post.get_absolute_url()
        self.assertEqual(url, f'/posts/{self.post.pk}/')
