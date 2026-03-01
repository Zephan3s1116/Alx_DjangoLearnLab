from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from datetime import date
from .models import Transaction
from categories.models import Category

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(
            name='Test Category',
            type='expense',
            is_default=True
        )
    
    def test_transaction_creation(self):
        """Test creating a transaction"""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('100.00'),
            type='expense',
            description='Test transaction',
            date=date.today()
        )
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.amount, Decimal('100.00'))
        self.assertEqual(str(transaction), f"Expense: 100.00 on {date.today()}")
    
    def test_transaction_ordering(self):
        """Test transactions are ordered by date descending"""
        Transaction.objects.create(
            user=self.user, category=self.category,
            amount=100, type='expense', date='2026-01-01'
        )
        Transaction.objects.create(
            user=self.user, category=self.category,
            amount=200, type='expense', date='2026-02-01'
        )
        transactions = Transaction.objects.all()
        self.assertEqual(transactions[0].amount, Decimal('200.00'))

class TransactionAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(
            name='Food', type='expense', is_default=True
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_transaction(self):
        """Test creating transaction via API"""
        data = {
            'category': self.category.id,
            'amount': '50.00',
            'type': 'expense',
            'description': 'Groceries',
            'date': '2026-02-20'
        }
        response = self.client.post('/api/transactions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
    
    def test_list_transactions(self):
        """Test listing transactions"""
        Transaction.objects.create(
            user=self.user, category=self.category,
            amount=100, type='expense', date=date.today()
        )
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_transaction_summary(self):
        """Test transaction summary endpoint"""
        Transaction.objects.create(
            user=self.user, category=self.category,
            amount=1000, type='income', date=date.today()
        )
        Transaction.objects.create(
            user=self.user, category=self.category,
            amount=400, type='expense', date=date.today()
        )
        response = self.client.get('/api/transactions/summary/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['total_income']), Decimal('1000.00'))
        self.assertEqual(Decimal(response.data['total_expenses']), Decimal('400.00'))
