"""
Comment System Tests

This module contains test cases for the comment functionality.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment


class CommentTests(TestCase):
    """Test cases for Comment CRUD operations."""
    
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
        
        # Create test comment
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            content='This is a test comment.'
        )
    
    def test_comment_creation(self):
        """Test that comments are created correctly."""
        self.assertEqual(self.comment.content, 'This is a test comment.')
        self.assertEqual(self.comment.author, self.user1)
        self.assertEqual(self.comment.post, self.post)
    
    def test_comment_str_method(self):
        """Test the comment string representation."""
        expected = f'Comment by user1 on Test Post'
        self.assertEqual(str(self.comment), expected)
    
    def test_comment_create_requires_login(self):
        """Test that creating comment requires authentication."""
        response = self.client.get(
            reverse('comment-create', args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_comment_create_authenticated(self):
        """Test creating comment when authenticated."""
        self.client.login(username='user1', password='Pass123!')
        
        response = self.client.post(
            reverse('comment-create', args=[self.post.pk]),
            {'content': 'New test comment'}
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(
            Comment.objects.filter(content='New test comment').exists()
        )
    
    def test_comment_update_author_only(self):
        """Test that only author can update their comment."""
        # Login as comment author
        self.client.login(username='user1', password='Pass123!')
        
        response = self.client.post(
            reverse('comment-update', args=[self.comment.pk]),
            {'content': 'Updated comment content'}
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after update
        
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment content')
    
    def test_comment_update_non_author_forbidden(self):
        """Test that non-author cannot update comment."""
        # Login as different user
        self.client.login(username='user2', password='Pass123!')
        
        response = self.client.get(
            reverse('comment-update', args=[self.comment.pk])
        )
        
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_comment_delete_author_only(self):
        """Test that only author can delete their comment."""
        # Login as comment author
        self.client.login(username='user1', password='Pass123!')
        
        response = self.client.post(
            reverse('comment-delete', args=[self.comment.pk])
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(
            Comment.objects.filter(pk=self.comment.pk).exists()
        )
    
    def test_comment_delete_non_author_forbidden(self):
        """Test that non-author cannot delete comment."""
        # Login as different user
        self.client.login(username='user2', password='Pass123!')
        
        response = self.client.get(
            reverse('comment-delete', args=[self.comment.pk])
        )
        
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_comments_display_on_post_detail(self):
        """Test that comments appear on post detail page."""
        response = self.client.get(
            reverse('post-detail', args=[self.post.pk])
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test comment.')
        self.assertContains(response, 'user1')
    
    def test_comment_count_on_post_detail(self):
        """Test that comment count is displayed correctly."""
        response = self.client.get(
            reverse('post-detail', args=[self.post.pk])
        )
        
        self.assertContains(response, 'Comments (1)')
