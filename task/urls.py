from django.urls import path, include
from .views import TaskApiView,TaskDetailApiView,UploadApiView,UploadDetailApiView

app_name = 'task'
api_v1_urls = (
    [
        path('task', TaskApiView.as_view()),
        path('task/<int:pk>', TaskDetailApiView.as_view()),
        path('upload', UploadApiView.as_view()),
        path('upload/<str:filename>', UploadDetailApiView.as_view()),
    ],
    'api_v1')

urlpatterns = [
    path('v1/', include(api_v1_urls)),
    
]
