from django.urls import path
from .views import (
    GoalListCreateView,
    GoalDetailView,
    update_goal_progress,
    complete_goal
)

app_name = 'goals'

urlpatterns = [
    path('', GoalListCreateView.as_view(), name='goal-list'),
    path('<int:pk>/', GoalDetailView.as_view(), name='goal-detail'),
    path('<int:pk>/update-progress/', update_goal_progress, name='goal-update-progress'),
    path('<int:pk>/complete/', complete_goal, name='goal-complete'),
]
