from django.urls import path, include
from .views import TaskListApiView

app_name = 'task'
urlpatterns = [
    path('v1', TaskListApiView.as_view()),
]