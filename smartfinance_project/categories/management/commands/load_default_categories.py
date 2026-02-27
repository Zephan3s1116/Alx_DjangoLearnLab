from django.core.management.base import BaseCommand
from categories.models import Category

class Command(BaseCommand):
    help = 'Load default income and expense categories'
    
    def handle(self, *args, **kwargs):
        # Income categories
        income_categories = [
            {'name': 'Salary', 'icon': 'salary', 'color': '#4CAF50'},
            {'name': 'Freelance', 'icon': 'briefcase', 'color': '#2196F3'},
            {'name': 'Investment Returns', 'icon': 'trending-up', 'color': '#FF9800'},
            {'name': 'Other Income', 'icon': 'dollar', 'color': '#9C27B0'},
        ]
        
        # Expense categories
        expense_categories = [
            {'name': 'Food and Dining', 'icon': 'restaurant', 'color': '#FF5722'},
            {'name': 'Transportation', 'icon': 'car', 'color': '#3F51B5'},
            {'name': 'Housing', 'icon': 'home', 'color': '#795548'},
            {'name': 'Utilities', 'icon': 'lightbulb', 'color': '#607D8B'},
            {'name': 'Entertainment', 'icon': 'movie', 'color': '#E91E63'},
            {'name': 'Healthcare', 'icon': 'medical', 'color': '#00BCD4'},
            {'name': 'Shopping', 'icon': 'shopping-bag', 'color': '#FFC107'},
            {'name': 'Education', 'icon': 'book', 'color': '#673AB7'},
            {'name': 'Travel', 'icon': 'airplane', 'color': '#009688'},
            {'name': 'Other Expenses', 'icon': 'pin', 'color': '#9E9E9E'},
        ]
        
        # Create income categories
        for cat in income_categories:
            Category.objects.get_or_create(
                name=cat['name'],
                type='income',
                user=None,
                defaults={
                    'is_default': True,
                    'icon': cat['icon'],
                    'color': cat['color']
                }
            )
            self.stdout.write(self.style.SUCCESS(f'Created income category: {cat["name"]}'))
        
        # Create expense categories
        for cat in expense_categories:
            Category.objects.get_or_create(
                name=cat['name'],
                type='expense',
                user=None,
                defaults={
                    'is_default': True,
                    'icon': cat['icon'],
                    'color': cat['color']
                }
            )
            self.stdout.write(self.style.SUCCESS(f'Created expense category: {cat["name"]}'))
        
        self.stdout.write(self.style.SUCCESS('Default categories loaded successfully'))
