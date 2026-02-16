"""
Accounts Serializers

This module defines serializers for user authentication and profile management.
Uses serializers.CharField() and get_user_model() patterns.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Get the custom user model
User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Uses serializers.CharField() for password fields.
    Creates users with get_user_model().objects.create_user()
    """
    
    # Using serializers.CharField() for password field
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'bio', 'profile_picture']
        extra_kwargs = {
            'email': {'required': True}
        }
    
    def validate(self, data):
        """Validate that passwords match."""
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        """Create user using get_user_model().objects.create_user()"""
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        
        # Use get_user_model().objects.create_user()
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password
        )
        
        if 'bio' in validated_data:
            user.bio = validated_data['bio']
        if 'profile_picture' in validated_data:
            user.profile_picture = validated_data['profile_picture']
        
        user.save()
        Token.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login using serializers.CharField()"""
    username = serializers.CharField()
    password = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 
                  'followers_count', 'following_count', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']
