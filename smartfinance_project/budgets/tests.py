from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Budget
from categories.models import Category
from transactions.models import Transaction
from datetime import date

class BudgetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(
            name='Food', type='expense', is_default=True
        )
    
    def test_budget_creation(self):
        """Test creating a budget"""
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('500.00'),
            month=2,
            year=2026
        )
        self.assertEqual(budget.amount, Decimal('500.00'))
        self.assertEqual(budget.get_spent_amount(), Decimal('0.00'))
    
    def test_budget_spent_calculation(self):
        """Test spent amount calculation"""
        budget = Budget.objects.create(
            user=self.user, category=self.category,
            amount=500, month=2, year=2026
        )
        Transaction.objects.create(
            user=self.user, category=self.category,
            amount=200, type='expense', date='2026-02-15'
        )
        self.assertEqual(budget.get_spent_amount(), Decimal('200.00'))
        self.assertEqual(budget.get_remaining_amount(), Decimal('300.00'))
        self.assertEqual(budget.get_percentage_used(), 40.0)
    
    def test_budget_status(self):
        """Test budget status indicators"""
        budget = Budget.objects.create(
            user=self.user, category=self.category,
            amount=100, month=2, year=2026
        )
        # Under budget
        Transaction.objects.create(
            user=self.user, category=self.category,
            amount=50, type='expense', date='2026-02-15'
        )
        self.assertEqual(budget.get_status(), 'under')
        
        # Near limit
        Transaction.objects.create(
            user=self.user, category=self.category,
            amount=35, type='expense', date='2026-02-16'
        )
        self.assertEqual(budget.get_status(), 'near')

class BudgetAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(
            name='Food', type='expense', is_default=True
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_budget(self):
        """Test creating budget via API"""
        data = {
            'category': self.category.id,
            'amount': '500.00',
            'month': 2,
            'year': 2026
        }
        response = self.client.post('/api/budgets/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('spent_amount', response.data)
        self.assertIn('status', response.data)
