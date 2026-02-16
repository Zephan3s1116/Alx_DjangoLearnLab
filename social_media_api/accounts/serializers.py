"""
Accounts Serializers

This module defines serializers for user authentication and profile management.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Use get_user_model() to get the custom user model
User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Handles creation of new users with password hashing.
    Includes password confirmation validation.
    """
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Enter a secure password"
    )
    
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Confirm your password"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'bio', 'profile_picture']
        extra_kwargs = {
            'email': {'required': True},
            'bio': {'required': False},
            'profile_picture': {'required': False}
        }
    
    def validate(self, data):
        """
        Validate that passwords match.
        
        Args:
            data: Dictionary of field data
            
        Returns:
            Validated data
            
        Raises:
            serializers.ValidationError: If passwords don't match
        """
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': "Passwords do not match."
            })
        return data
    
    def create(self, validated_data):
        """
        Create and return a new user with encrypted password.
        
        Args:
            validated_data: Validated field data
            
        Returns:
            User: The created user instance
        """
        # Remove password_confirm as it's not needed for user creation
        validated_data.pop('password_confirm', None)
        
        # Extract password
        password = validated_data.pop('password')
        
        # Create user using get_user_model().objects.create_user()
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password
        )
        
        # Set optional fields
        if 'bio' in validated_data:
            user.bio = validated_data['bio']
        if 'profile_picture' in validated_data:
            user.profile_picture = validated_data['profile_picture']
        
        user.save()
        
        # Create authentication token for the user
        Token.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Validates credentials and returns user data with token.
    """
    
    username = serializers.CharField(
        required=True,
        help_text="Enter your username"
    )
    
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        help_text="Enter your password"
    )


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile display and updates.
    
    Includes follower and following counts as read-only fields.
    """
    
    followers_count = serializers.IntegerField(
        read_only=True,
        help_text="Number of followers"
    )
    
    following_count = serializers.IntegerField(
        read_only=True,
        help_text="Number of users being followed"
    )
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'bio',
            'profile_picture',
            'followers_count',
            'following_count',
            'date_joined'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'followers_count', 'following_count']
        extra_kwargs = {
            'email': {'required': False},
            'bio': {'required': False},
            'profile_picture': {'required': False}
        }
