"""
Unit Tests for Django REST Framework API Views

This module contains comprehensive unit tests for the Book API endpoints,
testing CRUD operations, filtering, searching, ordering, permissions, and authentication.

Test Categories:
1. Authentication Tests
2. CRUD Operation Tests (Create, Read, Update, Delete)
3. Filtering Tests
4. Searching Tests
5. Ordering Tests
6. Permission Tests
7. Edge Cases and Error Handling

Usage:
    python manage.py test api
    python manage.py test api.test_views
    python manage.py test api.test_views.BookAPITestCase
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Book, Author
import json


class BookAPITestCase(TestCase):
    """
    Comprehensive test suite for Book API endpoints.
    
    Tests all CRUD operations, filtering, searching, ordering,
    permissions, and authentication mechanisms.
    """
    
    def setUp(self):
        """
        Set up test environment before each test.
        
        Creates:
        - Test users (authenticated and unauthenticated)
        - Authentication tokens
        - Sample authors and books
        - API client
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123',
            email='otheruser@example.com'
        )
        
        # Create authentication tokens
        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)
        
        # Create API client
        self.client = APIClient()
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        self.author3 = Author.objects.create(name='J.R.R. Tolkien')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Sorcerer\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        
        self.book3 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        
        self.book4 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author3
        )
        
        # API endpoints
        self.list_url = '/api/books/'
        self.create_url = '/api/books/create/'
    
    # ========================================================================
    # Authentication Tests
    # ========================================================================
    
    def test_authentication_token_creation(self):
        """Test that authentication tokens are created correctly."""
        self.assertIsNotNone(self.token)
        self.assertIsNotNone(self.other_token)
        self.assertEqual(self.token.user, self.user)
    
    def test_authenticated_request(self):
        """Test that authenticated requests work correctly."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_read_access(self):
        """Test that unauthenticated users can read (GET) books."""
        # Remove authentication
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_create_denied(self):
        """Test that unauthenticated users cannot create books."""
        self.client.credentials()
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # ========================================================================
    # CRUD Operation Tests - CREATE
    # ========================================================================
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data = {
            'title': 'New Test Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('book', response.data)
        self.assertEqual(response.data['book']['title'], 'New Test Book')
        self.assertEqual(response.data['book']['publication_year'], 2020)
        
        # Verify book was created in database
        self.assertTrue(
            Book.objects.filter(title='New Test Book').exists()
        )
    
    def test_create_book_validation_future_year(self):
        """Test that creating a book with future year fails validation."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)
    
    def test_create_book_missing_required_fields(self):
        """Test that creating a book without required fields fails."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Missing title
        data = {
            'publication_year': 2020,
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # ========================================================================
    # CRUD Operation Tests - READ
    # ========================================================================
    
    def test_list_books(self):
        """Test retrieving list of all books."""
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 4)
    
    def test_retrieve_single_book(self):
        """Test retrieving a single book by ID."""
        url = f'/api/books/{self.book1.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.author1.id)
    
    def test_retrieve_nonexistent_book(self):
        """Test retrieving a book that doesn't exist returns 404."""
        url = '/api/books/99999/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ========================================================================
    # CRUD Operation Tests - UPDATE
    # ========================================================================
    
    def test_update_book_authenticated(self):
        """Test updating a book with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        url = f'/api/books/{self.book1.id}/update/'
        data = {
            'title': 'Updated Harry Potter Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('book', response.data)
        self.assertEqual(response.data['book']['title'], 'Updated Harry Potter Title')
        
        # Verify database was updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Harry Potter Title')
    
    def test_partial_update_book(self):
        """Test partially updating a book (PATCH)."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        url = f'/api/books/{self.book1.id}/update/'
        data = {
            'title': 'Partially Updated Title'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['book']['title'], 'Partially Updated Title')
        
        # Verify other fields unchanged
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.publication_year, 1997)
    
    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books."""
        self.client.credentials()
        
        url = f'/api/books/{self.book1.id}/update/'
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # ========================================================================
    # CRUD Operation Tests - DELETE
    # ========================================================================
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Create a book to delete
        book_to_delete = Book.objects.create(
            title='Book to Delete',
            publication_year=2020,
            author=self.author1
        )
        
        url = f'/api/books/{book_to_delete.id}/delete/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('deleted_book', response.data)
        self.assertEqual(response.data['deleted_book']['title'], 'Book to Delete')
        
        # Verify book was deleted from database
        self.assertFalse(
            Book.objects.filter(id=book_to_delete.id).exists()
        )
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books."""
        self.client.credentials()
        
        url = f'/api/books/{self.book1.id}/delete/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify book still exists
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_nonexistent_book(self):
        """Test deleting a nonexistent book returns 404."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        url = '/api/books/99999/delete/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ========================================================================
    # Filtering Tests
    # ========================================================================
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        url = f'{self.list_url}?publication_year=1997'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['publication_year'], 1997)
    
    def test_filter_by_publication_year_gte(self):
        """Test filtering books by publication year (greater than or equal)."""
        url = f'{self.list_url}?publication_year__gte=1997'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return books from 1997, 1998
        self.assertGreaterEqual(len(response.data['results']), 2)
        
        for book in response.data['results']:
            self.assertGreaterEqual(book['publication_year'], 1997)
    
    def test_filter_by_publication_year_lte(self):
        """Test filtering books by publication year (less than or equal)."""
        url = f'{self.list_url}?publication_year__lte=1997'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for book in response.data['results']:
            self.assertLessEqual(book['publication_year'], 1997)
    
    def test_filter_by_publication_year_range(self):
        """Test filtering books by publication year range."""
        url = f'{self.list_url}?publication_year__gte=1996&publication_year__lte=1998'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # 1996, 1997, 1998
    
    def test_filter_by_author(self):
        """Test filtering books by author."""
        url = f'{self.list_url}?author={self.author1.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 Harry Potter books
        
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author1.id)
    
    def test_filter_by_title_icontains(self):
        """Test case-insensitive title filtering."""
        url = f'{self.list_url}?title__icontains=harry'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    # ========================================================================
    # Searching Tests
    # ========================================================================
    
    def test_search_by_title(self):
        """Test searching books by title."""
        url = f'{self.list_url}?search=Harry'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
        # Verify results contain search term
        for book in response.data['results']:
            self.assertIn('Harry', book['title'])
    
    def test_search_by_author_name(self):
        """Test searching books by author name."""
        url = f'{self.list_url}?search=Rowling'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 books by Rowling
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        url_lower = f'{self.list_url}?search=harry'
        url_upper = f'{self.list_url}?search=HARRY'
        
        response_lower = self.client.get(url_lower)
        response_upper = self.client.get(url_upper)
        
        self.assertEqual(response_lower.status_code, status.HTTP_200_OK)
        self.assertEqual(response_upper.status_code, status.HTTP_200_OK)
        
        # Both should return same results
        self.assertEqual(
            len(response_lower.data['results']),
            len(response_upper.data['results'])
        )
    
    def test_search_no_results(self):
        """Test searching with term that matches no books."""
        url = f'{self.list_url}?search=NonexistentBook'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    
    # ========================================================================
    # Ordering Tests
    # ========================================================================
    
    def test_order_by_title_ascending(self):
        """Test ordering books by title (ascending)."""
        url = f'{self.list_url}?ordering=title'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_by_title_descending(self):
        """Test ordering books by title (descending)."""
        url = f'{self.list_url}?ordering=-title'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_order_by_publication_year_ascending(self):
        """Test ordering books by publication year (ascending)."""
        url = f'{self.list_url}?ordering=publication_year'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years))
    
    def test_order_by_publication_year_descending(self):
        """Test ordering books by publication year (descending)."""
        url = f'{self.list_url}?ordering=-publication_year'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))
    
    # ========================================================================
    # Combined Query Tests
    # ========================================================================
    
    def test_filter_and_order_combined(self):
        """Test combining filtering and ordering."""
        url = f'{self.list_url}?author={self.author1.id}&ordering=publication_year'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Verify ordering
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years))
    
    def test_search_and_order_combined(self):
        """Test combining search and ordering."""
        url = f'{self.list_url}?search=Harry&ordering=title'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify ordering
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
    
    def test_filter_search_order_combined(self):
        """Test combining filtering, searching, and ordering."""
        url = f'{self.list_url}?author={self.author1.id}&search=Harry&ordering=-publication_year'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify all books are by correct author
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author1.id)
        
        # Verify ordering
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))
    
    # ========================================================================
    # Permission Tests
    # ========================================================================
    
    def test_permission_read_public(self):
        """Test that read operations are public."""
        # No authentication
        self.client.credentials()
        
        # List books
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Retrieve single book
        url = f'/api/books/{self.book1.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_permission_write_requires_auth(self):
        """Test that write operations require authentication."""
        # No authentication
        self.client.credentials()
        
        # Try to create
        data = {'title': 'Test', 'publication_year': 2020, 'author': self.author1.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Try to update
        url = f'/api/books/{self.book1.id}/update/'
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Try to delete
        url = f'/api/books/{self.book1.id}/delete/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # ========================================================================
    # Edge Cases and Error Handling
    # ========================================================================
    
    def test_invalid_book_id_format(self):
        """Test that invalid book ID format returns 404."""
        url = '/api/books/invalid-id/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_empty_request_body_create(self):
        """Test creating book with empty request body."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.post(self.create_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_pagination(self):
        """Test that pagination works correctly."""
        # Create more books to trigger pagination
        for i in range(15):
            Book.objects.create(
                title=f'Test Book {i}',
                publication_year=2020,
                author=self.author1
            )
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), 10)  # Page size is 10


class AuthenticationTestCase(TestCase):
    """Test cases specifically for authentication mechanisms."""
    
    def setUp(self):
        """Set up test users and client."""
        self.user = User.objects.create_user(
            username='authuser',
            password='authpass123'
        )
        self.client = APIClient()
    
    def test_token_authentication(self):
        """Test token-based authentication."""
        token = Token.objects.create(user=self.user)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_token(self):
        """Test that invalid token is rejected."""
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid-token-key')
        
        # Try to create a book (requires auth)
        response = self.client.post('/api/books/create/', {})
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_missing_token(self):
        """Test that missing token is handled correctly."""
        # Try to create without authentication
        response = self.client.post('/api/books/create/', {})
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
