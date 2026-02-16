"""
Posts Serializers

This module defines serializers for Post and Comment models.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    
    Includes author information and handles creation.
    """
    
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        source='author',
        read_only=True
    )
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'author_id',
            'content',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'author', 'author_id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create comment with current user as author."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    
    Includes author information, comment count, and nested comments.
    """
    
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        source='author',
        read_only=True
    )
    comments_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'comments_count',
            'comments'
        ]
        read_only_fields = ['id', 'author', 'author_id', 'created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        """Return the number of comments on this post."""
        return obj.comments.count()
    
    def create(self, validated_data):
        """Create post with current user as author."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
