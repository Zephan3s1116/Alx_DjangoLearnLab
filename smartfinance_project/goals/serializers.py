from rest_framework import serializers
from .models import Goal
from django.utils import timezone

class GoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.FloatField(read_only=True, source='get_progress_percentage')
    remaining_amount = serializers.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        read_only=True,
        source='get_remaining_amount'
    )
    
    class Meta:
        model = Goal
        fields = [
            'id', 'name', 'target_amount', 'current_amount', 'deadline',
            'is_completed', 'completed_at', 'description',
            'progress_percentage', 'remaining_amount',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_completed', 'completed_at', 'created_at', 'updated_at']
    
    def validate_target_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Target amount must be greater than zero.")
        return value
    
    def validate_current_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Current amount cannot be negative.")
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class GoalUpdateProgressSerializer(serializers.Serializer):
    """Serializer for updating goal progress."""
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
