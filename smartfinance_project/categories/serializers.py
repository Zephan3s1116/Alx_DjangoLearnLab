from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'type_display', 'is_default', 'icon', 'color', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_default']
    
    def validate(self, data):
        user = self.context['request'].user
        name = data.get('name')
        category_type = data.get('type')
        
        # Check for duplicate custom category
        if Category.objects.filter(user=user, name=name, type=category_type).exists():
            raise serializers.ValidationError("You already have a category with this name and type.")
        
        return data
    
    def create(self, validated_data):
        # Auto-assign user for custom categories
        validated_data['user'] = self.context['request'].user
        validated_data['is_default'] = False
        return super().create(validated_data)
