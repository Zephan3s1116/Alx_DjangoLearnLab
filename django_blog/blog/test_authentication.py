"""
Authentication System Tests

This module contains test cases for the user authentication system.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AuthenticationTestCase(TestCase):
    """Test cases for user authentication."""
    
    def setUp(self):
        """Set up test client and test user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
    
    def test_register_page_loads(self):
        """Test that registration page loads correctly."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')
    
    def test_login_page_loads(self):
        """Test that login page loads correctly."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
    
    def test_profile_requires_login(self):
        """Test that profile page requires authentication."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_successful_registration(self):
        """Test user registration with valid data."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'NewPass123!',
            'password2': 'NewPass123!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_successful_login(self):
        """Test user login with correct credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home
    
    def test_failed_login(self):
        """Test user login with incorrect credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertContains(response, 'Invalid username or password')
    
    def test_logout(self):
        """Test user logout."""
        # First login
        self.client.login(username='testuser', password='TestPass123!')
        
        # Then logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to home
    
    def test_profile_access_when_logged_in(self):
        """Test that logged-in users can access profile."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile Settings')
    
    def test_profile_update(self):
        """Test updating user profile."""
        self.client.login(username='testuser', password='TestPass123!')
        
        response = self.client.post(reverse('profile'), {
            'username': 'testuser',
            'email': 'updated@example.com'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after update
        
        # Check if email was updated
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'updated@example.com')
