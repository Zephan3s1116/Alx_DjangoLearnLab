from django.db import models
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Category
from .serializers import CategorySerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories (default + user's custom) or create a custom category.
    
    GET /api/categories/
    - Returns all default categories + user's custom categories
    - Filter by type: ?type=income or ?type=expense
    
    POST /api/categories/
    - Create a new custom category
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type', 'is_default']
    search_fields = ['name']
    
    def get_queryset(self):
        # Return default categories + user's custom categories
        return Category.objects.filter(
            models.Q(is_default=True) | models.Q(user=self.request.user)
        )

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a category.
    
    - Can only modify/delete custom categories (not defaults)
    - Can only modify/delete own categories
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, is_default=False)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_default:
            return Response(
                {'error': 'Cannot delete default categories'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
