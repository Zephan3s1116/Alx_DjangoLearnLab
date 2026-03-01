from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Goal

class GoalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
    
    def test_goal_creation(self):
        """Test creating a goal"""
        goal = Goal.objects.create(
            user=self.user,
            name='Emergency Fund',
            target_amount=Decimal('10000.00'),
            current_amount=Decimal('2000.00')
        )
        self.assertEqual(goal.get_progress_percentage(), 20.0)
        self.assertEqual(goal.get_remaining_amount(), Decimal('8000.00'))
    
    def test_goal_progress(self):
        """Test goal progress calculation"""
        goal = Goal.objects.create(
            user=self.user,
            name='Vacation',
            target_amount=1000,
            current_amount=750
        )
        self.assertEqual(goal.get_progress_percentage(), 75.0)
        self.assertFalse(goal.is_completed)

class GoalAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
    
    def test_create_goal(self):
        """Test creating goal via API"""
        data = {
            'name': 'New Car',
            'target_amount': '20000.00',
            'current_amount': '5000.00',
            'deadline': '2026-12-31'
        }
        response = self.client.post('/api/goals/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('progress_percentage', response.data)
    
    def test_update_goal_progress(self):
        """Test updating goal progress"""
        goal = Goal.objects.create(
            user=self.user, name='Savings',
            target_amount=1000, current_amount=500
        )
        response = self.client.patch(
            f'/api/goals/{goal.id}/update-progress/',
            {'amount': '200.00'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        goal.refresh_from_db()
        self.assertEqual(goal.current_amount, Decimal('700.00'))
