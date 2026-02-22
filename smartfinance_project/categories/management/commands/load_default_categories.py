from django.core.management.base import BaseCommand
from categories.models import Category

class Command(BaseCommand):
    help = 'Load default income and expense categories'
    
    def handle(self, *args, **kwargs):
        # Income categories
        income_categories = [
            {'name': 'Salary', 'icon': '💰', 'color': '#4CAF50'},
            {'name': 'Freelance', 'icon': '💼', 'color': '#2196F3'},
            {'name': 'Investment Returns', 'icon': '📈', 'color': '#FF9800'},
            {'name': 'Other Income', 'icon': '💵', 'color': '#9C27B0'},
        ]
        
        # Expense categories
        expense_categories = [
            {'name': 'Food & Dining', 'icon': '🍔', 'color': '#FF5722'},
            {'name': 'Transportation', 'icon': '🚗', 'color': '#3F51B5'},
            {'name': 'Housing', 'icon': '🏠', 'color': '#795548'},
            {'name': 'Utilities', 'icon': '💡', 'color': '#607D8B'},
            {'name': 'Entertainment', 'icon': '🎬', 'color': '#E91E63'},
            {'name': 'Healthcare', 'icon': '⚕️', 'color': '#00BCD4'},
            {'name': 'Shopping', 'icon': '🛍️', 'color': '#FFC107'},
            {'name': 'Education', 'icon': '📚', 'color': '#673AB7'},
            {'name': 'Travel', 'icon': '✈️', 'color': '#009688'},
            {'name': 'Other Expenses', 'icon': '📌', 'color': '#9E9E9E'},
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
        
        self.stdout.write(self.style.SUCCESS('\n✅ Default categories loaded successfully!'))
