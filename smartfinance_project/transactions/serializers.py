from rest_framework import serializers
from .models import Transaction
from categories.serializers import CategorySerializer
from datetime import date

class TransactionSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'category', 'category_details', 'amount', 'type', 'type_display',
            'description', 'date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
    def validate(self, data):
        # Validate category type matches transaction type
        category = data.get('category')
        transaction_type = data.get('type')
        
        if category and transaction_type:
            if category.type != transaction_type:
                raise serializers.ValidationError({
                    'category': f'Category must be of type {transaction_type}.'
                })
        
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TransactionSummarySerializer(serializers.Serializer):
    """Serializer for transaction summary statistics."""
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_savings = serializers.DecimalField(max_digits=12, decimal_places=2)
    savings_rate = serializers.FloatField()
    transaction_count = serializers.IntegerField()
    income_count = serializers.IntegerField()
    expense_count = serializers.IntegerField()
