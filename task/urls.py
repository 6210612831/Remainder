from django.urls import path, include
from .views_apis import TaskApiView,TaskDetailApiView,PeriodTaskApiView,PeriodTaskDetailApiView

from . import views_fronts
app_name = 'task'
api_v1_urls = (
    [
        path('periodtask', PeriodTaskApiView.as_view()),
        path('periodtask/<int:pk>', PeriodTaskDetailApiView.as_view()),
        path('task', TaskApiView.as_view()),
        path('task/<int:pk>', TaskDetailApiView.as_view()),
    ],
    'api_v1')



urlpatterns = [
    path('api/v1/', include(api_v1_urls)),
    path("", views_fronts.index, name="index"),
    path("login", views_fronts.login_view, name="login"),
    path("logout", views_fronts.logout_view, name="logout"),
    path("register", views_fronts.register, name="register"),
    path("test", views_fronts.test, name="test"),

    # path('api/v1/', include(front_urls)),
]
