from rest_framework import serializers
from .models import Budget
from categories.serializers import CategorySerializer

class BudgetSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    spent_amount = serializers.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        read_only=True,
        source='get_spent_amount'
    )
    remaining_amount = serializers.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        read_only=True,
        source='get_remaining_amount'
    )
    percentage_used = serializers.FloatField(read_only=True, source='get_percentage_used')
    status = serializers.CharField(read_only=True, source='get_status')
    
    class Meta:
        model = Budget
        fields = [
            'id', 'category', 'category_details', 'amount', 'month', 'year',
            'spent_amount', 'remaining_amount', 'percentage_used', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_month(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError("Month must be between 1 and 12.")
        return value
    
    def validate_year(self, value):
        if value < 2000 or value > 2100:
            raise serializers.ValidationError("Year must be between 2000 and 2100.")
        return value
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Budget amount must be greater than zero.")
        return value
    
    def validate(self, data):
        # Check category is expense type
        category = data.get('category')
        if category and category.type != 'expense':
            raise serializers.ValidationError({
                'category': 'Budgets can only be created for expense categories.'
            })
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class BudgetStatusSerializer(serializers.Serializer):
    """Serializer for overall budget status summary."""
    total_budgeted = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_remaining = serializers.DecimalField(max_digits=12, decimal_places=2)
    overall_percentage = serializers.FloatField()
    budgets_count = serializers.IntegerField()
    over_budget_count = serializers.IntegerField()
    near_limit_count = serializers.IntegerField()
    under_budget_count = serializers.IntegerField()
