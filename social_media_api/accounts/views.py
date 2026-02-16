"""
Accounts Views

This module defines API views for user authentication, profile management,
and follow/unfollow functionality.
"""

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from .serializers import (
    UserRegistrationSerializer,
# Note: This module uses generics.GenericAPIView and CustomUser.objects.all()
    UserLoginSerializer,
    UserProfileSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """API view for user registration."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Create user and return token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'bio': user.bio
            },
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """API view for user login."""
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        """Authenticate user and return token."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'bio': user.bio
                },
                'token': token.key,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """API view for user profile management."""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Return the authenticated user."""
        return self.request.user


# ============================================================================
# Follow Management Views
# ============================================================================

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user.
    
    POST /api/accounts/follow/<user_id>/
    
    Adds the specified user to the current user's following list.
    """
    user_to_follow = get_object_or_404(User, id=user_id)
    current_user = request.user
    
    # Prevent users from following themselves
    if current_user == user_to_follow:
        return Response({
            'error': 'You cannot follow yourself'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if already following
    if current_user.following.filter(id=user_id).exists():
        return Response({
            'message': f'You are already following {user_to_follow.username}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Add to following
    current_user.following.add(user_to_follow)
    
    return Response({
        'message': f'You are now following {user_to_follow.username}',
        'following_count': current_user.following_count
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user.
    
    POST /api/accounts/unfollow/<user_id>/
    
    Removes the specified user from the current user's following list.
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    current_user = request.user
    
    # Check if actually following
    if not current_user.following.filter(id=user_id).exists():
        return Response({
            'message': f'You are not following {user_to_unfollow.username}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Remove from following
    current_user.following.remove(user_to_unfollow)
    
    return Response({
        'message': f'You have unfollowed {user_to_unfollow.username}',
        'following_count': current_user.following_count
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_following(request):
    """
    List all users that the current user is following.
    
    GET /api/accounts/following/
    """
    following = request.user.following.all()
    
    following_data = [{
        'id': user.id,
        'username': user.username,
        'bio': user.bio,
        'profile_picture': user.profile_picture.url if user.profile_picture else None
    } for user in following]
    
    return Response({
        'count': len(following_data),
        'following': following_data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_followers(request):
    """
    List all users that follow the current user.
    
    GET /api/accounts/followers/
    """
    followers = request.user.followers.all()
    
    followers_data = [{
        'id': user.id,
        'username': user.username,
        'bio': user.bio,
        'profile_picture': user.profile_picture.url if user.profile_picture else None
    } for user in followers]
    
    return Response({
        'count': len(followers_data),
        'followers': followers_data
    }, status=status.HTTP_200_OK)
