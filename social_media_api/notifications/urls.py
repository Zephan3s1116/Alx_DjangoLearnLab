from django.urls import path
from .views import NotificationListView, mark_notification_read, mark_all_read

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
    path('<int:pk>/read/', mark_notification_read, name='mark-read'),
    path('read-all/', mark_all_read, name='mark-all-read'),
]
