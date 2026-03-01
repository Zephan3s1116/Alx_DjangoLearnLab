from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone
from .models import Goal
from .serializers import GoalSerializer, GoalUpdateProgressSerializer

class GoalListCreateView(generics.ListCreateAPIView):
    """
    List all goals or create a new goal.
    
    Filtering:
    - ?is_completed=true or ?is_completed=false
    - ?ordering=-deadline (order by deadline)
    """
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_completed']
    ordering_fields = ['deadline', 'target_amount', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a goal.
    """
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_goal_progress(request, pk):
    """
    Update goal progress by adding an amount.
    
    PATCH /api/goals/{id}/update-progress/
    Body: {"amount": 100.00}
    """
    try:
        goal = Goal.objects.get(pk=pk, user=request.user)
    except Goal.DoesNotExist:
        return Response({'error': 'Goal not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = GoalUpdateProgressSerializer(data=request.data)
    if serializer.is_valid():
        amount = serializer.validated_data['amount']
        goal.current_amount += amount
        
        # Check if goal is completed
        if goal.current_amount >= goal.target_amount and not goal.is_completed:
            goal.is_completed = True
            goal.completed_at = timezone.now()
        
        goal.save()
        
        response_serializer = GoalSerializer(goal)
        return Response({
            'message': 'Progress updated successfully',
            'goal': response_serializer.data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complete_goal(request, pk):
    """
    Mark a goal as complete.
    
    PATCH /api/goals/{id}/complete/
    """
    try:
        goal = Goal.objects.get(pk=pk, user=request.user)
    except Goal.DoesNotExist:
        return Response({'error': 'Goal not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if goal.is_completed:
        return Response({'error': 'Goal is already completed'}, status=status.HTTP_400_BAD_REQUEST)
    
    goal.is_completed = True
    goal.completed_at = timezone.now()
    goal.current_amount = goal.target_amount
    goal.save()
    
    serializer = GoalSerializer(goal)
    return Response({
        'message': 'Goal marked as complete',
        'goal': serializer.data
    })
