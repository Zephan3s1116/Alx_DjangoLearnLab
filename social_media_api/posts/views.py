"""
Posts Views

This module defines API views for Post and Comment CRUD operations,
and feed functionality.
"""

from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow authors to edit/delete their objects."""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Post model providing CRUD operations."""
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
        """Get all comments for a specific post."""
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model providing CRUD operations."""
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
        """Optionally filter comments by post."""
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset


# ============================================================================
# Feed View
# ============================================================================

class FeedView(generics.ListAPIView):
    """
    API view for user feed.
    
    Returns posts from users that the current user follows,
    ordered by creation date (newest first).
    
    GET /api/posts/feed/
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return posts from followed users.
        
        Includes posts from users in the current user's following list,
        ordered by creation date descending.
        """
        current_user = self.request.user
        
        # Get all users that the current user follows
        following_users = current_user.following.all()
        
        # Get posts from those users
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        """Override to add custom response format."""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'count': queryset.count(),
            'posts': serializer.data
        })
