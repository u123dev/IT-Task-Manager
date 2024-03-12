from django.urls import path

from task_manager.views import index

urlpatterns = [
    path("", index, name="index"),
    path("", index, name="position-list"),
    path("", index, name="worker-list"),
    path("", index, name="tasktype-list"),
]

app_name = "task_manager"
