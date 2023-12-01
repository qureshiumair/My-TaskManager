from django.urls import path
from . import views


urlpatterns = [
    path("user_tasks", views.UserTaskManagerView.as_view(),
         name="UserTaskManagerView"),
]
