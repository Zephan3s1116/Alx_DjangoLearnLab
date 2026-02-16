"""
Posts Views

This module defines API views for Post and Comment CRUD operations.
"""

from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit/delete their objects.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only allowed to the author
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model providing CRUD operations.
    
    List, Create, Retrieve, Update, Delete operations for posts.
    Includes filtering, searching, and pagination.
    """
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'created_at']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Set the author to the current user when creating a post."""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Get all comments for a specific post.
        
        GET /posts/{id}/comments/
        """
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment model providing CRUD operations.
    
    List, Create, Retrieve, Update, Delete operations for comments.
    """
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post', 'author', 'created_at']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    
    def perform_create(self, serializer):
        """Set the author to the current user when creating a comment."""
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        """
        Optionally filter comments by post if 'post' query parameter is provided.
        """
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset
