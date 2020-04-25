from django.urls import path

from .views import TaskListAPIView, TaskDetailAPIView, TaskCompletedAPIView

app_name = 'api-tasks'

urlpatterns = [
    path('', TaskListAPIView.as_view(), name='list'),
    path('<int:id>/', TaskDetailAPIView.as_view(), name='detail'),
    path('<int:id>/completed/', TaskCompletedAPIView.as_view(), name='complete'),
]
